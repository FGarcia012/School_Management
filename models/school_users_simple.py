# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)

class SchoolUser(models.Model):
    _inherit = 'res.users'

    # Campos específicos para el sistema escolar (todos opcionales para evitar errores)
    school_role = fields.Selection([
        ('super_admin', 'Super Administrador'),
        ('teacher', 'Maestro/Administrador'),
        ('student', 'Alumno'),
    ], string='Rol en el Sistema Escolar')
    
    student_number = fields.Char(string='Número de Estudiante')
    teacher_code = fields.Char(string='Código de Maestro')
    grade_level = fields.Char(string='Grado/Nivel')
    alumno_id = fields.Many2one('school.alumno', string='Perfil de Alumno')
    phone_number = fields.Char(string='Teléfono')
    emergency_contact = fields.Char(string='Contacto de Emergencia')
    parent_email = fields.Char(string='Email de Padres')
    is_active_student = fields.Boolean(string='Estudiante Activo', default=True)
    registration_date = fields.Datetime(string='Fecha de Registro', default=fields.Datetime.now)

    @api.model
    def assign_super_admin_role(self):
        """Función para asignar el rol de super admin al usuario admin"""
        try:
            admin_user = self.search([('login', '=', 'admin')], limit=1)
            if admin_user:
                admin_user.write({'school_role': 'super_admin'})
                try:
                    group_super_admin = self.env.ref('school_management.group_school_super_admin')
                    if group_super_admin:
                        admin_user.write({'groups_id': [(4, group_super_admin.id)]})
                except Exception as e:
                    _logger.warning("No se pudo asignar grupo super admin: %s" % str(e))
        except Exception as e:
            _logger.warning("No se pudo configurar super admin: %s" % str(e))
        return True

    def _assign_groups_by_role(self, user, role):
        """Asigna grupos de seguridad según el rol - Versión simplificada"""
        try:
            group_ref = None
            if role == 'super_admin':
                group_ref = self.env.ref('school_management.group_school_super_admin', raise_if_not_found=False)
            elif role == 'teacher':
                group_ref = self.env.ref('school_management.group_school_teacher', raise_if_not_found=False)
            elif role == 'student':
                group_ref = self.env.ref('school_management.group_school_student', raise_if_not_found=False)
            
            if group_ref:
                user.write({'groups_id': [(4, group_ref.id)]})
                
        except Exception as e:
            _logger.warning("Error asignando grupos: %s" % str(e))


class SchoolUserRegistration(models.TransientModel):
    """Wizard simplificado para registro de nuevos usuarios"""
    _name = 'school.user.registration'
    _description = 'Registro de Usuario Escolar'
    
    # Información básica
    name = fields.Char(string='Nombre Completo', required=True)
    login = fields.Char(string='Usuario/Email', required=True)
    password = fields.Char(string='Contraseña', required=True)
    
    # Rol
    school_role = fields.Selection([
        ('teacher', 'Maestro/Administrador'),
        ('student', 'Alumno'),
    ], string='Rol', required=True, default='student')
    
    # Campos opcionales
    student_number = fields.Char(string='Número de Estudiante')
    teacher_code = fields.Char(string='Código de Maestro')
    curso_id = fields.Many2one('school.curso', string='Curso')
    phone_number = fields.Char(string='Teléfono')
    
    @api.multi
    def register_user(self):
        """Crear el nuevo usuario - Versión simplificada"""
        self.ensure_one()
        
        try:
            # Crear usuario básico
            user_vals = {
                'name': self.name,
                'login': self.login,
                'password': self.password,
                'school_role': self.school_role,
            }
            
            # Agregar campos opcionales si están presentes
            if self.student_number:
                user_vals['student_number'] = self.student_number
            if self.teacher_code:
                user_vals['teacher_code'] = self.teacher_code
            if self.phone_number:
                user_vals['phone_number'] = self.phone_number
            
            # Crear el usuario
            user = self.env['res.users'].create(user_vals)
            
            # Si es estudiante y tiene curso, crear perfil de alumno
            if self.school_role == 'student' and self.curso_id:
                try:
                    alumno = self.env['school.alumno'].create({
                        'name': self.name,
                        'numero': self.student_number or '',
                        'curso_id': self.curso_id.id,
                    })
                    user.write({'alumno_id': alumno.id})
                except:
                    pass  # No fallar si no se puede crear el alumno
            
            # Asignar grupos
            school_user = self.env['res.users'].browse(user.id)
            school_user._assign_groups_by_role(school_user, self.school_role)
            
            return {
                'type': 'ir.actions.client',
                'tag': 'reload',
            }
            
        except Exception as e:
            raise exceptions.UserError(_('Error al crear usuario: %s') % str(e))