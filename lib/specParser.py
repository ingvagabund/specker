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

import logging
import sys
from specManipulator import SpecManipulator
from specFile import SpecFile
from specToken import SpecTokenList
from specStatement import *
from specError import SpecBadIf, SpecBadToken

class SpecParser(SpecManipulator):
	@staticmethod
	def parse_loop(token_list, parent, allowed, disallowed):
		ret = []
		while True:
			found = False
			token = token_list.touch()
			SpecManipulator.logger.debug("- parsing round: '%s'" % str(token))

			if token.token is None:
				break

			for t in allowed:
				if t == token:
					ret.append(t.parse(token_list, parent, allowed, disallowed))
					found = True
					break

			if not found:
				SpecManipulator.logger.debug("- unparsed token '%s' on line %s" % (str(token), str(token.line)))
				break;

		return ret

	def __init__(self):
		SpecManipulator.logger = logging.getLogger('specker-parser')
		SpecManipulator.logger.addHandler(logging.StreamHandler(sys.stderr))

	def init(self, spec):
		self.token_list = SpecTokenList(spec)

	def parse_preamble(self):
		allowed = [
						self.IF_T, self.GLOBAL_T,
				] + self.DEFINITION_TS

		ret = SpecParser.parse_loop(self.token_list, None, allowed, self.SECTION_TS)
		unparsed = self.token_list.touch()
		SpecManipulator.logger.debug("-- preamble finished with token '%s' on line %d" % (str(unparsed), unparsed.line))
		return ret

	def parse_loop_section(self, parent = None):
		ret = self.parse_preamble()
		allowed = self.ALL_TS			# allowed within section
		disallowed = self.SECTION_TS			# allowed within section

		found = True
		while found:
			found = False
			token = self.token_list.touch()

			SpecManipulator.logger.debug("-- parsing section '%s' " % str(token))

			if token.token is None: # EOF
				break

			for s in self.ALL_TS:
				if s == token:
					found = True
					section = s.parse(self.token_list, parent, allowed, disallowed)
					ret.append(section)
					if type(section) is not SpecStIf and type(section) is not SpecStGlobal and \
							type(section) is not SpecStDescription and type(section) is not SpecStFiles:
						SpecManipulator.logger.debug("-- removing " + str(token) + " from allowed")
						allowed.remove(s)
						disallowed.append(s)
					# TODO: call registered callback
					break

		SpecManipulator.logger.debug("-- unparsed beginning of a section: " + str(token))

		return ret

	def parse(self):
		self.statements = self.parse_loop_section(None)

		eof = self.token_list.touch()
		if eof.token != None:
			raise SpecBadToken("Unexpected symbol '" + str(eof.token) + "' on line " + str(eof.line))
		return self.statements

	def getStatements(self):
		return self.statements

