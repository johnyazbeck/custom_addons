{
    'name': "My Bike Shop",
    'summary': "Module de gestion pour un magasin de vélos",
    'description': "Gestion de vélos et locations",
    'author': "Yazbeck John et Jose Bigoro",
    'website': "https://github.com/johnyazbeck/custom_addons",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/bike_menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}