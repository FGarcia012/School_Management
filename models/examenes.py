# -*- coding: utf-8 -*-
from openerp import models, fields, api

class Examen(models.Model):
    _name = 'school.examen'
    _description = 'Examen'

    name = fields.Char('Nombre del Examen', required=True)
    curso_id = fields.Many2one('school.curso', 'Curso')
    pregunta = fields.Text('Pregunta')
    respuesta = fields.Text('Respuesta')
    punteo = fields.Float('Punteo')

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Examen',
            'res_model': 'examen.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Examen',
            'res_model': 'examen.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_name': self.name,
                'default_curso_id': self.curso_id.id,
                'default_pregunta': self.pregunta,
                'default_respuesta': self.respuesta,
                'default_punteo': self.punteo
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Examen',
            'res_model': 'examen.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }