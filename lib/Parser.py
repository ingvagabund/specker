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

import logging
import sys
from SpecFile import SpecFile
from Token import Token, TokenList
from Statement import *

class ChunkParser:
	def __init__(self, token, func):
		self.token = token
		self.func = func

	def __str__(self):
		return self.token

	def __eq__(self, other):
		return self.token == other.token

	def parse(self, token_list, parent, allowed, disallowed):
		return self.func(token_list, parent, allowed, disallowed)

class Parser:
	logger = None

	@staticmethod
	def parse_if(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing if")
		pointer = token_list.getPointer()
		st_if = StIf(parent)
		t = token_list.get()

		if str(t) != '%if':
			token_list.setPointer(pointer)
			raise ValueError('Expected %if')

		st_if.if_token = t
		st_exp = StExpression(st_if)
		st_exp.parse(token_list)
		st_if.setExpr(st_exp)
		st_if.setTrueBranch(Parser.parse_loop(token_list, st_if, allowed, disallowed + ['%else', '%endif']))

		t = token_list.get()
		if str(t) == '%else':
			st_if.setFalseBranch(Parser.parse_loop(token_list, st_if, allowed, disallowed + ['%else', '%endif']))
			st_if.else_token = t
			t = token_list.get()

		if t.token == None or str(t) != '%endif':
			token_list.setPointer(pointer)
			raise ValueError('Unexpected token ' + str(t) + ', expected %endif')

		st_if.endif_token = t
		return st_if

	@staticmethod
	def parse_global(token_list, parent, allowed = None, disallowed = None):
		Parser.logger.debug("-- parsing global")
		st_global = StGlobal(parent)
		t = token_list.get()
		if str(t) != '%global':
			token_list.unget()
			raise ValueError('Expected %global')
		st_global.global_token = t

		t = token_list.get() # TODO: parse as expression
		if t.token == None or str(t).startswith('%'):
			token_list.unget()
			raise ValueError('Unexpected token, expected variable name')

		st_global.setVariable(t)

		st_exp = StExpression(st_global)
		st_exp.parse(token_list)
		st_global.setValue(st_exp)

		return st_global

	@staticmethod
	def parse_definition(token_list, parent, allowed = None, disallowed = None):
		Parser.logger.debug("-- parsing definition")
		st_definition = StDefinition(parent)
		t = token_list.get()
		if t not in Parser.DEFINITION_TS:
			token_list.unget()
			raise ValueError('Expected definition')
		st_definition.name = t

		st_exp = StExpression(st_definition)
		st_exp.parse(token_list)
		st_definition.setValue(st_exp)

		return st_definition

	@staticmethod
	def parse_section(token_list, parent, allowed, disallowed, section_type):
		Parser.logger.debug("--- parsing generic section")
		st_section = section_type(parent)
		st_section.tokens.append(token_list.get())
		st_section.tokens += token_list.getWhileNot(disallowed)
		return st_section

	@staticmethod
	def parse_description(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing description")
		st_section = StDescription(parent)
		st_section.parse(token_list, allowed, disallowed)

		return st_section

	@staticmethod
	def parse_files(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing files")
		st_section = StFiles(parent)
		st_section.tokens.append(token_list.get())
		st_section.tokens = token_list.getWhileNot(disallowed)
		return st_section

	@staticmethod
	def parse_build(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing build")
		# TODO: implement
		return Parser.parse_section(token_list, parent, allowed, disallowed, StBuild)

	@staticmethod
	def parse_changelog(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing changelog")
		st_changelog = StChangelog(parent)
		st_changelog.parse(token_list)
		return st_changelog

	@staticmethod
	def parse_check(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing check")
		# TODO: implement
		return Parser.parse_section(token_list, parent, allowed, disallowed, StCheck)

	@staticmethod
	def parse_clean(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing clean")
		# TODO: implement
		return Parser.parse_section(token_list, parent, allowed, disallowed, StClean)

	@staticmethod
	def parse_install(token_list, parent, allowed, disallowed):
		Parser.logger.debug("-- parsing install")
		# TODO: implement
		return Parser.parse_section(token_list, parent, allowed, disallowed, StInstall)

	@staticmethod
	def parse_package(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing package")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPackage)

	@staticmethod
	def parse_prep(token_list, parent, allowed, disallowed):
		# TODO: implement
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPrep)

	@staticmethod
	def parse_pre(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing prep")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPre)

	@staticmethod
	def parse_post(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing post")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPost)

	@staticmethod
	def parse_preun(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing preun")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPreun)

	@staticmethod
	def parse_postun(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing postun")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPostun)

	@staticmethod
	def parse_pretrans(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing pretrans")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPretrans)

	@staticmethod
	def parse_posttrans(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing posttrans")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StPosttrans)

	@staticmethod
	def parse_trigger(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing trigger")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StTrigger)

	@staticmethod
	def parse_triggerin(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing triggerin")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StTriggerin)

	@staticmethod
	def parse_triggerprein(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing triggerprein")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StTriggerprein)

	@staticmethod
	def parse_triggerun(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing triggerun")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StTriggerun)

	@staticmethod
	def parse_triggerpostun(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing triggerpostun")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StTriggerpostun)

	@staticmethod
	def parse_verifyscript(token_list, parent, allowed, disallowed):
		# TODO: implement
		Parser.logger.debug("-- parsing verifyscript")
		return Parser.parse_section(token_list, parent, allowed, disallowed, StVerifyscript)

	@staticmethod
	def parse_loop(token_list, parent, allowed, disallowed):
		ret = []
		while True:
			found = False
			token = token_list.touch()
			Parser.logger.debug("- parsing round: '%s'" % str(token))

			if token.token is None:
				break

			for t in disallowed:
				if t == token:
					Parser.logger.debug("- token '%s' not allowed here, skipping " % str(token))
					break

			for t in allowed:
				if t == token:
					ret.append(t.parse(token_list, parent, allowed, disallowed))
					found = True
					break

			if not found:
				Parser.logger.debug("- unparsed token '%s' on line %s" % (str(token), str(token.line)))
				break;

		return ret

	# Sections
	BUILD_T 				= ChunkParser('%build', parse_build.__func__)
	CHANGELOG_T 		= ChunkParser('%changelog', parse_changelog.__func__)
	CHECK_T 				= ChunkParser('%check', parse_check.__func__)
	CLEAN_T 				= ChunkParser('%clean', parse_clean.__func__)
	DESCRIPTION_T 		= ChunkParser('%description', parse_description.__func__)
	FILES_T 				= ChunkParser('%files', parse_files.__func__)
	INSTALL_T 			= ChunkParser('%install', parse_install.__func__)
	PACKAGE_T 			= ChunkParser('%package', parse_package.__func__)
	PREP_T 				= ChunkParser('%prep', parse_prep.__func__)
	PRE_T 				= ChunkParser('%pre', parse_pre.__func__)
	POST_T 				= ChunkParser('%post', parse_post.__func__)
	PREUN_T 				= ChunkParser('%preun', parse_preun.__func__)
	POSTUN_T 			= ChunkParser('%postun', parse_postun.__func__)
	PRETRANS_T 			= ChunkParser('%pretrans', parse_pretrans.__func__)
	POSTTRANS_T			= ChunkParser('%posttrans', parse_posttrans.__func__)
	TRIGGER_T 			= ChunkParser('%trigger', parse_trigger.__func__)
	TRIGGERIN_T 		= ChunkParser('%triggerin', parse_triggerin.__func__)
	TRIGGERPREIN_T 	= ChunkParser('%triggerprein', parse_triggerprein.__func__)
	TRIGGERUN_T 		= ChunkParser('%triggerun', parse_triggerun.__func__)
	TRIGGERPOSTUN_T 	= ChunkParser('%triggerpostun', parse_triggerpostun.__func__)
	VERIFYSCRIPT_T 	= ChunkParser('%verifyscript', parse_verifyscript.__func__)
	SECTION_TS			= [
						BUILD_T, CHANGELOG_T, CHECK_T, CLEAN_T, DESCRIPTION_T,
						FILES_T, INSTALL_T, PACKAGE_T, PREP_T, PRE_T, POST_T,
						PREUN_T, POSTUN_T, PRETRANS_T, POSTTRANS_T, TRIGGER_T,
						TRIGGERIN_T, TRIGGERPREIN_T, TRIGGERUN_T, TRIGGERPOSTUN_T,
						VERIFYSCRIPT_T
						]
	#
	IF_T					= ChunkParser('%if', parse_if.__func__)
	GLOBAL_T				= ChunkParser('%global', parse_global.__func__)
	# Definitions
	NAME_T				= ChunkParser('Name:', parse_definition.__func__)
	VERSION_T			= ChunkParser('Version:', parse_definition.__func__)
	RELEASE_T			= ChunkParser('Release:', parse_definition.__func__)
	SUMMARY_T			= ChunkParser('Summary:', parse_definition.__func__)
	LICENSE_T			= ChunkParser('License:', parse_definition.__func__)
	URL_T					= ChunkParser('URL:', parse_definition.__func__)
	SOURCE_T				= ChunkParser('Source:', parse_definition.__func__)
	EXCLUSIVEARCH_T	= ChunkParser('ExclusiveArch:', parse_definition.__func__)
	BUILDREQUIRES_T	= ChunkParser('BuildRequires:', parse_definition.__func__)
	REQUIRES_T			= ChunkParser('Requires:', parse_definition.__func__)
	PROVIDES_T			= ChunkParser('Provides:', parse_definition.__func__)
	DEFINITION_TS		= [
						NAME_T, VERSION_T, RELEASE_T, SUMMARY_T, LICENSE_T, URL_T,
						SOURCE_T, EXCLUSIVEARCH_T, BUILDREQUIRES_T, REQUIRES_T,
						PROVIDES_T
						]

	ALL_TS				= SECTION_TS + [IF_T, GLOBAL_T] + DEFINITION_TS

	def __init__(self, spec):
		Parser.logger = logging.getLogger('specker-parser')
		Parser.logger.addHandler(logging.StreamHandler(sys.stderr))
		self.token_list = TokenList(SpecFile(spec))
		self.registered_parsers = []

	def parse_preamble(self):
		allowed = [
						self.IF_T, self.GLOBAL_T,
				] + self.DEFINITION_TS

		ret = Parser.parse_loop(self.token_list, None, allowed, self.SECTION_TS)
		unparsed = self.token_list.touch()
		Parser.logger.debug("-- preamble finished with token '%s' on line %d" % (str(unparsed), unparsed.line))
		return ret

	def register_parser(self, statement_type, callback):
		self.registered_parsers.insert(0, (statement_type, callback))

	def parse_loop_section(self, parent = None):
		ret = self.parse_preamble()
		allowed = self.ALL_TS			# allowed within section
		disallowed = self.SECTION_TS	# disallowed within section

		while True:
			found = False
			token = self.token_list.touch()

			Parser.logger.debug("-- parsing section '%s' " % str(token))

			if token.token is None: # EOF
				break

			for s in self.ALL_TS:
				if s == token:
					found = True
					section = s.parse(self.token_list, parent, allowed, disallowed)
					ret.append(section)
					if type(section) is not StIf and type(section) is not StGlobal and \
							type(section) is not StDescription and type(section) is not StFiles:
						Parser.logger.debug("-- removing " + str(token) + " from allowed")
						allowed.remove(s)
						disallowed.append(s)
					# TODO: call registered callback
					break

			if not found:
				Parser.logger.debug("-- unparsed beginning of a section: " + str(token))
				break

		return ret

	def parse(self):
		self.raw_statements = self.parse_loop_section(None)

		eof = self.token_list.touch()
		if eof.token != None:
			raise ValueError("Unexpected symbol '" + str(eof.token) + "' on line " + str(eof.line))
		self.sections = [x for x in self.raw_statements if x.parent is None and type(x) is not StIf]
		return self.raw_statements

	def setLoggingLevel(self, level):
		print "logging level"
		Parser.logger.setLevel(level)

	def print_str(self):
		ret = ""
		for s in self.raw_statements:
			ret += s.print_str()
		return ret

	def print_file(self, f):
		for s in self.raw_statements:
			s.print_file(f)

