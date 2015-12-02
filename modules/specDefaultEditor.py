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
A spec model editor
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import re
from specSection import *
from specDebug import SpecDebug
from specToken import SpecToken, SpecTokenList
from specError import SpecNotFound, SpecNotImplemented
from specModelEditor import SpecModelEditor

class SpecDefaultEditor(SpecModelEditor):
	'''
	A spec model editor
	'''
	def __init__(self, reader, writer):
		self.set_model_reader(reader)
		self.set_model_writer(writer)
		self.MANIPULATORS = [
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

	def get_editor_class(self, cls):
		'''
		Get editor based on class
		@param cls: class to be used
		@type cls: __class__
		@return: matched editor class
		@rtype: L{SpecSectionEditor}
		@raise SpecNotFound: if editor class is not found
		'''
		found = False
		for editor in self.MANIPULATORS:
			if issubclass(cls, editor.obj):
				found = True
				return editor
		if not found:
			raise SpecNotImplemented("Not implemented editor")

	def get_editor(self, section):
		'''
		Get editor based on instance
		@param section: instance to be used to get editor
		@type section: L{SpecSectionEditor}
		@return: editor class to be used for provided instance
		@rtype:  L{SpecSectionEditor}
		@raise SpecNotFound: if editor is not found
		'''
		return self.get_editor_class(section.__class__)

	def find_section_edit(self, section_type, replacement, verbose = True):
		'''
		Call editor's edit method for specific section type
		@param section_type: section type to be used when calling edit
		@type section_type: __class__
		@param replacement: parameter for edit method
		@type replacement: string
		@param verbose: if True raise an exception if editor is not found
		@type verbose: Boolean
		@return: section used for edit
		@rtype: L{SpecSection} or None
		@raise SpecNotFound: if editor is not found
		@raise SpecNotImplemented: if more than one section matches section type
		'''
		s = self.get_model_reader().find_section(section_type)

		if s is not None:
			if len(s) > 1:
				raise SpecNotImplemented("Cannot edit more then one section")

			SpecDebug.logger.debug("- editing section '%s'", str(s[0]))
			self.get_editor(s[0]).edit(s[0], replacement)
		elif verbose:
			raise SpecNotFound("Error: section type '%s' not found" % section_type)

		return s[0] if s else None

	def sections_add(self, sections):
		'''
		Add sections to model
		@param sections: section to be added
		@type : L{SpecSection}
		@return: None
		@rtype: None
		@todo: remove/use only model to add?
		'''
		for section in sections:
			SpecDebug.logger.debug("- adding section '%s'", str(section))
			self.get_model_writer().add(section)

	def find_section_add(self, section_type, items, verbose = True):
		'''
		Add items to a section
		@param section_type: section type to be used when calling add
		@type section_type: __class__
		@param items: items to be added to a section of type section type
		@type items: editor specific
		@param verbose: if True raise an exception if editor is not found
		@type verbose: Boolean
		@return: section used for edit
		@rtype: L{SpecSection} or None
		@raise SpecNotFound: if editor is not found
		@raise SpecNotImplemented: if more than one section matches section type
		'''
		s = self.get_model_reader().find_section(section_type)

		if s is not None:
			SpecDebug.logger.debug("- adding section to '%s'", str(s[0]))
			self.get_editor(s[0]).add(s[0], items)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s[0] if s else None

	def find_definition_add(self, definition, packages):
		'''
		Add definition to packages
		@param definition: a string representation of a definition e.g. 'Requires:'
		@type definition: string
		@param packages: definitions to be added to packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		definition_editor = self.get_editor_class(SpecStDefinition)
		package_editor = self.get_editor_class(SpecStPackage)

		for pkg in packages:
			if pkg == '-':
				for val in packages['-']:
					d = definition_editor.create(None, definition, val)
					self.get_model_writer().add(d)
			else:
				found = False
				for st_pkg in self.get_model_reader().get_sections():
					if issubclass(st_pkg.__class__, SpecStPackage):
						if st_pkg.pkg != None and str(st_pkg.get_package()) == pkg:
							found = True
							for val in packages[str(st_pkg.get_package())]:
								d = definition_editor.create(st_pkg, definition, val)
								package_editor.add_definition(st_pkg, d)

				if not found:
					raise SpecNotFound("Package '%s' not found" % pkg)

	def find_definition_remove(self, definition, packages):
		'''
		Find definition in specific package and remove it
		@param definition: a string representation of a definition e.g. 'Requires:'
		@type definition: string
		@param packages: definitions to be removed from packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		for pkg in packages:
			if pkg == '-':
				for st_def in self.get_model_reader().model.get_sections():
					if issubclass(st_def.__class__, SpecStDefinition):
						if definition.match(str(st_def.get_name())):
							for val in packages['-']:
								if st_def.get_value() == val:
									self.get_model_writer().remove(st_def)
			else:
				found = False
				for st_pkg in self.get_model_reader().model.get_sections():
					if type(st_pkg) is SpecStPackage:
						if st_pkg.pkg != None and str(st_pkg.pkg) == pkg:
								st_pkg.remove_definition(definition, packages[pkg])
				if not found:
					raise SpecNotFound("Package '%s' not found" % pkg)

	################################################################################

	def provides_add(self, packages):
		'''
		Add 'Provides:' to packages
		@param packages: provides to be added to packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		self.find_definition_add('Provides:', packages)

	def provides_remove(self, packages):
		'''
		Remove 'Provides:' from packages
		@param packages: provides to be removed from packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		self.find_definition_remove(re.compile('Provides:'), packages)

	def requires_add(self, packages):
		'''
		Add 'Requires:' to packages
		@param packages: requires to be added to packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		self.find_definition_add('Requires:', packages)

	def requires_remove(self, packages):
		'''
		Remove 'Requires:' from packages
		@param packages: requires to be removed from packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		self.find_definition_remove(re.compile('Requires:'), packages)

	def buildrequires_add(self, packages):
		'''
		Add 'BuildRequires:' to packages
		@param packages: buil requires to be added to packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		self.find_definition_add('BuildRequires:', packages)

	def buildrequires_remove(self, packages):
		'''
		Remove 'BuildRequires:' from packages
		@param packages: build requires to be removed from packages e.g. {'devel':
		['gcc', 'gdb'], '-': ['gcc']}; use '-' or None for main package
		@type packages: dict
		@return: None
		@rtype: None
		@raise SpecNotFound: if package is not found
		'''
		return self.find_definition_remove(re.compile('BuildRequires:'), packages)

	def changelogentry_add(self, date, username, email, version, msg):
		'''
		Add an entry to the changelog
		@param date: date used in entry
		@type date: datetime
		@param username: user name
		@type username: string
		@param email: email
		@type email: string
		@param version: version, if None, last version is used
		@type version: string
		@param msg: a message to be placed to the changelog entry
		@type msg: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if changelog section is not found
		@raise SpecNotImplemented: if multiple changelog sections are found
		'''
		changelog = self.get_model_reader().find_section(SpecStChangelog)
		if len(changelog) > 1:
			raise SpecNotImplemented("Adding to multiple %changelogs not supported")
		if len(changelog) != 1:
			raise SpecNotFound("Cannot add changelog entry, changelog not found")

		self.get_editor(changelog[0]).add_entry(changelog[0], date, username, email, version, msg)

	def description_edit(self, replacement, package = None):
		'''
		Edit description section
		@param replacement: section replacement
		@type replacement: string
		@param package: package which description should be replaced or None/'-'
		for main package
		@type package: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStDescription, replacement)

	def build_edit(self, replacement):
		'''
		Edit build section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStBuild, replacement)

	def check_edit(self, replacement):
		'''
		Edit check section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStCheck, replacement)

	def clean_edit(self, replacement):
		'''
		Edit clean section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStClean, replacement)

	def files_edit(self, replacement):
		'''
		Edit files section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStFiles, replacement)

	def install_edit(self, replacement):
		'''
		Edit install section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStInstall, replacement)

	def package_add(self, items):
		'''
		Add packages
		@param items: name of the packages to be added, e.g. ['devel', 'test']
		@type items: list of strings
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		@todo: rename to packages_add()
		'''
		# TODO: check for duplicit entry
		for pkg_name in items:
			pkg = self.get_editor_class(SpecStPackage).create(None, pkg_name)
			self.get_model_writer().add(pkg)

	def package_remove(self, items):
		'''
		Remove packages
		@param items: name of the packages to be removed, e.g. ['devel', 'test']
		@type items: list of strings
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		@todo: rename to packages_remove()
		'''
		for item in items:
			for st_pkg in self.get_model_reader().get_sections():
				if not issubclass(st_pkg.__class__, SpecStPackage):
					continue

				if (item == '-' or item is None) and st_pkg.get_package() is None:
					self.get_model_writer().remove(st_pkg)
				elif item is not None and st_pkg.get_package() is not None and \
						item == str(st_pkg.get_package()):
					self.get_model_writer().remove(st_pkg)

	def prep_edit(self, replacement):
		'''
		Edit prep section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPrep, replacement)

	def pre_edit(self, replacement):
		'''
		Edit pre section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPre, replacement)

	def post_edit(self, replacement):
		'''
		Edit post section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPost, replacement)

	def preun_edit(self, replacement):
		'''
		Edit preun section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPreun, replacement)

	def postun_edit(self, replacement):
		'''
		Edit postun section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPostun, replacement)

	def pretrans_edit(self, replacement):
		'''
		Edit pretrans section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPretrans, replacement)

	def posttrans_edit(self, replacement):
		'''
		Edit posttrans section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStPosttrans, replacement)

	def triggerin_edit(self, replacement):
		'''
		Edit triggerin section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStTriggerin, replacement)

	def triggerprein_edit(self, replacement):
		'''
		Edit triggerprein section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStTriggerin, replacement)

	def triggerun_edit(self, replacement):
		'''
		Edit triggerun section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStTriggerun, replacement)

	def triggerpostun_edit(self, replacement):
		'''
		Edit triggerpostun section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStTriggerpostun, replacement)

	def verifyscript_edit(self, replacement):
		'''
		Edit verifyscript section
		@param replacement: section replacement
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotFound: if section is not found
		@raise SpecNotImplemented: if multiple sections are found
		'''
		self.find_section_edit(SpecStVerifyscript, replacement)

###############################################################################

class SpecSectionEditor(object):
	'''
	Generic spec section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = [ SpecStBuild, SpecStCheck, SpecStClean, SpecStDescription, SpecStFiles, SpecStInstall,
				SpecStPrep, SpecStPre, SpecStPost, SpecStPreun, SpecStPostun, SpecStPretrans,
				SpecStPosttrans, SpecStTrigger, SpecStTriggerin, SpecStTriggerprein, SpecStTriggerun,
				SpecStTriggerpostun, SpecStVerifyscript ]

	@classmethod
	def edit(cls, section, replacement):
		'''
		Edit a section
		@param section: section instance to be edited
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		new_tokens = SpecTokenList(replacement)
		section.set_tokens(new_tokens)

class SpecExpressionEditor(SpecSectionEditor):
	'''
	An expression editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStExpression

	@classmethod
	def edit(cls, replacement):
		'''
		Edit an expression
		@param replacement: a replacement to be used
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotImplemented: always, not implemented yet
		'''
		raise SpecNotImplemented("Editing expression not implemented")

class SpecIfEditor(SpecSectionEditor):
	'''
	'%if' editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStIf

	@classmethod
	def edit(cls, replacement):
		'''
		Edit an if statement
		@param replacement: a replacement to be used
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotImplemented: always, not implemented yet
		'''
		raise SpecNotImplemented("Editing %if not implemented")

