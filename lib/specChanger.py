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

import sys
from specManipulator import SpecManipulator
from specStatement import *
from specError import SpecNotFound, SpecNotImplemented

class SpecChanger(SpecManipulator):
	def __init__(self, statements = None):
		if statements is not None:
			self.setStatements(statements)

	def setStatements(self, statements):
		self.statements = statements
		self.sections = [x for x in statements if x.parent is None and type(x) is not SpecStIf]

	def getStatements(self):
		return self.statements

	def find_section(self, section_type):
		for s in self.sections:
			if isinstance(s, section_type):
				return s

		return None

	def find_section_print(self, section_type, f = sys.stdout, verbose = True):
		s = self.find_section(section_type)

		if s is not None:
			s.print_file(f)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

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

	def find_definition_print(self, definition, package, f = sys.stdout):
		# TODO: use this for particular package as well
		for s in self.statements:
			if type(s) is StDefinition and str(s.name) == definition:
				s.value.print_file(f, raw = True)
				f.write('\n') # Add delim since raw token is printed

	def find_definition_add(self, package, items):
		raise SpecNotImplemented("Not Implemented")

	def find_definition_remove(self, package, items):
		raise SpecNotImplemented("Not Implemented")

	def provides_show(self, package, f = sys.stdout):
		return self.find_definition_print('Provides:', package, f)

	def provides_add(self, package, items):
		return self.find_definition_add('Provides:', package, items)

	def provides_remove(self, package, items):
		return self.find_definition_remove('Provides:', package, items)

	def requires_show(self, package, f = sys.stdout):
		return self.find_definition_print('Requires:', package, f)

	def requires_add(self, package, items):
		return self.find_definition_add('Requires:', package, items)

	def requires_remove(self, package, items):
		return self.find_definition_remove('Requires:', package, items)

	def buildrequires_show(self, package, f = sys.stdout):
		return self.find_definition_print('BuildRequires:', package, f)

	def buildrequires_add(self, package, items):
		return self.find_definition_add('BuildRequires:', package, items)

	def buildrequires_remove(self, package, items):
		return self.find_definition_remove('BuildRequires:', package, items)

	def changelog_show(self, f = sys.stdout):
		# TODO: do pretty print
		return self.find_section_print(SpecStChangelog, f)

	def changelog_add(self, items):
		return self.find_section_add(SpecStChangelog, items)

	def changelog_remove(self, items):
		return self.find_section_remove(SpecStChangelog, items)

	def description_show(self, package = None, f = sys.stdout):
		return self.find_section_print(SpecStDescription, f)

	def description_edit(self, replacement, package = None):
		return self.find_section_edit(SpecStDescription, replacement)

	def build_show(self, f = sys.stdout):
		return self.find_section_print(SpecStBuild, f)

	def build_edit(self, replacement):
		return self.find_section_edit(SpecStBuild, replacement)

	def check_show(self, f = sys.stdout):
		return self.find_section_print(SpecStCheck, f)

	def check_edit(self, replacement):
		return self.find_section_edit(SpecStCheck, replacement)

	def clean_show(self, f = sys.stdout):
		return self.find_section_print(SpecStClean, f)

	def clean_edit(self, replacement):
		return self.find_section_edit(SpecStClean, replacement)

	def files_show(self, f = sys.stdout):
		return self.find_section_print(SpecStFiles, f)

	def files_add(self, items):
		return self.find_section_add(SpecStFiles, items)

	def files_remove(self, items):
		return self.find_section_remove(SpecStFiles, items)

	def install_show(self, f = sys.stdout):
		return self.find_section_print(SpecStInstall, f)

	def install_edit(self, replacement):
		return self.find_section_edit(SpecStInstall, replacement)

	def package_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPackage, f)

	def package_add(self, items):
		return self.find_section_add(SpecStPackage, items)

	def package_remove(self, items):
		return self.find_section_remove(SpecStPackage, items)

	def prep_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPrep, f)

	def prep_edit(self, replacement):
		return self.find_section_edit(SpecStPrep, replacement)

	def pre_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPre, f)

	def pre_edit(self, replacement):
		return self.find_section_edit(SpecStPre, replacement)

	def post_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPost, f)

	def post_edit(self, replacement):
		return self.find_section_edit(SpecStPost, replacement)

	def preun_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPreun, f)

	def preun_edit(self, replacement):
		return self.find_section_edit(SpecStPreun, replacement)

	def postun_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPostun, f)

	def postun_edit(self, replacement):
		return self.find_section_edit(SpecStPostun, replacement)

	def pretrans_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPretrans, f)

	def pretrans_edit(self, replacement):
		return self.find_section_edit(SpecStPretrans, replacement)

	def posttrans_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPosttrans, f)

	def posttrans_edit(self, replacement):
		return self.find_section_edit(SpecStPosttrans, replacement)

	def triggerin_show(self, f = sys.stdout):
		return self.find_section_print(SpecStTriggerin, f)

	def triggerin_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerprein_show(self, f = sys.stdout):
		return self.find_section_print(SpecStTriggerprein, f)

	def triggerprein_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerun_show(self, f = sys.stdout):
		return self.find_section_print(SpecStTriggerun, f)

	def triggerun_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerun, replacement)

	def triggerpostun_show(self, f = sys.stdout):
		return self.find_section_print(SpecStPostun, f)

	def triggerpostun_edit(self, replacement):
		return self.find_section_edit(SpecStTriggerpostun, replacement)

	def verifyscript_show(self, f = sys.stdout):
		return self.find_section_print(SpecStVerifyscript, f)

	def verifyscript_edit(self, replacement):
		return self.find_section_edit(SpecStVerifyscript, replacement)

