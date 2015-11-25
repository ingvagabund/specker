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
A spec main manipulator
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specSection import *

class SpecManipulator(object):
	'''
	A generic class for classes which tend to manipulate with spec model
	'''
	def __init__(self, model = None):
		self.model = model

	def setModel(self, model):
		'''
		Set model to manipulate with
		@param model: a spec model
		@type model: L{SpecModel}
		@return: None
		@rtype: None
		'''
		self.model = model

	def getModel(self):
		'''
		Get used spec model
		@return: spec model
		@rtype: L{SpecModel}
		'''
		return self.model

	def find_definitions_all(self, statements):
		'''
		Find all definitions within spec model
		@param statements: statements to be looked for in
		@type statements: list of L{SpecSection}
		@return: list of definitions
		@rtype: list of L{SpecStDefinition}
		@raise SpecNotFound:
		@todo: move to the model itself?
		'''
		ret = []

		for s in statements:
			if issubclass(s.__class__, SpecStIf):
				b = self.find_definitions_all(s.getTrueBranch())
				if b:
					ret += b
				b = self.find_definitions_all(s.getFalseBranch())
				if b:
					ret += b
			elif issubclass(s.__class__, SpecStDefinition):
				ret.append(s)
			elif issubclass(s.__class__, SpecStPackage):
				b = self.find_definitions_all(s.getDefs())
				if b:
					ret += b

		return ret

