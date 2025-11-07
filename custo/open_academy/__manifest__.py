{
    "name": "Open Academy",
    "version": "19.0.1.0.0",
    "license": "LGPL-3",
    "depends": ["base", "contacts"],
    "data": [
        "security/ir.model.access.csv",
        "views/session_view.xml",
        "views/partner_views.xml",
    ],
    "demo": [
        "demo/demo.xml",   # uniquement des données d'exemple, optionnel
    ],
    "installable": True,
    "application": True,
}
