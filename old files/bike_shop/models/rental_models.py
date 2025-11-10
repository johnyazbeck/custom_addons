from odoo import models, fields, api
from datetime import datetime, timedelta

class BikeRental(models.Model):
    _name = 'bike.shop.rental'
    _description = 'Location de vélo'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Référence', default='Nouvelle Location')
    bike_id = fields.Many2one('bike.shop.product', string='Vélo', required=True)
    customer_id = fields.Many2one('res.partner', string='Client', required=True)
    
    start_date = fields.Datetime(string='Date de début', required=True)
    end_date = fields.Datetime(string='Date de fin', required=True)
    rental_duration = fields.Integer(string='Durée (jours)', compute='_compute_duration')
    
    rental_type = fields.Selection([
        ('hour', 'À l\'heure'),
        ('day', 'À la journée'),
        ('week', 'À la semaine'),
    ], string='Type de location', required=True)
    
    unit_price = fields.Float(string='Prix unitaire')
    total_price = fields.Float(string='Prix total', compute='_compute_total_price')
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('returned', 'Retourné'),
        ('cancelled', 'Annulée'),
    ], string='État', default='draft')
    
    notes = fields.Text(string='Notes')
    
    @api.depends('start_date', 'end_date')
    def _compute_duration(self):
        for record in self:
            if record.start_date and record.end_date:
                start = fields.Datetime.from_string(record.start_date)
                end = fields.Datetime.from_string(record.end_date)
                record.rental_duration = (end - start).days
            else:
                record.rental_duration = 0
    
    @api.depends('rental_duration', 'unit_price', 'rental_type')
    def _compute_total_price(self):
        for record in self:
            if record.rental_type == 'hour':
                record.total_price = record.unit_price * (record.rental_duration * 24)
            elif record.rental_type == 'week':
                record.total_price = record.unit_price * (record.rental_duration / 7)
            else:
                record.total_price = record.unit_price * record.rental_duration
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nouvelle Location') == 'Nouvelle Location':
            vals['name'] = self.env['ir.sequence'].next_by_code('bike.shop.rental') or 'Nouvelle Location'
        return super().create(vals)
    
    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_start(self):
        self.write({'state': 'in_progress'})
    
    def action_return(self):
        self.write({'state': 'returned'})
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})