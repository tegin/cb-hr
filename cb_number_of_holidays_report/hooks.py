# Copyright 2020 Creu Blanca
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    cr.execute(
        """
        ALTER TABLE hr_leave
        ADD COLUMN IF NOT EXISTS count_in_holidays_report BOOLEAN DEFAULT TRUE
    """
    )
