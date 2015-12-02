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

import logging
import sys
from specError import SpecNotImplemented

class SpecDebug(object):
	'''
	Library debug control
	@cvar logger: library logger
	'''
	logger = logging.getLogger('specker-lib')
	logger.addHandler(logging.StreamHandler(sys.stderr))

	def __init__(self):
		raise SpecNotImplemented("Cannot instantiate SpecDebug")

	@classmethod
	def start_debug(cls):
		'''
		Start debugging
		@return: None
		@rtype: None
		'''
		cls.logger.setLevel(logging.DEBUG)
		cls.debug("Logging started")

	@classmethod
	def stop_debug(cls):
		'''
		Stop debugging
		@return: None
		@rtype: None
		'''
		cls.debug("Logging stopped")
		cls.logger.setLevel(logging.ERROR)

	@classmethod
	def set_handler(cls, handler):
		'''
		Set output handler, default sys.stderr
		@param handler: handler to be used
		@type handler: file
		@return: None
		@rtype: None
		'''
		cls.logger.addHandler(handler)

	@classmethod
	def debug(cls, msg):
		'''
		Print debug message
		@param msg: message to be printed
		@type msg: string
		@return: None
		@rtype: None
		'''
		cls.logger.debug("[DEBUG] " + msg)

	@classmethod
	def log(cls, msg):
		'''
		Print log message
		@param msg: message to be printed
		@type msg: string
		@return: None
		@rtype: None
		'''
		cls.logger.log("[LOG] " + msg)

	@classmethod
	def error(cls, msg):
		'''
		Print error message
		@param msg: message to be printed
		@type msg: string
		@return: None
		@rtype: None
		'''
		cls.logger.error('Error: ' + msg)

