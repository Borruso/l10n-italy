# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl <gborruso@dinamicheaziendali.it>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.TransientModel):
    _inherit = "account.move"

    def _l10n_it_edi_search_partner(self, company, vat, codice_fiscale, email):
        partner = super()._l10n_it_edi_search_partner(
            company, vat, codice_fiscale, email
        )
        # if not partner:
        # TODO: create partner
        return partner
