# -*- coding: utf-8 -*-
from openerp import models, fields, api

class AlumnoWizard(models.TransientModel):
    _name = 'alumno.wizard'
    _description = 'Wizard para CRUD de Alumno'

    name = fields.Char('Nombre', required=True)
    numero = fields.Char('Número de estudiante')
    curso_id = fields.Many2one('school.curso', 'Curso')
    mode = fields.Selection([
        ('agregar', 'Agregar'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar')
    ], string='Modo', default='agregar')

    @api.model
    def default_get(self, fields):
        res = super(AlumnoWizard, self).default_get(fields)
        context = self.env.context
        
        if context.get('active_id') and context.get('default_mode') == 'actualizar':
            alumno = self.env['school.alumno'].browse(context['active_id'])
            res.update({
                'name': alumno.name,
                'numero': alumno.numero,
                'curso_id': alumno.curso_id.id,
            })
        elif context.get('active_id') and context.get('default_mode') == 'eliminar':
            alumno = self.env['school.alumno'].browse(context['active_id'])
            res.update({
                'name': alumno.name,
                'numero': alumno.numero,
                'curso_id': alumno.curso_id.id,
            })
        return res

    @api.multi
    def execute_action(self):
        self.ensure_one()
        if self.mode == 'agregar':
            return self.agregar_alumno()
        elif self.mode == 'actualizar':
            return self.actualizar_alumno()
        elif self.mode == 'eliminar':
            return self.eliminar_alumno()

    @api.multi
    def agregar_alumno(self):
        self.ensure_one()
        self.env['school.alumno'].create({
            'name': self.name,
            'numero': self.numero,
            'curso_id': self.curso_id.id,
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def actualizar_alumno(self):
        self.ensure_one()
        alumno_id = self.env.context.get('active_id')
        if alumno_id:
            self.env['school.alumno'].browse(alumno_id).write({
                'name': self.name,
                'numero': self.numero,
                'curso_id': self.curso_id.id,
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def eliminar_alumno(self):
        self.ensure_one()
        alumno_id = self.env.context.get('active_id')
        if alumno_id:
            self.env['school.alumno'].browse(alumno_id).unlink()
        return {'type': 'ir.actions.act_window_close'}