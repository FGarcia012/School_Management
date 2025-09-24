# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from datetime import datetime

class ReporteCursos(models.AbstractModel):
    _name = 'report.school_management.reporte_cursos_template'
    
    @api.multi
    def render_html(self, data=None):
        """Renderiza el reporte de cursos"""
        cursos = self.env['school.curso'].search([])
        
        docargs = {
            'doc_ids': cursos.ids,
            'doc_model': 'school.curso',
            'docs': cursos,
            'data': data,
            'total_cursos': len(cursos),
            'fecha_reporte': datetime.now(),
        }
        return self.env['report'].render('school_management.reporte_cursos_template', docargs)

class ReporteAlumnos(models.AbstractModel):
    _name = 'report.school_management.reporte_alumnos_template'
    
    @api.multi
    def render_html(self, data=None):
        """Renderiza el reporte de alumnos"""
        alumnos = self.env['school.alumno'].search([])
        
        docargs = {
            'doc_ids': alumnos.ids,
            'doc_model': 'school.alumno',
            'docs': alumnos,
            'data': data,
            'total_alumnos': len(alumnos),
            'fecha_reporte': datetime.now(),
        }
        return self.env['report'].render('school_management.reporte_alumnos_template', docargs)

class ReporteExamenes(models.AbstractModel):
    _name = 'report.school_management.reporte_examenes_template'
    
    @api.multi
    def render_html(self, data=None):
        """Renderiza el reporte de examenes"""
        examenes = self.env['school.examen'].search([])
        
        docargs = {
            'doc_ids': examenes.ids,
            'doc_model': 'school.examen',
            'docs': examenes,
            'data': data,
            'total_examenes': len(examenes),
            'fecha_reporte': datetime.now(),
        }
        return self.env['report'].render('school_management.reporte_examenes_template', docargs)

class ReporteHorarios(models.AbstractModel):
    _name = 'report.school_management.reporte_horarios_template'
    
    @api.multi
    def render_html(self, data=None):
        """Renderiza el reporte de horarios"""
        horarios = self.env['school.horario'].search([])
        
        docargs = {
            'doc_ids': horarios.ids,
            'doc_model': 'school.horario',
            'docs': horarios,
            'data': data,
            'total_horarios': len(horarios),
            'fecha_reporte': datetime.now(),
        }
        return self.env['report'].render('school_management.reporte_horarios_template', docargs)

class ReporteAulas(models.AbstractModel):
    _name = 'report.school_management.reporte_aulas_template'
    
    @api.multi
    def render_html(self, data=None):
        """Renderiza el reporte de aulas"""
        aulas = self.env['school.aula'].search([])
        
        docargs = {
            'doc_ids': aulas.ids,
            'doc_model': 'school.aula',
            'docs': aulas,
            'data': data,
            'total_aulas': len(aulas),
            'fecha_reporte': datetime.now(),
        }
        return self.env['report'].render('school_management.reporte_aulas_template', docargs)