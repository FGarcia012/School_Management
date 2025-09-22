# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Alumno(models.Model):
    _name = 'school.alumno'
    _description = 'Alumno'

    name = fields.Char('Nombre', required=True)
    numero = fields.Char('Número de estudiante', required=True)
    
    # Relaciones principales
    aula_id = fields.Many2one('school.aula', 'Aula Asignada', required=True)
    curso_ids = fields.Many2many('school.curso', 'alumno_curso_rel', 'alumno_id', 'curso_id', 'Cursos Inscritos')
    
    # Relaciones computadas para información
    examen_ids = fields.One2many('school.examen', 'alumno_id', 'Exámenes a Presentar')
    
    # Campos informativos
    total_cursos = fields.Integer('Total de Cursos', compute='_compute_total_cursos', store=True)
    
    @api.depends('curso_ids')
    def _compute_total_cursos(self):
        for alumno in self:
            alumno.total_cursos = len(alumno.curso_ids)
    
    @api.constrains('numero')
    def _check_numero_unico(self):
        for alumno in self:
            if alumno.numero:
                existing = self.search([('numero', '=', alumno.numero), ('id', '!=', alumno.id)])
                if existing:
                    raise ValidationError("El número de estudiante '%s' ya está asignado a otro alumno." % alumno.numero)
    
    @api.constrains('aula_id')
    def _check_capacidad_aula(self):
        for alumno in self:
            if alumno.aula_id:
                # Contar alumnos en el aula (incluyendo este alumno)
                alumnos_en_aula = self.search([('aula_id', '=', alumno.aula_id.id)])
                if len(alumnos_en_aula) > alumno.aula_id.capacidad:
                    raise ValidationError(
                        "No se puede asignar al alumno al aula '%s'. "
                        "La capacidad máxima es de %d estudiantes." % 
                        (alumno.aula_id.name, alumno.aula_id.capacidad)
                    )

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_name': self.name,
                'default_numero': self.numero,
                'default_aula_id': self.aula_id.id if self.aula_id else False
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }