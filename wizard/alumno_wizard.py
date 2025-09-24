# -*- coding: utf-8 -*-
from openerp import models, fields, api

class AlumnoWizard(models.TransientModel):
    _name = 'alumno.wizard'
    _description = 'Wizard para CRUD de Alumno'

    name = fields.Char('Nombre', required=True)
    numero = fields.Char('Numero de estudiante')
    aula_id = fields.Many2one('school.aula', 'Aula Asignada')
    curso_ids = fields.Many2many('school.curso', string='Cursos Inscritos')
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
                'aula_id': alumno.aula_id.id if alumno.aula_id else False,
                'curso_ids': [(6, 0, alumno.curso_ids.ids)],
            })
        elif context.get('active_id') and context.get('default_mode') == 'eliminar':
            alumno = self.env['school.alumno'].browse(context['active_id'])
            res.update({
                'name': alumno.name,
                'numero': alumno.numero,
                'aula_id': alumno.aula_id.id if alumno.aula_id else False,
                'curso_ids': [(6, 0, alumno.curso_ids.ids)],
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
            'aula_id': self.aula_id.id if self.aula_id else False,
            'curso_ids': [(6, 0, self.curso_ids.ids)],
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def actualizar_alumno(self):
        self.ensure_one()
        alumno_id = self.env.context.get('active_id')
        if alumno_id:
            self.env['school.alumno'].browse(alumno_id).write({
                'name': self.name,
                'aula_id': self.aula_id.id if self.aula_id else False,
                'curso_ids': [(6, 0, self.curso_ids.ids)],
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def eliminar_alumno(self):
        self.ensure_one()
        alumno_id = self.env.context.get('active_id')
        if alumno_id:
            self.env['school.alumno'].browse(alumno_id).unlink()
        return {'type': 'ir.actions.act_window_close'}