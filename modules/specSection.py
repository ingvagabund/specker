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
Basic L{SpecSection} and derived classes representing a section
in a specfile
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import re
from specSectionMeta import *

class SpecSection(object):
	'''
	A generic spec section
	'''
	__metaclass__ = SpecSectionMeta

	def __init__(self, parent = None):
		self.parent = parent
		self.tokens = []

	def get_parent(self):
		'''
		Get parent section
		@return: parent section
		@rtype: L{SpecSection}
		'''
		return self.parent

	def set_parent(self, parent):
		'''
		Set parent section
		@param parent: parent section
		@type parent: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.parent = parent

class SpecStIf(SpecSection):
	'''
	%if section/statement representation
	'''
	__metaclass__ = SpecStIfMeta

	def __init__(self, parent):
		self.parent = parent
		self.if_token = None
		self.expr = None
		self.true_branch = None
		self.else_token = None
		self.false_branch = []
		self.endif_token = None

	def set_if_token(self, token):
		'''
		Set %if token
		@param token: token to be set
		@type token: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.if_token = token

	def set_expr(self, expr):
		'''
		Set expression of if statement
		@param expr: expression to be set
		@type expr: L{SpecStExpression}
		@return: None
		@rtype: None
		'''
		self.expr = expr

	def set_true_branch(self, branch):
		'''
		Set true branch of %if
		@param branch: list of sections
		@type branch: list of L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.true_branch = branch

	def set_else_token(self, els):
		'''
		Set %else token
		@param els: token to be set
		@type els: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.else_token = els

	def set_false_branch(self, branch):
		'''
		Set false branch of %if
		@param branch: list of sections
		@type branch: list of L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.false_branch = branch

	def set_endif_token(self, endi):
		'''
		Set %endif token
		@param endi: token to be set
		@type endi: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.endif_token = endi

	def get_if_token(self):
		'''
		Get %if token
		@return: %if token
		@rtype: L{SpecToken}
		'''
		return self.if_token

	def get_expr(self):
		'''
		Get expression of %if
		@return: expression
		@rtype: L{SpecStExpression}
		'''
		return self.expr

	def get_true_branch(self):
		'''
		Get true branch
		@return: true branch
		@rtype: list of L{SpecSection}
		'''
		return self.true_branch

	def get_else_token(self):
		'''
		Get %else token
		@return: else token
		@rtype: L{SpecToken}
		'''
		return self.else_token

	def get_false_branch(self):
		'''
		Get false branch
		@return: false branch
		@rtype: list of L{SpecSection}
		'''
		return self.false_branch

	def get_endif_token(self):
		'''
		Get %endif token
		@return: endif token
		@rtype: L{SpecToken}
		'''
		return self.endif_token

class SpecStDefinition(SpecSection):
	'''
	Definition representation
	'''
	__metaclass__ = SpecStDefinitionMeta

	def __init__(self, parent):
		self.parent = parent
		self.name = None
		self.value = None

	def set_name(self, name):
		'''
		Set definition name
		@param name: definition name
		@type name: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.name = name

	def set_value(self, val):
		'''
		Set value of the definition
		@param val: definition value
		@type val: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.value = val

	def get_name(self):
		'''
		Get definition name
		@return: definition name
		@rtype: L{SpecToken}
		'''
		return self.name

	def get_value(self):
		'''
		Get definition value
		@return: definition value
		@rtype: list of L{SpecToken}
		'''
		return self.value

	def get_package(self):
		'''
		Get package referred by definition
		@return: referred package
		@rtype: L{SpecStPackage}
		'''
		parent = self.parent
		while parent != None:
			if issubclass(parent.__class__, SpecStPackage):
				return parent
			parent = self.parent

		return None

class SpecStGlobal(SpecSection):
	'''
	%global representation
	'''
	__metaclass__ = SpecStGlobalMeta

	def __init__(self, parent):
		self.parent = parent
		self.global_token = None
		self.variable = None
		self.value = None

	def set_global_token(self, glb):
		'''
		Set %global token
		@param glb: global token
		@type glb: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.global_token = glb

	def set_variable(self, var):
		'''
		Set global variable
		@param var: global variable
		@type var: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.variable = var

	def set_value(self, val):
		'''
		Set global value
		@param val: gloabl value
		@type val: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.value = val

	def get_global_token(self):
		'''
		Get global token
		@return: global token
		@rtype: L{SpecToken}
		'''
		return self.global_token

	def get_variable(self):
		'''
		Get global variable
		@return: global variable
		@rtype: L{SpecToken}
		'''
		return self.variable

	def get_value(self):
		'''
		Get global value
		@return: global value
		@rtype: list of L{SpecToken}
		'''
		return self.value

class SpecStDefine(SpecSection):
	'''
	%define representation
	'''
	__metaclass__ = SpecStDefineMeta

	def __init__(self, parent):
		self.parent = parent
		self.define_token = None
		self.variable = None
		self.value = None

	def set_define_token(self, dfn):
		'''
		Set %define token
		@param dfn: global token
		@type dfn: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.define_token = dfn

	def set_variable(self, var):
		'''
		Set define variable
		@param var: define variable
		@type var: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.variable = var

	def set_value(self, val):
		'''
		Set define value
		@param val: gloabl value
		@type val: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.value = val

	def get_define_token(self):
		'''
		Get define token
		@return: define token
		@rtype: L{SpecToken}
		'''
		return self.define_token

	def get_variable(self):
		'''
		Get define variable
		@return: define variable
		@rtype: L{SpecToken}
		'''
		return self.variable

	def get_value(self):
		'''
		Get define value
		@return: define value
		@rtype: list of L{SpecToken}
		'''
		return self.value

