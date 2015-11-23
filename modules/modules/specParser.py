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
import copy
import datetime
import functools
from specSection import *
from specToken import SpecTokenList
from specModel import SpecModel
from specManipulator import SpecManipulator
from specDebug import SpecDebug
from specError import SpecBadToken, SpecBadIf

class SpecParser(SpecManipulator):
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

	def init(self, f):
		self.token_list = SpecTokenList(f)

	@staticmethod
	def sectionBeginingCallback(obj, token_list):
		return obj.sectionBegining(token_list)

	def sectionBegining(self, token_list):
		for parser in self.PARSERS:
			ret = parser.sectionBegining(token_list)
			if ret is not None:
				return ret

		return None # Not found

	def parse_loop(self, token_list, parent, allowed):
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
		allowed = [ SpecIfParser, SpecDefinitionParser, SpecGlobalParser ]

		ret = self.parse_loop(self.token_list, None, allowed)
		unparsed = self.token_list.touch()
		SpecDebug.logger.debug("-- preamble finished with token '%s' on line %d" % (str(unparsed), unparsed.line))
		return ret

	def parse_loop_section(self, parent):
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
		self.model = SpecModel()

		self.model.append_items(self.parse_preamble())
		self.model.append_items(self.parse_loop_section(None))

		eof = self.token_list.touch()
		if not eof.isEOF():
			raise SpecBadToken("Unexpected symbol '" + str(eof.token) + "' on line " + str(eof.line))

	def getModel(self):
		return self.model

class SpecSectionParser(object):
	obj = [ SpecStBuild, SpecStCheck, SpecStClean, SpecStDescription, SpecStFiles, SpecStInstall,
				SpecStPrep, SpecStPre, SpecStPost, SpecStPreun, SpecStPostun, SpecStPretrans,
				SpecStPosttrans, SpecStTrigger, SpecStTriggerin, SpecStTriggerprein, SpecStTriggerun,
				SpecStTriggerpostun, SpecStVerifyscript ]

	def __init__(self):
		raise ValueError("Cannot instantiate")

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()

		for o in SpecSectionParser.obj:
			if str(token) == str(o):
				return o

		return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		section = cls.sectionBegining(token_list)
		if not section: # section not found
			return None

		# TODO: eof check
		ret = section(parent)
		ret.setTokenSection(token_list.get())
		ret.setTokens(token_list.getWhileNot(functools.partial(ctx.sectionBeginingCallback, ctx)))

		return ret

class SpecIfParser(SpecSectionParser):
	obj = SpecStIf

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()
		if str(token) == '%if' or str(token) == '%ifarch':
			return SpecIfParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		if not cls.sectionBegining(token_list):
			return None

		pointer = token_list.getPointer()

		stif = SpecIfParser.obj(parent)
		stif.setIfToken(token_list.get())
		# TODO: stif.setExpr(ctx.parseExpresion(parent, token_list))
		stif.setExpr(token_list.get())
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
	obj = SpecStDefinition

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()

		if str(token) in [ 'Name:', 'Version:', 'Release:', 'Summary:', 'License:',
				'URL:', 'ExclusiveArch:', 'BuildRequires:', 'Provides:', 'Requires']:
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
		if not cls.sectionBegining(token_list):
			return None

		# TODO: eof check
		ret = SpecDefinitionParser.obj(parent)
		ret.setName(token_list.get())
		ret.setValue(token_list.getLine())

		return ret

class SpecGlobalParser(SpecSectionParser):
	obj = SpecStGlobal

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()
		if str(token) == str(SpecGlobalParser.obj):
			return SpecGlobalParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		if not cls.sectionBegining(token_list):
			return None

		# TODO: eof check
		ret = SpecGlobalParser.obj(parent)
		ret.setGlobalToken(token_list.get())
		ret.setVariable(token_list.get())
		ret.setValue(token_list.getLine())

		return ret

class SpecBuildParser(SpecSectionParser):
	obj = SpecStBuild

