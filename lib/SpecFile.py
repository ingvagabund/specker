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

import sys
from SpecError import SpecBadIndex

class SpecFile:
	def __init__(self, spec):
		self.content = spec.read()
		self.pointer = 0
		self.length = len(self.content)

	def inFile(self, position = None):
		if position == None:
			position = self.pointer
		return position >= 0 and self.pointer < self.length

	def seek(self, offset):
		tmp = offset + self.pointer

		if not self.inFile(tmp):
			raise SpecBadIndex('Bad seek')

		self.pointer = tmp

	def readLine(self):
		if not self.inFile('Not in File'):
			return -1

		res = ""
		while True:
			c = self.getc()

			if c == -1:
				break;

			res += c

			if c == '\n':
				break

		if len(res) == 0:
			return None
		else:
			return res

	def getc(self):
		if self.pointer == self.length:
			return -1

		c = self.content[self.pointer]
		self.pointer += 1
		return c

	def touch(self):
		return self.content[self.pointer]

	def ungetc(self):
		if self.pointer == 0:
			raise SpecBadIndex('Cannot do ungetc at the beginning')

		if self.pointer != self.length:
			self.pointer -= 1

	def reset(self):
		self.pointer = 0
