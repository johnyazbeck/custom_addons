# -*- coding: utf-8 -*-
from odoo import models, fields

class Course(models.Model):
    _name = 'open.academy.course'
    _description = 'Open Academy Course'
    
    name = fields.Char(string='Nom du cours', required=True)
    description = fields.Text(string='Description')