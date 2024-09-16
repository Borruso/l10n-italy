# Copyright 2024 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.l10n_it_edi.models.account_move import get_text
from odoo.tools import html2plaintext


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    l10n_it_edi_attachment_preview_link = fields.Char(
        string="Preview link",
        compute="_compute_l10n_it_edi_attachment_preview_link",
    )

    # -------------------------------------------------------------------------
    # Computes
    # -------------------------------------------------------------------------

    @api.depends("l10n_it_edi_attachment_id")
    def _compute_l10n_it_edi_attachment_preview_link(self):
        for move in self:
            if move.l10n_it_edi_attachment_id:
                move.l10n_it_edi_attachment_preview_link = (
                    move.get_base_url()
                    + f"/fatturapa/preview/{move.l10n_it_edi_attachment_id.id}"
                )
            else:
                move.l10n_it_edi_attachment_preview_link = ""

    # -------------------------------------------------------------------------
    # Business actions
    # -------------------------------------------------------------------------

    def action_l10n_it_edi_attachment_preview(self):
        self.ensure_one()

        return {
            "type": "ir.actions.act_url",
            "name": "Show preview",
            "url": self.l10n_it_edi_attachment_preview_link,
            "target": "new",
        }

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _l10n_it_edi_get_values(self, pdf_values=None):
        res = super()._l10n_it_edi_get_values(pdf_values)

        causale_list = []
        if self.narration:

            try:
                narration_text = html2plaintext(self.narration)
            except Exception:
                narration_text = ""

            # max length of Causale is 200
            for causale in narration_text.split("\n"):
                if not causale:
                    continue
                causale_list_200 = [
                    causale[i : i + 200] for i in range(0, len(causale), 200)
                ]
                for causale200 in causale_list_200:
                    causale_list.append(causale200)

        res["causale"] = causale_list

        return res

    @api.model
    def _l10n_it_buyer_seller_info(self):
        buyer_seller_info = super()._l10n_it_buyer_seller_info()
        partners_info = {
            "buyer": buyer_seller_info["buyer"],
            "seller": buyer_seller_info["seller"],
        }

        for partner_role, partner_info in partners_info.items():
            if partner_role == "buyer":
                partner_info_xpath = "//CessionarioCommittente//DatiAnagrafici"
            elif partner_role == "seller":
                partner_info_xpath = "//CedentePrestatore//DatiAnagrafici"
            else:
                continue
            partner_info["name_xpath"] = f"{partner_info_xpath}//Anagrafica//Denominazione"
            partner_info["first_name_xpath"] = f"{partner_info_xpath}//Anagrafica//Nome"
            partner_info["last_name_xpath"] = f"{partner_info_xpath}//Anagrafica//Cognome"
            partner_info["eori_code_xpath"] = f"{partner_info_xpath}//Anagrafica//CodEORI"
            partner_info["country_code_xpath"] = f"{partner_info_xpath}//IdFiscaleIVA//IdPaese"
        return buyer_seller_info

    def _l10n_it_edi_extension_prepare_partner_values(self, invoice_data):
        buyer_seller_info = self._l10n_it_buyer_seller_info()
        is_incoming = self.is_purchase_document(include_receipts=True)
        partner_role = 'seller' if is_incoming else 'buyer'
        partner_info = buyer_seller_info[partner_role]

        tree = invoice_data["xml_tree"]
        name = get_text(tree, partner_info['name_xpath'])
        country_code = get_text(tree, partner_info['country_code_xpath'])
        country = self.env["res.country"].search([("code", "=", country_code)], limit=1)
        vals = {
            "vat": get_text(tree, partner_info['vat_xpath']),
            "l10n_it_codice_fiscale": get_text(tree, partner_info['codice_fiscale_xpath']),
            "is_company": bool(len(name)),
            "l10n_it_extension_eori_code": get_text(tree, partner_info['eori_code_xpath']),
            "country_id": country.id,
        }

        if name:
            vals["name"] = name

        # Remove fields check when module partner_firstname
        # is migrated and added as a dependency
        partner_fields = self.env["res.partner"]._fields.keys()
        if first_name := get_text(tree, partner_info['first_name_xpath']) and "firstname" in partner_fields:
            vals["firstname"] = first_name
        if last_name := get_text(tree, partner_info['last_name_xpath']) and "lastname" in partner_fields:
            vals["lastname"] = last_name
        return vals

    def _l10n_it_edi_extension_create_partner(self, invoice_data):
        partner_values = self._l10n_it_edi_extension_prepare_partner_values(invoice_data)
        return self.env["res.partner"].create(partner_values)

    def _l10n_it_edi_import_invoice(self, invoice, data, is_new):
        invoice = super()._l10n_it_edi_import_invoice(invoice, data, is_new)
        if invoice and not invoice.partner_id:
            partner = self._l10n_it_edi_extension_create_partner(data)
            invoice.partner_id = partner
        return invoice
