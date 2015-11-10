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

import SpecParser
from SpecError import SpecBadToken, SpecNotImplemented

class SpecStatementMeta(type):
	def __repr__(c):
		return "generic spec statement"

class SpecStatement(object):
	parent = None
	tokens = []
	__metaclass__ = SpecStatementMeta

	def __init__(self, parent = None):
		self.parent = parent
		self.tokens = []

	def print_file(self, f, raw = False):
		for t in self.tokens:
			t.print_file(f, raw)

	def print_str(self):
		ret = ""
		for t in self.tokens:
			ret += t.print_str()
		return ret

	def edit(self, replacement):
		raise SpecNotImplemented("Not Implemented")

	def add(self, items):
		raise SpecNotImplemented("Not Implemented")

	def remove(self, items):
		raise SpecNotImplemented("Not Implemented")

class SpecStIfMeta(SpecStatementMeta):
	def __repr__(c):
		return "%if"

class SpecStIf(SpecStatement):
	__metaclass__ = SpecStIfMeta

	def __init__(self, parent):
		SpecStatement.__init__(self, parent)
		self.if_token = None
		self.expr = None
		self.true_branch = None
		self.else_token = None
		self.false_branch = []
		self.endif_token = None

	def print_file(self, f):
		self.if_token.print_file(f)
		self.expr.print_file(f)
		for s in self.true_branch:
			s.print_file(f)
		self.else_token.print_file(f) if self.else_token is not None else None
		for s in self.false_branch:
			s.print_file(f)
		self.endif_token.print_file(f)

	def print_str(self):
		ret = self.if_token.print_str()
		ret += self.expr.print_str()
		for s in self.true_branch:
			ret += s.print_str()
		ret += self.else_token.print_str() if self.else_token is not None else ""
		for s in self.false_branch:
			ret += s.print_str()
		ret +=self.endif_token.print_str()
		return ret

	def setExpr(self, token_list):
		self.expr = token_list

	def getExpr(self, token_list):
		self.expr = token_list

	def setTrueBranch(self, token_list):
		self.true_branch = token_list

	def getTrueBranch(self):
		return self.true_branch

	def setFalseBranch(self, token_list): # e.g. else
		self.false_branch = token_list

	def getFalseBranch(self):
		return self.false_branch

class SpecStDefinitionMeta(SpecStatementMeta):
	def __repr__(c):
		return "spec definition"

class SpecStDefinition(SpecStatement):
	__metaclass__ = SpecStDefinitionMeta

	def __init__(self, parent):
		SpecStatement.__init__(self, parent)
		self.name = None
		self.value = None

	def print_file(self, f):
		self.name.print_file(f)
		self.value.print_file(f)

	def print_str(self):
		ret = self.name.print_str()
		ret += self.value.print_str()
		return ret

	def setValue(self, value):
		self.value = value

	def getValue(self):
		return self.value

class SpecStGlobalMeta(SpecStatementMeta):
	def __repr__(c):
		return "%global"

class SpecStGlobal(SpecStatement):
	__metaclass__ = SpecStGlobalMeta

	def __init__(self, parent):
		SpecStatement.__init__(self, parent)
		self.global_token = None
		self.variable = None
		self.value = None

	def print_file(self, f):
		self.global_token.print_file(f)
		self.variable.print_file(f)
		self.value.print_file(f)

	def print_str(self):
		ret = self.global_token.print_str()
		ret += self.variable.print_str()
		ret += self.value.print_str()
		return ret

	def setVariable(self, variable):
		self.variable = variable

	def getVariable(self):
		return self.variable

	def setValue(self, value):
		self.value = value

	def getValue(self):
		return self.value

class SpecStEofMeta(SpecStatementMeta):
	def __repr__(c):
		return "<EOF>"

class SpecStEof(SpecStatement):
	__metaclass__ = SpecStEofMeta

	def __init__(self, parent = None):
		SpecStatement.__init__(self, parent)
		self.eof_token = None

	def print_file(self, f):
		self.eof_token.print_file(f)

	def print_str(self):
		return self.eof_token.print_str()

	def setEofToken(self, token):
	# this stores whitespaces at the EOF
		self.eof_token = token

	def getEofToken(self):
		return self.eof_token

class SpecStExpressionMeta(SpecStatementMeta):
	def __repr__(c):
		return "spec expression"

class SpecStExpression(SpecStatement):
	__metaclass__ = SpecStExpressionMeta

	def __init__(self, parent):
		SpecStatement.__init__(self, parent)

	def parse(self, token_list):
		# TODO: implement
		self.tokens.append(token_list.get())
		return self.tokens

class SpecStSectionMeta(SpecStatementMeta):
	def __repr__(c):
		return "generic spec section"

class SpecStSection(SpecStatement):
	__metaclass__ = SpecStSectionMeta

	def __init__(self, parent):
		SpecStatement.__init__(self, parent)
	# TODO: implement

class SpecStDescriptionMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%description"

class SpecStDescription(SpecStSection):
	__metaclass__ = SpecStDescriptionMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)

	def parse(self, token_list, allowed, disallowed):
		self.tokens.append(token_list.get())
		self.tokens += token_list.getWhileNot(disallowed)

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStBuildMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%build"

