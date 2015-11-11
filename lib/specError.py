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

class SpecNotImplemented(NotImplementedError):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadToken(ValueError):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecNotFound(ValueError):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadIf(ValueError):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

class SpecBadIndex(IndexError):
	def __init__(self, message):
		self.message = message

	def __str__(self):
		return self.message

