#  Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields
from odoo.tests import tagged

from odoo.addons.l10n_it_edi_extension.tests.common import Common


@tagged("post_install", "-at_install")
class TestAccountMoveExport(Common):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_accompanying_invoice"

        cls.italian_delivery_carrier = cls.env["res.partner"].create(
            {
                "name": "Italian Carrier",
                "vat": "IT12345678903",
                "country_id": cls.env.ref("base.it").id,
                "company_id": False,
                "is_company": True,
            }
        )

    def test_export_delivery_data(self):
        italian_partner = self.italian_partner_a
        italian_partner.default_transport_condition_id = self.env.ref(
            "l10n_it_delivery_note.transport_condition_PF"
        )
        italian_partner.default_goods_appearance_id = self.env.ref(
            "l10n_it_delivery_note.goods_appearance_CAR"
        )
        italian_partner.default_transport_reason_id = self.env.ref(
            "l10n_it_delivery_note.transport_reason_VEN"
        )
        italian_partner.default_transport_method_id = self.env.ref(
            "l10n_it_delivery_note.transport_method_MIT"
        )

        invoice = self.init_invoice(
            "out_invoice",
            amounts=[100],
            company=self.company,
            partner=italian_partner,
            taxes=self.default_tax,
        )
        invoice.write(
            {
                "partner_shipping_id": self.italian_shipping_partner_a.id,
                "delivery_carrier_id": self.italian_delivery_carrier.id,
                "delivery_packages": 1,
                "delivery_gross_weight": 10.0,
                "delivery_net_weight": 9.5,
                "delivery_transport_datetime": fields.Date.from_string("2025-11-06"),
                "invoice_incoterm_id": self.env.ref("account.incoterm_CPT").id,
            }
        )
        invoice.action_post()
        self._assert_export_invoice(invoice, "delivery_data.xml")
