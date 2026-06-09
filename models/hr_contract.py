# -*- coding: utf-8 -*-

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrContract(models.Model):
    _inherit = "hr.contract"

    # FVRZ specific fields
    fvrz_trainer_level = fields.Selection(
        string='FVRZ Trainer Level',
        selection=[
            ('trainer_level_1', 'Trainer Level 1'),
            ('trainer_level_2', 'Trainer Level 2'),
            ('trainer_level_3', 'Trainer Level 3'),
        ],
        required=False,
    )
    fvrz_trainer_level_amount = fields.Monetary(
        string="FVRZ Trainer Level Amount",
        currency_field='currency_id',
        readonly=True,
    )

    fvrz_trainer_travel_allowance = fields.Selection(
        string='FVRZ Trainer Flat-rate travel allowance',
        selection=[
            ('xshort', '01 - 05km between home and club sport facility'),
            ('short', '06 - 15km between home and club sport facility'),
            ('medium', '16 - 25km between home and club sport facility'),
            ('long', '>26km between home and club sport facility'),
        ],
        required=False,
    )
    fvrz_trainer_travel_allowance_amount = fields.Monetary(
        string="FVRZ Trainer Flat-rate travel allowance Amount",
        currency_field='currency_id',
        readonly=True,
    )

    fvrz_total_allowance_amount = fields.Monetary(
        string="FVRZ Total Allowance Amount",
        currency_field='currency_id',
        compute='_compute_fvrz_total_allowance_amount',
        readonly=True,
    )

    @api.onchange('fvrz_trainer_level')
    def _onchange_fvrz_trainer_level(self):
        if self.fvrz_trainer_level == 'trainer_level_1':
            self.fvrz_trainer_level_amount = 6000
        elif self.fvrz_trainer_level == 'trainer_level_2':
            self.fvrz_trainer_level_amount = 4000
        elif self.fvrz_trainer_level == 'trainer_level_3':
            self.fvrz_trainer_level_amount = 2900
        else:
            self.fvrz_trainer_level_amount = False

    @api.onchange('fvrz_trainer_travel_allowance')
    def _onchange_fvrz_trainer_travel_allowance(self):
        if not self.fvrz_trainer_level:
            raise UserError(_("Please select the FVRZ Trainer Level before selecting the Flat-rate travel allowance."))
        
        if self.fvrz_trainer_level == 'trainer_level_1':
            if self.fvrz_trainer_travel_allowance == 'xshort':
                self.fvrz_trainer_travel_allowance_amount = 1800
            elif self.fvrz_trainer_travel_allowance == 'short':
                self.fvrz_trainer_travel_allowance_amount = 2900
            elif self.fvrz_trainer_travel_allowance == 'medium':
                self.fvrz_trainer_travel_allowance_amount = 4100
            elif self.fvrz_trainer_travel_allowance == 'long':
                self.fvrz_trainer_travel_allowance_amount = 6800
            else:
                self.fvrz_trainer_travel_allowance_amount = False
        elif self.fvrz_trainer_level == 'trainer_level_2':
            if self.fvrz_trainer_travel_allowance == 'xshort':
                self.fvrz_trainer_travel_allowance_amount = 1500
            elif self.fvrz_trainer_travel_allowance == 'short':
                self.fvrz_trainer_travel_allowance_amount = 2300
            elif self.fvrz_trainer_travel_allowance == 'medium':
                self.fvrz_trainer_travel_allowance_amount = 3100
            elif self.fvrz_trainer_travel_allowance == 'long':
                self.fvrz_trainer_travel_allowance_amount = 5100
            else:
                self.fvrz_trainer_travel_allowance_amount = False
        elif self.fvrz_trainer_level == 'trainer_level_3':
            if self.fvrz_trainer_travel_allowance == 'xshort':
                self.fvrz_trainer_travel_allowance_amount = 1300
            elif self.fvrz_trainer_travel_allowance == 'short':
                self.fvrz_trainer_travel_allowance_amount = 1800
            elif self.fvrz_trainer_travel_allowance == 'medium':
                self.fvrz_trainer_travel_allowance_amount = 2400
            elif self.fvrz_trainer_travel_allowance == 'long':
                self.fvrz_trainer_travel_allowance_amount = 3800
            else:
                self.fvrz_trainer_travel_allowance_amount = False
        else:
            self.fvrz_trainer_travel_allowance_amount = False

    @api.depends('fvrz_trainer_level_amount', 'fvrz_trainer_travel_allowance_amount')
    def _compute_fvrz_total_allowance_amount(self):
        for contract in self:
            total_amount = 0
            if contract.fvrz_trainer_level_amount:
                total_amount += contract.fvrz_trainer_level_amount
            if contract.fvrz_trainer_travel_allowance_amount:
                total_amount += contract.fvrz_trainer_travel_allowance_amount
            contract.fvrz_total_allowance_amount = total_amount