class SpecStEof(SpecSection):
	'''
	EOF representation
	@note: EOF token has to be stored, because of 1:1 reconstruction of a spec
	file. EOF token can store prepend part; it is also used as a mark
	'''
	__metaclass__ = SpecStEofMeta

	def __init__(self, parent = None):
		self.parent = None
		self.eof_token = None

	def set_eof_token(self, eof):
		'''
		Set EOF token
		@param eof: EOF token
		@type eof: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.eof_token = eof

	def get_eof_token(self):
		'''
		Get EOF token
		@return: EOF token
		@rtype: L{SpecToken}
		'''
		return self.eof_token

class SpecStExpression(SpecSection):
	'''
	An expression representation
	'''
	__metaclass__ = SpecStExpressionMeta

	def __init__(self, parent):
		self.parent = parent
		self.tokens = None

	def set_tokens(self, tkns):
		'''
		Set tokens of an expression
		@param tkns: expression tokens
		@type tkns: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.tokens = tkns

	def get_tokens(self):
		'''
		Get expression tokens
		@return: expression tokens
		@rtype: list of L{SpecToken}
		'''
		return self.tokens

class SpecStSection(SpecSection):
	'''
	Generic representation of a multi-line ("block") section
	'''
	__metaclass__ = SpecStSectionMeta

	def __init__(self, parent):
		self.parent = parent
		self.token_section = None
		self.tokens = []

	def set_token_section(self, tkn):
		'''
		Set section token - e.g. '%build'
		@param tkn: section token
		@type tkn: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.token_section = tkn

	def set_tokens(self, tkns):
		'''
		Set section tokens
		@param tkns: section tokens
		@type tkns: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.tokens = tkns

	def get_token_section(self):
		'''
		Get section token
		@return: section token, e.g. '%build'
		@rtype: L{SpecToken}
		'''
		return self.token_section

	def get_tokens(self):
		'''
		Get section tokens
		@return: section tokens
		@rtype: list of L{SpecToken}
		'''
		return self.tokens

class SpecStDescription(SpecStSection):
	'''
	Description section representation
	'''
	__metaclass__ = SpecStDescriptionMeta

class SpecStBuild(SpecStSection):
	'''
	Build section representation
	'''
	__metaclass__ = SpecStBuildMeta

class SpecStChangelog(SpecStSection):
	'''
	Changelog section representation
	'''
	class SpecStChangelogEntry(SpecStSection):
		'''
		Changelog entry representation
		'''
		__metaclass__ = SpecStChangelogEntryMeta

		def __init__(self, parent):
			self.parent = parent
			self.star = None
			self.date = None
			self.date_parsed = None
			self.user = None
			self.user_email = None
			self.version_delim = None
			self.version = None
			self.message = None

		def set_star(self, star):
			'''
			Set star token, e.g. '*'
			@param star: star token
			@type star: L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.star = star

		def set_date(self, date):
			'''
			Set date tokens
			@param date: date tokens, e.g. ['Wed', 'Nov', '25', '2015']
			@type date: list of L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.date = date

		def set_date_parsed(self, date_parsed):
			'''
			Set parsed date
			@param date_parsed: parsed date
			@type date_parsed: datetime
			@return: None
			@rtype: None
			'''
			self.date_parsed = date_parsed

		def set_user(self, user):
			'''
			Set user token
			@param user: user token
			@type user: L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.user = user

		def set_user_email(self, user_email):
			'''
			Set user email
			@param user_email: user email
			@type user_email: L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.user_email = user_email

		def set_version_delim(self, version_delim):
			'''
			Set version delimiter
			@param version_delim: version delimiter, e.g. '-'
			@type version_delim: L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.version_delim = version_delim

		def set_version(self, version):
			'''
			Set version token
			@param version: version token
			@type version: L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.version = version

		def set_message(self, message):
			'''
			Set changelog message
			@param message: changelog message
			@type message: list of L{SpecToken}
			@return: None
			@rtype: None
			'''
			self.message = message

		def get_star(self):
			'''
			Get star token
			@return: star token
			@rtype: L{SpecToken}
			'''
			return self.star

		def get_date(self):
			'''
			Get date tokens
			@return: date tokens
			@rtype: list of L{SpecToken}
			'''
			return self.date

		def get_date_parsed(self):
			'''
			Get parsed date
			@return: parsed date
			@rtype: datetime
			'''
			return self.date_parsed

		def get_user(self):
			'''
			Get user token
			@return: user token
			@rtype: L{SpecToken}
			'''
			return self.user

		def get_user_email(self):
			'''
			Get user email token
			@return: user email token
			@rtype: L{SpecToken}
			'''
			return self.user_email

		def get_version_delim(self):
			'''
			Get version delimiter ('-')
			@return: version delimiter
			@rtype: L{SpecToken}
			'''
			return self.version_delim

		def get_version(self):
			'''
			Get version token
			@return: version token
			@rtype: L{SpecToken}
			'''
			return self.version

		def get_message(self):
			'''
			Get changelog entry message
			@return: changelog entry message
			@rtype: list of L{SpecToken}
			'''
			return self.message

	__metaclass__ = SpecStChangelogMeta

	def __init__(self, parent):
		self.parent = parent
		self.token_section = None
		self.entries = []

	def set_entries(self, entries):
		'''
		Set changelog entries
		@param entries: changelog entries
		@type entries: list of L{SpecStChangelogEntry}
		@return: None
		@rtype: None
		'''
		self.entries = entries

	def get_entries(self):
		'''
		Get changelog entries
		@return: list of changelog entries
		@rtype: list of L{SpecStChangelogEntry}
		'''
		return self.entries

	def append_entry(self, entry):
		'''
		Append a changelog entry
		@param entry: changelog entry to be appended
		@type entry: L{SpecStChangelogEntry}
		'''
		self.entries.append(entry)

	def insert_entry(self, entry):
		'''
		Insert a changelog entry at the beginning
		@param entry: changelog entry to be inserted
		@type entry: L{SpecStChangelog.SpecStChangelogEntry}
		'''
		self.entries.insert(0, entry)

