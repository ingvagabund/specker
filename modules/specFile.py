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
A spec FILE abstraction
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import sys
from specError import SpecBadIndex

class SpecFile:
	'''
	A file abstraction with relative and absolute access using a pointer into
	a buffer.
	'''
	def __init__(self, spec):
		'''
		Initialize C{SpecFile}
		@param spec: file or string to be read
		@type spec: file or string
		@return: None
		@rtype: None
		'''
		if type(spec) is file:
			self.content = spec.read()
		else: # string
			self.content = spec
		self.pointer = 0
		self.length = len(self.content)

	def in_file(self, position = None):
		'''
		Check if (current/absolute) position is in file
		@param position: Position within a file (number of bytes offset)
		@type position: number or number
		@return: True if current position is still in file boundaries
		@rtype: Boolean
		'''
		if position == None:
			position = self.pointer
		return position >= 0 and self.pointer < self.length

	def seek(self, offset):
		'''
		Set pointer relatively to the current position according to offset
		@param offset: relative positive/negative offset
		@type offset: number
		@return: None
		@rtype: None
		'''
		tmp = offset + self.pointer

		if not self.in_file(tmp):
			raise SpecBadIndex('Bad seek')

		self.pointer = tmp

	def read_line(self):
		'''
		Read rest of the line
		@return: line read
		@rtype: string
		'''
		if not self.in_file():
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
		'''
		Get one char from the buffer and advance the buffer pointer
		@return: character read from the buffer or -1 if end of buffer reached
		@rtype: char
		'''
		if self.pointer == self.length:
			return -1

		c = self.content[self.pointer]
		self.pointer += 1
		return c

	def touch(self):
		'''
		Get one char from the buffer and B{DO NOT} advance the buffer pointer
		@return: character read from the buffer or -1 if end of buffer reached
		@rtype: char
		'''
		if self.pointer == self.length:
			return -1
		else:
			return self.content[self.pointer]

	def ungetc(self):
		'''
		Move the buffer pointer one step back
		@return: None
		@rtype: None
		@raise SpecBadIndex: if called when pointing at the beginning of the buffer
		'''
		if self.pointer == 0:
			raise SpecBadIndex('Cannot do ungetc at the beginning')

		if self.pointer != self.length:
			self.pointer -= 1

	def reset(self):
		'''
		Reset buffer pointer to point at the beginning of the buffer
		@return: None
		@rtype: None
		'''
		self.pointer = 0

