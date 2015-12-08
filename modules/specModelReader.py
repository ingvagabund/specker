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
An adapter used to communicate with model, read methods
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specModelTransformator import SpecModelTransformator

class SpecModelReader(SpecModelTransformator):
	'''
	An adapter used to communicate with model - non-modifying methods
	'''
	def find_section(self, section_type):
		'''
		Find a section of a specific type type
		@param section_type: section type to look for
		@type section_type: __class__
		@return: list of sections of the provided type or None
		@rtype: list of L{SpecSection}
		'''
		return self.model.find_section(section_type)

	def find_definitions_all(self):
		'''
		Find all definitions within spec model
		@return: list of definitions
		@rtype: list of L{SpecStDefinition}
		@raise SpecNotFound:
		@todo: move to the model itself?
		'''
		return self.model.find_definitions_all()

