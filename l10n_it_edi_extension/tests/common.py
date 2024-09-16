#  Copyright 2024 Simone Rubino - Aion Tech
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.l10n_it_edi.tests.common import TestItEdi
from odoo import tests


@tests.tagged("post_install", "-at_install")
class TestItEDIExtension(TestItEdi):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.module = "l10n_it_edi_extension"
