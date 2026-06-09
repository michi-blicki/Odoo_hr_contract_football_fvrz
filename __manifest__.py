# -*- coding: utf-8 -*-
{
    'name': "HR Contract - Football Contracts for FVRZ clubs",

    'summary': "Add specific contract values for clubs associated with FVRZ to hr.contract",

    'description': """
This module adds football specific contract values for clubs associated with FVRZ to hr.contract.
The FVRZ has an aggreement with the tax authorities of the canton of Zurich, Switzerland, which allows associated
clubs to pay their football trainers within the grassroots or amateur football framework with a special tax regime. 
These regelementations are described in the document
"Spesenreglement für Trainer von Fussballvereinen des Fussbalverbandes Region Zürich (FVRZ)"
(https://www.fvrz.ch/Portaldata/10/Resources/dokumente/weisungenhandbuch/Spesenreglement_TrainerVersion1.pdf).
Football icon of Odoo HR Contract Football module by https://www.flaticon.com/de/kostenloses-icon/fussball_2817805.
    """,

    'author': "Michael Blickenstorfer",
    'website': "https://github.com/michi-blicki/Odoo_hr_contract_football_fvrz",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '18.0.1.0.0',
    'license': "AGPL-3",
    'application': False,
    'auto_install': False,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['hr_contract_football'],

    # always loaded
    'data': [
        'views/view_hr_contract_form_football_fvrz.xml',
    ],

    #
    # Hooks
    #'pre_init_hook': 'pre_init_hook',
    #'post_init_hook': 'post_init_hook',
    #'uninstall_hook': 'uninstall_hook',
}

