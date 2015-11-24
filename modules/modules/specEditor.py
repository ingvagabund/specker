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
specker-lib - spec model editor
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import re
from specSection import *
from specToken import SpecToken, SpecTokenList
from specError import SpecNotFound, SpecNotImplemented
from specManipulator import SpecManipulator

class SpecEditor(SpecManipulator):
	'''
	TODO
	'''
	def __init__(self, model):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.model = model
		self.EDITORS = [
				SpecIfEditor,
				SpecDefinitionEditor,
				SpecGlobalEditor,
				SpecBuildEditor,
				SpecChangelogEditor,
				SpecCheckEditor,
				SpecCleanEditor,
				SpecDescriptionEditor,
				SpecFilesEditor,
				SpecInstallEditor,
				SpecPackageEditor,
				SpecPrepEditor,
				SpecPreEditor,
				SpecPostEditor,
				SpecPreunEditor,
				SpecPostunEditor,
				SpecPretransEditor,
				SpecPosttransEditor,
				SpecTriggerEditor,
				SpecTriggerinEditor,
				SpecTriggerpreinEditor,
				SpecTriggerunEditor,
				SpecTriggerpostunEditor,
				SpecVerifyscriptEditor
			]

	def register(self, editor):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		# TODO: move to SpecManipulator
		found = False
		for idx, item in enumerate(self.EDITORS):
			if issubclass(editor, item):
				found = True
				self.EDITORS[idx] = editor

		if not found:
			raise SpecNotFound("Invalid editor '%s' registration" % editor.__name__)

	def getEditorClass(self, cls):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		found = False
		for editor in self.EDITORS:
			if issubclass(cls, editor.obj):
				found = True
				return editor
		if not found:
			raise SpecNotImplemented("Not implemented editor")

	def getEditor(self, section):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.getEditorClass(section.__class__)

	def find_section_edit(self, section_type, replacement, verbose = True):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		s = self.model.find_section(section_type)

		if s is not None:
			if len(s) > 1:
				raise SpecNotImplemented("Cannot edit more then one section")

			self.getEditor(s[0]).edit(s[0], replacement)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

	def sections_add(self, sections):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for section in sections:
			self.model.add(section)

	def find_section_add(self, section_type, items, verbose = True):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		s = self.model.find_section(section_type)

		if s is not None:
			self.getEditor(s[0]).add(s[0], items)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

	def find_definition_add(self, definition, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		definition_editor = self.getEditorClass(SpecStDefinition)
		package_editor = self.getEditorClass(SpecStPackage)

		for pkg in packages:
			if pkg == '-':
				for val in packages['-']:
					d = definition_editor.create(None, definition, val)
					self.model.add(d)
			else:
				for st_pkg in self.model.getSections():
					found = False
					if issubclass(st_pkg.__class__, SpecStPackage):
						if st_pkg.pkg != None and str(st_pkg.getPackage()) == pkg:
							found = True
							for val in packages[str(st_pkg.getPackage())]:
								d = definition_editor.create(st_pkg, definition, val)
								package_editor.addDefinition(st_pkg, d)

				if not found:
					raise SpecNotFound("Package '%s' not found" % pkg)

	def find_definition_remove(self, definition, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for pkg in packages:
			if pkg == '-':
				for st_def in self.model.getSections():
					if issubclass(st_def.__class__, SpecStDefinition):
						if definition.match(str(st_def.getName())):
							for val in packages['-']:
								if st_def.getValue() == val:
									self.model.remove(st_def)
			else:
				for st_pkg in self.model.getSections():
					if type(st_pkg) is SpecStPackage:
						if st_pkg.pkg != None and str(st_pkg.pkg) == pkg:
								st_pkg.remove_definition(definition, packages[pkg])

	################################################################################

	def provides_add(self, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_add('Provides:', packages)

	def provides_remove(self, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_remove(re.compile('Provides:'), packages)

	def requires_add(self, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_add('Requires:', packages)

	def requires_remove(self, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_remove(re.compile('Requires:'), packages)

	def buildrequires_add(self, package):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_add('BuildRequires:', package)

	def buildrequires_remove(self, packages):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_definition_remove(re.compile('BuildRequires:'), packages)

	def changelogentry_add(self, date, username, email, version, msg):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		changelog = self.model.find_section(SpecStChangelog)
		if len(changelog) > 1:
			raise SpecNotImplemented("Adding to multiple %changelogs not supported")
		if len(changelog) != 1:
			raise SpecNotFound("Cannot add changelog entry, changelog not found")

		self.getEditor(changelog[0]).addEntry(changelog[0], date, username, email, version, msg)

	def description_edit(self, replacement, package = None):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStDescription, replacement)

	def build_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStBuild, replacement)

	def check_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStCheck, replacement)

	def clean_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStClean, replacement)

	def files_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStFiles, replacement)

	def install_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStInstall, replacement)

	def package_add(self, items):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		# TODO: check for duplicit entry
		for pkg_name in items:
			pkg = self.getEditorClass(SpecStPackage).create(None, pkg_name)
			self.model.add(pkg)

	def package_remove(self, items):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for item in items:
			for st_pkg in self.model.getSections():
				if not issubclass(st_pkg.__class__, SpecStPackage):
					continue

				if (item == '-' or item is None) and st_pkg.getPackage() is None:
					self.model.remove(st_pkg)
				elif item is not None and st_pkg.getPackage() is not None and \
						item == str(st_pkg.getPackage()):
					self.model.remove(st_pkg)

	def prep_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPrep, replacement)

	def pre_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPre, replacement)

	def post_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPost, replacement)

	def preun_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPreun, replacement)

	def postun_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPostun, replacement)

	def pretrans_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPretrans, replacement)

	def posttrans_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStPosttrans, replacement)

	def triggerin_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerprein_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStTriggerin, replacement)

	def triggerun_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStTriggerun, replacement)

	def triggerpostun_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStTriggerpostun, replacement)

	def verifyscript_edit(self, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_edit(SpecStVerifyscript, replacement)

###############################################################################

class SpecSectionEditor(object):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = [ SpecStBuild, SpecStCheck, SpecStClean, SpecStDescription, SpecStFiles, SpecStInstall,
				SpecStPrep, SpecStPre, SpecStPost, SpecStPreun, SpecStPostun, SpecStPretrans,
				SpecStPosttrans, SpecStTrigger, SpecStTriggerin, SpecStTriggerprein, SpecStTriggerun,
				SpecStTriggerpostun, SpecStVerifyscript ]

	@classmethod
	def edit(cls, section, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		new_tokens = SpecTokenList(replacement)
		section.setTokens(new_tokens)

class SpecExpressionEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStExpression

	@classmethod
	def edit(cls, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		raise SpecNotImplemented("Editing expression not implemented")

class SpecIfEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStIf

	@classmethod
	def edit(cls, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		raise SpecNotImplemented("Editing %if not implemented")

class SpecDefinitionEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStDefinition

	@classmethod
	def create(cls, parent, name, value):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = SpecDefinitionEditor.obj(parent)
		ret.setName(SpecToken.create(name))
		ret.setValue(SpecToken.create(value, append="\n"))
		return ret

class SpecGlobalEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStGlobal

	@classmethod
	def edit(cls, replacement):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		raise SpecNotImplemented("Editing %global not implemented")

class SpecBuildEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStBuild

class SpecChangelogEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStChangelog

	@classmethod
	def addEntry(cls, changelog, date, username, email, version, msg):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		entry = SpecChangelogEditor.obj.SpecStChangelogEntry(changelog)
		entry.setStar(SpecToken.create('*'))
		entry.setDate(SpecToken.create(date.strftime("%a %b %d %Y")))
		entry.setDateParsed(date)
		entry.setUser(SpecToken.create(username))
		entry.setUserEmail(SpecToken.create('<' + email + '>'))
		entry.setVersionDelim(SpecToken.create('-'))
		if version is None:
			entry.setVersion(changelog.getEntries()[0].getVersion())
		else:
			entry.setVersion(SpecToken.create(version, append = '\n'))
		entry.setMessage(SpecToken.create(msg, append = '\n'))
		changelog.insertEntry(entry)

class SpecCheckEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStCheck

class SpecCleanEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStClean

class SpecDescriptionEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStDescription

class SpecFilesEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStFiles

class SpecInstallEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStInstall

class SpecPackageEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPackage

	@classmethod
	def create(cls, parent, pkg = None):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = SpecStPackage(parent)
		pkg = None if pkg == None or pkg == '-' else pkg
		if pkg is not None:
			ret.setPackage(SpecToken().create(pkg, append = '\n'))
		ret.setTokenSection(SpecToken().create('%package', append = '\n' if pkg is None else ' '))
		return ret

	@classmethod
	def addDefinition(cls, pkg, definition):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		# TODO: based on alphabet?
		pkg.defsAppend(definition)

class SpecPrepEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPrep

class SpecPreEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPre

class SpecPostEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPost

class SpecPreunEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPreun

class SpecPostunEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPostun

class SpecPretransEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPretrans

class SpecPosttransEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPosttrans

class SpecTriggerEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTrigger

class SpecTriggerinEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerprein

class SpecTriggerunEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptEditor(SpecSectionEditor):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStVerifyscript

