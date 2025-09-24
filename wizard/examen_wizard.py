# -*- coding: utf-8 -*-
from openerp import models, fields, api

class ExamenWizard(models.TransientModel):
    _name = 'examen.wizard'
    _description = 'Wizard para CRUD de Examen'

    name = fields.Char('Nombre del Examen', required=True)
    curso_id = fields.Many2one('school.curso', 'Curso')
    pregunta = fields.Text('Pregunta')
    respuesta = fields.Text('Respuesta')
    punteo_maximo = fields.Float('Punteo Maximo', default=100.0)
    mode = fields.Selection([
        ('agregar', 'Agregar'),
        ('actualizar', 'Actualizar'),
        ('eliminar', 'Eliminar')
    ], string='Modo', default='agregar')

    @api.model
    def default_get(self, fields):
        res = super(ExamenWizard, self).default_get(fields)
        context = self.env.context
        
        if context.get('active_id') and context.get('default_mode') == 'actualizar':
            examen = self.env['school.examen'].browse(context['active_id'])
            res.update({
                'name': examen.name,
                'curso_id': examen.curso_id.id,
                'pregunta': examen.pregunta,
                'respuesta': examen.respuesta,
                'punteo_maximo': examen.punteo_maximo,
            })
        elif context.get('active_id') and context.get('default_mode') == 'eliminar':
            examen = self.env['school.examen'].browse(context['active_id'])
            res.update({
                'name': examen.name,
                'curso_id': examen.curso_id.id,
                'pregunta': examen.pregunta,
                'respuesta': examen.respuesta,
                'punteo_maximo': examen.punteo_maximo,
            })
        return res

    @api.multi
    def execute_action(self):
        self.ensure_one()
        if self.mode == 'agregar':
            return self.agregar_examen()
        elif self.mode == 'actualizar':
            return self.actualizar_examen()
        elif self.mode == 'eliminar':
            return self.eliminar_examen()

    @api.multi
    def agregar_examen(self):
        self.ensure_one()
        self.env['school.examen'].create({
            'name': self.name,
            'curso_id': self.curso_id.id,
            'pregunta': self.pregunta,
            'respuesta': self.respuesta,
            'punteo_maximo': self.punteo_maximo,
        })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def actualizar_examen(self):
        self.ensure_one()
        examen_id = self.env.context.get('active_id')
        if examen_id:
            self.env['school.examen'].browse(examen_id).write({
                'name': self.name,
                'curso_id': self.curso_id.id,
                'pregunta': self.pregunta,
                'respuesta': self.respuesta,
                'punteo_maximo': self.punteo_maximo,
            })
        return {'type': 'ir.actions.act_window_close'}

    @api.multi
    def eliminar_examen(self):
        self.ensure_one()
        examen_id = self.env.context.get('active_id')
        if examen_id:
            self.env['school.examen'].browse(examen_id).unlink()
        return {'type': 'ir.actions.act_window_close'}