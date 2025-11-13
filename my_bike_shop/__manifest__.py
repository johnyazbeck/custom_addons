{
    'name': "My Bike Shop",
    'summary': "Module de gestion pour un magasin de vélos - Vente et Location",
    'description': """
        Gestion complète d'un magasin de vélos
        ======================================
        - Vente de vélos et accessoires
        - Location de vélos (courte/longue durée)
        - Gestion des stocks et clients
    """,
    'author': "Yazbeck John et Jose Bigoro",
    'website': "https://github.com/johnyazbeck/custom_addons",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base', 'sale', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',  # Assurez-vous que le nom est correct
        'views/views.xml',
        'views/bike_menus.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}