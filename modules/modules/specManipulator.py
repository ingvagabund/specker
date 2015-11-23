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

from specSection import *

class SpecManipulator(object):
	def find_definitions_all(self, statements):
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
