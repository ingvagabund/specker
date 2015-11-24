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
specker-lib - spec file parser
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import re
import copy
import datetime
import functools
import sys
from specSection import *
from specToken import SpecTokenList
from specModel import SpecModel
from specManipulator import SpecManipulator
from specDebug import SpecDebug
from specError import SpecBadToken, SpecBadIf


class SpecParser(SpecManipulator):
	'''
	TODO
	'''
	def __init__(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.PARSERS = [
				SpecIfParser,
				SpecDefinitionParser,
				SpecGlobalParser,
				SpecBuildParser,
				SpecChangelogParser,
				SpecCheckParser,
				SpecCleanParser,
				SpecDescriptionParser,
				SpecFilesParser,
				SpecInstallParser,
				SpecPackageParser,
				SpecPrepParser,
				SpecPreParser,
				SpecPostParser,
				SpecPreunParser,
				SpecPostunParser,
				SpecPretransParser,
				SpecPosttransParser,
				SpecTriggerParser,
				SpecTriggerinParser,
				SpecTriggerpreinParser,
				SpecTriggerunParser,
				SpecTriggerpostunParser,
				SpecVerifyscriptParser
			]

		self.model = None
		self.token_list = None

	def register(self, parser):
		'''
		TODO
		@type parser: TODO
		@param parser: TODO
		@rtype: TODO
		@return: TODO
		@raises SpecNotFound: TODO
		'''
		# TODO: move to SpecManipulator
		found = False
		for idx, item in enumerate(self.PARSERS):
			if issubclass(parser, item):
				found = True
				self.PARSERS[idx] = parser

		if not found:
			raise SpecNotFound("Invalid parser '%s' registration" % parser.__name__)

	def init(self, f):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.token_list = SpecTokenList(f)

	@staticmethod
	def sectionBeginingCallback(obj, token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return obj.sectionBegining(token_list)

	def sectionBegining(self, token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for parser in self.PARSERS:
			ret = parser.sectionBegining(token_list)
			if ret is not None:
				return ret

		return None # Not found

	def parse_loop(self, token_list, parent, allowed):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = []

		found = True
		while found:
			found = False
			token = token_list.touch()
			SpecDebug.logger.debug("- parsing round: '%s'" % str(token))

			if token.isEOF():
				break

			for t in allowed:
				section = t.parse(token_list, parent, allowed, self)
				if section:
					found = True
					SpecDebug.logger.debug("- adding parsed section '%s' (preamble)" % type(section))
					ret.append(section)
					break

			if not found:
				SpecDebug.logger.debug("- unparsed token '%s' on line %s" % (str(token), str(token.line)))

		return ret

	def parse_preamble(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		allowed = [ SpecIfParser, SpecDefinitionParser, SpecGlobalParser ]

		ret = self.parse_loop(self.token_list, None, allowed)
		unparsed = self.token_list.touch()
		SpecDebug.logger.debug("-- preamble finished with token '%s' on line %d" % (str(unparsed), unparsed.line))
		return ret

	def parse_loop_section(self, parent):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = []
		allowed = copy.deepcopy(self.PARSERS)

		found = True
		while found:
			found = False
			token = self.token_list.touch()

			SpecDebug.logger.debug("-- parsing section '%s' " % str(token))

			if token.isEOF():
				break

			for t in allowed:
				section = t.parse(self.token_list, parent, allowed, self)
				if section:
					found = True
					SpecDebug.logger.debug("- adding parsed section '%s'" % type(section))
					ret.append(section)
					c = section.__class__
					if not issubclass(c, SpecStIf) and not issubclass(c, SpecStGlobal) and not \
							issubclass(c, SpecStDescription) and not issubclass(c, SpecStFiles):
						SpecDebug.logger.debug("-- removing " + str(token) + " from allowed")
						if section in allowed:
							allowed.remove(section)
					break

		SpecDebug.logger.debug("-- unparsed beginning of a section: " + str(token))

		return ret

	def parse(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.model = SpecModel()

		self.model.append_items(self.parse_preamble())
		self.model.append_items(self.parse_loop_section(None))

		eof = self.token_list.touch()
		if not eof.isEOF():
			raise SpecBadToken("Unexpected symbol '" + str(eof.token) + "' on line " + str(eof.line))

class SpecSectionParser(object):
	'''
	TODO
	'''
	obj = [ SpecStBuild, SpecStCheck, SpecStClean, SpecStDescription, SpecStFiles, SpecStInstall,
				SpecStPrep, SpecStPre, SpecStPost, SpecStPreun, SpecStPostun, SpecStPretrans,
				SpecStPosttrans, SpecStTrigger, SpecStTriggerin, SpecStTriggerprein, SpecStTriggerun,
				SpecStTriggerpostun, SpecStVerifyscript ]

	def __init__(self):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		raise ValueError("Cannot instantiate")

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()

		for o in SpecSectionParser.obj:
			if str(token) == str(o):
				return o

		return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		section = cls.sectionBegining(token_list)
		if not section: # section not found
			return None

		ret = section(parent)
		ret.setTokenSection(token_list.get())
		#could be empty
		ret.setTokens(token_list.getWhileNot(functools.partial(ctx.sectionBeginingCallback, ctx)))

		return ret

class SpecExpressionParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStExpression

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		raise ValueError("Spec expression has no beginning")

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		ret = SpecExpressionParser.obj(parent)

		tokens = SpecTokenList()
		tkn = token_list.get()
		tokens.tokenListAppend(tkn)
		while tkn.sameLine(token_list.touch()):
			tkn = token_list.get()
			tokens.tokenListAppend(tkn)

		ret.setTokens(tokens)
		return ret

class SpecIfParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStIf

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()
		if str(token) == '%if' or str(token) == '%ifarch':
			return SpecIfParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not cls.sectionBegining(token_list):
			return None

		pointer = token_list.getPointer()

		stif = SpecIfParser.obj(parent)
		stif.setIfToken(token_list.get())
		stif.setExpr(SpecExpressionParser.parse(token_list, parent, allowed, ctx))
		stif.setTrueBranch(ctx.parse_loop(token_list, stif, allowed))
		token = token_list.touch()
		if str(token) == '%else':
			stif.setElseToken(token_list.get())
			stif.setFalseBranch(ctx.parse_loop(token_list, stif, allowed))
			token = token_list.touch()

		if str(token) != '%endif':
			token_list.setPointer(pointer)
			raise ValueError("Unexpected token '%s' on line '%s', expected 'endif'"
					% (str(token), str(token.getLine())))

		stif.setEndifToken(token_list.get())
		return stif

class SpecDefinitionParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStDefinition

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()

		if str(token) in [ 'Name:', 'Version:', 'Release:', 'Summary:', 'License:',
				'URL:', 'ExclusiveArch:', 'BuildRequires:', 'Provides:', 'Requires:',
				'Source:', 'BuildArch:']:
			return SpecDefinitionParser.obj

		p = re.compile('BuildRequires(.*):') # This could be adjusted later on
		if p.match(str(token)):
			return SpecDefinitionParser.obj

		p = re.compile('Requires(.*):') # This could be adjusted later on
		if p.match(str(token)):
			return SpecDefinitionParser.obj

		p = re.compile('Provides(.*):') # This could be adjusted later on
		if p.match(str(token)):
			return SpecDefinitionParser.obj

		p = re.compile('Source[0-9]+:')
		if p.match(str(token)):
				return SpecDefinitionParser.obj

		return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not cls.sectionBegining(token_list):
			return None

		ret = SpecDefinitionParser.obj(parent)
		ret.setName(token_list.get())
		ret.setValue(token_list.getLine())
		if ret.getValue().isEOF():
			raise ValueError("Expected definition value, got '%s'" % str(ret.getValue()))

		return ret

class SpecGlobalParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStGlobal

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()
		if str(token) == str(SpecGlobalParser.obj):
			return SpecGlobalParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not cls.sectionBegining(token_list):
			return None

		ret = SpecGlobalParser.obj(parent)
		ret.setGlobalToken(token_list.get())
		ret.setVariable(token_list.get())
		if ret.getVariable().isEOF():
			raise ValueError("Expected variable, got '%s'" % str(ret.getVariable()))

		ret.setValue(SpecExpressionParser.parse(token_list, ret, allowed, ctx))
		return ret

class SpecBuildParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStBuild

class SpecChangelogParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStChangelog

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()
		if str(token) == str(SpecChangelogParser.obj):
			return SpecChangelogParser.obj

		return None

	@classmethod
	def parseEntry(cls, token_list, parent, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		def parse_date(date):
			s = str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + ' ' + str(date[3])
			return datetime.datetime.strptime(s, '%a %b %d %Y')

		def changelogEntryBeginningCallback(obj, token_list):
			# is there some section?
			if obj.sectionBeginingCallback(obj, token_list):
				return True

			# or is there another changelog entry?
			return str(token_list.touch()) == '*'

		entry = SpecChangelogParser.obj.SpecStChangelogEntry(parent)

		star = token_list.get()
		if str(star) != '*':
			token_list.unget()
			raise SpecBadToken("Expected token '*', got '%s'" % star)
		entry.setStar(star)

		date = SpecTokenList()
		for _ in xrange(0, 4):
			date.tokenListAppend(token_list.get())
		entry.setDate(date)

		date_parsed = parse_date(date)
		entry.setDateParsed(date_parsed)

		user = SpecTokenList()
		while not str(token_list.touch()).startswith('<'):
			user.tokenListAppend(token_list.get())
		entry.setUser(user)

		user_email = token_list.get()
		entry.setUserEmail(user_email)

		version_delim = token_list.get()
		if str(version_delim) != '-':
			token_list.unget()
			raise SpecBadToken("Expected token '-', got '%s'" % self.star)
		entry.setVersionDelim(version_delim)

		version = token_list.get()
		entry.setVersion(version)

		entry.setMessage(token_list.getWhileNot(functools.partial(changelogEntryBeginningCallback, ctx)))

		return entry

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not cls.sectionBegining(token_list):
			return None

		ret = SpecChangelogParser.obj(parent)
		ret.setTokenSection(token_list.get())

		while str(token_list.touch()) == '*':
			entry = cls.parseEntry(token_list, ret, ctx)
			if entry:
				ret.appendEntry(entry)

		return ret

class SpecCheckParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStCheck

class SpecCleanParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStClean

class SpecDescriptionParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStDescription

class SpecFilesParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStFiles

class SpecInstallParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStInstall

class SpecPackageParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPackage

	@staticmethod
	def sectionBegining(token_list):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		token = token_list.touch()

		if str(token) == str(SpecPackageParser.obj):
			return SpecPackageParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		if not cls.sectionBegining(token_list):
			return None

		section = SpecPackageParser.obj(parent)
		section.setTokenSection(token_list.get())
		if section.getTokenSection().sameLine(token_list.touch()):
			section.setPackage(token_list.get())
		section.setDefs(ctx.parse_loop(token_list, section, [SpecIfParser, SpecDefinitionParser]))

		return section

class SpecPrepParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPrep

class SpecPreParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPre

class SpecPostParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPost

class SpecPreunParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPreun

class SpecPostunParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPostun

class SpecPretransParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPretrans

class SpecPosttransParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStPosttrans

class SpecTriggerParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStTrigger

class SpecTriggerinParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStTriggerprein

class SpecTriggerunParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptParser(SpecSectionParser):
	'''
	TODO
	'''
	obj = SpecStVerifyscript

