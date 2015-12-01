# -*- coding: utf-8 -*-
# ####################################################################
# specker-lib - spec file manipulation library
# Copyright (C) 2015  Fridolin Pokorny, fpokorny@redhat.com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ####################################################################
'''
Library debug control
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import sys
import logging

class SpecDebug(object):
	'''
	Library debug control, use C{SpecDebug.logger.serLoggingLevel(level)} to
	initialize logger. Level could be one of the following (C{import logging}):
	  - logging.DEBUG
	  - logging.CRITICAL
	  - logging.ERROR
	  - logging.WARNING
	  - logging.INFO
	  - logging.DEBUG
	You can adjust handler when initializing, otherwise it defaults to
	C{sys.stderr}.
	@cvar logger: library logger
	'''
	logger = logging.getLogger('specker-lib')
	logger.addHandler(logging.StreamHandler(sys.stderr))

