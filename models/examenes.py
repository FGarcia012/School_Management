# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning

class Examen(models.Model):
    _name = 'school.examen'
    _description = 'Examen del Curso'

    name = fields.Char('Nombre del Examen', required=True)
    curso_id = fields.Many2one('school.curso', 'Curso', required=True)
    
    # Informacion del examen
    fecha_examen = fields.Date('Fecha del Examen')
    tipo_examen = fields.Selection([
        ('parcial', 'Examen Parcial'),
        ('final', 'Examen Final'),
        ('quiz', 'Quiz'),
        ('proyecto', 'Proyecto'),
        ('tarea', 'Tarea')
    ], 'Tipo de Examen', default='parcial')
    
    pregunta = fields.Text('Pregunta/Descripcion')
    respuesta = fields.Text('Respuesta Esperada')
    punteo_maximo = fields.Float('Punteo Maximo', default=100.0, required=True)
    
    calificacion_ids = fields.One2many('school.calificacion', 'examen_id', 'Calificaciones')
    
    total_estudiantes = fields.Integer('Total Estudiantes', compute='_compute_estadisticas', store=True)
    promedio_examen = fields.Float('Promedio del Examen', compute='_compute_estadisticas', store=True)
    aprobados = fields.Integer('Estudiantes Aprobados', compute='_compute_estadisticas', store=True)
    reprobados = fields.Integer('Estudiantes Reprobados', compute='_compute_estadisticas', store=True)
    
    @api.depends('calificacion_ids')
    def _compute_estadisticas(self):
        for examen in self:
            calificaciones = examen.calificacion_ids
            examen.total_estudiantes = len(calificaciones)
            
            if calificaciones:
                punteos = [c.punteo for c in calificaciones if c.punteo > 0]
                examen.promedio_examen = sum(punteos) / len(punteos) if punteos else 0.0
                examen.aprobados = len([c for c in calificaciones if c.aprobado])
                examen.reprobados = len([c for c in calificaciones if not c.aprobado and c.punteo > 0])
            else:
                examen.promedio_examen = 0.0
                examen.aprobados = 0
                examen.reprobados = 0
    
    @api.constrains('punteo_maximo')
    def _check_punteo_maximo(self):
        for examen in self:
            if examen.punteo_maximo <= 0:
                raise Warning("El punteo maximo debe ser mayor a 0.")
    
    @api.multi
    def generar_calificaciones(self):
        """Genera calificaciones para todos los estudiantes inscritos en el curso"""
        for examen in self:
            estudiantes = examen.curso_id.alumno_ids
            for estudiante in estudiantes:
                existing = self.env['school.calificacion'].search([
                    ('examen_id', '=', examen.id),
                    ('alumno_id', '=', estudiante.id)
                ])
                if not existing:
                    self.env['school.calificacion'].create({
                        'examen_id': examen.id,
                        'alumno_id': estudiante.id,
                        'punteo': 0.0,
                        'estado': 'pendiente'
                    })
        return True
    
    @api.multi
    def unlink(self):
        """Override para manejar eliminacion segura de examenes"""
        for examen in self:
            curso = examen.curso_id
            otros_examenes = curso.examen_ids.filtered(lambda e: e.id != examen.id)
            
            if curso.alumno_ids and len(otros_examenes) == 0:
                raise Warning(
                    "No se puede eliminar el examen '%s' porque es el ultimo examen del curso '%s' "
                    "y hay %d estudiante(s) inscrito(s). Un curso con estudiantes debe tener al menos un examen." % 
                    (examen.name, curso.name, len(curso.alumno_ids))
                )        
        return super(Examen, self).unlink()

    # Metodos para los botones de accion
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
                'default_punteo_maximo': self.punteo_maximo
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


class Calificacion(models.Model):
    _name = 'school.calificacion'
    _description = 'Calificacion de Estudiante en Examen'

    examen_id = fields.Many2one('school.examen', 'Examen', required=True, ondelete='cascade')
    alumno_id = fields.Many2one('school.alumno', 'Estudiante', required=True)
    
    # Calificacion
    punteo = fields.Float('Punteo Obtenido', default=0.0)
    respuesta_estudiante = fields.Text('Respuesta del Estudiante')
    
    # Campos computados
    punteo_maximo = fields.Float('Punteo Maximo', related='examen_id.punteo_maximo', readonly=True)
    porcentaje_obtenido = fields.Float('% Obtenido', compute='_compute_porcentaje', store=True)
    aprobado = fields.Boolean('Aprobado', compute='_compute_aprobado', store=True)
    
    # Estado
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('entregado', 'Entregado'),
        ('calificado', 'Calificado')
    ], 'Estado', default='pendiente')
    
    fecha_entrega = fields.Datetime('Fecha de Entrega')
    fecha_calificacion = fields.Datetime('Fecha de Calificacion')
    comentarios = fields.Text('Comentarios del Profesor')
    
    def __str__(self):
        return u'%s - %s (%s pts)' % (self.alumno_id.name, self.examen_id.name, self.punteo)
    
    @api.depends('punteo', 'punteo_maximo')
    def _compute_porcentaje(self):
        for calificacion in self:
            if calificacion.punteo_maximo > 0:
                calificacion.porcentaje_obtenido = (calificacion.punteo * 100.0) / calificacion.punteo_maximo
            else:
                calificacion.porcentaje_obtenido = 0.0
    
    @api.depends('porcentaje_obtenido')
    def _compute_aprobado(self):
        for calificacion in self:
            calificacion.aprobado = calificacion.porcentaje_obtenido >= 60.0 
    
    @api.constrains('punteo', 'punteo_maximo')
    def _check_punteos_validos(self):
        for calificacion in self:
            if calificacion.punteo < 0:
                raise Warning("El punteo obtenido no puede ser negativo.")
            if calificacion.punteo > calificacion.punteo_maximo:
                raise Warning("El punteo obtenido no puede ser mayor al punteo maximo.")
    
    @api.constrains('alumno_id', 'examen_id')
    def _check_alumno_en_curso(self):
        for calificacion in self:
            if calificacion.examen_id.curso_id not in calificacion.alumno_id.curso_ids:
                raise Warning(
                    "El estudiante '%s' no esta inscrito en el curso '%s'." % 
                    (calificacion.alumno_id.name, calificacion.examen_id.curso_id.name)
                )
    
    _sql_constraints = [
        ('unique_alumno_examen', 'unique(alumno_id, examen_id)', 
         'Un estudiante no puede tener multiples calificaciones para el mismo examen.')
    ]
