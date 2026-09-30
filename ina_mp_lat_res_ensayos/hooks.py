# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def post_init_hook(env):
    env.ref("base.group_user")._apply_group(env.ref("stock.group_production_lot"))
