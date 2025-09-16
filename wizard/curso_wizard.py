# -*- coding: utf-8 -*-
from openerp import models, fields, api

class CursoWizard(models.TransientModel):
    _name = 'curso.wizard'
    _description = 'Wizard para CRUD de Curso'

    name = fields.Char('Nombre del Curso', required=True)
    description = fields.Text('Descripción')
    mode = fields.Selection([
        ('agregar', 'Agregar'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar')
    ], string='Modo', default='agregar')

    @api.model
    def default_get(self, fields):
        res = super(CursoWizard, self).default_get(fields)
        context = self.env.context
        
        if context.get('active_id') and context.get('default_mode') == 'actualizar':
            curso = self.env['school.curso'].browse(context['active_id'])
            res.update({
                'name': curso.name,
                'description': curso.description,
            })
        elif context.get('active_id') and context.get('default_mode') == 'eliminar':
            curso = self.env['school.curso'].browse(context['active_id'])
            res.update({
                'name': curso.name,
                'description': curso.description,
            })
        return res

    @api.multi
    def execute_action(self):
        self.ensure_one()
        if self.mode == 'agregar':
            return self.agregar_curso()
        elif self.mode == 'actualizar':
            return self.actualizar_curso()
        elif self.mode == 'eliminar':
            return self.eliminar_curso()

    @api.multi
    def agregar_curso(self):
        self.ensure_one()
        self.env['school.curso'].create({
            'name': self.name,
            'description': self.description,
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def actualizar_curso(self):
        self.ensure_one()
        curso_id = self.env.context.get('active_id')
        if curso_id:
            self.env['school.curso'].browse(curso_id).write({
                'name': self.name,
                'description': self.description,
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def eliminar_curso(self):
        self.ensure_one()
        curso_id = self.env.context.get('active_id')
        if curso_id:
            self.env['school.curso'].browse(curso_id).unlink()
        return {'type': 'ir.actions.act_window_close'}