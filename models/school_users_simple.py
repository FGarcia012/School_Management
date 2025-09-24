# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
import logging
from datetime import datetime
_logger = logging.getLogger(__name__)

class SchoolUser(models.Model):
    _inherit = 'res.users'

    school_role = fields.Selection([
        ('super_admin', 'Super Administrador'),
        ('teacher', 'Maestro/Administrador'),
        ('student', 'Alumno'),
    ], string='Rol en el Sistema Escolar')
    
    student_number = fields.Char(string='Numero de Estudiante')
    teacher_code = fields.Char(string='Codigo de Maestro')
    grade_level = fields.Char(string='Grado/Nivel')
    alumno_id = fields.Many2one('school.alumno', string='Perfil de Alumno')
    phone_number = fields.Char(string='Telefono')
    emergency_contact = fields.Char(string='Contacto de Emergencia')
    parent_email = fields.Char(string='Email de Padres')
    is_active_student = fields.Boolean(string='Estudiante Activo', default=True)
    registration_date = fields.Datetime(string='Fecha de Registro', default=fields.Datetime.now)

    @api.model
    def assign_super_admin_role(self):
        """Funcion para asignar el rol de super admin al usuario admin"""
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
        """Asigna grupos de seguridad segun el rol - Version simplificada"""
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
    """Wizard para crear perfiles de acceso - Solo Super Admin"""
    _name = 'school.user.registration'
    _description = 'Creacion de Perfiles de Acceso'
    
    name = fields.Char(string='Nombre Completo', required=True, 
                      help='Nombre completo de la persona')
    login = fields.Char(string='Email/Usuario', required=True,
                       help='Email que usara para acceder al sistema (debe ser unico)')
    password = fields.Char(string='Contrasena Temporal', required=True,
                          help='Contrasena inicial (la persona puede cambiarla despues)')
    
    school_role = fields.Selection([
        ('teacher', 'Crear Perfil de Maestro'),
        ('student', 'Crear Perfil de Alumno'),
    ], string='Tipo de Perfil a Crear', required=True, default='teacher',
       help='Que tipo de acceso tendra esta persona?')
    
    grade_level = fields.Char(string='Grado/Nivel',
                             help='Ejemplo: 3 Primaria, 2 Secundaria')
    aula_id = fields.Many2one('school.aula', string='Aula Asignada',
                             help='Seleccionar aula donde estara el estudiante')
    
    specialization = fields.Char(string='Materia/Especializacion',
                                help='Ejemplo: Matematicas, Historia, Ciencias')
    
    phone_number = fields.Char(string='Telefono Personal')
    parent_email = fields.Char(string='Email de Contacto Familiar',
                              help='Para estudiantes: email de padres o tutores')
    emergency_contact = fields.Char(string='Contacto de Emergencia',
                                   help='Nombre y telefono de contacto de emergencia')
    
    # Campo informativo
    notes = fields.Text(string='Notas Adicionales',
                       help='Cualquier informacion adicional sobre este perfil')
    
    @api.constrains('school_role', 'aula_id')
    def _check_student_aula_required(self):
        for record in self:
            if record.school_role == 'student' and not record.aula_id:
                raise exceptions.Warning(_('El aula es obligatoria para los estudiantes.'))

    @api.onchange('school_role')
    def _onchange_school_role(self):
        """Limpiar campos no relevantes cuando cambia el rol"""
        if self.school_role == 'teacher':
            self.grade_level = False
            self.aula_id = False
            self.parent_email = False
        elif self.school_role == 'student':
            self.specialization = False

    def _generate_student_number(self):
        """Generar numero de estudiante automatico"""
        year = datetime.now().year
        
        last_student = self.env['school.alumno'].search([
            ('numero', '!=', False)
        ], order='numero desc', limit=1)
        
        if last_student and last_student.numero:
            try:
                last_number = int(last_student.numero[-3:])
                new_number = "%s%03d" % (year, last_number + 1)
            except:
                new_number = "%s001" % year
        else:
            new_number = "%s001" % year
        
        while self.env['school.alumno'].search([('numero', '=', new_number)]):
            try:
                last_num = int(new_number[-3:])
                new_number = "%s%03d" % (year, last_num + 1)
            except:
                new_number = "%s001" % year
                break
        
        return new_number

    def _generate_teacher_code(self):
        """Generar codigo de maestro automatico"""
        last_teacher = self.env['res.users'].search([
            ('school_role', '=', 'teacher'),
            ('teacher_code', '!=', False)
        ], order='teacher_code desc', limit=1)
        
        if last_teacher and last_teacher.teacher_code:
            try:
                last_number = int(last_teacher.teacher_code.replace('PROF', ''))
                new_code = "PROF%03d" % (last_number + 1)
            except:
                new_code = "PROF001"
        else:
            new_code = "PROF001"
        
        while self.env['res.users'].search([('teacher_code', '=', new_code)]):
            try:
                last_num = int(new_code.replace('PROF', ''))
                new_code = "PROF%03d" % (last_num + 1)
            except:
                new_code = "PROF001"
                break
        
        return new_code

    @api.multi
    def register_user(self):
        """Crear perfil de acceso - Solo Super Admin"""
        self.ensure_one()
        
        if not self.env.user.has_group('school_management.group_school_super_admin'):
            raise exceptions.AccessError(_('Solo el Super Administrador puede crear perfiles de acceso.'))
        
        try:
            if not self.password or len(self.password) < 6:
                raise exceptions.Warning(_('La contrasena debe tener al menos 6 caracteres.'))
            
            existing_user = self.env['res.users'].search([('login', '=', self.login)], limit=1)
            if existing_user:
                raise exceptions.Warning(_('Ya existe un usuario con este email: %s') % self.login)
            
            student_number = ''
            teacher_code = ''
            
            if self.school_role == 'student':
                student_number = self._generate_student_number()
            elif self.school_role == 'teacher':
                teacher_code = self._generate_teacher_code()
            
            user_vals = {
                'name': self.name,
                'login': self.login,
                'password': self.password,
                'school_role': self.school_role,
                'phone_number': self.phone_number or '',
                'is_active_student': True if self.school_role == 'student' else False,
                'emergency_contact': self.emergency_contact or '',
            }
            
            if self.school_role == 'student':
                user_vals.update({
                    'student_number': student_number,
                    'grade_level': self.grade_level or '',
                    'parent_email': self.parent_email or '',
                })
            elif self.school_role == 'teacher':
                user_vals.update({
                    'teacher_code': teacher_code,
                })
            
            user = self.env['res.users'].create(user_vals)
            
            if self.school_role == 'student':
                aula = self.aula_id
                if not aula:
                    aula = self.env['school.aula'].search([], limit=1)
                    if not aula:
                        raise exceptions.Warning(_('No hay aulas disponibles. Debe crear al menos una aula antes de crear estudiantes.'))
                
                alumno = self.env['school.alumno'].create({
                    'name': self.name,
                    'numero': student_number,
                    'aula_id': aula.id,
                })
                user.write({'alumno_id': alumno.id})
            
            school_user = self.env['res.users'].browse(user.id)
            school_user._assign_groups_by_role(school_user, self.school_role)
            
            role_name = dict(self._fields['school_role'].selection).get(self.school_role, '').replace('Crear Perfil de ', '')
            credentials_info = ""
            
            if self.school_role == 'student':
                credentials_info = "\n- Numero de Estudiante: %s\n- Aula: %s" % (student_number, aula.name)
            elif self.school_role == 'teacher':
                credentials_info = "\n- Codigo de Maestro: %s" % teacher_code
            
            message = """Perfil creado exitosamente:
- Nombre: %s
- Rol: %s
- Email/Usuario: %s%s

Cualquier persona puede ingresar desde cualquier dispositivo usando estas credenciales.""" % (self.name, role_name, self.login, credentials_info)
            
            result_wizard = self.env['school.user.registration.result'].create({
                'message': message,
                'user_created': True,
            })
            
            return {
                'type': 'ir.actions.act_window',
                'name': _('Perfil de Acceso Creado'),
                'res_model': 'school.user.registration.result',
                'res_id': result_wizard.id,
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
            }
            
        except Exception as e:
            raise exceptions.Warning(_('Error al crear el perfil de acceso: %s') % str(e))


class SchoolUserRegistrationResult(models.TransientModel):
    """Wizard para mostrar resultado exitoso"""
    _name = 'school.user.registration.result'
    _description = 'Resultado de Creacion de Perfil'
    
    message = fields.Text(string='Resultado', readonly=True)
    user_created = fields.Boolean(string='Usuario Creado', readonly=True)
    
    @api.multi
    def action_close(self):
        """Cerrar el wizard"""
        return {'type': 'ir.actions.act_window_close'}