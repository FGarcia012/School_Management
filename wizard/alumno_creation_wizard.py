# -*- coding: utf-8 -*-
from openerp import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)

class AlumnoCreationWizard(models.TransientModel):
    """Wizard para que Maestros puedan crear alumnos facilmente"""
    _name = 'school.alumno.creation.wizard'
    _description = 'Creacion Rapida de Alumnos'
    
    name = fields.Char(string='Nombre Completo del Alumno', required=True,
                      help='Nombre completo del estudiante')
    
    grade_level = fields.Char(string='Grado/Nivel', required=True,
                             help='Ejemplo: 3 Primaria, 2 Secundaria')
    aula_id = fields.Many2one('school.aula', string='Aula', required=True,
                             help='Aula donde estara el estudiante')
    
    parent_email = fields.Char(string='Email de Padres/Tutores',
                              help='Email de contacto de los padres')
    parent_phone = fields.Char(string='Telefono de Padres/Tutores',
                              help='Telefono de contacto de los padres')
    emergency_contact = fields.Char(string='Contacto de Emergencia',
                                   help='Nombre y telefono de emergencia')
    
    create_user_profile = fields.Boolean(string='Crear Perfil de Acceso al Sistema',
                                        default=False,
                                        help='Quiere que el alumno pueda acceder al sistema desde otros dispositivos?')
    
    login_email = fields.Char(string='Email para Acceder al Sistema',
                             help='Email que usara el alumno para entrar al sistema')
    temp_password = fields.Char(string='Contrasena Temporal',
                               help='Contrasena inicial (el alumno puede cambiarla)')
    
    @api.onchange('create_user_profile')
    def _onchange_create_user_profile(self):
        """Limpiar campos de acceso si se desactiva la opcion"""
        if not self.create_user_profile:
            self.login_email = ''
            self.temp_password = ''

    @api.constrains('login_email')
    def _check_unique_email(self):
        """Validar que el email sea unico si se va a crear perfil"""
        for record in self:
            if record.create_user_profile and record.login_email:
                existing = self.env['res.users'].search([('login', '=', record.login_email)])
                if existing:
                    raise exceptions.Warning(_('Ya existe un usuario con este email: %s') % record.login_email)

    def _generate_student_number(self):
        """Generar numero de estudiante automatico"""
        year = fields.Date.today().year
        last_student = self.env['school.alumno'].search([], order='numero desc', limit=1)
        
        if last_student and last_student.numero:
            try:
                last_number = int(last_student.numero[-3:])
                new_number = "%s%03d" % (year, last_number + 1)
            except:
                new_number = "%s001" % year
        else:
            new_number = "%s001" % year
        
        return new_number

    @api.multi
    def create_alumno(self):
        """Crear el alumno (con o sin perfil de acceso)"""
        self.ensure_one()
        
        if not (self.env.user.has_group('school_management.group_school_super_admin') or 
                self.env.user.has_group('school_management.group_school_teacher')):
            raise exceptions.AccessError(_('Solo Super Administradores y Maestros pueden crear alumnos.'))
        
        try:
            student_number = self._generate_student_number()
            
            alumno = self.env['school.alumno'].create({
                'name': self.name,
                'numero': student_number,
                'aula_id': self.aula_id.id,
            })
            
            user_created = False
            login_info = ""
            
            if self.create_user_profile and self.login_email and self.temp_password:
                
                if not self.env.user.has_group('school_management.group_school_super_admin'):
                    raise exceptions.Warning(_('Solo el Super Administrador puede crear perfiles de acceso. Puede crear el alumno sin perfil y pedirle al Super Admin que cree el perfil despues.'))
                
                try:
                    user_vals = {
                        'name': self.name,
                        'login': self.login_email,
                        'password': self.temp_password,
                        'school_role': 'student',
                        'student_number': student_number,
                        'grade_level': self.grade_level,
                        'parent_email': self.parent_email or '',
                        'phone_number': self.parent_phone or '',
                        'emergency_contact': self.emergency_contact or '',
                        'is_active_student': True,
                        'alumno_id': alumno.id,
                    }
                    
                    user = self.env['res.users'].create(user_vals)
                    
                    group_student = self.env.ref('school_management.group_school_student', raise_if_not_found=False)
                    if group_student:
                        user.write({'groups_id': [(4, group_student.id)]})
                    
                    user_created = True
                    login_info = "\n\nPERFIL DE ACCESO CREADO:\n* Email: %s\n* Contrasena: %s\n* El alumno puede acceder desde cualquier dispositivo" % (self.login_email, self.temp_password)
                    
                except Exception as e:
                    _logger.warning("Error creando perfil de acceso: %s" % str(e))
                    login_info = "\n\nADVERTENCIA: El alumno se creo correctamente, pero hubo un error creando el perfil de acceso: %s" % str(e)
            
            success_message = "Alumno creado exitosamente:\n\n" \
                            "INFORMACION ACADEMICA:\n" \
                            "* Nombre: %s\n" \
                            "* Numero de Estudiante: %s\n" \
                            "* Grado/Nivel: %s\n" \
                            "* Aula: %s\n\n" \
                            "INFORMACION DE CONTACTO:\n" \
                            "* Email de Padres: %s\n" \
                            "* Telefono de Padres: %s\n" \
                            "* Contacto de Emergencia: %s%s" % (
                self.name,
                student_number,
                self.grade_level,
                self.aula_id.name,
                self.parent_email or 'No especificado',
                self.parent_phone or 'No especificado',
                self.emergency_contact or 'No especificado',
                login_info
            )
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Alumno Creado'),
                    'message': _(success_message),
                    'type': 'success',
                    'sticky': True,
                }
            }
            
        except Exception as e:
            raise exceptions.Warning(_('Error al crear el alumno: %s') % str(e))

