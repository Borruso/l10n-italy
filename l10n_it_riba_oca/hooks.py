# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openupgradelib import openupgrade

OLD_MODULE_NAME = "l10n_it_riba"
NEW_MODULE_NAME = "l10n_it_riba_oca"
RENAMED_MODELS = [
    (
        "report.l10n_it_riba.slip_qweb",
        "report.l10n_it_riba_oca.slip_qweb",
    ),
]
RENAMED_XMLIDS = [
    ("seq_riba_slip", "seq_riba_slip"),
    ("print_slip_qweb", "print_slip_qweb"),
    ("access_riba_slip_uinvoice", "access_riba_slip_uinvoice"),
    ("access_riba_slip_group_invoice", "access_riba_slip_group_invoice"),
    ("access_riba_slip_user", "access_riba_slip_user"),
    ("access_riba_slip_accountant", "access_riba_slip_accountant"),
    ("access_riba_slip_line_uinvoice", "access_riba_slip_line_uinvoice"),
    ("access_riba_slip_line_group_invoice", "access_riba_slip_line_group_invoice"),
    ("access_riba_slip_line_user", "access_riba_slip_line_user"),
    ("access_riba_slip_line_accountant", "access_riba_slip_line_accountant"),
    ("access_riba_slip_move_line_uinvoice", "access_riba_slip_move_line_uinvoice"),
    (
        "access_riba_slip_move_line_group_invoice",
        "access_riba_slip_move_line_group_invoice",
    ),
    ("access_riba_slip_move_line_user", "access_riba_slip_move_line_user"),
    (
        "access_riba_slip_move_line_accountant",
        "access_riba_slip_move_line_accountant",
    ),
    ("access_riba_past_due", "access_riba_past_due"),
    ("access_riba_credit", "access_riba_credit"),
    ("riba_slip_company_rule", "riba_slip_company_rule"),
    ("riba_slip_line_company_rule", "riba_slip_line_company_rule"),
    ("view_riba_to_issue_tree", "view_riba_to_issue_tree"),
    ("action_riba_to_issue", "action_riba_to_issue"),
    ("menu_riba_to_issue", "menu_riba_to_issue"),
    ("view_slip_riba_filter", "view_slip_riba_filter"),
    ("view_slip_riba_tree", "view_slip_riba_tree"),
    ("view_riba_slip_line_form", "view_riba_slip_line_form"),
    ("slip_riba_action", "slip_riba_action"),
    ("slip_layout", "slip_layout"),
    ("slip_qweb", "slip_qweb"),
    ("riba_credit", "riba_credit"),
    ("riba_credit_action", "riba_credit_action"),
    ("riba_past_due", "riba_past_due"),
    ("riba_past_due_action", "riba_past_due_action"),
]


def migrate_old_module(cr):
    openupgrade.rename_models(
        cr,
        RENAMED_MODELS,
    )
    full_renamed_xmlids = [
        (
            ".".join((OLD_MODULE_NAME, old_xmlid)),
            ".".join((NEW_MODULE_NAME, new_xmlid)),
        )
        for old_xmlid, new_xmlid in RENAMED_XMLIDS
    ]
    openupgrade.rename_xmlids(
        cr,
        full_renamed_xmlids,
    )


def pre_absorb_old_module(cr):
    cr.execute(
        """
            SELECT
                id
            FROM
                ir_module_module
            WHERE
                name = 'l10n_it_riba_oca'
                AND state IN ('installed', 'to upgrade')
                AND author like '%OCA%'
        """,
    )
    result = cr.fetchone()
    if bool(result):
        openupgrade.update_module_names(
            cr,
            [
                (OLD_MODULE_NAME, NEW_MODULE_NAME),
            ],
            merge_modules=True,
        )
        migrate_old_module(cr)
