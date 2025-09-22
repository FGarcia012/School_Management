# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Aula(models.Model):
    _name = 'school.aula'
    _description = 'Aula'

    name = fields.Char('Nombre', required=True)
    capacidad = fields.Integer('Capacidad', required=True, default=30)
    
    # Relaciones con otros modelos
    alumno_ids = fields.One2many('school.alumno', 'aula_id', 'Alumnos Asignados')
    curso_ids = fields.One2many('school.curso', 'aula_id', 'Cursos que se Imparten') 
    horario_ids = fields.One2many('school.horario', 'aula_id', 'Horarios Programados')
    
    # Campos computados
    total_alumnos = fields.Integer('Total de Alumnos', compute='_compute_total_alumnos', store=True)
    capacidad_disponible = fields.Integer('Capacidad Disponible', compute='_compute_capacidad_disponible', store=True)
    porcentaje_ocupacion = fields.Float('% Ocupación', compute='_compute_porcentaje_ocupacion', store=True)
    
    @api.depends('alumno_ids')
    def _compute_total_alumnos(self):
        for aula in self:
            aula.total_alumnos = len(aula.alumno_ids)
    
    @api.depends('capacidad', 'total_alumnos')
    def _compute_capacidad_disponible(self):
        for aula in self:
            aula.capacidad_disponible = aula.capacidad - aula.total_alumnos
    
    @api.depends('capacidad', 'total_alumnos')
    def _compute_porcentaje_ocupacion(self):
        for aula in self:
            if aula.capacidad > 0:
                aula.porcentaje_ocupacion = (aula.total_alumnos * 100.0) / aula.capacidad
            else:
                aula.porcentaje_ocupacion = 0.0
    
    @api.constrains('capacidad')
    def _check_capacidad_positiva(self):
        for aula in self:
            if aula.capacidad <= 0:
                raise ValidationError("La capacidad del aula debe ser mayor a 0")
    
    @api.constrains('alumno_ids', 'capacidad')
    def _check_capacidad_maxima(self):
        for aula in self:
            if len(aula.alumno_ids) > aula.capacidad:
                raise ValidationError(
                    "El aula '%s' ha excedido su capacidad máxima de %d estudiantes. "
                    "Actualmente tiene %d estudiantes asignados." % 
                    (aula.name, aula.capacidad, len(aula.alumno_ids))
                )

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