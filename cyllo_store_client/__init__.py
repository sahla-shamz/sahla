# -*- coding: utf-8 -*-
from . import models


def post_load():
    """Re-register the folders apps are installed into at server start, so
    apps activated from the store keep loading after a restart."""
    import os
    from odoo import addons
    from odoo.modules.module import get_module_path
    from odoo.tools import config
    parent = os.path.dirname(get_module_path('cyllo_store_client'))
    for path in (os.path.join(os.path.dirname(parent), 'marketplace'),
                 os.path.join(config['data_dir'], 'marketplace_addons')):
        if os.path.isdir(path) and path not in addons.__path__:
            addons.__path__.append(path)
