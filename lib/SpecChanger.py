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
from SpecManipulator import SpecManipulator
from Statement import *
from SpecError import SpecNotFound, SpecNotImplemented

class SpecChanger(SpecManipulator):
	def __init__(self, statements = None):
		if statements is not None:
			self.setStatements(statements)

	def setStatements(self, statements):
		self.statements = statements
		self.sections = [x for x in statements if x.parent is None and type(x) is not StIf]

	def getStatements(self):
		return self.statements

	def find_section(self, section_type):
		for s in self.sections:
			if type(s) is section_type:
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

	def provides_show(self, package, f = sys.stdout):
		return self.find_definition_print('Provides:', package, f)

	def provides_add(self, package, what):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def provides_remove(self, package, what, f = sys.stdout):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def requires_show(self, package, f = sys.stdout):
		return self.find_definition_print('Requires:', package, f)

	def requires_add(self, package, what):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def requires_remove(self, package, what, f = sys.stdout):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def buildrequires_show(self, package, f = sys.stdout):
		return self.find_definition_print('BuildRequires:', package, f)

	def buildrequires_add(self, package, what):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def buildrequires_remove(self, package, what, f = sys.stdout):
		# TODO: implement
		raise SpecNotImplemented("Not Implemented")

	def changelog_show(self, f = sys.stdout):
		# TODO: do pretty print
		return self.find_section_print(StChangelog, f)

	def changelog_add(self, items):
		return self.find_section_add(StChangelog, items)

	def changelog_remove(self, what):
		raise SpecNotImplemented("Not Implemented")

	def description_show(self, package = None, f = sys.stdout):
		return self.find_section_print(StDescription, f)

	def description_edit(self, replacement, package = None):
		return self.find_section_edit(StDescription, replacement)

	def build_show(self, f = sys.stdout):
		return self.find_section_print(StBuild, f)

	def build_edit(self, replacement):
		return self.find_section_edit(StBuild, replacement)

	def check_show(self, f = sys.stdout):
		return self.find_section_print(StCheck, f)

	def check_edit(self, replacement):
		return self.find_section_edit(StCheck, replacement)

	def clean_show(self, f = sys.stdout):
		return self.find_section_print(StClean, f)

	def clean_edit(self, replacement):
		return self.find_section_edit(StClean, replacement)

	def files_show(self, f = sys.stdout):
		raise SpecNotImplemented("Not Implemented")
		return self.find_section_print(StFiles, f)

	def files_add(self, items):
		return self.find_section_add(StFiles, items)

	def files_remove(self, files):
		raise SpecNotImplemented("Not Implemented")

	def install_show(self, f = sys.stdout):
		return self.find_section_print(StInstall, f)

	def install_edit(self, replacement):
		return self.find_section_edit(StInstall, replacement)

	def package_show(self, f = sys.stdout):
		return self.find_section_print(StPackage, f)

	def package_add(self, package):
		return self.find_section_add(StPackage, items)

	def package_remove(self, package):
		raise SpecNotImplemented("Not Implemented")

	def prep_show(self, f = sys.stdout):
		return self.find_section_print(StPrep, f)

	def prep_edit(self, replacement):
		return self.find_section_edit(StPrep, replacement)

	def pre_show(self, f = sys.stdout):
		return self.find_section_print(StPre, f)

	def pre_edit(self, replacement):
		return self.find_section_edit(StPre, replacement)

	def post_show(self, f = sys.stdout):
		return self.find_section_print(StPost, f)

	def post_edit(self, replacement):
		return self.find_section_edit(StPost, replacement)

	def preun_show(self, f = sys.stdout):
		return self.find_section_print(StPreun, f)

	def preun_edit(self, replacement):
		return self.find_section_edit(StPreun, replacement)

	def postun_show(self, f = sys.stdout):
		return self.find_section_print(StPostun, f)

	def postun_edit(self, replacement):
		return self.find_section_edit(StPostun, replacement)

	def pretrans_show(self, f = sys.stdout):
		return self.find_section_print(StPretrans, f)

	def pretrans_edit(self, replacement):
		return self.find_section_edit(StPretrans, replacement)

	def posttrans_show(self, f = sys.stdout):
		return self.find_section_print(StPosttrans, f)

	def posttrans_edit(self, replacement):
		return self.find_section_edit(StPosttrans, replacement)

	def triggerin_show(self, f = sys.stdout):
		return self.find_section_print(StTriggerin, f)

	def triggerin_edit(self, replacement):
		return self.find_section_edit(StTriggerin, replacement)

	def triggerprein_show(self, f = sys.stdout):
		return self.find_section_print(StTriggerprein, f)

	def triggerprein_edit(self, replacement):
		return self.find_section_edit(StTriggerin, replacement)

	def triggerun_show(self, f = sys.stdout):
		return self.find_section_print(StTriggerun, f)

	def triggerun_edit(self, replacement):
		return self.find_section_edit(StTriggerun, replacement)

	def triggerpostun_show(self, f = sys.stdout):
		return self.find_section_print(StPostun, f)

	def triggerpostun_edit(self, replacement):
		return self.find_section_edit(StTriggerpostun, replacement)

	def verifyscript_show(self, f = sys.stdout):
		return self.find_section_print(StVerifyscript, f)

	def verifyscript_edit(self, replacement):
		return self.find_section_edit(StVerifyscript, replacement)

