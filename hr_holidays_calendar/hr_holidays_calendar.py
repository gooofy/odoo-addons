# -*- coding: utf-8 -*-
##############################################################################
#
#    This file is part of hr_holidays_calendar, 
#
#    based on code from:
#      OpenERP, Open Source Management Solution
#      Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    based on ideas from:
#      https://www.odoo.com/de_DE/forum/hilfe-1/question/place-two-models-on-one-view-12350
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta, date
import openerp
from openerp import api, tools, models, fields, SUPERUSER_ID, netsvc
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp.osv import osv
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta
import openerp.addons.decimal_precision as dp
import traceback
import logging

_logger = logging.getLogger(__name__)

class hr_holidays_summary(models.Model):

    _name = "hr.holidays.summary"
    _auto = False

    name             = openerp.fields.Char(string="Description", readonly=True)
    date_from        = openerp.fields.Datetime(string="Start Date", readonly=True)
    date_to          = openerp.fields.Datetime(string="End Date", readonly=True)
    employee_id      = openerp.fields.Many2one(comodel_name='hr.employee', string='Employee', readonly=True)

    _order = "date_from ASC"

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'hr_holidays_summary')
        cr.execute("""
                    CREATE view hr_holidays_summary as (
                    SELECT l.id || 'l' as id,
                              e.name_related as name,
                              l.employee_id as employee_id,
                              l.date_from as date_from,
                              l.date_to as date_to
                              FROM hr_holidays l, hr_employee e
                              WHERE l.employee_id = e.id
                              GROUP BY l.id, l.date_from, l.date_to, e.name_related
                    )

                    UNION (

                    SELECT p.id || 'p' as id,
                              p.name as name,
                              -1 as employee_id,       
                              p.date as date_from,
                              p.date as date_to
                              FROM hr_holidays_public_line p
                              GROUP BY p.id, p.date

                    )
        """)

hr_holidays_summary()

# class gls_partner_label_wizard(models.TransientModel):
# 
#     _name = "gls_shipping_label.gls_partner_label_wizard"
#     _description = "GLS Partner Label Wizard"
# 
#     number_of_packages        = openerp.fields.Integer(string="Number of Packages", default=1, required=True)
#     manual_weight             = openerp.fields.Float(string="Manual Weight", required=True)
#     weight_uom_id             = openerp.fields.Many2one(comodel_name='product.uom', string='Unit of Measure', required=True, readonly="1")
#     partner_id                = openerp.fields.Many2one(comodel_name='res.partner', string='Partner', required=True, readonly="1")
# 
#     @api.model
#     def default_get(self, fields):
# 
#         _logger.debug ('gls_partner_label_wizard: default_get')
# 
#         if self.env.context is None:
#             context = {}
#         else:
#             context = self.env.context
# 
#         res = super(gls_partner_label_wizard, self).default_get(fields)
# 
#         _logger.debug ('gls_partner_label_wizard: default_get, context=%s, fields=%s' % (repr(context), repr(fields)))
# 
#         if 'weight_uom_id' in fields:
# 
#             uom_categ_id = self.env['ir.model.data'].xmlid_to_res_id('product.product_uom_categ_kgm')
#             weight_uom   = self.env['product.uom'].search([('category_id', '=', uom_categ_id), ('factor', '=', 1)], limit=1)
# 
#             res.update({'weight_uom_id': weight_uom.id})
# 
#         return res
# 
#     @api.multi
#     def print_gls_label(self):
# 
#         for wiz in self:
#             if wiz.manual_weight == 0:
#                 raise osv.except_osv(_('Error!'),_('Manual weight is zero!'))
#             if wiz.number_of_packages == 0:
#                 raise osv.except_osv(_('Error!'),_('Number of packages is zero!'))
# 
#         return self.env['report'].get_action(self, 'gls_shipping_label.gls_shipping_label_partner')
# 
# gls_partner_label_wizard()
# 
# 
# class res_partner(osv.Model):
#     _inherit = 'res.partner'
# 
#     @api.multi
#     def print_gls_label(self):
# 
#         for partner in self:
# 
#             gls_wizard = self.env['gls_shipping_label.gls_partner_label_wizard'].create({'partner_id': partner.id, 'manual_weight': 0.0})
# 
#             return {
#                 'name'           : 'GLS Partner Label Wizard',
#                 'views'          : [[False, 'form']],
#                 'res_model'      : 'gls_shipping_label.gls_partner_label_wizard',
#                 'type'           : 'ir.actions.act_window',
#                 'target'         : 'new',
#                 'res_id'         : gls_wizard.id,
#                 'context'        : self.env.context,
#             }
# 
#         return True
# 
# res_partner()
# 
