# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Italy - E-invoicing - DDT",
    "version": "18.0.1.0.0",
    "category": "Accounting/Localizations/EDI",
    "summary": "DDT in fatture elettroniche",
    "author": "Giuseppe Borruso, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/l10n-italy",
    "license": "AGPL-3",
    "depends": [
        "l10n_it_delivery_note",
        "l10n_it_edi",
    ],
    "data": [
        "data/invoice_it_template.xml",
    ],
    "auto_install": True,
    "installable": True,
}
