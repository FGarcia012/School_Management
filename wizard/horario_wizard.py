# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class HorarioWizard(models.TransientModel):
    _name = 'horario.wizard'
    _description = 'Wizard para Horarios'

    mode = fields.Selection([
        ('agregar', 'Agregar'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar'),
        ('generar_plantilla', 'Generar Plantilla')
    ], 'Modo', required=True)

    curso_id = fields.Many2one('school.curso', 'Curso')
    aula_id = fields.Many2one('school.aula', 'Aula')
    dia_semana = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ], 'Día de la Semana')
    
    hora_inicio = fields.Float('Hora de Inicio')
    hora_fin = fields.Float('Hora de Fin')
    turno = fields.Selection([
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
    ], 'Turno')
    profesor = fields.Char('Profesor')

    cursos_ids = fields.Many2many('school.curso', string='Cursos para Plantilla')
    aula_plantilla_id = fields.Many2one('school.aula', 'Aula para Plantilla')
    turno_plantilla = fields.Selection([
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
    ], 'Turno para Plantilla')

    @api.multi
    def ejecutar_accion(self):
        if self.mode == 'agregar':
            return self._agregar_horario()
        elif self.mode == 'actualizar':
            return self._actualizar_horario()
        elif self.mode == 'eliminar':
            return self._eliminar_horario()
        elif self.mode == 'generar_plantilla':
            return self._generar_plantilla()

    def _agregar_horario(self):
        vals = {
            'curso_id': self.curso_id.id,
            'aula_id': self.aula_id.id,
            'dia_semana': self.dia_semana,
            'hora_inicio': self.hora_inicio,
            'hora_fin': self.hora_fin,
            'turno': self.turno,
            'profesor': self.profesor,
        }
        
        horario = self.env['school.horario'].create(vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Horarios',
            'res_model': 'school.horario',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def _actualizar_horario(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            horario = self.env['school.horario'].browse(active_id)
            vals = {
                'curso_id': self.curso_id.id,
                'aula_id': self.aula_id.id,
                'dia_semana': self.dia_semana,
                'hora_inicio': self.hora_inicio,
                'hora_fin': self.hora_fin,
                'turno': self.turno,
                'profesor': self.profesor,
            }
            horario.write(vals)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Horarios',
            'res_model': 'school.horario',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def _eliminar_horario(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            horario = self.env['school.horario'].browse(active_id)
            horario.unlink()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Horarios',
            'res_model': 'school.horario',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'target': 'current',
        }

    def _generar_plantilla(self):
        if not self.cursos_ids or not self.aula_plantilla_id or not self.turno_plantilla:
            raise ValidationError('Debe seleccionar cursos, aula y turno para generar la plantilla.')
        
        horario_model = self.env['school.horario']
        cursos_ids = [curso.id for curso in self.cursos_ids]
        
        horarios_creados = horario_model.generar_horario_semanal(
            cursos_ids, 
            self.aula_plantilla_id.id, 
            self.turno_plantilla
        )
        
        if horarios_creados:
            return {
                'type': 'ir.actions.act_window',
                'name': 'Horarios Creados',
                'res_model': 'school.horario',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', horarios_creados)],
                'target': 'current',
            }
        else:
            raise ValidationError('No se pudieron crear horarios. Verifique conflictos existentes.')

    @api.onchange('turno')
    def _onchange_turno(self):
        """Sugiere horarios según el turno seleccionado"""
        if self.turno == 'matutino':
            self.hora_inicio = 8.0
            self.hora_fin = 9.0
        elif self.turno == 'vespertino':
            self.hora_inicio = 14.0
            self.hora_fin = 15.0