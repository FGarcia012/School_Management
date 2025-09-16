# -*- coding: utf-8 -*-
from openerp import models, fields, api

class AulaWizard(models.TransientModel):
    _name = 'aula.wizard'
    _description = 'Wizard para CRUD de Aula'

    name = fields.Char('Nombre', required=True)
    capacidad = fields.Integer('Capacidad')
    mode = fields.Selection([
        ('agregar', 'Agregar'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar')
    ], string='Modo', default='agregar')

    @api.model
    def default_get(self, fields):
        res = super(AulaWizard, self).default_get(fields)
        context = self.env.context
        
        if context.get('active_id') and context.get('default_mode') == 'actualizar':
            aula = self.env['school.aula'].browse(context['active_id'])
            res.update({
                'name': aula.name,
                'capacidad': aula.capacidad,
            })
        elif context.get('active_id') and context.get('default_mode') == 'eliminar':
            aula = self.env['school.aula'].browse(context['active_id'])
            res.update({
                'name': aula.name,
                'capacidad': aula.capacidad,
            })
        return res

    @api.multi
    def execute_action(self):
        self.ensure_one()
        if self.mode == 'agregar':
            return self.agregar_aula()
        elif self.mode == 'actualizar':
            return self.actualizar_aula()
        elif self.mode == 'eliminar':
            return self.eliminar_aula()

    @api.multi
    def agregar_aula(self):
        self.ensure_one()
        self.env['school.aula'].create({
            'name': self.name,
            'capacidad': self.capacidad,
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def actualizar_aula(self):
        self.ensure_one()
        aula_id = self.env.context.get('active_id')
        if aula_id:
            self.env['school.aula'].browse(aula_id).write({
                'name': self.name,
                'capacidad': self.capacidad,
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def eliminar_aula(self):
        self.ensure_one()
        aula_id = self.env.context.get('active_id')
        if aula_id:
            self.env['school.aula'].browse(aula_id).unlink()
        return {'type': 'ir.actions.act_window_close'}