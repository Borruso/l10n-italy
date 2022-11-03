# Copyright 2022 Giuseppe Borruso <https://github.com/Borruso>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(
        env.cr,
        [
            (
                "l10n_it_appointment_code.view_appointment_code_tree",
                "l10n_it_appointment_code.view_l10n_it_appointment_code_tree",
            ),
            (
                "l10n_it_appointment_code.view_appointment_code_form",
                "l10n_it_appointment_code.view_l10n_it_appointment_code_form",
            ),
            (
                "l10n_it_appointment_code.action_appointment_code",
                "l10n_it_appointment_code.action_l10n_it_appointment_code",
            ),
            (
                "l10n_it_appointment_code.menu_appointment_code",
                "l10n_it_appointment_code.menu_l10n_it_appointment_code",
            ),
            (
                "l10n_it_appointment_code.access_appointment_code_user",
                "l10n_it_appointment_code.access_l10n_it_appointment_code_user",
            ),
            (
                "l10n_it_appointment_code.access_appointment_code_manager",
                "l10n_it_appointment_code.access_l10n_it_appointment_code_manager",
            ),
        ],
    )
    openupgrade.rename_models(
        env.cr,
        [
            ("appointment.code", "l10n_it_appointment.code"),
        ],
    )
    openupgrade.rename_tables(
        env.cr,
        [
            ("appointment_code", "l10n_it_appointment_code"),
        ],
    )
    openupgrade.rename_fields(
        env,
        [
            (
                "l10n_it_appointment.code",
                "l10n_it_appointment_code",
                "code",
                "l10n_it_code",
            ),
            (
                "l10n_it_appointment.code",
                "l10n_it_appointment_code",
                "name",
                "l10n_it_name",
            ),
        ],
    )
