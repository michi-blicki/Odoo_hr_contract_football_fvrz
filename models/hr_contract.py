# -*- coding: utf-8 -*-

from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = "hr.contract"

    _FVRZ_LEVEL_AMOUNTS = {
        'trainer_level_1': 6000,
        'trainer_level_2': 4000,
        'trainer_level_3': 2900,
    }

    _FVRZ_TRAVEL_AMOUNTS = {
        'trainer_level_1': {
            'xshort': 1800,
            'short': 2900,
            'medium': 4100,
            'long': 6800,
        },
        'trainer_level_2': {
            'xshort': 1500,
            'short': 2300,
            'medium': 3100,
            'long': 5100,
        },
        'trainer_level_3': {
            'xshort': 1300,
            'short': 1800,
            'medium': 2400,
            'long': 3800,
        },
    }

    # FVRZ specific fields
    fvrz_trainer_level = fields.Selection(
        string='FVRZ Trainer Level',
        selection=[
            ('trainer_level_1', 'Trainer Level 1'),
            ('trainer_level_2', 'Trainer Level 2'),
            ('trainer_level_3', 'Trainer Level 3'),
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
            ('xshort', '01 - 05km between home and club sport facility'),
            ('short', '06 - 15km between home and club sport facility'),
            ('medium', '16 - 25km between home and club sport facility'),
            ('long', '>26km between home and club sport facility'),
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