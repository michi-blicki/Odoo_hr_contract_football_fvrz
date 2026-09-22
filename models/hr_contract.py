# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    _FVRZ_LEVEL_AMOUNTS = {
        '1': 6000,
        '2': 4000,
        '3': 2900,
    }

    _FVRZ_TRAVEL_AMOUNTS = {
        '1': {
            '1': 1800,
            '2': 2900,
            '3': 4100,
            '4': 6800,
        },
        '2': {
            '1': 1500,
            '2': 2300,
            '3': 3100,
            '4': 5100,
        },
        '3': {
            '1': 1300,
            '2': 1800,
            '3': 2400,
            '4': 3800,
        },
    }

    # FVRZ specific fields
    fvrz_trainer_level = fields.Selection(
        string='FVRZ Trainer Level',
        selection=[
            ('1', 'Trainer Level 1'),
            ('2', 'Trainer Level 2'),
            ('3', 'Trainer Level 3'),
        ],
        required=False,
        store=True,
    )
    fvrz_trainer_level_amount = fields.Monetary(
        string="FVRZ Trainer Level Amount",
        currency_field='currency_id',
        compute='_compute_fvrz_trainer_level_amount',
        readonly=True,
        store=True,
    )

    fvrz_trainer_travel_allowance = fields.Selection(
        string='FVRZ Trainer Flat-rate travel allowance',
        selection=[
            ('1', '01 - 05km between home and club sport facility'),
            ('2', '06 - 15km between home and club sport facility'),
            ('3', '16 - 25km between home and club sport facility'),
            ('4', '>26km between home and club sport facility'),
        ],
        required=False,
        store=True,
    )
    fvrz_trainer_travel_allowance_amount = fields.Monetary(
        string="FVRZ Trainer Flat-rate travel allowance Amount",
        currency_field='currency_id',
        compute='_compute_fvrz_trainer_travel_allowance_amount',
        readonly=True,
        store=True,
    )

    fvrz_total_allowance_amount = fields.Monetary(
        string="FVRZ Total Allowance Amount",
        currency_field='currency_id',
        compute='_compute_fvrz_total_allowance_amount',
        readonly=True,
        store=True,
    )

    @api.depends('fvrz_trainer_level')
    def _compute_fvrz_trainer_level_amount(self):
        for contract in self:
            contract.fvrz_trainer_level_amount = self._FVRZ_LEVEL_AMOUNTS.get(contract.fvrz_trainer_level, 0.0)

    @api.depends('fvrz_trainer_level', 'fvrz_trainer_travel_allowance')
    def _compute_fvrz_trainer_travel_allowance_amount(self):
        for contract in self:
            level_amounts = self._FVRZ_TRAVEL_AMOUNTS.get(contract.fvrz_trainer_level, {})
            contract.fvrz_trainer_travel_allowance_amount = level_amounts.get(contract.fvrz_trainer_travel_allowance, 0.0)

    @api.depends('fvrz_trainer_level_amount', 'fvrz_trainer_travel_allowance_amount')
    def _compute_fvrz_total_allowance_amount(self):
        for contract in self:
            contract.fvrz_total_allowance_amount = (
                (contract.fvrz_trainer_level_amount or 0.0)
                + (contract.fvrz_trainer_travel_allowance_amount or 0.0)
            )