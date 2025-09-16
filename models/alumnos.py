# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Alumno(models.Model):
    _name = 'school.alumno'
    _description = 'Alumno'

    name = fields.Char('Nombre', required=True)
    numero = fields.Char('Número de estudiante')
    curso_id = fields.Many2one('school.curso', 'Curso')

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
                'default_curso_id': self.curso_id.id
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