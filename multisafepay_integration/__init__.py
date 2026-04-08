# -*- coding: utf-8 -*-

from . import models
from . import controllers
from odoo.addons.payment import setup_provider, reset_payment_provider


def post_init_hook(env):
    """setup the provider in the account payment method"""
    setup_provider(env, 'multisafe')


def uninstall_hook(env):
    """uninstall the payment provider"""
    reset_payment_provider(env, 'multisafe')