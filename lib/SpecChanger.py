# -*- coding: utf-8 -*-
# ####################################################################
# specker - a simple spec file tool
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

class SpecChanger(SpecManipulator):
	def __init__(self, statements = None):
		if statements is not None:
			self.setStatements(statements)

	def setStatements(self, statements):
		self.statements = statements
		self.sections = [x for x in statements if x.parent is None and type(x) is not StIf]

	def getStatements(self):
		return self.statements

	def changelog_show(self, f = sys.stdout):
		# TODO: do pretty print
		for s in self.sections:
			if type(s) is StChangelog:
				s.print_file(f)
				break

	def changelog_add(self, items):
		pass

	def changelog_remove(self, what):
		pass

	def description_show(self, package = None, f = sys.stdout):
		pass

	def description_edit(self, definition, package = None):
		pass

	def build_show(self, f = sys.stdout):
		pass

	def build_edit(self, build):
		pass

	def check_show(self, f = sys.stdout):
		pass

	def check_edit(self, edit):
		pass

	def clean_show(self, f = sys.stdout):
		pass

	def files_show(self, f = sys.stdout):
		pass

	def files_add(self, files):
		pass

	def files_remove(self, files):
		pass

	def install_show(self, f = sys.stdout):
		pass

	def install_edit(self, install):
		pass

	def package_show(self, f = sys.stdout):
		pass

	def package_add(self, package):
		pass

	def package_remove(self, package):
		pass

	def prep_show(self, f = sys.stdout):
		pass

	def prep_edit(self, prep):
		pass

	def pre_show(self, f = sys.stdout):
		pass

	def pre_edit(self, pre):
		pass

	def post_show(self, f = sys.stdout):
		pass

	def post_edit(self, post):
		pass

	def preun_show(self, f = sys.stdout):
		pass

	def preun_edit(self, preun):
		pass

	def postun_show(self, f = sys.stdout):
		pass

	def postun_edit(self, postun):
		pass

	def pretrans_show(self, f = sys.stdout):
		pass

	def pretrans_edit(self, pretrans):
		pass

	def posttrans_show(self, f = sys.stdout):
		pass

	def posttrans_edit(self, posttrans):
		pass

	def triggerin_show(self, f = sys.stdout):
		pass

	def triggerin_edit(self, triggerin):
		pass

	def triggerprein_show(self, f = sys.stdout):
		pass

	def triggerprein_edit(self, triggerprein):
		pass

	def triggerun_show(self, f = sys.stdout):
		pass

	def triggerun_edit(self, triggerun):
		pass

	def triggerpostun_show(self, f = sys.stdout):
		pass

	def triggerpostun_edit(self, triggerpostun):
		pass

	def verifyscript_show(self, f = sys.stdout):
		pass

	def verifyscript_edit(self, verifyscript):
		pass

