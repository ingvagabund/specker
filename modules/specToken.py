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
A spec token abstraction
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''
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

