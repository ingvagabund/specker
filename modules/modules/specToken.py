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

from specFile import SpecFile
from specError import SpecBadIndex

class SpecToken:
	def __init__(self, specFile = None):

		def readComment(specFile):
			ret = ""
			while True:
				c = specFile.touch()
				if c != '\n':
					ret += specFile.getc()
				else:
					break
			return ret

		self.prepend = "" # prepended whitespaces
		self.append = ""  # appended whitespaces
		self.token = ""
		self.line  = None
		self.eol_count = 0

		if specFile is None:
			return

		token_parsed = False

		while True:
			c = specFile.getc()

			if c == -1:
				if token_parsed:
					specFile.ungetc()
					break
				else:
					self.token = None
					break
			elif c == ' ' or c == '\t' or c == '\n':
				if token_parsed:
					self.append += c
				else:
					self.prepend += c

				if c == '\n':
					self.eol_count += 1
			elif c == '\\' and specFile.touch() == '\n':
				if token_parsed:
					self.append += c
					self.append += specFile.getc()
				else:
					self.prepend += c
					self.prepend += specFile.getc()

				self.eol_count += 1
			elif c == '#':
				if token_parsed:
					# TODO: make better decision, e.g. '^  #comment$'
					if len(self.append) > 0 and self.append[-1] == '\n':
						specFile.ungetc()
						break
					else:
						self.append += c
						self.append += readComment(specFile)
				else:
					self.prepend += c
					self.prepend += readComment(specFile)

			else:
				if len(self.append) == 0:
					self.token += c
					token_parsed = True
				else:
					specFile.ungetc()
					break

	def __str__(self):
		if self.token == None:
			return "<EOF>"
		else:
			return self.token

	def __len__(self):
		return len(self.token)

	def write(self, f, raw = False):
		if not raw:
			f.write(self.prepend)

		if self.token is not None:
			f.write(self.token)

		if not raw:
			f.write(self.append)

	def sameLine(self, token2):
		return self.line == token2.line

	@staticmethod
	def create(token, prepend = '', append = ' '):
		# note that line is not set
		ret = SpecToken()
		ret.prepend = prepend
		ret.token = token
		ret.append = append
		return ret

	def isEOF(self):
		return self.token == None

	def getLine(self):
		return self.line

class SpecTokenList:
	def __init__(self, spec = None):
		self.current = 0
		self.pointer = 0
		self.token_list = []

		# TODO: pass spec in another method
		if spec is None:
			return

		line = 1
		specFile = SpecFile(spec)
		while True:
			t = SpecToken(specFile)
			self.token_list.append(t)

			t.line = line
			line += t.eol_count

			if t.token == None:
				break

	def isEOF(self):
		return self.pointer == len(self.token_list)

	def next(self):
		if self.current == len(self.token_list):
			raise StopIteration
		else:
			self.current += 1
			return self.token_list[self.current - 1]

	def get(self):
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof
		self.pointer += 1
		return self.token_list[self.pointer - 1]

	def touch(self):
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof

		return self.token_list[self.pointer]

	def getLine(self):
		ret = []

		while not self.isEOF():
			token_next = self.touch()

			if len(ret) == 0:
				ret.append(self.get())
				continue

			token_prev = ret[-1]

			if token_next.line != token_prev.line:
				# check for escaped \n
				if token_prev.append[-2:] != "\\\n":
					break
			ret.append(self.get())

		# return TokenList
		l = SpecTokenList()
		l.token_list = ret
		return l

	def getWhileNot(self, callback):
		ret = []

		while not self.touch().isEOF():
			if callback(self):
				break
			ret.append(self.get())

		# return TokenList
		l = SpecTokenList()
		l.token_list = ret
		return l

	def unget(self):
		if self.pointer == 0:
			raise SpecBadIndex('Cannot unget')
		self.pointer -= 1

	def getPointer(self):
		return self.pointer

	def setPointer(self, val):
		if val < 0 or val > len(self.token_list):
			raise SpecBadIndex('TokenList pointer out of bound')
		self.pointer = val

	def __len__(self):
		return len(self.token_list)

	def __iter__(self):
		self.current = 0
		return self

	def __next__(self): # Python 3
		return self.next()

	def write(self, f):
		for token in self.token_list:
			token.write(f)

	def tokenListAppend(self, item):
		self.token_list.append(item)

	def __getitem__(self, i):
		return self.token_list[i]

