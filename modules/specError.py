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
Exceptions used within library
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

class SpecNotImplemented(NotImplementedError):
	'''
	Exception used for not implemented actions
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadToken(ValueError):
	'''
	Exception used when an unexpected token is reached
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecNotFound(ValueError):
	'''
	Exception used when desired object is not found (e.g. editing not-existing
	section in a spec file)
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadIf(ValueError):
	'''
	Exception used when an unterminated or malformed if is found
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadIndex(IndexError):
	'''
	Exception used when indexing outside boundaries
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadParam(ValueError):
	'''
	Exception used when an unknown parameter is passed
	'''
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

