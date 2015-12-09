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
A spec token list
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''
import cStringIO
from specError import SpecBadIndex
from specFile import SpecFile
from specToken import SpecToken

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

			line += t.eol_count_prepend
			t.line = line
			line += t.eol_count_append

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

	def get_raw(self):
		'''
		Get string representation of token list
		@return: string representation
		@rtype: string
		'''
		output = cStringIO.StringIO()
		self.write(output, True)
		ret = output.getvalue()
		output.close()
		return ret

	def token_list_append(self, item):
		'''
		Append item to the token list
		@param item: item to be added
		@type item: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.token_list.append(item)

	def token_list_append_items(self, items):
		'''
		Append multiple items to the token list
		@param items: items to be added
		@type items: L{SpecTokenList}
		@return: None
		@rtype: None
		'''
		for item in items:
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

	def __setitem__(self, i, item):
		'''
		Set item using direct access
		@param i: index to token list
		@type i: number
		@param item: item to be set
		@type item: L{SpecToken}
		@return: token on given position
		@rtype: L{SpecToken}
		'''
		self.token_list[i] = item

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

