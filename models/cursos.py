# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError

class Curso(models.Model):
    _name = 'school.curso'
    _description = 'Curso'

    name = fields.Char('Nombre del Curso', required=True)
    description = fields.Text('Descripción')
    codigo = fields.Char('Código del Curso', required=True)
    
    # Relaciones principales
    aula_id = fields.Many2one('school.aula', 'Aula Principal')
    profesor_id = fields.Many2one('res.users', 'Profesor Asignado')
    
    # Relaciones con estudiantes y evaluaciones
    alumno_ids = fields.Many2many('school.alumno', 'alumno_curso_rel', 'curso_id', 'alumno_id', 'Estudiantes Inscritos')
    examen_ids = fields.One2many('school.examen', 'curso_id', 'Exámenes del Curso')
    horario_ids = fields.One2many('school.horario', 'curso_id', 'Horarios Programados')
    
    # Campos computados
    total_estudiantes = fields.Integer('Total de Estudiantes', compute='_compute_total_estudiantes', store=True)
    total_examenes = fields.Integer('Total de Exámenes', compute='_compute_total_examenes', store=True)
    promedio_examenes = fields.Float('Promedio de Exámenes', compute='_compute_promedio_examenes', store=True)
    
    @api.depends('alumno_ids')
    def _compute_total_estudiantes(self):
        for curso in self:
            curso.total_estudiantes = len(curso.alumno_ids)
    
    @api.depends('examen_ids')
    def _compute_total_examenes(self):
        for curso in self:
            curso.total_examenes = len(curso.examen_ids)
    
    @api.depends('examen_ids.punteo')
    def _compute_promedio_examenes(self):
        for curso in self:
            if curso.examen_ids:
                total_punteo = sum(examen.punteo for examen in curso.examen_ids if examen.punteo)
                curso.promedio_examenes = total_punteo / len(curso.examen_ids) if curso.examen_ids else 0.0
            else:
                curso.promedio_examenes = 0.0
    
    @api.constrains('codigo')
    def _check_codigo_unico(self):
        for curso in self:
            if curso.codigo:
                existing = self.search([('codigo', '=', curso.codigo), ('id', '!=', curso.id)])
                if existing:
                    raise ValidationError("El código de curso '%s' ya está asignado a otro curso." % curso.codigo)
    
    @api.constrains('examen_ids')
    def _check_minimo_examenes(self):
        for curso in self:
            if curso.total_examenes < 1:
                raise ValidationError(
                    "El curso '%s' debe tener al menos un examen asignado." % curso.name
                )
    
    @api.constrains('alumno_ids', 'aula_id')
    def _check_capacidad_aula_curso(self):
        for curso in self:
            if curso.aula_id and curso.alumno_ids:
                if len(curso.alumno_ids) > curso.aula_id.capacidad:
                    raise ValidationError(
                        "El curso '%s' tiene %d estudiantes inscritos, "
                        "pero el aula '%s' solo tiene capacidad para %d estudiantes." % 
                        (curso.name, len(curso.alumno_ids), curso.aula_id.name, curso.aula_id.capacidad)
                    )

    # Métodos para los botones de acción
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Curso',
            'res_model': 'curso.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_curso_wizard_agregar').id,
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Curso',
            'res_model': 'curso.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_curso_wizard_actualizar').id,
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_name': self.name,
                'default_description': self.description
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Curso',
            'res_model': 'curso.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_curso_wizard_eliminar').id,
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }