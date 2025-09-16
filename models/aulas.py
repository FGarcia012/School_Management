# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Aula(models.Model):
    _name = 'school.aula'
    _description = 'Aula'

    name = fields.Char('Nombre', required=True)
    capacidad = fields.Integer('Capacidad')

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Aula',
            'res_model': 'aula.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Aula',
            'res_model': 'aula.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_name': self.name,
                'default_capacidad': self.capacidad
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Aula',
            'res_model': 'aula.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }