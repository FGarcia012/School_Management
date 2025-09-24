# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning
import datetime

class Alumno(models.Model):
    _name = 'school.alumno'
    _description = 'Alumno'

    name = fields.Char('Nombre', required=True)
    numero = fields.Char('Numero de estudiante', readonly=True, copy=False)
    
    # Relaciones principales
    aula_id = fields.Many2one('school.aula', 'Aula Asignada', required=True)
    curso_ids = fields.Many2many('school.curso', 'alumno_curso_rel', 'alumno_id', 'curso_id', 'Cursos Inscritos')
    user_ids = fields.One2many('res.users', 'alumno_id', 'Usuarios Asociados')
    
    calificacion_ids = fields.One2many('school.calificacion', 'alumno_id', 'Calificaciones')
    
    # Campos informativos
    total_cursos = fields.Integer('Total de Cursos', compute='_compute_total_cursos', store=True)
    
    @api.depends('curso_ids')
    def _compute_total_cursos(self):
        for alumno in self:
            alumno.total_cursos = len(alumno.curso_ids)
    
    @api.constrains('numero')
    def _check_numero_unico(self):
        for alumno in self:
            if alumno.numero:
                existing = self.search([('numero', '=', alumno.numero), ('id', '!=', alumno.id)])
                if existing:
                    raise Warning("El numero de estudiante '%s' ya esta asignado a otro alumno." % alumno.numero)
    
    @api.constrains('aula_id')
    def _check_capacidad_aula(self):
        for alumno in self:
            if alumno.aula_id:
                alumnos_en_aula = self.search([('aula_id', '=', alumno.aula_id.id)])
                if len(alumnos_en_aula) > alumno.aula_id.capacidad:
                    raise Warning(
                        "No se puede asignar al alumno al aula '%s'. "
                        "La capacidad maxima es de %d estudiantes." % 
                        (alumno.aula_id.name, alumno.aula_id.capacidad)
                    )

    # Generacion automatica del carnet
    @api.model
    def create(self, vals):
        if 'numero' not in vals or not vals['numero']:
            vals['numero'] = self._generar_numero_carnet()
        return super(Alumno, self).create(vals)
    
    @api.model
    def _generar_numero_carnet(self):
        """Genera el numero de carnet automaticamente con formato ano + secuencial de 3 digitos"""
        current_year = datetime.datetime.now().year
        
        # Buscar el ultimo numero de carnet del ano actual
        prefix = str(current_year)
        last_alumno = self.search([
            ('numero', 'like', prefix + '%')
        ], order='numero desc', limit=1)
        
        if last_alumno:
            # Extraer el numero secuencial del ultimo carnet
            last_number = last_alumno.numero
            try:
                sequence = int(last_number.replace(prefix, ''))
                next_sequence = sequence + 1
            except ValueError:
                next_sequence = 1
        else:
            next_sequence = 1
        # Formatear como ano + 3 digitos
        return '%s%03d' % (current_year, next_sequence)

    @api.multi
    def unlink(self):
        """Override para manejar eliminacion segura de alumnos"""
        for alumno in self:
            if alumno.calificacion_ids:
                calificaciones_count = len(alumno.calificacion_ids)
                self.env['school.calificacion'].search([
                    ('alumno_id', '=', alumno.id)
                ]).unlink()
        
        return super(Alumno, self).unlink()

    # Metodos para los botones de accion
    @api.multi
    def abrir_wizard_agregar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Agregar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_alumno_wizard_agregar').id,
            'target': 'new',
            'context': {'default_mode': 'agregar'}
        }

    @api.multi
    def abrir_wizard_actualizar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Actualizar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_alumno_wizard_actualizar').id,
            'target': 'new',
            'context': {
                'default_mode': 'actualizar',
                'active_id': self.id,
                'default_name': self.name,
                'default_numero': self.numero,
                'default_aula_id': self.aula_id.id if self.aula_id else False
            }
        }

    @api.multi
    def abrir_wizard_eliminar(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Eliminar Alumno',
            'res_model': 'alumno.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.env.ref('school_management.view_alumno_wizard_eliminar').id,
            'target': 'new',
            'context': {
                'default_mode': 'eliminar',
                'active_id': self.id,
                'default_name': self.name
            }
        }