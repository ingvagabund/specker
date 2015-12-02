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
A spec file token abstraction and token list representation
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specFile import SpecFile
from specError import SpecBadIndex

class SpecToken:
	'''
	Token abstraction
	'''
	def __init__(self, specFile = None):
		'''
		Init L{SpecToken}
		@param specFile: L{SpecFile} to parse
		@type specFile: L{SpecFile}
		@return: None
		@rtype: None
		'''
		def read_comment(specFile):
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
						self.append += read_comment(specFile)
				else:
					self.prepend += c
					self.prepend += read_comment(specFile)

			else:
				if len(self.append) == 0:
					self.token += c
					token_parsed = True
				else:
					specFile.ungetc()
					break

	def __str__(self):
		'''
		Get raw string representation
		@return: string representation of a token
		@rtype: string
		'''
		if self.token == None:
			return "<EOF>"
		else:
			return self.token

	def __len__(self):
		'''
		Length of the token itself
		@return: token length
		@rtype: number
		'''
		return len(self.token)

	def write(self, f, raw = False):
		'''
		Write token to a file
		@param f: file to write token to
		@type f: FILE
		@param raw: if True, token is written without append and prepend part
		@type raw: Boolean
		@return: None
		@rtype: None
		'''
		if not raw:
			f.write(self.prepend)

		if self.token is not None:
			f.write(self.token)

		if not raw:
			f.write(self.append)

	def string(self, raw = False):
		'''
		Get token string representation
		@param raw: if True, token is written without append and prepend part
		@type raw: True
		@return: string representation of a token
		@rtype: string
		'''
		ret = ""
		if not raw:
			ret += self.prepend
		if self.token is not None:
			ret += self.token
		if not raw:
			ret +=  self.append
		return ret

	def same_line(self, token):
		'''
		Check if (next) token is on the same line as myself
		@param token: token to be checked
		@type token: L{SpecToken}
		@return: True if token is on the same line
		@rtype: Boolean
		'''
		return (self.line + self.append.count('\\\n')) == token.line

	@staticmethod
	def create(token, prepend = '', append = ' '):
		'''
		Create a token
		@param token: string which represents token
		@type token: string
		@param prepend: string to be prepended before token
		@type prepend: string
		@param append: string to be appended after token
		@type append: string
		@return: newly instantiated token
		@rtype: L{SpecToken}
		'''
		# note that line is not set
		ret = SpecToken()
		ret.prepend = prepend
		ret.token = token
		ret.append = append
		return ret

	def is_eof(self):
		'''
		Check if token is EOF token
		@return: True if token is EOF token
		@rtype: Boolean
		'''
		return self.token == None

	def get_line(self):
		'''
		Get line number where token was presented
		@return: line number or None if no line info was provided
		@rtype: number
		'''
		return self.line

	def set_append(self, append):
		'''
		Set append part for the token
		@param append: a string to be appended
		@type append: string
		@return: None
		@rtype: None
		'''
		self.append = append

	def set_prepend(self, prepend):
		'''
		Set prepend part for the token
		@param prepend: a string to be prepended
		@type prepend: string
		@return: None
		@rtype: None
		'''
		self.prepend = prepend

	def set_token(self, token):
		'''
		Set token
		@param token: token which should be used for token instance
		@type token: string
		@return: None
		@rtype: None
		'''
		self.token = token

class SpecTokenList:
	'''
	List of token abstraction with a working pointer
	'''
	def __init__(self, spec = None):
		'''
		Init L{SpecTokenList}
		@param spec: file or string to be parsed
		@type spec: string/file
		@return: None
		@rtype: None
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

	def is_eof(self):
		'''
		Check if pointer points at the end of file
		@return: True if pointer points at the end of file
		@rtype: Boolean
		'''
		return self.pointer == len(self.token_list)

	def next(self):
		'''
		Get next token from list
		@return: next token
		@rtype: L{SpecToken}
		@raise StopIteration: when end of token list is reached
		'''
		if self.current == len(self.token_list):
			raise StopIteration
		else:
			self.current += 1
			return self.token_list[self.current - 1]

	def get(self):
		'''
		Get token from list and advance pointer
		@return: next token
		@rtype: L{SpecToken}
		'''
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof
		self.pointer += 1
		return self.token_list[self.pointer - 1]

	def touch(self):
		'''
		Get token from list and B{DO NOT} advance pointer
		@return: next token
		@rtype: L{SpecToken}
		@raise SpecNotFound:
		'''
		if self.pointer == len(self.token_list):
			return self.token_list[-1] # eof

		return self.token_list[self.pointer]

	def get_line(self):
		'''
		Get tokens on the current line
		@return: list of tokens on the same line
		@rtype: L{SpecTokenList}
		'''
		ret = []

		while not self.is_eof():
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

		l = SpecTokenList()
		l.token_list = ret
		return l

	def get_while_not(self, callback):
		'''
		Get list of token until predicate is False
		@param callback: callback to be called, predicate
		@type callback: func(L{SpecTokenList}) -> Boolean
		@return: list of tokens until predicate was not True
		@rtype: L{SpecTokenList}
		'''
		ret = []

		while not self.touch().is_eof():
			if callback(self):
				break
			ret.append(self.get())

		# return TokenList
		l = SpecTokenList()
		l.token_list = ret
		return l

	def unget(self):
		'''
		Move the buffer pointer one step back
		@return: None
		@rtype: None
		@raise SpecBadIndex: when called at the beginning
		'''
		if self.pointer == 0:
			raise SpecBadIndex('Cannot unget at the beginning')
		self.pointer -= 1

	def get_pointer(self):
		'''
		Get value of the current buffer pointer
		@return: buffer pointer
		@rtype: number
		'''
		return self.pointer

	def set_pointer(self, val):
		'''
		Set value of the current buffer pointer
		@param val: new buffer pointer
		@type val: number
		@raise SpecBadIndex: when a pointer reaches boundaries
		'''
		if val < 0 or val > len(self.token_list):
			raise SpecBadIndex('TokenList pointer out of bound')
		self.pointer = val

	def __len__(self):
		'''
		Return length of the list
		@return: length of the list
		@rtype: number
		'''
		return len(self.token_list)

	def __iter__(self):
		'''
		Get iterator
		@return: token list
		@rtype: L{SpecTokenList}
		'''
		self.current = 0
		return self

	def __next__(self): # Python 3
		'''
		Get next token when iterating
		@return: next token
		@rtype: L{SpecToken}
		'''
		return self.next()

	def write(self, f, raw = False):
		'''
		Write whole token to a file
		@param f: file to write to
		@type f: FILE
		@param raw: True if write without append and prepend token part
		@type raw: Boolean
		@return: None
		@rtype: None
		'''
		for token in self.token_list:
			token.write(f, raw)

	def token_list_append(self, item):
		'''
		Append item to the token list
		@param item: item to be added
		@type item: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.token_list.append(item)

	def __getitem__(self, i):
		'''
		Get item for direct access
		@param i: index to token list
		@type i: number
		@return: token on given position
		@rtype: L{SpecToken}
		'''
		return self.token_list[i]

	def __eq__(self, str_compare):
		'''
		Compare token list with a string
		@param str_compare: string to be compared with
		@type str_compare: string
		@return: True if string is same as value of tokens in token list
		@rtype: None
		'''
		str_created = ""
		for token in self.token_list:
			str_created += token.string(raw = True)
		return str_created == str_compare

