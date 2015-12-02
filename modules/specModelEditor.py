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
A generic spec model editor class
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specModelManipulator import SpecModelManipulator

class SpecModelEditor(SpecModelManipulator):
	'''
	A generic spec model editor class
	'''
	def __init__(self, reader, writer):
		self.set_model_reader(reader)
		self.set_model_writer(writer)
		raise SpecNotImplemented("Editor not implemented")

	def set_model_reader(self, model_reader):
		'''
		Register a spec model reader
		@param model_reader: a spec model reader to be registered
		@type model_reader: L{SpecModelReader}
		@return: None
		@rtype: None
		'''
		self.model_reader = model_reader

	def set_model_writer(self, model_writer):
		'''
		Register a spec model writer
		@param model_writer: a spec model writer to be registered
		@type model_writer: L{SpecModelWriter}
		@return: None
		@rtype: None
		'''
		self.model_writer = model_writer

	def get_model_reader(self):
		'''
		Get registered spec model reader
		@return: a spec model reader
		@rtype: L{SpecModelReader}
		'''
		return self.model_reader

	def get_model_writer(self):
		'''
		Get registered spec model writer
		@return: a spec model writer
		@rtype: L{SpecModelWriter}
		'''
		return self.model_writer

