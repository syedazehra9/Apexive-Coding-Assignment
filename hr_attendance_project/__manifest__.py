# -*- coding: utf-8 -*-
{
    'name': 'Attendance Project and Tasks',
    'version': '16.0.0.1',
    'category': 'HR',
    'author': 'Nida Zehra',
    'summary': 'Modification of Attendance in Odoo',
    'description': """
Modification of Attendance Module in Odoo
Enhance the existing Attendance module in Odoo to allow users to:
Select a Project: Users should be able to choose a specific project while checking in.
Select a Project Task: Along with selecting a project, users should also be able to select a specific task related to the chosen project.
Write Descriptions: Enable users to add a description for their activities during both check-in and check-out.
    """,
    'depends': ['hr_attendance','project'],
    'data': [
        'views/hr_attendance_view.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'hr_attendance_project/static/src/js/hr_attendance_inherit.js',
            'hr_attendance_project/static/src/xml/hr_attendance_inherit.xml',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
}