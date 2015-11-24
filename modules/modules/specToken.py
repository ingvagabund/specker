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
specker-lib - a spec file token abstraction and token list representation
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specFile import SpecFile
from specError import SpecBadIndex

class SpecToken:
	'''
	TODO
	'''
	def __init__(self, specFile = None):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
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
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if self.token == None:
			return "<EOF>"
		else:
			return self.token

	def __len__(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return len(self.token)

	def write(self, f, raw = False):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not raw:
			f.write(self.prepend)

		if self.token is not None:
			f.write(self.token)

		if not raw:
			f.write(self.append)

	def string(self, raw = False):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = ""
		if not raw:
			ret += self.prepend
		if self.token is not None:
			ret += self.token
		if not raw:
			ret +=  self.append
		return ret

	def sameLine(self, token2):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.line == token2.line

	@staticmethod
	def create(token, prepend = '', append = ' '):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		# note that line is not set
		ret = SpecToken()
		ret.prepend = prepend
		ret.token = token
		ret.append = append
		return ret

	def isEOF(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.token == None

	def getLine(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.line

	def setAppend(self, append):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.append = append

	def setPrepend(self, prepend):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.prepend = prepend

	def setToken(self, token):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.token = token

class SpecTokenList:
	'''
	TODO
	'''
	def __init__(self, spec = None):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
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
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.pointer == len(self.token_list)

	def next(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if self.current == len(self.token_list):
			raise StopIteration
		else:
			self.current += 1
			return self.token_list[self.current - 1]

	def get(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof
		self.pointer += 1
		return self.token_list[self.pointer - 1]

	def touch(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof

		return self.token_list[self.pointer]

	def getLine(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
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
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
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
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if self.pointer == 0:
			raise SpecBadIndex('Cannot unget')
		self.pointer -= 1

	def getPointer(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.pointer

	def setPointer(self, val):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if val < 0 or val > len(self.token_list):
			raise SpecBadIndex('TokenList pointer out of bound')
		self.pointer = val

	def __len__(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return len(self.token_list)

	def __iter__(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.current = 0
		return self

	def __next__(self): # Python 3
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.next()

	def write(self, f, raw = False):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for token in self.token_list:
			token.write(f, raw)

	def tokenListAppend(self, item):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.token_list.append(item)

	def __getitem__(self, i):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.token_list[i]

	def __eq__(self, str_compare):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		str_created = ""
		for token in self.token_list:
			str_created += token.string(raw = True)
		return str_created == str_compare

