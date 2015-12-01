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
A spec file parser
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
	A spec parser
	'''
	def __init__(self):
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
		Register a spec parser
		@param parser: parser to be registered
		@type parser: L{SpecSectionParser}
		@rtype: None
		@return: None
		@raise SpecNotFound: if provided parser cannot be registered e.g. invalid parser
		@todo: move to SpecManipulator
		'''
		found = False
		for idx, item in enumerate(self.PARSERS):
			if issubclass(parser, item):
				found = True
				self.PARSERS[idx] = parser

		if not found:
			raise SpecNotFound("Invalid parser '%s' registration" % parser.__name__)

	def init(self, f):
		'''
		Init parser
		@param f: FILE or a string to init parser from
		@type f: FILE or a string
		@return: None
		@rtype: None
		'''
		self.token_list = SpecTokenList(f)

	@staticmethod
	def sectionBeginningCallback(obj, token_list):
		'''
		A callback for L{SpecTokenList} used to check whether next token is
		a section token
		@param obj: self instance
		@type obj: L{SpecParser} instance
		@param token_list: token list to be used
		@type token_list: L{SpecTokenList}
		@return: section parser to be used for parsing the upcoming section
		@rtype: L{SpecParser}
		'''
		return obj.sectionBegining(token_list)

	def sectionBegining(self, token_list):
		'''
		Check whether next token is a section token
		@param token_list: token list to be used
		@type token_list: L{SpecTokenList}
		@return: section parser to be used to parse the upcoming section
		@rtype: L{SpecParser}
		'''
		for parser in self.PARSERS:
			ret = parser.sectionBegining(token_list)
			if ret is not None:
				return ret

		return None # Not found

	def parse_loop(self, token_list, parent, allowed):
		'''
		Main parse loop to get list of parsed sections
		@param token_list: a list of tokens to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section
		@type parent: L{SpecSection}
		@param allowed: allowed sections to be parsed, section parsers
		@type allowed: list of L{SpecSectionParser}
		@return: list of parsed sections
		@rtype: L{SpecSection}
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
		Parse preamble of a spec file
		@return: parsed sections in preamble
		@rtype: list of L{SpecSection}
		'''
		allowed = [ SpecIfParser, SpecDefinitionParser, SpecGlobalParser ]

		ret = self.parse_loop(self.token_list, None, allowed)
		unparsed = self.token_list.touch()
		SpecDebug.logger.debug("-- preamble finished with token '%s' on line %d" % (str(unparsed), unparsed.line))
		return ret

	def parse_loop_section(self):
		'''
		Parse sections after preamble
		@return: list of parsed sections
		@rtype: list of L{SpecSection}
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
				section = t.parse(self.token_list, None, allowed, self)
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
		Main parser entry point - parse provided spec file
		@return: None
		@rtype:
		@raise SpecBadToken: when an unexpected token is reached
		'''
		self.model = SpecModel()

		self.model.append_items(self.parse_preamble())
		self.model.append_items(self.parse_loop_section())

		eof = self.token_list.touch()
		if not eof.isEOF():
			raise SpecBadToken("Unexpected symbol '" + str(eof.token) + "' on line " + str(eof.line))

