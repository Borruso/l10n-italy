#  Copyright 2024 Giuseppe Borruso <gborruso@dinamicheaziendali.it>
#  License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    companies = env["res.company"].search([])
    for company in companies:
        dn_types = env["stock.delivery.note.type"].search(
            [("company_id", "=", company.id)]
        )
        dn_types._update_available_delivery_note_types()
