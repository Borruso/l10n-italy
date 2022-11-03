# Copyright 2017 Alessandro Camilli - Openforce
# Copyright 2019 Stefano Consolaro (Associazione PNLUG - Gruppo Odoo)
# Copyright 2021 Alex Comba - Agile Business Group
# Copyright 2022 Giuseppe Borruso - Dinamiche Aziendali

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AppointmentCode(models.Model):
    _name = "l10n_it_appointment.code"
    _description = "Appointment Code"

    @api.constrains("l10n_it_code")
    def _check_code(self):
        for appointment_code in self:
            domain = [("l10n_it_code", "=", appointment_code.l10n_it_code)]
            elements = self.search(domain)
            if len(elements) > 1:
                raise ValidationError(
                    _("The element with code %s already exists")
                    % appointment_code.l10n_it_code
                )

    l10n_it_code = fields.Char()
    l10n_it_name = fields.Char()
