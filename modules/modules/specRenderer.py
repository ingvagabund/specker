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
A spec model rendering
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

import sys
import re
from specError import SpecNotFound
from specSection import *
from specManipulator import SpecManipulator

class SpecRenderer(SpecManipulator):
	'''
	TODO
	'''
	def __init__(self, model):
		self.RENDERERS = [
				SpecIfRenderer,
				SpecDefinitionRenderer,
				SpecGlobalRenderer,
				SpecBuildRenderer,
				SpecChangelogRenderer,
				SpecCheckRenderer,
				SpecCleanRenderer,
				SpecDescriptionRenderer,
				SpecFilesRenderer,
				SpecInstallRenderer,
				SpecPackageRenderer,
				SpecPrepRenderer,
				SpecPreRenderer,
				SpecPostRenderer,
				SpecPreunRenderer,
				SpecPostunRenderer,
				SpecPretransRenderer,
				SpecPosttransRenderer,
				SpecTriggerRenderer,
				SpecTriggerinRenderer,
				SpecTriggerpreinRenderer,
				SpecTriggerunRenderer,
				SpecTriggerpostunRenderer,
				SpecVerifyscriptRenderer
			]

		self.model = model

	def register(self, renderer):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		# TODO: move to SpecManipulator
		found = False
		for idx, item in enumerate(self.RENDERERS):
			if issubclass(renderer, item):
				found = True
				self.RENDERERS[idx] = renderer
				break

		if not found:
			raise SpecNotFound("Invalid renderer '%s' registration" % renderer.__name__)

	def render_list(self, l, f):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for section in l:
			self.render_section(section, f)

	def render(self, f):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.render_list(self.model.getSections(), f)

	def render_section(self, s, f):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		found = False
		for renderer in self.RENDERERS:
			if issubclass(s.__class__, renderer.obj):
				found = True
				renderer(s).render(f, self)
		if not found:
			raise NotImplementedError("Not implemented renderer")

	def find_section_print(self, section_type, f = sys.stdout, verbose = True):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		s = self.model.find_section(section_type)

		if s is not None:
			for sec in s:
				self.render_section(sec, f)
		elif verbose:
			raise SpecNotFound("Error: section '%s' not found" % section_type)

		return s

	def print_definitions(self, defs, definition, packages, f):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for d in defs:
			if definition.match(str(d.name)):
				pkg = d.getPackage()
				if pkg:
					pkg = pkg.getPackage()
				if str(pkg) in packages or (pkg is None and '-' in packages) or '*' in packages:
					if pkg is None:
						f.write('-:')
					else:
						pkg.write(f, raw = True)
						f.write(':') # add delim since raw

					d.getValue().write(f, raw = True)
					f.write('\n') # Add delim since raw token is printed

	def provides_show(self, package, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('Provides:'), package, f)

	def requires_show(self, packages, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('Requires:'), packages, f)

	def buildrequires_show(self, package, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('BuildRequires:'), package, f)

	def changelog_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStChangelog, f)

	def description_show(self, package = None, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStDescription, f)

	def build_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStBuild, f)

	def check_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStCheck, f)

	def clean_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStClean, f)

	def files_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStFiles, f)

	def install_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStInstall, f)

	def package_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPackage, f)

	def prep_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPrep, f)

	def pre_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPre, f)

	def post_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPost, f)

	def preun_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPreun, f)

	def postun_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPostun, f)

	def pretrans_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPretrans, f)

	def posttrans_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPosttrans, f)

	def triggerin_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStTriggerin, f)

	def triggerprein_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStTriggerprein, f)

	def triggerun_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStTriggerun, f)

	def triggerpostun_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStPostun, f)

	def verifyscript_show(self, f = sys.stdout):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		return self.find_section_print(SpecStVerifyscript, f)

class SpecSectionRenderer(object):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStSection

	def __init__(self, section):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section = section

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getTokenSection().write(f)
		self.section.getTokens().write(f)

class SpecExpressionRenderer(object):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStExpression

	def __init__(self, section):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section = section

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		for token in self.section.getTokens():
			token.write(f)

class SpecIfRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStIf

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getIfToken().write(f)
		SpecExpressionRenderer(self.section.getExpr()).render(f, ctx)
		ctx.render_list(self.section.getTrueBranch(), f)
		if self.section.getElseToken():
			self.section.getElseToken().write(f)
			ctx.render_list(self.section.getFalseBranch(), f)
		self.section.getEndifToken().write(f)

class SpecGlobalRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStGlobal

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getGlobalToken().write(f)
		self.section.getVariable().write(f)
		SpecExpressionRenderer(self.section.getValue()).render(f, ctx)

class SpecBuildRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStBuild

class SpecChangelogRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStChangelog

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getTokenSection().write(f)

		for entry in self.section.getEntries():
			entry.getStar().write(f)
			entry.getDate().write(f)
			entry.getUser().write(f)
			entry.getUserEmail().write(f)
			entry.getVersionDelim().write(f)
			entry.getVersion().write(f)
			entry.getMessage().write(f)

class SpecCheckRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStCheck

class SpecCleanRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStClean

class SpecDescriptionRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStDescription

class SpecFilesRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStFiles

class SpecInstallRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStInstall

class SpecPackageRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPackage

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getTokenSection().write(f)
		if self.section.getPackage():
			self.section.getPackage().write(f)
		ctx.render_list(self.section.getDefs(), f)

class SpecPrepRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPrep

class SpecPreRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPre

class SpecPostRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPost

class SpecPreunRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPreun

class SpecPostunRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPostun

class SpecPretransRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPretrans

class SpecPosttransRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStPosttrans

class SpecDefinitionRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStDefinition

	def render(self, f, ctx):
		'''
		TODO
		@param XXX:
		@type XXX: number
		@return: None
		@rtype:
		@raise SpecNotFound:
		'''
		self.section.getName().write(f)
		self.section.getValue().write(f)

class SpecTriggerRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTrigger

class SpecTriggerinRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerprein

class SpecTriggerunRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptRenderer(SpecSectionRenderer):
	'''
	TODO
	@cvar obj: TODO
	'''
	obj = SpecStVerifyscript

