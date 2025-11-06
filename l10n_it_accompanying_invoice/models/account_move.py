# Copyright 2017 Lorenzo Battistini - Agile Business Group
# Copyright 2020 Simone Vanin - Agile Business Group
# Copyright 2023 Simone Rubino - Aion Tech
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, models


class AccountMove(models.Model):
    _name = "account.move"
    _inherit = [
        "account.move",
        "l10n_it_delivery_note.delivery_mixin",
    ]

    @api.onchange(
        "partner_id",
    )
    def _onchange_partner_shipping_data(self):
        for invoice in self:
            partner = invoice.partner_id
            if partner:
                invoice.delivery_transport_reason_id = (
                    partner.default_transport_reason_id
                )
                invoice.delivery_transport_condition_id = (
                    partner.default_transport_condition_id
                )
                invoice.delivery_transport_method_id = (
                    partner.default_transport_method_id
                )
                invoice.delivery_goods_appearance_id = (
                    partner.default_goods_appearance_id
                )

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)

        delivery_carrier_info_values = (
            self.delivery_carrier_id._l10n_it_edi_get_values()
        )

        res["delivery_carrier_info"] = delivery_carrier_info_values

        return res
