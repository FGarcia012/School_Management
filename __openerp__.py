{
    'name': 'School Management',
    'version': '1.0',
    'author': 'Alexander',
    'category': 'Education',
    'description': """
Sistema de Gestión Escolar Completo.
Incluye gestión de Cursos, Alumnos, Aulas, Exámenes y Horarios.
Sistema de usuarios con roles: Super Admin, Maestro y Alumno.
Reportes, filtros y vistas tree, form y graph.
Registro y login de usuarios con asignación automática de permisos.
Sistema de horarios híbrido con validaciones automáticas y generación de plantillas.
""",
    'depends': ['base', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'reports/reporte_cursos.xml',
        'reports/reporte_alumnos.xml',
        'reports/reporte_examenes.xml',
        'reports/reporte_horarios.xml',
        'reports/reporte_aulas.xml',
        'views/cursos_view.xml',
        'views/alumnos_view.xml',
        'views/aulas_view.xml',
        'views/examenes_view.xml',
        'views/calificaciones_view.xml',
        'views/horarios_view.xml',
        'views/school_users_view.xml',
        'views/curso_wizard_view.xml',
        'views/alumno_wizard_view.xml',
        'views/aula_wizard_view.xml',
        'views/examen_wizard_view.xml',
        'views/horario_wizard_view.xml',
        'views/school_menu.xml',
        'data/aulas_demo.xml',
        'data/cursos_demo.xml',
        'data/alumnos_demo.xml',
        'data/post_install.xml',
        'data/examenes_demo.xml',
        'data/horarios_demo.xml',
    ],
    'demo': [
        'data/aulas_demo.xml',
        'data/cursos_demo.xml',
        'data/alumnos_demo.xml',
        'data/post_install.xml',
        'data/examenes_demo.xml',
        'data/horarios_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}