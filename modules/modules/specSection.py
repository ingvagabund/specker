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

import re
from specSectionMeta import *

class SpecSection(object):
	__metaclass__ = SpecSectionMeta

	def __init__(self, parent = None):
		self.parent = parent
		self.tokens = []

	def getParent(self):
		return self.parent

class SpecStIf(SpecSection):
	__metaclass__ = SpecStIfMeta

	def __init__(self, parent):
		self.parent = parent
		self.if_token = None
		self.expr = None
		self.true_branch = None
		self.else_token = None
		self.false_branch = []
		self.endif_token = None

	def setIfToken(self, token):
		self.if_token = token

	def setExpr(self, expr):
		self.expr = expr

	def setTrueBranch(self, branch):
		self.true_branch = branch

	def setElseToken(self, els):
		self.else_token = els

	def setFalseBranch(self, branch):
		self.false_branch = branch

	def setEndifToken(self, endi):
		self.endif_token = endi

	def getIfToken(self):
		return self.if_token

	def getExpr(self):
		return self.expr

	def getTrueBranch(self):
		return self.true_branch

	def getElseToken(self):
		return self.else_token

	def getFalseBranch(self):
		return self.false_branch

	def getEndifToken(self):
		return self.endif_token

class SpecStDefinition(SpecSection):
	__metaclass__ = SpecStDefinitionMeta

	def __init__(self, parent):
		self.parent = parent
		self.name = None
		self.value = None

	def setName(self, name):
		self.name = name

	def setValue(self, val):
		self.value = val

	def getName(self):
		return self.name

	def getValue(self):
		return self.value

	def getPackage(self):
		parent = self.parent
		while parent != None:
			if issubclass(parent.__class__, SpecStPackage):
				return parent
			parent = self.parent

		return None

class SpecStGlobal(SpecSection):
	__metaclass__ = SpecStGlobalMeta

	def __init__(self, parent):
		self.parent = parent
		self.global_token = None
		self.variable = None
		self.value = None

	def setGlobalToken(self, glb):
		self.global_token = glb

	def setVariable(self, var):
		self.variable = var

	def setValue(self, val):
		self.value = val

	def getGlobalToken(self):
		return self.global_token

	def getVariable(self):
		return self.variable

	def getValue(self):
		return self.value

class SpecStEof(SpecSection):
	__metaclass__ = SpecStEofMeta

	def __init__(self, parent = None):
		self.parent = None
		self.eof_token = None

	def setEofToken(self, eof):
		self.eof_token = eof

	def getEofToken(self):
		return self.eof_token

class SpecStExpression(SpecSection):
	__metaclass__ = SpecStExpressionMeta

	def __init__(self, parent):
		self.parent = parent
		self.tokens = None

	def setTokens(self, tkns):
		self.tokens = tkns

	def getTokens(self):
		return self.tokens

class SpecStSection(SpecSection):
	__metaclass__ = SpecStSectionMeta

	def __init__(self, parent):
		self.parent = parent
		self.token_section = None
		self.tokens = []

	def setTokenSection(self, tkn):
		self.token_section = tkn

	def setTokens(self, tkns):
		self.tokens = tkns

	def getTokenSection(self):
		return self.token_section

	def getTokens(self):
		return self.tokens

class SpecStDescription(SpecStSection):
	__metaclass__ = SpecStDescriptionMeta

class SpecStBuild(SpecStSection):
	__metaclass__ = SpecStBuildMeta

class SpecStChangelog(SpecStSection):
	class SpecStChangelogEntry(SpecStSection):
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

		def setStar(self, star):
			self.star = star

		def setDate(self, date):
			self.date = date

		def setDateParsed(self, date_parsed):
			self.date_parsed = date_parsed

		def setUser(self, user):
			self.user = user

		def setUserEmail(self, user_email):
			self.user_email = user_email

		def setVersionDelim(self, version_delim):
			self.version_delim = version_delim

		def setVersion(self, version):
			self.version = version

		def setMessage(self, message):
			self.message = message

		def getStar(self):
			return self.star

		def getDate(self):
			return self.date

		def getDateParsed(self):
			return self.date_parsed

		def getUser(self):
			return self.user

		def getUserEmail(self):
			return self.user_email

		def getVersionDelim(self):
			return self.version_delim

		def getVersion(self):
			return self.version

		def getMessage(self):
			return self.message

	__metaclass__ = SpecStChangelogMeta

	def __init__(self, parent):
		self.parent = parent
		self.token_section = None
		self.entries = []

	def setEntries(self, entries):
		self.entries = entries

	def setTokenSection(self, tkn):
		self.token_section = tkn

	def getTokenSection(self):
		return self.token_section

	def getEntries(self):
		return self.entries

	def appendEntry(self, entry):
		self.entries.append(entry)

	def insertEntry(self, entry):
		self.entries.insert(0, entry)

class SpecStCheck(SpecStSection):
	__metaclass__ = SpecStCheckMeta

class SpecStClean(SpecStSection):
	__metaclass__ = SpecStCleanMeta

class SpecStFiles(SpecStSection):
	__metaclass__ = SpecStFilesMeta

class SpecStInstall(SpecStSection):
	__metaclass__ = SpecStInstallMeta

class SpecStPackage(SpecStSection):
	__metaclass__ = SpecStPackageMeta

	def __init__(self, parent):
		self.parent = parent
		self.pkg = None
		self.defs = []
		self.token_section = None

	def setDefs(self, defs):
		self.defs = defs

	def setPackage(self, pkg):
		self.pkg = pkg

	def getPackage(self):
		return self.pkg

	def getDefs(self):
		return self.defs

	def defsAppend(self, item):
		return self.defs.append(item)

class SpecStPrep(SpecStSection):
	__metaclass__ = SpecStPrepMeta

class SpecStPre(SpecStSection):
	__metaclass__ = SpecStPreMeta

class SpecStPost(SpecStSection):
	__metaclass__ = SpecStPostMeta

class SpecStPreun(SpecStSection):
	__metaclass__ = SpecStPreunMeta

class SpecStPostun(SpecStSection):
	__metaclass__ = SpecStPostunMeta

class SpecStPretrans(SpecStSection):
	__metaclass__ = SpecStPretransMeta

class SpecStPosttrans(SpecStSection):
	__metaclass__ = SpecStPosttransMeta

class SpecStTrigger(SpecStSection):
	__metaclass__ = SpecStTriggerMeta

class SpecStTriggerin(SpecStSection):
	__metaclass__ = SpecStTriggerinMeta

class SpecStTriggerprein(SpecStSection):
	__metaclass__ = SpecStTriggerpreinMeta

class SpecStTriggerun(SpecStSection):
	__metaclass__ = SpecStTriggerunMeta

class SpecStTriggerpostun(SpecStSection):
	__metaclass__ = SpecStTriggerpostunMeta

class SpecStVerifyscript(SpecStSection):
	__metaclass__ = SpecStVerifyscriptMeta

