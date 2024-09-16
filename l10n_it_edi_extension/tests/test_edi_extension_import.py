#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged
from odoo.addons.l10n_it_edi_extension.tests.common import TestItEDIExtension


@tagged("post_install", "-at_install")
class TestItEDIExtensionImport(TestItEDIExtension):

    def test_create_partner(self):
        """If partner does not exist, it is created during import."""
        partner_name = "SOCIETA' ALPHA SRL"
        # pre-condition
        partner = self.env["res.partner"].search([
            ("name", "=", partner_name),
        ], limit=1)
        self.assertFalse(partner)

        # Act
        invoice = self._assert_import_invoice("IT01234567890_FPR03.xml", [{}])

        # Assert
        partner = invoice.partner_id
        self.assertEqual(partner.name, partner_name)