class SpecStCheck(SpecStSection):
	'''
	Check section representation
	'''
	__metaclass__ = SpecStCheckMeta

class SpecStClean(SpecStSection):
	'''
	Clean section representation
	'''
	__metaclass__ = SpecStCleanMeta

class SpecStFiles(SpecStSection):
	'''
	Files section representation
	'''
	__metaclass__ = SpecStFilesMeta

class SpecStInstall(SpecStSection):
	'''
	Install section representation
	'''
	__metaclass__ = SpecStInstallMeta

class SpecStPackage(SpecStSection):
	'''
	Package section representation
	'''
	__metaclass__ = SpecStPackageMeta

	def __init__(self, parent):
		self.parent = parent
		self.pkg = None
		self.defs = []
		self.token_section = None

	def set_defs(self, defs):
		'''
		Set package definitions
		@param defs: definitions to be set
		@type defs: list of L{SpecStDefinition}
		@return: None
		@rtype: None
		'''
		self.defs = defs

	def set_package(self, pkg):
		'''
		Set package token
		@param pkg: package token
		@type pkg: L{SpecToken}
		@return: None
		@rtype: None
		'''
		self.pkg = pkg

	def get_package(self):
		'''
		Get package token
		@return: package token
		@rtype: L{SpecToken}
		'''
		return self.pkg

	def get_defs(self):
		'''
		Get package definitions
		@return: package definitions
		@rtype: list of L{SpecStDefinition}
		'''
		return self.defs

	def defs_append(self, item):
		'''
		Append definition to package definitions
		@param item: definition to be appended
		@type item: L{SpecStDefinition}
		@return: None
		@rtype: None
		'''
		self.defs.append(item)

class SpecStPrep(SpecStSection):
	'''
	Prep section representation
	'''
	__metaclass__ = SpecStPrepMeta

class SpecStPre(SpecStSection):
	'''
	Pre section representation
	'''
	__metaclass__ = SpecStPreMeta

class SpecStPost(SpecStSection):
	'''
	Post section representation
	'''
	__metaclass__ = SpecStPostMeta

class SpecStPreun(SpecStSection):
	'''
	Preun section representation
	'''
	__metaclass__ = SpecStPreunMeta

class SpecStPostun(SpecStSection):
	'''
	Postun section representation
	'''
	__metaclass__ = SpecStPostunMeta

class SpecStPretrans(SpecStSection):
	'''
	Pretrans section representation
	'''
	__metaclass__ = SpecStPretransMeta

class SpecStPosttrans(SpecStSection):
	'''
	Posttrans section representation
	'''
	__metaclass__ = SpecStPosttransMeta

class SpecStTrigger(SpecStSection):
	'''
	Trigger section representation
	'''
	__metaclass__ = SpecStTriggerMeta

class SpecStTriggerin(SpecStSection):
	'''
	Triggerin section representation
	'''
	__metaclass__ = SpecStTriggerinMeta

class SpecStTriggerprein(SpecStSection):
	'''
	Triggerprein section representation
	'''
	__metaclass__ = SpecStTriggerpreinMeta

class SpecStTriggerun(SpecStSection):
	'''
	Triggerpreun section representation
	'''
	__metaclass__ = SpecStTriggerunMeta

class SpecStTriggerpostun(SpecStSection):
	'''
	Triggerpostun section representation
	'''
	__metaclass__ = SpecStTriggerpostunMeta

class SpecStVerifyscript(SpecStSection):
	'''
	Verifyscript section representation
	'''
	__metaclass__ = SpecStVerifyscriptMeta

