# -*- coding: utf-8 -*-

{
    'name': 'Contract Dynamic Fields',
    'version': '11.0.1.0.0',
    'summary': """Ajouter des champs au formulaire du contrat d'employé""",
    'description': """Ajouter des champs personnalisés au formulaire du contrat d'employé""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Thomas ATCHA',
    'company': 'Roots technologies',
    'maintainer': 'Roots technologies',
    'website': "https://www.roots-technologies.com",
    'depends': ['base', 'hr','hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_fields_view.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
