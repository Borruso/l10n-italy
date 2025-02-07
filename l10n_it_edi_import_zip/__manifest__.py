# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl <gborruso@dinamicheaziendali.it>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Italy - E-invoicing - Import ZIP",
    "summary": "Permette di importare in uno ZIP diversi file XML di "
    "fatture elettroniche",
    "version": "18.0.1.0.0",
    "category": "Localization/Italy",
    "website": "https://github.com/OCA/l10n-italy",
    "author": "Giuseppe Borruso, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "account",
        "l10n_it_edi",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/wizard_import_fatturapa.xml",
    ],
    "application": False,
    "installable": True,
}
