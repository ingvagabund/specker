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

class Statement(object):
	parent = None
	tokens = []

	def __init__(self, parent = None):
		self.parent = parent
		self.tokens = []

	def print_file(self, f):
		for t in self.tokens:
			t.print_file(f)

	def print_str(self):
		ret = ""
		for t in self.tokens:
			ret += t.print_str()
		return ret

class StIf(Statement):
	def __init__(self, parent):
		Statement.__init__(self, parent)
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

class StDefinition(Statement):
	def __init__(self, parent):
		Statement.__init__(self, parent)
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

class StGlobal(Statement):
	def __init__(self, parent):
		Statement.__init__(self, parent)
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

class StEof(Statement):
	def __init__(self, parent = None):
		Statement.__init__(self, parent)
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

class StExpression(Statement):
	def __init__(self, parent):
		Statement.__init__(self, parent)

	def parse(self, token_list):
		# TODO: implement
		self.tokens.append(token_list.get())
		return self.tokens

class StSection(Statement):
	def __init__(self, parent):
		Statement.__init__(self, parent)
	# TODO: implement

class StDescription(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StBuild(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StChangelog(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StCheck(StSection):
	def __init__(self, parent):
		StSection.__init__(parent)
	# TODO: implement

class StClean(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StFiles(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StInstall(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPackage(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPrep(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPre(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPost(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPreun(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPostun(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPretrans(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StPosttrans(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StTriggerin(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StTriggerprein(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StTriggerun(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StTriggerpostun(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

class StVerifyscript(StSection):
	def __init__(self, parent):
		StSection.__init__(self, parent)
	# TODO: implement

