# -*- coding: utf-8 -*-
# ####################################################################
# specker - a simple spec file tool
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

from SpecManipulator import SpecManipulator
from Statement import *

class SpecChanger(SpecManipulator):
	def __init__(self, statements = None):
		if statements is not None:
			self.setStatements(statements)

	def setStatements(self, statements):
		self.statements = statements
		self.sections = [x for x in statements if x.parent is None and type(x) is not StIf]

	def getStatements(self):
		return self.statements

	def changelog_list(self, f):
		# TODO: do pretty print
		for s in self.sections:
			if type(s) is StChangelog:
				s.print_file(f)
				break

	def changelog_add(self, items):
		pass

	def changelog_remove(self, what):
		pass

