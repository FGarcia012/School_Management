# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Examen(models.Model):
    _name = 'school.examen'
    _description = 'Examen'

    name = fields.Char('Nombre del Examen', required=True)
    curso_id = fields.Many2one('school.curso', 'Curso', required=True)
    alumno_id = fields.Many2one('school.alumno', 'Estudiante')
    
    # Información del examen
    fecha_examen = fields.Date('Fecha del Examen')
    tipo_examen = fields.Selection([
        ('parcial', 'Examen Parcial'),
        ('final', 'Examen Final'),
        ('quiz', 'Quiz'),
        ('proyecto', 'Proyecto'),
        ('tarea', 'Tarea')
    ], 'Tipo de Examen', default='parcial')
    
    # Contenido del examen
    pregunta = fields.Text('Pregunta/Descripción')
    respuesta = fields.Text('Respuesta Esperada')
    punteo = fields.Float('Punteo Obtenido', default=0.0)
    punteo_maximo = fields.Float('Punteo Máximo', default=100.0)
    
    # Estados del examen
    estado = fields.Selection([
        ('programado', 'Programado'),
        ('en_curso', 'En Curso'),
        ('completado', 'Completado'),
        ('calificado', 'Calificado')
    ], 'Estado', default='programado')
    
    # Campos computados
    porcentaje_obtenido = fields.Float('% Obtenido', compute='_compute_porcentaje', store=True)
    aprobado = fields.Boolean('Aprobado', compute='_compute_aprobado', store=True)
    
    @api.depends('punteo', 'punteo_maximo')
    def _compute_porcentaje(self):
        for examen in self:
            if examen.punteo_maximo > 0:
                examen.porcentaje_obtenido = (examen.punteo * 100.0) / examen.punteo_maximo
            else:
                examen.porcentaje_obtenido = 0.0
    
    @api.depends('porcentaje_obtenido')
    def _compute_aprobado(self):
        for examen in self:
            examen.aprobado = examen.porcentaje_obtenido >= 60.0  # 60% para aprobar
    
    @api.constrains('punteo', 'punteo_maximo')
    def _check_punteos_validos(self):
        for examen in self:
            if examen.punteo < 0:
                raise ValidationError("El punteo obtenido no puede ser negativo.")
            if examen.punteo_maximo <= 0:
                raise ValidationError("El punteo máximo debe ser mayor a 0.")
            if examen.punteo > examen.punteo_maximo:
                raise ValidationError("El punteo obtenido no puede ser mayor al punteo máximo.")
    
    @api.constrains('alumno_id', 'curso_id')
    def _check_alumno_en_curso(self):
        for examen in self:
            if examen.alumno_id and examen.curso_id:
                if examen.curso_id not in examen.alumno_id.curso_ids:
                    raise ValidationError(
                        "El estudiante '%s' no está inscrito en el curso '%s'." % 
                        (examen.alumno_id.name, examen.curso_id.name)
                    )

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Examen',
            'res_model': 'examen.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_examen_wizard_agregar').id,
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
            'view_id': self.env.ref('school_management.view_examen_wizard_actualizar').id,
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
            'view_id': self.env.ref('school_management.view_examen_wizard_eliminar').id,
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }