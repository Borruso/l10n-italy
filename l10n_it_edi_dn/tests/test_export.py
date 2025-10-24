# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import datetime, timedelta

from odoo import Command, fields

from .common import Common


class TestExportDeliveryNote(Common):
    def test_export_dn(self):
        vals = {
            "partner_id": self.italian_partner_a.id,
            "company_id": self.company.id,
            "invoice_date": fields.Date.from_string("2025-10-24"),
            "order_line": [
                Command.create(
                    {
                        "product_id": self.env.ref("product.product_product_3").id,
                        "product_uom_qty": 1,
                        "price_unit": 100,
                        "tax_id": [Command.set(self.default_tax.ids)],
                    }
                ),
                Command.create(
                    {
                        "product_id": self.env.ref("product.product_product_5").id,
                        "product_uom_qty": 2,
                        "price_unit": 50,
                        "tax_id": [Command.set(self.default_tax.ids)],
                    }
                ),
                Command.create(
                    {
                        "product_id": self.env.ref("product.product_product_6").id,
                        "product_uom_qty": 11,
                        "price_unit": 75,
                        "tax_id": [Command.set(self.default_tax.ids)],
                    }
                ),
                Command.create(
                    {
                        "product_id": self.env.ref("product.product_product_8").id,
                        "product_uom_qty": 1,
                        "price_unit": 125,
                        "tax_id": [Command.set(self.default_tax.ids)],
                    }
                ),
            ],
        }
        sales_order = self.env["sale.order"].with_company(self.company).create(vals)

        sales_order.action_confirm()
        picking = sales_order.picking_ids
        self.assertEqual(len(picking), 1)
        self.assertEqual(len(picking.move_ids), 4)

        picking.move_ids.quantity = False
        picking.move_ids[0].quantity = 1
        picking.move_ids[1].quantity = 2
        picking.move_ids[2].quantity = 11
        picking.move_ids[3].quantity = 1

        result = picking.button_validate()
        self.assertTrue(result)

        vals = {
            "partner_sender_id": self.company.partner_id.id,
            "partner_id": self.italian_partner_a.id,
            "partner_shipping_id": self.italian_partner_a.id,
            "company_id": self.company.id,
            "date": fields.Date.from_string("2025-10-24"),
        }
        delivery_note = (
            self.env["stock.delivery.note"].with_company(self.company).create(vals)
        )
        delivery_note.transport_datetime = datetime.now() + timedelta(days=1, hours=3)
        delivery_note.picking_ids = picking
        delivery_note.action_confirm()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, "confirm")
        self.assertEqual(delivery_note.invoice_status, "to invoice")

        delivery_note.action_invoice()
        self.assertEqual(len(delivery_note.line_ids), 4)
        self.assertEqual(delivery_note.state, "invoiced")
        self.assertEqual(delivery_note.invoice_status, "invoiced")
        self.assertEqual(sales_order.invoice_status, "invoiced")

        invoices = sales_order.invoice_ids
        self.assertEqual(len(invoices), 1)

        dn_invoice = invoices[0]
        self.assertEqual(delivery_note.invoice_ids, dn_invoice)
        dn_invoice.action_post()
        self._assert_export_invoice(dn_invoice, "export_dn.xml")