class SpecSectionParser(object):
	'''
	Generic section parser
	@cvar obj: sections parsed by this parser
	'''
	obj = [ SpecStBuild, SpecStCheck, SpecStClean, SpecStDescription, SpecStFiles, SpecStInstall,
				SpecStPrep, SpecStPre, SpecStPost, SpecStPreun, SpecStPostun, SpecStPretrans,
				SpecStPosttrans, SpecStTrigger, SpecStTriggerin, SpecStTriggerprein, SpecStTriggerun,
				SpecStTriggerpostun, SpecStVerifyscript ]

	def __init__(self):
		'''
		Init
		@return: None
		@rtype: None
		@raise SpecNotImplemented: always, parser should not be instantiated
		'''
		raise SpecNotImplemented("Cannot instantiate")

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		token = token_list.touch()

		for o in SpecSectionParser.obj:
			if str(token) == str(o):
				return o

		return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
		'''
		section = cls.sectionBegining(token_list)
		if not section: # section not found
			return None

		ret = section(parent)
		ret.setTokenSection(token_list.get())
		#could be empty
		ret.setTokens(token_list.getWhileNot(functools.partial(ctx.sectionBeginningCallback, ctx)))

		return ret

class SpecExpressionParser(SpecSectionParser):
	'''
	Parse an expression
	'''
	obj = SpecStExpression

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		raise ValueError("Spec expression has no beginning")

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse if
	'''
	obj = SpecStIf

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		token = token_list.touch()
		if str(token) == '%if' or str(token) == '%ifarch':
			return SpecIfParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse a definition
	'''
	obj = SpecStDefinition

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
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
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse %global
	'''
	obj = SpecStGlobal

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		token = token_list.touch()
		if str(token) == str(SpecGlobalParser.obj):
			return SpecGlobalParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse %build section
	'''
	obj = SpecStBuild

class SpecChangelogParser(SpecSectionParser):
	'''
	Parse %changelog section
	'''
	obj = SpecStChangelog

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		token = token_list.touch()
		if str(token) == str(SpecChangelogParser.obj):
			return SpecChangelogParser.obj

		return None

	@classmethod
	def parseEntry(cls, token_list, parent, ctx):
		'''
		Parse a changelog entry
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}

		'''
		def parse_date(date):
			s = str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + ' ' + str(date[3])
			return datetime.datetime.strptime(s, '%a %b %d %Y')

		def changelogEntryBeginningCallback(obj, token_list):
			# is there some section?
			if obj.sectionBeginningCallback(obj, token_list):
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
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse %check section
	'''
	obj = SpecStCheck

class SpecCleanParser(SpecSectionParser):
	'''
	Parse %clean section
	'''
	obj = SpecStClean

class SpecDescriptionParser(SpecSectionParser):
	'''
	Parse a description
	'''
	obj = SpecStDescription

class SpecFilesParser(SpecSectionParser):
	'''
	Parse %files section
	'''
	obj = SpecStFiles

class SpecInstallParser(SpecSectionParser):
	'''
	Parse %install section
	'''
	obj = SpecStInstall

class SpecPackageParser(SpecSectionParser):
	'''
	Parse %package section
	'''
	obj = SpecStPackage

	@staticmethod
	def sectionBegining(token_list):
		'''
		Check if next token is a section beginning
		@param token_list: token list to use
		@type token_list: L{SpecTokenList}
		@return: None or a parser to be used to parse the section
		@rtype: L{SpecSectionParser}
		'''
		token = token_list.touch()

		if str(token) == str(SpecPackageParser.obj):
			return SpecPackageParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		'''
		Parse section from token list
		@param token_list: a token list to be used
		@type token_list: L{SpecTokenList}
		@param parent: parent section or None
		@type parent: L{SpecSection}
		@param allowed: allowed sections within the section
		@type allowed: list of L{SpecSection}
		@param ctx: parsing context
		@type ctx: L{SpecParser}
		@return: parsed section
		@rtype: L{SpecSection}
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
	Parse %prep section
	'''
	obj = SpecStPrep

class SpecPreParser(SpecSectionParser):
	'''
	Parse %pre section
	'''
	obj = SpecStPre

class SpecPostParser(SpecSectionParser):
	'''
	Parse %post section
	'''
	obj = SpecStPost

class SpecPreunParser(SpecSectionParser):
	'''
	Parse %preun section
	'''
	obj = SpecStPreun

class SpecPostunParser(SpecSectionParser):
	'''
	Parse %postun section
	'''
	obj = SpecStPostun

class SpecPretransParser(SpecSectionParser):
	'''
	Parse %pretrans section
	'''
	obj = SpecStPretrans

class SpecPosttransParser(SpecSectionParser):
	'''
	Parse %posttrans section
	'''
	obj = SpecStPosttrans

class SpecTriggerParser(SpecSectionParser):
	'''
	Parse %trigger section
	'''
	obj = SpecStTrigger

class SpecTriggerinParser(SpecSectionParser):
	'''
	Parse %triggerin section
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinParser(SpecSectionParser):
	'''
	Parse %triggerprein section
	'''
	obj = SpecStTriggerprein

class SpecTriggerunParser(SpecSectionParser):
	'''
	Parse %triggerun section
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunParser(SpecSectionParser):
	'''
	Parse %triggerpostun section
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptParser(SpecSectionParser):
	'''
	Parse %verifyscript section
	'''
	obj = SpecStVerifyscript

