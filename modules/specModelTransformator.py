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
An adapter used to communicate with model
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specModel import SpecModel

class SpecModelTransformator(object):
	'''
	An adapter used to communicate with model
	'''
	def __init__(self):
		self.model = SpecModel()

	def set_model(self, model):
		'''
		Set model to manipulate with
		@param model: a spec model
		@type model: L{SpecModel}
		@return: None
		@rtype: None
		'''
		self.model = model

	def get_model(self):
		'''
		Get used spec model
		@return: spec model
		@rtype: L{SpecModel}
		'''
		return self.model

	def append(self, section):
		'''
		Append a section
		@param section: a section to be appended
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.model.append(section)

	def remove(self, section):
		'''
		Remove a section
		@param section: a section to be removed
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.model.remove(section)

	def append_items(self, items):
		'''
		Append multiple sections
		@param items: sections to be added
		@type items: list of L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.model.append_items(items)

	def add(self, section):
		'''
		Add a section, try to guess the most suitable position for the section
		@param section: section to be added
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		return self.model.add(section)

	def get_sections(self):
		'''
		Get list of all sections
		@return: list of sections
		@rtype: list of L{SpecSection}
		'''
		return self.model.get_sections()

	def find_section(self, section_type):
		'''
		Find a section of a specific type type
		@param section_type: section type to look for
		@type section_type: __class__
		@return: list of sections of the provided type or None
		@rtype: list of L{SpecSection}
		'''
		return self.model.find_section()

	def find_definitions_all(self):
		'''
		Find all definitions within spec model
		@return: list of definitions
		@rtype: list of L{SpecStDefinition}
		@raise SpecNotFound:
		@todo: move to the model itself?
		'''
		return self.model.find_definitions_all()

class SpecModelWriter(SpecModelTransformator):
	'''
	An adapter used to communicate with model - modifying methods used by
	L{SpecModelEditor} and L{SpecModelParser}
	'''
	pass

class SpecModelReader(SpecModelTransformator):
	'''
	An adapter used to communicate with model - non-modifying methods
	'''
	pass

