{
    'name': "My Bike Shop",
    'summary': "Module de gestion pour un magasin de vélos",
    'description': "Gestion de vélos et locations",
    'author': "Yazbeck John et Jose Bigoro",
    'website': "https://github.com/johnyazbeck/custom_addons",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/views.xml',
        'views/bike_menus.xml',
        'views/templates.xml',
        # RETIREZ demo/demo.xml de la section data
    ],
    'demo': [
        'demo/demo.xml',  # Gardez-le seulement ici
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}