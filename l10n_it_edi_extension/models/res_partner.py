#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_it_extension_eori_code = fields.Char(
        string="EORI Code",
        size=20,
    )