class SpecChangelogParser(SpecSectionParser):
	obj = SpecStChangelog

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()
		if str(token) == str(SpecChangelogParser.obj):
			return SpecChangelogParser.obj

		return None

	@classmethod
	def parseItem(cls, token_list, parent, ctx):
			def parse_date(date):
				s = str(date[0]) + ' ' + str(date[1]) + ' ' + str(date[2]) + ' ' + str(date[3])
				return datetime.datetime.strptime(s, '%a %b %d %Y')

			def changelogItemBeginningCallback(obj, token_list):
				# is there some section?
				if obj.sectionBeginingCallback(obj, token_list):
					return True

				# or is there another changelog item?
				return str(token_list.touch()) == '*'

			item = SpecChangelogParser.obj.SpecStChangelogItem(parent)

			star = token_list.get()
			if str(star) != '*':
				token_list.unget()
				raise SpecBadToken("Expected token '*', got '%s'" % star)
			item.setStar(star)

			date = SpecTokenList()
			for _ in xrange(0, 4):
				date.tokenListAppend(token_list.get())
			item.setDate(date)

			date_parsed = parse_date(date)
			item.setDateParsed(date_parsed)

			user = SpecTokenList()
			while not str(token_list.touch()).startswith('<'):
				user.tokenListAppend(token_list.get())
			item.setUser(user)

			user_email = token_list.get()
			item.setUserEmail(user_email)

			version_delim = token_list.get()
			if str(version_delim) != '-':
				token_list.unget()
				raise SpecBadToken("Expected token '-', got '%s'" % self.star)
			item.setVersionDelim(version_delim)

			version = token_list.get()
			item.setVersion(version)

			item.setMessage(token_list.getWhileNot(functools.partial(changelogItemBeginningCallback, ctx)))

			return item

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		if not cls.sectionBegining(token_list):
			return None

		ret = SpecChangelogParser.obj(parent)
		ret.setTokenSection(token_list.get())

		while str(token_list.touch()) == '*':
			item = cls.parseItem(token_list, ret, ctx)
			if item:
				ret.appendItem(item)

		return ret

class SpecCheckParser(SpecSectionParser):
	obj = SpecStCheck

class SpecCleanParser(SpecSectionParser):
	obj = SpecStClean

class SpecDescriptionParser(SpecSectionParser):
	obj = SpecStDescription

class SpecFilesParser(SpecSectionParser):
	obj = SpecStFiles

class SpecInstallParser(SpecSectionParser):
	obj = SpecStInstall

class SpecPackageParser(SpecSectionParser):
	obj = SpecStPackage

	@staticmethod
	def sectionBegining(token_list):
		token = token_list.touch()

		if str(token) == str(SpecPackageParser.obj):
			return SpecPackageParser.obj
		else:
			return None

	@classmethod
	def parse(cls, token_list, parent, allowed, ctx):
		if not cls.sectionBegining(token_list):
			return None

		section = SpecPackageParser.obj(parent)
		section.setTokenSection(token_list.get())
		if section.getTokenSection().sameLine(token_list.touch()):
			section.setPackage(token_list.get())
		section.setDefs(ctx.parse_loop(token_list, section, [SpecIfParser, SpecDefinitionParser]))

		return section

class SpecPrepParser(SpecSectionParser):
	obj = SpecStPrep

class SpecPreParser(SpecSectionParser):
	obj = SpecStPre

class SpecPostParser(SpecSectionParser):
	obj = SpecStPost

class SpecPreunParser(SpecSectionParser):
	obj = SpecStPreun

class SpecPostunParser(SpecSectionParser):
	obj = SpecStPostun

class SpecPretransParser(SpecSectionParser):
	obj = SpecStPretrans

class SpecPosttransParser(SpecSectionParser):
	obj = SpecStPosttrans

class SpecTriggerParser(SpecSectionParser):
	obj = SpecStTrigger

class SpecTriggerinParser(SpecSectionParser):
	obj = SpecStTriggerin

class SpecTriggerpreinParser(SpecSectionParser):
	obj = SpecStTriggerprein

class SpecTriggerunParser(SpecSectionParser):
	obj = SpecStTriggerun

class SpecTriggerpostunParser(SpecSectionParser):
	obj = SpecStTriggerpostun

class SpecVerifyscriptParser(SpecSectionParser):
	obj = SpecStVerifyscript

