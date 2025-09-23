# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime, time

class Horario(models.Model):
    _name = 'school.horario'
    _description = 'Horario Escolar'
    _order = 'dia_semana, hora_inicio'

    name = fields.Char('Nombre', compute='_compute_name', store=True)
    curso_id = fields.Many2one('school.curso', 'Curso', required=True)
    aula_id = fields.Many2one('school.aula', 'Aula', required=True)
    dia_semana = fields.Selection([
        ('lunes', 'Lunes'),
        ('martes', 'Martes'),
        ('miercoles', 'Miércoles'),
        ('jueves', 'Jueves'),
        ('viernes', 'Viernes'),
    ], 'Día de la Semana', required=True)
    
    hora_inicio = fields.Float('Hora de Inicio', required=True, help='Formato 24 horas (ej: 8.0 para 8:00 AM)')
    hora_fin = fields.Float('Hora de Fin', required=True, help='Formato 24 horas (ej: 9.0 para 9:00 AM)')
    
    turno = fields.Selection([
        ('matutino', 'Matutino'),
        ('vespertino', 'Vespertino'),
    ], 'Turno', required=True)
    
    profesor = fields.Char('Profesor')
    activo = fields.Boolean('Activo', default=True)
    
    # Campos computados para mejor visualización
    hora_inicio_display = fields.Char('Hora Inicio', compute='_compute_hora_display', store=True)
    hora_fin_display = fields.Char('Hora Fin', compute='_compute_hora_display', store=True)
    duracion = fields.Float('Duración (horas)', compute='_compute_duracion', store=True)

    @api.depends('curso_id', 'dia_semana', 'hora_inicio_display')
    def _compute_name(self):
        for record in self:
            if record.curso_id and record.dia_semana and record.hora_inicio_display:
                record.name = '%s - %s %s' % (
                    record.curso_id.name,
                    record.dia_semana.title(),
                    record.hora_inicio_display
                )
            else:
                record.name = 'Nuevo Horario'

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_hora_display(self):
        for record in self:
            record.hora_inicio_display = self._float_to_time_string(record.hora_inicio)
            record.hora_fin_display = self._float_to_time_string(record.hora_fin)

    @api.depends('hora_inicio', 'hora_fin')
    def _compute_duracion(self):
        for record in self:
            record.duracion = record.hora_fin - record.hora_inicio

    def _float_to_time_string(self, float_time):
        """Convierte tiempo float a string formato HH:MM"""
        if not float_time:
            return ''
        
        hours = int(float_time)
        minutes = int((float_time - hours) * 60)
        
        if hours == 0:
            time_str = '12:%02d AM' % minutes
        elif hours < 12:
            time_str = '%d:%02d AM' % (hours, minutes)
        elif hours == 12:
            time_str = '12:%02d PM' % minutes
        else:
            time_str = '%d:%02d PM' % (hours - 12, minutes)
            
        return time_str

    @api.constrains('hora_inicio', 'hora_fin')
    def _check_horas(self):
        for record in self:
            if record.hora_inicio >= record.hora_fin:
                raise ValidationError('La hora de inicio debe ser menor que la hora de fin.')
            
            if record.hora_inicio < 6.0 or record.hora_fin > 22.0:
                raise ValidationError('Los horarios deben estar entre las 6:00 AM y 10:00 PM.')

    @api.constrains('curso_id', 'aula_id', 'dia_semana', 'hora_inicio', 'hora_fin')
    def _check_conflictos(self):
        for record in self:
            conflicto_aula = self.search([
                ('id', '!=', record.id),
                ('aula_id', '=', record.aula_id.id),
                ('dia_semana', '=', record.dia_semana),
                ('activo', '=', True),
                '|',
                '&', ('hora_inicio', '<=', record.hora_inicio), ('hora_fin', '>', record.hora_inicio),
                '&', ('hora_inicio', '<', record.hora_fin), ('hora_fin', '>=', record.hora_fin),
            ])
            
            if conflicto_aula:
                raise ValidationError(
                    'Conflicto de horario: El aula "%s" ya está ocupada el %s de %s a %s por el curso "%s".' % (
                        record.aula_id.name,
                        record.dia_semana,
                        conflicto_aula[0].hora_inicio_display,
                        conflicto_aula[0].hora_fin_display,
                        conflicto_aula[0].curso_id.name
                    )
                )

    @api.model
    def crear_plantilla_matutino(self):
        """Crea una plantilla de horario matutino básico"""
        plantilla = [
            {'hora_inicio': 8.0, 'hora_fin': 9.0}, 
            {'hora_inicio': 9.0, 'hora_fin': 10.0}, 
            {'hora_inicio': 10.3, 'hora_fin': 11.3},  
            {'hora_inicio': 11.3, 'hora_fin': 12.3}, 
        ]
        return plantilla

    @api.model
    def crear_plantilla_vespertino(self):
        """Crea una plantilla de horario vespertino básico"""
        plantilla = [
            {'hora_inicio': 14.0, 'hora_fin': 15.0},  
            {'hora_inicio': 15.0, 'hora_fin': 16.0},  
            {'hora_inicio': 16.3, 'hora_fin': 17.3},  
            {'hora_inicio': 17.3, 'hora_fin': 18.3},  
        ]
        return plantilla

    @api.multi
    def generar_horario_semanal(self, cursos_ids, aula_id, turno):
        """Genera un horario semanal básico para una lista de cursos"""
        if turno == 'matutino':
            plantilla = self.crear_plantilla_matutino()
        else:
            plantilla = self.crear_plantilla_vespertino()
        
        dias = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']
        horarios_creados = []
        
        for dia in dias:
            for i, slot in enumerate(plantilla):
                if i < len(cursos_ids):
                    vals = {
                        'curso_id': cursos_ids[i],
                        'aula_id': aula_id,
                        'dia_semana': dia,
                        'hora_inicio': slot['hora_inicio'],
                        'hora_fin': slot['hora_fin'],
                        'turno': turno,
                    }
                    try:
                        horario = self.create(vals)
                        horarios_creados.append(horario.id)
                    except ValidationError:
                        continue
        
        return horarios_creados

    @api.multi
    def unlink(self):
        """Override para manejar eliminación segura de horarios"""
        for horario in self:
            if horario.activo:
                horario.write({'activo': False})
                continue
        return super(Horario, self).unlink()

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Horario',
            'res_model': 'horario.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Horario',
            'res_model': 'horario.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_curso_id': self.curso_id.id,
                'default_aula_id': self.aula_id.id,
                'default_dia_semana': self.dia_semana,
                'default_hora_inicio': self.hora_inicio,
                'default_hora_fin': self.hora_fin,
                'default_turno': self.turno,
                'default_profesor': self.profesor,
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Horario',
            'res_model': 'horario.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
            }
        }