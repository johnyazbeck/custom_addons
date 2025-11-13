from odoo import models, fields, api
from datetime import datetime, timedelta

class BikeProduct(models.Model):
    _name = 'bike.shop.product'
    _description = 'Produit du magasin de vélos'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Nom du produit', required=True, tracking=True)
    product_type = fields.Selection([
        ('bike', 'Vélo'),
        ('part', 'Pièce détachée'),
        ('accessory', 'Accessoire'),
    ], string='Type de produit', required=True, default='bike')
    
    brand = fields.Char(string='Marque', tracking=True)
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
    
    quantity = fields.Integer(string='Quantité en stock', default=0)
    min_stock = fields.Integer(string='Stock minimum', default=1)
    
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


class BikeRental(models.Model):
    _name = 'bike.shop.rental'
    _description = 'Location de vélo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'start_date desc'

    name = fields.Char(string='Référence', default='Nouvelle Location', readonly=True)
    bike_id = fields.Many2one('bike.shop.product', string='Vélo', required=True, 
                             domain="[('product_type', '=', 'bike')]")
    customer_id = fields.Many2one('res.partner', string='Client', required=True)
    
    start_date = fields.Datetime(string='Date de début', required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(string='Date de fin', required=True)
    rental_duration = fields.Integer(string='Durée (jours)', compute='_compute_duration', store=True)
    
    rental_type = fields.Selection([
        ('hour', 'À l\'heure'),
        ('day', 'À la journée'),
        ('week', 'À la semaine'),
    ], string='Type de location', required=True, default='day')
    
    unit_price = fields.Float(string='Prix unitaire')
    total_price = fields.Float(string='Prix total', compute='_compute_total_price', store=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('returned', 'Retourné'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft', tracking=True)
    
    notes = fields.Text(string='Notes')
    
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
    for record in self:
        if record.start_date and record.end_date:
            # En Odoo 19, les Datetime sont déjà des objets datetime
            duration = (record.end_date - record.start_date).days
            record.rental_duration = duration if duration > 0 else 1
        else:
            record.rental_duration = 0
    
    @api.depends('rental_duration', 'unit_price', 'rental_type')
    def _compute_total_price(self):
        for record in self:
            if record.rental_type == 'hour':
                record.total_price = record.unit_price * (record.rental_duration * 24)
            elif record.rental_type == 'week':
                record.total_price = record.unit_price * (max(record.rental_duration / 7, 1))
            else:
                record.total_price = record.unit_price * record.rental_duration
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouvelle Location') == 'Nouvelle Location':
            vals['name'] = self.env['ir.sequence'].next_by_code('bike.shop.rental') or 'Nouvelle Location'
        return super().create(vals)
    
    @api.onchange('bike_id', 'rental_type')
    def _onchange_bike_rental_type(self):
        if self.bike_id:
            if self.rental_type == 'hour':
                self.unit_price = self.bike_id.rental_price_hour
            elif self.rental_type == 'day':
                self.unit_price = self.bike_id.rental_price_day
            elif self.rental_type == 'week':
                self.unit_price = self.bike_id.rental_price_week
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_start(self):
        self.write({'state': 'in_progress'})
    
    def action_return(self):
        self.write({'state': 'returned'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})