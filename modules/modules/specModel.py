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

from specSection import *

class SpecModel(object):
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
		self.sections = []

	def append(self, section):
		self.sections.append(section)

	def remove(self, section):
		self.sections.remove(section)

	def append_items(self, array):
		for item in array:
			self.sections.append(item)

	def add(self, section):
		# TODO: add section based on order
		#def get_add_index(idx_find, idx):
		#	# first iterate downwards, when beginning reached, continue upwards
		#	# from idx till end of section is reached (should not occur)
		#	if idx_find < idx and idx_find > 0:
		#		return idx_find - 1
		#	elif idx_find < idx and idx_find == 0:
		#		return idx + 1
		#	elif idx_find > idx and idx_find < len(self.SPEC_SECTION_ORDER):
		#		return idx_find + 1
		#	elif idx_find == idx:
		#		return idx - 1
		#	else:
		#		return None

		#for section in sections:
		#	if type(section) is SpecStDefinition or type(section) is SpecStIf:
		#		raise SpecNotImplemented("Unable to add definitions and ifs")

		#	found = False
		#	if type(section) is not SpecStPackage:
		#		# simple replace
		#		for idx, sec in enumerate(self.statements):
		#			if type(sec) is type(section):
		#				self.statements[idx] = section
		#				found = True
		#				break

		#	if found:
		#		continue

		#	# replace failed, append section

		#	if type(section) is SpecStPackage:
		#		raise SpecNotImplemented("Adding %package section not implemented") # TODO: implement

		#	for idx, sec in enumerate(self.SPEC_SECTION_ORDER):
		#		if type(section) is sec:
		#			break

		#	# idx now points to the section in SPEC_SECTION_ORDER
		#	idx_find = idx
		#	while not found:
		#		idx_find = get_add_index(idx_find, idx)

		#		if idx_find is None:
		#			raise SpecNotFound("Section '%s' was not found in section order" % section)

		#		for i, sec in enumerate(self.statements):
		#			if type(sec) == self.SPEC_SECTION_ORDER[idx_find]:
		#				found = True
		#				self.statements.insert(i + 1, section)
		#				break

		#	if not found:
		#		raise SpecNotFound("Section '%s' was not added" % section)
		self.sections.insert(0, section)

	def remove(self, section):
		self.sections.remove(section)

	def getSections(self):
		return self.sections

	def find_section(self, section):
		ret = None
		for s in self.sections:
			if issubclass(s.__class__, section):
				if not ret:
					ret = []
				ret.append(s)
		return ret

