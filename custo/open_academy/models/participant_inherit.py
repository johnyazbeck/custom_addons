# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    birthdate = fields.Date(string="Date de naissance")
    age = fields.Integer(
        string="Âge",
        compute="_compute_age",
        store=True,
        help="Âge calculé à partir de la date de naissance.",
    )

    @api.depends("birthdate")
    def _compute_age(self):
        today = date.today()
        for partner in self:
            if partner.birthdate:
                partner.age = relativedelta(today, partner.birthdate).years
            else:
                partner.age = 0
