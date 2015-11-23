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
from specError import SpecNotFound, SpecNotImplemented
from specManipulator import SpecManipulator

class SpecChanger(SpecManipulator):
	def __init__(self, model):
		self.model = model

	def setModel(self, model):
		self.model = model

	def getModel(self):
		return self.model

	def write(self, f):
		# TODO: move to Renderer
		for s in self.model.getSections():
			s.write(f)

	def find_section_edit(self, section_type, replacement, verbose = True):
		s = self.find_section(section_type)

		if s is not None:
			s.edit(replacement)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

	def find_section_add(self, section_type, items, verbose = True):
		s = self.find_section(section_type)

		if s is not None:
			s.add(items)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

	def find_definition_add(self, definition, packages):
		for pkg in packages:
			if pkg == '-':
				# TODO: add in preamble
				pass
			else:
				for st_pkg in self.statements:
					if type(st_pkg) is SpecStPackage:
						if st_pkg.pkg != None and str(st_pkg.pkg) == pkg:
								st_pkg.add_definition(definition, packages[pkg])

	def find_definition_remove(self, definition, packages):
		for pkg in packages:
			if pkg == '-':
				# TODO: remove in preamble
				pass
			else:
				for st_pkg in self.statements:
					if type(st_pkg) is SpecStPackage:
						if st_pkg.pkg != None and str(st_pkg.pkg) == pkg:
								st_pkg.remove_definition(definition, packages[pkg])

	def sections_add(self, sections):
		def get_add_index(idx_find, idx):
			# first iterate downwards, when beginning reached, continue upwards
			# from idx till end of section is reached (should not occur)
			if idx_find < idx and idx_find > 0:
				return idx_find - 1
			elif idx_find < idx and idx_find == 0:
				return idx + 1
			elif idx_find > idx and idx_find < len(self.SPEC_SECTION_ORDER):
				return idx_find + 1
			elif idx_find == idx:
				return idx - 1
			else:
				return None

		for section in sections:
			if type(section) is SpecStDefinition or type(section) is SpecStIf:
				raise SpecNotImplemented("Unable to add definitions and ifs")

			found = False
			if type(section) is not SpecStPackage:
				# simple replace
				for idx, sec in enumerate(self.statements):
					if type(sec) is type(section):
						self.statements[idx] = section
						found = True
						break

			if found:
				continue

			# replace failed, append section

			if type(section) is SpecStPackage:
				raise SpecNotImplemented("Adding %package section not implemented") # TODO: implement

			for idx, sec in enumerate(self.SPEC_SECTION_ORDER):
				if type(section) is sec:
					break

			# idx now points to the section in SPEC_SECTION_ORDER
			idx_find = idx
			while not found:
				idx_find = get_add_index(idx_find, idx)

				if idx_find is None:
					raise SpecNotFound("Section '%s' was not found in section order" % section)

				for i, sec in enumerate(self.statements):
					if type(sec) == self.SPEC_SECTION_ORDER[idx_find]:
						found = True
						self.statements.insert(i + 1, section)
						break

			if not found:
				raise SpecNotFound("Section '%s' was not added" % section)

	def provides_add(self, packages):
		return self.find_definition_add('Provides:', packages)

	def provides_remove(self, packages):
		return self.find_definition_remove('Provides:', packages)

	def requires_add(self, packages):
		return self.find_definition_add('Requires:', packages)

	def requires_remove(self, packages):
		return self.find_definition_remove('Requires:', packages)

	def buildrequires_add(self, package):
		return self.find_definition_add('BuildRequires:', package)

	def buildrequires_remove(self, packages):
		return self.find_definition_remove('BuildRequires:', packages)

	#TODO: def changelog_add(self, date, usname, email, version, msg):
	def changelog_add(self, items):
		return self.find_section_add(SpecStChangelog, items)

	def changelog_remove(self, items):
		return self.find_section_remove(SpecStChangelog, items)

	def description_edit(self, replacement, package = None):
		return self.find_section_edit(SpecStDescription, replacement)

	def build_edit(self, replacement):
		return self.find_section_edit(SpecStBuild, replacement)

	def check_edit(self, replacement):
		return self.find_section_edit(SpecStCheck, replacement)

	def clean_edit(self, replacement):
		return self.find_section_edit(SpecStClean, replacement)

	def files_edit(self, replacement):
		return self.find_section_edit(SpecStFiles, replacement)

	def install_edit(self, replacement):
		return self.find_section_edit(SpecStInstall, replacement)

	def package_add(self, items):
		return self.find_section_add(SpecStPackage, items)

	def package_remove(self, items):
		return self.find_section_remove(SpecStPackage, items)

	def prep_edit(self, replacement):
		return self.find_section_edit(SpecStPrep, replacement)

	def pre_edit(self, replacement):
		return self.find_section_edit(SpecStPre, replacement)

	def post_edit(self, replacement):
		return self.find_section_edit(SpecStPost, replacement)

	def preun_edit(self, replacement):
		return self.find_section_edit(SpecStPreun, replacement)

	def postun_edit(self, replacement):
		return self.find_section_edit(SpecStPostun, replacement)

	def pretrans_edit(self, replacement):
		return self.find_section_edit(SpecStPretrans, replacement)

	def posttrans_edit(self, replacement):
		return self.find_section_edit(SpecStPosttrans, replacement)

	def triggerin_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerprein_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerun_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerun, replacement)

	def triggerpostun_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerpostun, replacement)

	def verifyscript_edit(self, replacement):
		return self.find_section_edit(SpecStVerifyscript, replacement)

