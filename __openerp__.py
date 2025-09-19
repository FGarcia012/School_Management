{
    'name': 'School Management',
    'version': '1.0',
    'author': 'Alexander',
    'category': 'Education',
    'description': """
Sistema de Gestión Escolar Completo.
Incluye gestión de Cursos, Alumnos, Aulas y Exámenes.
Sistema de usuarios con roles: Super Admin, Maestro y Alumno.
Reportes, filtros y vistas tree, form y graph.
Registro y login de usuarios con asignación automática de permisos.
""",
    'depends': ['base', 'web'],
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/cursos_view.xml',
        'views/alumnos_view.xml',
        'views/aulas_view.xml',
        'views/examenes_view.xml',
        'views/school_users_view.xml',
        'views/curso_wizard_view.xml',
        'views/alumno_wizard_view.xml',
        'views/aula_wizard_view.xml',
        'views/examen_wizard_view.xml',
        'views/school_menu.xml',
        'data/cursos_demo.xml',
        'data/alumnos_demo.xml',
        'data/aulas_demo.xml',
        'data/examenes_demo.xml',
    ],
    'demo': [
        'data/cursos_demo.xml',
        'data/alumnos_demo.xml',
        'data/aulas_demo.xml',
        'data/examenes_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}