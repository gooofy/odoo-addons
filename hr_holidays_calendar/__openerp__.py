# -*- coding: utf-8 -*-
##############################################################################
#    
#    Copyright (C) 2017 Heiko Schaefer, Guenter Bartsch
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
{
    'name': "Holiday Summary Calendar",
    'version': '0.1',
    'category': 'Human Resources',
    'summary': "Holiday Summary Calendar",
    'description': """
""",
    'author': 'Heiko Schaefer, Guenter Bartsch',
    'website': 'https://github.com/gooofy/odoo-addons',
    'license': 'AGPL-3',
    'depends': ['hr_public_holidays', 'hr_holidays'],
    'data' : [
        'hr_holidays_calendar.xml',
        ],
    'css': [],
    'demo' : [],
    'active': False,
    'installable': True
}