class SpecStBuild(SpecStSection):
	__metaclass__ = SpecStBuildMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStChangelogItemMeta(SpecStSectionMeta):
	def __repr__(c):
		return "spec changelog item"

class SpecStChangelogItem(SpecStSection):
	__metaclass__ = SpecStChangelogItemMeta

	def __init__(self, parent):
		self.star = None
		self.date = None
		self.user = None
		self.user_email = None
		self.version_delim = None
		self.version = None
		self.parent = parent

	def parse_header(self, token_list):
		self.star = token_list.get()
		if str(self.star) != '*':
			token_list.unget()
			raise SpecBadToken("Expected token '*', got '%s'" % self.star)

		self.date = []
		for _ in xrange(0, 4): # TODO: parse dayOfWeek, month, day, year
			self.date.append(token_list.get())

		self.user = [token_list.get()] # TODO: multiple words
		self.user_email = token_list.get()
		self.version_delim = token_list.get()

		if str(self.version_delim) != '-':
			token_list.unget()
			raise SpecBadToken("Expected token '-', got '%s'" % self.star)

		self.version = token_list.get()

	def parse(self, token_list):
		self.parse_header(token_list)
		self.message = token_list.getWhileNot(SpecParser.SpecParser.SECTION_TS + ['*'])

	def print_file(self, f):
		self.star.print_file(f)
		for d in self.date:
			d.print_file(f)
		for u in self.user:
			u.print_file(f)
		self.user_email.print_file(f)
		self.version_delim.print_file(f)
		self.version.print_file(f)

		for m in self.message:
			m.print_file(f)

	def print_str(self):
		ret = self.star.print_str()

		for d in self.date:
			ret += d.print_str()

		for u in self.user:
			ret += u.print_str()

		ret += self.user_email.print_str()
		ret += self.version_delim.print_str()
		ret += self.version.print_str()

		for m in self.message:
			ret += m.print_str()

		return ret

class SpecStChangelogMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%changelog"

class SpecStChangelog(SpecStSection):
	__metaclass__ = SpecStChangelogMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
		self.token = None # [([hader_tokens], [message_tokens]), ...]
		self.items = None

	def parse(self, token_list):
		self.token = token_list.get()
		if str(self.token) != '%changelog':
			raise SpecBadToken("Unexpected token '%s', expected \%changelog" % str(token))

		self.items = []
		while str(token_list.touch()) == '*':
			st_item = SpecStChangelogItem(self)
			st_item.parse(token_list)
			self.items.append(st_item)

	def print_file(self, f):
		self.token.print_file(f)
		for i in self.items:
			i.print_file(f)

	def print_str(self):
		ret = ""

		ret += self.token.print_str()
		for i in self.items:
			ret += i.print_str()

		return ret

class SpecStCheckMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%check"

class SpecStCheck(SpecStSection):
	__metaclass__ = SpecStCheckMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStCleanMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%clean"

class SpecStClean(SpecStSection):
	__metaclass__ = SpecStCleanMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStFilesMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%files"

class SpecStFiles(SpecStSection):
	__metaclass__ = SpecStFilesMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

class SpecStInstallMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%install"

class SpecStInstall(SpecStSection):
	__metaclass__ = SpecStInstallMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPackageMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%package"

class SpecStPackage(SpecStSection):
	__metaclass__ = SpecStPackageMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

class SpecStPrepMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%prep"

class SpecStPrep(SpecStSection):
	__metaclass__ = SpecStPrepMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPreMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%pre"

class SpecStPre(SpecStSection):
	__metaclass__ = SpecStPreMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPostMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%post"

class SpecStPost(SpecStSection):
	__metaclass__ = SpecStPostMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPreunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%preun"

class SpecStPreun(SpecStSection):
	__metaclass__ = SpecStPreunMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPostunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%postun"

class SpecStPostun(SpecStSection):
	__metaclass__ = SpecStPostunMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPretransMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%pretrans"

class SpecStPretrans(SpecStSection):
	__metaclass__ = SpecStPretransMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStPosttransMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%posttrans"

class SpecStPosttrans(SpecStSection):
	__metaclass__ = SpecStPosttransMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStTriggerinMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerin"

class SpecStTriggerin(SpecStSection):
	__metaclass__ = SpecStTriggerinMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStTriggerpreinMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerprein"

class SpecStTriggerprein(SpecStSection):
	__metaclass__ = SpecStTriggerpreinMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStTriggerunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerpreun"

class SpecStTriggerun(SpecStSection):
	__metaclass__ = SpecStTriggerunMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStTriggerpostunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerpostun"

class SpecStTriggerpostun(SpecStSection):
	__metaclass__ = SpecStTriggerpostunMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

class SpecStVerifyscriptMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%verifyscript"

class SpecStVerifyscript(SpecStSection):
	__metaclass__ = SpecStVerifyscriptMeta

	def __init__(self, parent):
		SpecStSection.__init__(self, parent)
	# TODO: implement

	def edit(self, replacement):
		# TODO: implement
		self.tokens = []

