# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning

class Curso(models.Model):
    _name = 'school.curso'
    _description = 'Curso'

    name = fields.Char('Nombre del Curso', required=True)
    description = fields.Text('Descripcion')
    codigo = fields.Char('Codigo del Curso', required=True)
    
    # Relaciones principales
    aula_id = fields.Many2one('school.aula', 'Aula Principal')
    profesor_id = fields.Many2one('res.users', 'Profesor Asignado')
    
    # Relaciones con estudiantes y evaluaciones
    alumno_ids = fields.Many2many('school.alumno', 'alumno_curso_rel', 'curso_id', 'alumno_id', 'Estudiantes Inscritos')
    examen_ids = fields.One2many('school.examen', 'curso_id', 'Examenes del Curso')
    horario_ids = fields.One2many('school.horario', 'curso_id', 'Horarios Programados')
    
    # Campos computados
    total_estudiantes = fields.Integer('Total de Estudiantes', compute='_compute_total_estudiantes', store=True)
    total_examenes = fields.Integer('Total de Examenes', compute='_compute_total_examenes', store=True)
    promedio_examenes = fields.Float('Promedio de Examenes', compute='_compute_promedio_examenes', store=True)
    
    @api.depends('alumno_ids')
    def _compute_total_estudiantes(self):
        for curso in self:
            curso.total_estudiantes = len(curso.alumno_ids)
    
    @api.depends('examen_ids')
    def _compute_total_examenes(self):
        for curso in self:
            curso.total_examenes = len(curso.examen_ids)
    
    @api.depends('examen_ids.promedio_examen')
    def _compute_promedio_examenes(self):
        for curso in self:
            if curso.examen_ids:
                promedios = [examen.promedio_examen for examen in curso.examen_ids if examen.promedio_examen > 0]
                curso.promedio_examenes = sum(promedios) / len(promedios) if promedios else 0.0
            else:
                curso.promedio_examenes = 0.0
    
    @api.constrains('codigo')
    def _check_codigo_unico(self):
        for curso in self:
            if curso.codigo:
                existing = self.search([('codigo', '=', curso.codigo), ('id', '!=', curso.id)])
                if existing:
                    raise Warning("El codigo de curso '%s' ya esta asignado a otro curso." % curso.codigo)
    
    @api.constrains('examen_ids', 'alumno_ids')
    def _check_minimo_examenes(self):
        for curso in self:
            if curso.alumno_ids and curso.total_examenes < 1:
                raise Warning(
                    "El curso '%s' debe tener al menos un examen asignado antes de inscribir estudiantes." % curso.name
                )

    @api.multi
    def unlink(self):
        """Override para manejar eliminacion segura de cursos"""
        for curso in self:
            if curso.alumno_ids:
                raise Warning(
                    "No se puede eliminar el curso '%s' porque tiene %d estudiante(s) inscrito(s). "
                    "Primero desinscribe a todos los estudiantes." % 
                    (curso.name, len(curso.alumno_ids))
                )
            
            if curso.examen_ids:
                curso.examen_ids.unlink()
            
            if hasattr(curso, 'horario_ids') and curso.horario_ids:
                curso.horario_ids.unlink()
        
        return super(Curso, self).unlink()

    # Metodos para los botones de accion
    @api.constrains('alumno_ids', 'aula_id')
    def _check_capacidad_aula_curso(self):
        for curso in self:
            if curso.aula_id and curso.alumno_ids:
                if len(curso.alumno_ids) > curso.aula_id.capacidad:
                    raise Warning(
                        "El curso '%s' tiene %d estudiantes inscritos, "
                        "pero el aula '%s' solo tiene capacidad para %d estudiantes." % 
                        (curso.name, len(curso.alumno_ids), curso.aula_id.name, curso.aula_id.capacidad)
                    )

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

