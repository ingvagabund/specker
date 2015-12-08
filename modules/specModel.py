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
Basic operations on spec sections and spec section encapsulation
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

from specDebug import SpecDebug
from specSection import *
from specError import SpecNotImplemented, SpecNotFound

class SpecModel(object):
	'''
	A model representing spec file sections and basic manipulation methods
	'''
	# Default section order in a spec file
	SPEC_SECTION_ORDER = [
				SpecStDescription,
				SpecStPackage,
				SpecStPrep,
				SpecStBuild,
				SpecStClean,
				SpecStInstall,
				SpecStCheck,
				SpecStPost,
				SpecStPreun,
				SpecStPostun,
				SpecStPre,
				SpecStPretrans,
				SpecStPosttrans,
				SpecStTrigger,
				SpecStTriggerin,
				SpecStTriggerprein,
				SpecStTriggerun,
				SpecStTriggerpostun,
				SpecStVerifyscript,
				SpecStFiles,
				SpecStChangelog
			]

	def __init__(self):
		'''
		'''
		self.sections = []

	def append(self, section):
		'''
		Append a section
		@param section: a section to be appended
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.sections.append(section)

	def remove(self, section):
		'''
		Remove a section
		@param section: a section to be removed
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		'''
		if section in self.sections:
			self.sections.remove(section)
		else:
			raise SpecNotFound("Section '%s' not found", str(section))

	def append_items(self, items):
		'''
		Append multiple sections
		@param items: sections to be added
		@type items: list of L{SpecSection}
		@return: None
		@rtype: None
		'''
		for item in items:
			self.sections.append(item)

	def add(self, section):
		'''
		Add a section, try to guess the most suitable position for the section
		@param section: section to be added
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		def get_add_index(idx_find, idx):
			if idx_find == idx:
				ret = idx - 1
				diff = -1
			else:
				diff = idx_find - idx
				if diff < 0:
					ret = idx + (-diff)
				else:
					ret = idx - (diff + 1)
			# check bounds
			if ret < 0:
				ret = idx + (abs(diff) + 1)
				if ret >= len(self.SPEC_SECTION_ORDER):
					return None
			elif ret >= len(self.SPEC_SECTION_ORDER):
				ret = idx - abs(diff)
				if ret < 0:
					return None
			return ret

		if issubclass(section.__class__, SpecStDefinition) \
				or issubclass(section.__class__, SpecStIf):
			raise SpecNotImplemented("Unable to add definitions and ifs")

		found = False
		if not issubclass(section.__class__, SpecStPackage):
			# simple replace
			for idx, sec in enumerate(self.sections):
				if issubclass(sec.__class__, section.__class__):
					SpecDebug.debug("-- replacing section '%s'" % type(section))
					self.sections[idx] = section
					found = True
					break

		if found:
			return

		# replace failed, append section based on section order

		if issubclass(section.__class__, SpecStPackage):
			# This needs special checks based on package, not only package, but
			# description, ... as well
			raise SpecNotImplemented("Adding %package section not implemented") # TODO: implement

		for idx, sec in enumerate(self.SPEC_SECTION_ORDER):
			if issubclass(section.__class__, sec):
				break

		# idx now points to the section in SPEC_SECTION_ORDER
		idx_find = idx
		while not found:
			idx_find = get_add_index(idx_find, idx)

			if idx_find is None:
				raise SpecNotFound("Section '%s' was not found in section order" % section)

			for i, sec in enumerate(self.sections):
				if issubclass(sec.__class__, self.SPEC_SECTION_ORDER[idx_find]):
					found = True
					if idx_find > idx:
						SpecDebug.debug("-- addiding section '%s' at position before section '%s'" % (type(section), type(sec)))
						self.sections.insert(i, section)
					else:
						SpecDebug.debug("-- addiding section '%s' at position after section '%s'" % (type(section), type(sec)))
						self.sections.insert(i + 1, section)
					break

		if not found:
			raise SpecNotFound("Section '%s' was not added" % type(section))

	def get_sections(self):
		'''
		Get list of all sections
		@return: list of sections
		@rtype: list of L{SpecSection}
		'''
		return self.sections

	def find_section(self, section_type):
		'''
		Find a section of a specific type type
		@param section_type: section type to look for
		@type section_type: __class__
		@return: list of sections of the provided type or None
		@rtype: list of L{SpecSection}
		'''
		ret = None
		for s in self.sections:
			if issubclass(s.__class__, section_type):
				if not ret:
					ret = []
				ret.append(s)
		return ret

	def find_definitions_all(self):
		'''
		Find all definitions within spec model
		@return: list of definitions
		@rtype: list of L{SpecStDefinition}
		@raise SpecNotFound:
		@todo: move to the model itself?
		'''
		def xfind_definitions_all(sections):
			ret = []
			for s in sections:
				if issubclass(s.__class__, SpecStIf):
					b = xfind_definitions_all(s.get_true_branch())
					if b:
						ret += b
					b = xfind_definitions_all(s.get_false_branch())
					if b:
						ret += b
				elif issubclass(s.__class__, SpecStDefinition):
					ret.append(s)
				elif issubclass(s.__class__, SpecStPackage):
					b = xfind_definitions_all(s.get_defs())
					if b:
						ret += b
			return ret

		return xfind_definitions_all(self.sections)

