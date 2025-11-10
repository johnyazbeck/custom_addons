from odoo import models, fields, api

class BikeProduct(models.Model):
    _name = 'bike.shop.product'
    _description = 'Produit du magasin de vélos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du produit', required=True)
    product_type = fields.Selection([
        ('bike', 'Vélo'),
        ('part', 'Pièce détachée'),
        ('accessory', 'Accessoire'),
    ], string='Type de produit', required=True)
    
    brand = fields.Char(string='Marque')
    model = fields.Char(string='Modèle')
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
    ], string='Taille')
    color = fields.Char(string='Couleur')
    
    purchase_price = fields.Float(string='Prix d\'achat')
    sale_price = fields.Float(string='Prix de vente')
    rental_price_hour = fields.Float(string='Prix location/heure')
    rental_price_day = fields.Float(string='Prix location/jour')
    rental_price_week = fields.Float(string='Prix location/semaine')
    
    quantity = fields.Integer(string='Quantité en stock')
    min_stock = fields.Integer(string='Stock minimum')
    
    description = fields.Text(string='Description')
    is_available = fields.Boolean(string='Disponible', default=True)
    
    # Relations
    rental_ids = fields.One2many('bike.shop.rental', 'bike_id', string='Locations')
    
    @api.depends('quantity')
    def _compute_stock_status(self):
        for record in self:
            if record.quantity <= 0:
                record.stock_status = 'out_of_stock'
            elif record.quantity <= record.min_stock:
                record.stock_status = 'low_stock'
            else:
                record.stock_status = 'in_stock'
    
    stock_status = fields.Selection([
        ('in_stock', 'En stock'),
        ('low_stock', 'Stock faible'),
        ('out_of_stock', 'Rupture de stock'),
    ], string='Statut du stock', compute='_compute_stock_status', store=True)