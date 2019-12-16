from odoo import api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Loaded after installing the module."""
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        module = env['ir.module.module'].search([
            ('name', '=', 'hr_associate')])
        _logger.info('Overwriting translation terms')
        module.with_context(overwrite=True)._update_translations()
