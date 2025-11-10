{
    'name': 'Bike_Shop',
    'version': '1.0',
    'summary': 'Module de gestion pour un magasin de vélos - Vente et Location',
    'description': """
        Module de gestion pour un magasin de vélos
        ==========================================
        
        Fonctionnalités :
        - Gestion du catalogue de vélos
        - Location de vélos (courte et longue durée)
        - Gestion des clients et contrats
        - Suivi des ventes et locations
    """,
    'author': 'Votre Nom',
    'website': 'https://github.com/johnyazbeck/custom_addons',
    'category': 'Sales',
    'depends': ['base', 'sale', 'stock', 'product'],  # Ajout de 'product'
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/bike_views.xml',
        'views/rental_views.xml',
        'views/menu_views.xml',
        'demo/demo_data.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}