class SpecDefinitionEditor(SpecSectionEditor):
	'''
	Definition section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStDefinition

	@classmethod
	def create(cls, parent, name, value):
		'''
		Create a definition
		@param parent: parent section
		@type parent: L{SpecSection}
		@param name: name of the definition
		@type name: string
		@param value: value of the definition
		@type value: string
		@return: newly created definition
		@rtype: L{SpecStDefinition}
		'''
		ret = SpecDefinitionEditor.obj(parent)
		ret.set_name(SpecToken.create(name))
		ret.set_value(SpecToken.create(value, append="\n"))
		return ret

class SpecGlobalEditor(SpecSectionEditor):
	'''
	'%global' editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStGlobal

	@classmethod
	def edit(cls, replacement):
		'''
		Edit a '%global' statement
		@param replacement: a replacement to be used
		@type replacement: string
		@return: None
		@rtype: None
		@raise SpecNotImplemented: always, not implemented yet
		'''
		raise SpecNotImplemented("Editing %global not implemented")

class SpecBuildEditor(SpecSectionEditor):
	'''
	Build section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStBuild

class SpecChangelogEditor(SpecSectionEditor):
	'''
	Changelog section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = [SpecStChangelog, SpecStChangelog.SpecStChangelogEntry]

	@classmethod
	def add_entry(cls, changelog, date, username, email, version, msg):
		'''
		Add a changelog entry to provided changelog
		@param changelog: a changelog section to be used
		@type changelog: L{SpecStChangelog}
		@param date: date used in entry
		@type date: datetime
		@param username: user name
		@type username: string
		@param email: email
		@type email: string
		@param version: version, if None, last version is used
		@type version: string
		@param msg: a message to be placed to the changelog entry
		@type msg: string
		@return: newly added entry
		@rtype: L{SpecStChangelogEntry}
		'''
		entry = SpecChangelogEditor.obj.SpecStChangelogEntry(changelog)
		entry.set_star(SpecToken.create('*'))
		entry.set_date(SpecToken.create(date.strftime("%a %b %d %Y")))
		entry.set_date_parsed(date)
		entry.set_user(SpecToken.create(username))
		entry.set_user_email(SpecToken.create('<' + email + '>'))
		entry.set_version_delim(SpecToken.create('-'))
		if version is None:
			entry.set_version(changelog.get_entries()[0].get_version())
		else:
			entry.set_version(SpecToken.create(version, append = '\n'))
		entry.set_message(SpecToken.create(msg, append = '\n'))
		changelog.insert_entry(entry)

		return entry

