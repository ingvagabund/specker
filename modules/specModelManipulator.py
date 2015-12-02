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
A spec main model manipulator
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specDebug import SpecDebug
from specError import SpecNotFound, SpecNotImplemented

class SpecModelManipulator(object):
	'''
	A generic class for classes which tend to manipulate with spec model
	'''
	def __init__(self, model = None):
		self.MANIPULATORS = [ ]
		raise SpecNotImplemented("Manipulator not implemented")

	def register(self, manipulator):
		'''
		Register a spec model manipulator
		@param manipulator: an manipulator to be registered
		@type manipulator: L{SpecSectionEditor}/L{SpecSectionParser}/L{SpecSectionRenderer}
		@return: None
		@rtype: None
		@raise SpecNotFound: if provided manipulator cannot be registered e.g. invalid manipulator
		'''
		found = False
		for idx, item in enumerate(self.MANIPULATORS):
			if issubclass(manipulator, item):
				found = True
				SpecDebug.logger.debug("- registered new manipulator '%s'" % str(manipulator))
				self.MANIPULATORS[idx] = manipulator

		if not found:
			raise SpecNotFound("Invalid manipulator '%s' registration" % manipulator.__name__)

