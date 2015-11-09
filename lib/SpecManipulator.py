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

class SpecManipulator:
	logger = None
	def __init__(self):
		pass

	def setLoggingLevel(self, level):
		SpecManipulator.logger.setLevel(level)

	def print_str(self):
		ret = ""
		for s in self.statements:
			ret += s.print_str()
		return ret

	def print_file(self, f):
		for s in self.statements:
			s.print_file(f)