class SpecCheckEditor(SpecSectionEditor):
	'''
	Check section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStCheck

class SpecCleanEditor(SpecSectionEditor):
	'''
	Clean section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStClean

class SpecDescriptionEditor(SpecSectionEditor):
	'''
	Description section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStDescription

class SpecFilesEditor(SpecSectionEditor):
	'''
	Files section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStFiles

class SpecInstallEditor(SpecSectionEditor):
	'''
	Install section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStInstall

class SpecPackageEditor(SpecSectionEditor):
	'''
	Package section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPackage

	@classmethod
	def create(cls, parent, pkg = None):
		'''
		Create a package section
		@param parent: parent section
		@type parent: L{SpecSection}
		@param pkg: package name, None or '-' if main package
		@type pkg: string
		@return: newly created package section
		@rtype: L{SpecStPackage}
		'''
		ret = SpecStPackage(parent)
		pkg = None if pkg == None or pkg == '-' else pkg
		if pkg is not None:
			ret.set_package(SpecToken().create(pkg, append = '\n'))
		ret.set_token_section(SpecToken().create('%package', append = '\n' if pkg is None else ' '))
		return ret

	@classmethod
	def add_definition(cls, pkg, definition):
		'''
		Add a definition to the package
		@param pkg: package to add section to
		@type pkg: L{SpecStPackage}
		@return: None
		@rtype: None
		'''
		# TODO: based on alphabet?
		pkg.defs_append(definition)

class SpecPrepEditor(SpecSectionEditor):
	'''
	Prep section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPrep

class SpecPreEditor(SpecSectionEditor):
	'''
	Pre section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPre

class SpecPostEditor(SpecSectionEditor):
	'''
	Post spec section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPost

class SpecPreunEditor(SpecSectionEditor):
	'''
	Preun section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPreun

class SpecPostunEditor(SpecSectionEditor):
	'''
	Postun section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPostun

class SpecPretransEditor(SpecSectionEditor):
	'''
	Pretrans section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPretrans

class SpecPosttransEditor(SpecSectionEditor):
	'''
	Posttrans section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStPosttrans

class SpecTriggerEditor(SpecSectionEditor):
	'''
	Trigger section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStTrigger

class SpecTriggerinEditor(SpecSectionEditor):
	'''
	Triggerin section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinEditor(SpecSectionEditor):
	'''
	Triggerprein section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStTriggerprein

class SpecTriggerunEditor(SpecSectionEditor):
	'''
	Triggerun section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunEditor(SpecSectionEditor):
	'''
	Triggerpostun section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptEditor(SpecSectionEditor):
	'''
	Verifyscript section editor
	@cvar obj: sections that could be edited with this editor
	'''
	obj = SpecStVerifyscript

