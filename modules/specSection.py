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

	'''
	Get parent section
	@return: parent section
	@rtype: L{SpecSection}
	'''
	def getParent(self):
		return self.parent

	'''
	Set parent section
	@param parent: parent section
	@type parent: L{SpecSection}
	@return: None
	@rtype: None
	'''
	def setParent(self, parent):
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

	'''
	Set %if token
	@param token: token to be set
	@type token: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setIfToken(self, token):
		self.if_token = token

	'''
	Set expression of if statement
	@param expr: expression to be set
	@type expr: L{SpecStExpression}
	@return: None
	@rtype: None
	'''
	def setExpr(self, expr):
		self.expr = expr

	'''
	Set true branch of %if
	@param branch: list of sections
	@type branch: list of L{SpecSection}
	@return: None
	@rtype: None
	'''
	def setTrueBranch(self, branch):
		self.true_branch = branch

	'''
	Set %else token
	@param els: token to be set
	@type els: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setElseToken(self, els):
		self.else_token = els

	'''
	Set false branch of %if
	@param branch: list of sections
	@type branch: list of L{SpecSection}
	@return: None
	@rtype: None
	'''
	def setFalseBranch(self, branch):
		self.false_branch = branch

	'''
	Set %endif token
	@param token: token to be set
	@type token: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setEndifToken(self, endi):
		self.endif_token = endi

	'''
	Get %if token
	@return: %if token
	@rtype: L{SpecToken}
	'''
	def getIfToken(self):
		return self.if_token

	'''
	Get expression of %if
	@return: expression
	@rtype: L{SpecExpression}
	'''
	def getExpr(self):
		return self.expr

	'''
	Get true branch
	@return: true branch
	@rtype: list of L{SpecSection}
	'''
	def getTrueBranch(self):
		return self.true_branch

	'''
	Get %else token
	@return: else token
	@rtype: L{SpecToken}
	'''
	def getElseToken(self):
		return self.else_token

	'''
	Get false branch
	@return: false branch
	@rtype: list of L{SpecSection}
	'''
	def getFalseBranch(self):
		return self.false_branch

	'''
	Get %endif token
	@return: endif token
	@rtype: L{SpecToken}
	'''
	def getEndifToken(self):
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

	'''
	Set definition name
	@param name: definition name
	@type name: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setName(self, name):
		self.name = name

	'''
	Set value of the definition
	@param val: definition value
	@type val: list of L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setValue(self, val):
		self.value = val

	'''
	Get definition name
	@return: definition name
	@rtype: L{SpecToken}
	'''
	def getName(self):
		return self.name

	'''
	Get definition value
	@return: definition value
	@rtype: list of L{SpecToken}
	'''
	def getValue(self):
		return self.value

	'''
	Get package referred by definition
	@return: referred package
	@rtype: L{SpecStPackage}
	'''
	def getPackage(self):
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

	'''
	Set %global token
	@param glb: global token
	@type glb: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setGlobalToken(self, glb):
		self.global_token = glb

	'''
	Set global variable
	@param var: global variable
	@type var: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setVariable(self, var):
		self.variable = var

	'''
	Set global value
	@param val: gloabl value
	@type val: list of L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setValue(self, val):
		self.value = val

	'''
	Get global token
	@return: global token
	@rtype: L{SpecToken}
	'''
	def getGlobalToken(self):
		return self.global_token

	'''
	Get global variable
	@return: global variable
	@rtype: L{SpecToken}
	'''
	def getVariable(self):
		return self.variable

	'''
	Get global value
	@return: global value
	@rtype: list of L{SpecToken}
	'''
	def getValue(self):
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

	'''
	Set EOF token
	@param eof: EOF token
	@type eof: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setEofToken(self, eof):
		self.eof_token = eof

	'''
	Get EOF token
	@return: EOF token
	@rtype: L{SpecToken}
	'''
	def getEofToken(self):
		return self.eof_token

class SpecStExpression(SpecSection):
	'''
	An expression representation
	'''
	__metaclass__ = SpecStExpressionMeta

	def __init__(self, parent):
		self.parent = parent
		self.tokens = None

	'''
	Set tokens of an expression
	@param tkns: expression tokens
	@type tkns: list of L{SpecTokens}
	@return: None
	@rtype: None
	'''
	def setTokens(self, tkns):
		self.tokens = tkns

	'''
	Get expression tokens
	@return: expression tokens
	@rtype: list of L{SpecToken}
	'''
	def getTokens(self):
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

	'''
	Set section token - e.g. '%build'
	@param tkn: section token
	@type tkn: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setTokenSection(self, tkn):
		self.token_section = tkn

	'''
	Set section tokens
	@param tkns: section tokens
	@type tkns: list of L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setTokens(self, tkns):
		self.tokens = tkns

	'''
	Get section token
	@return: section token, e.g. '%build'
	@rtype: L{SpecToken}
	'''
	def getTokenSection(self):
		return self.token_section

	'''
	Get section tokens
	@return: section tokens
	@rtype: list of L{SpecToken}
	'''
	def getTokens(self):
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

		'''
		Set star token, e.g. '*'
		@param star: star token
		@type star: L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setStar(self, star):
			self.star = star

		'''
		Set date tokens
		@param date: date tokens, e.g. ['Wed', 'Nov', '25', '2015'}
		@type date: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setDate(self, date):
			self.date = date

		'''
		Set parsed date
		@param date: parsed date
		@type date: datetime
		@return: None
		@rtype: None
		'''
		def setDateParsed(self, date_parsed):
			self.date_parsed = date_parsed

		'''
		Set user token
		@param user: user token
		@type user: L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setUser(self, user):
			self.user = user

		'''
		Set user email
		@param user_email: user email
		@type user_email: L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setUserEmail(self, user_email):
			self.user_email = user_email

		'''
		Set version delimiter
		@param version_delim: version delimiter, e.g. '-'
		@type version_delim: L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setVersionDelim(self, version_delim):
			self.version_delim = version_delim

		'''
		Set version token
		@param version: version token
		@type version: L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setVersion(self, version):
			self.version = version

		'''
		Set changelog message
		@param message: changelog message
		@type message: list of L{SpecToken}
		@return: None
		@rtype: None
		'''
		def setMessage(self, message):
			self.message = message

		'''
		Get star token
		@return: star token
		@rtype: L{SpecToken}
		'''
		def getStar(self):
			return self.star

		'''
		Get date tokens
		@return: date tokens
		@rtype: list of L{SpecToken}
		'''
		def getDate(self):
			return self.date

		'''
		Get parsed date
		@return: parsed date
		@rtype: datetime
		'''
		def getDateParsed(self):
			return self.date_parsed

		'''
		Get user token
		@return: user token
		@rtype: L{SpecToken}
		'''
		def getUser(self):
			return self.user

		'''
		Get user email token
		@return: user email token
		@rtype: L{SpecToken}
		'''
		def getUserEmail(self):
			return self.user_email

		'''
		Get version delimiter ('-')
		@return: version delimiter
		@rtype: L{SpecToken}
		'''
		def getVersionDelim(self):
			return self.version_delim

		'''
		Get version token
		@return: version token
		@rtype: L{SpecToken}
		'''
		def getVersion(self):
			return self.version

		'''
		Get changelog entry message
		@return: changelog entry message
		@rtype: list of L{SpecToken}
		'''
		def getMessage(self):
			return self.message

	__metaclass__ = SpecStChangelogMeta

	def __init__(self, parent):
		self.parent = parent
		self.token_section = None
		self.entries = []

	'''
	Set changelog entries
	@param entries: changelog entries
	@type entries: list of L{SpecStChangelogEntry}
	@return: None
	@rtype: None
	'''
	def setEntries(self, entries):
		self.entries = entries

	'''
	Get changelog entries
	@return: list of changelog entries
	@rtype: list of L{SpecStChangelogEntry}
	'''
	def getEntries(self):
		return self.entries

	'''
	Append a changelog entry
	@param entry: changelog entry to be appended
	@type entry: L{SpecStChangelogEntry}
	'''
	def appendEntry(self, entry):
		self.entries.append(entry)

	'''
	Insert a changelog entry at the beginning
	@param entry: changelog entry to be inserted
	@type entry: L{SpecChangelogEntry}
	'''
	def insertEntry(self, entry):
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

	'''
	Set package definitions
	@param defs: definitions to be set
	@type defs: list of L{SpecStDefinition}
	@return: None
	@rtype: None
	'''
	def setDefs(self, defs):
		self.defs = defs

	'''
	Set package token
	@param pkg: package token
	@type pkg: L{SpecToken}
	@return: None
	@rtype: None
	'''
	def setPackage(self, pkg):
		self.pkg = pkg

	'''
	Get package token
	@return: package token
	@rtype: L{SpecToken}
	'''
	def getPackage(self):
		return self.pkg

	'''
	Get package definitions
	@return: package definitions
	@rtype: list of L{SpecStDefinition}
	'''
	def getDefs(self):
		return self.defs

	'''
	Append definition to package definitions
	@param item: definition to be appended
	@type item: L{SpecStDefinition}
	@return: None
	@rtype: None
	'''
	def defsAppend(self, item):
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

