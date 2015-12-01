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
	A spec renderer
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
		Register a spec renderer
		@param renderer: renderer to be registered
		@type renderer: L{SpecSectionRenderer}
		@rtype: None
		@return: None
		@raise SpecNotFound: if provided renderer cannot be registered e.g. invalid renderer
		@todo: move to SpecManipulator
		'''
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
		Render a list of sections
		@param l: a list to be rendered
		@type l: list of L{SpecSection}
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		for section in l:
			self.render_section(section, f)

	def render(self, f):
		'''
		Render whole model to a file
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		self.render_list(self.model.getSections(), f)

	def render_section(self, s, f):
		'''
		Render a section
		@param s: a section to be rendered
		@type s: L{SpecSection}
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		@raise SpecNotImplemented: if renderer for the section is not registered
		'''
		found = False
		for renderer in self.RENDERERS:
			if issubclass(s.__class__, renderer.obj):
				found = True
				renderer(s).render(f, self)
		if not found:
			raise SpecNotImplemented("Not implemented renderer")

	def find_section_print(self, section_type, f = sys.stdout, verbose = True):
		'''
		Find a section of a type and print/render it
		@param section_type: a section type to be found
		@type section_type: __class__
		@param f: a file to render to
		@type f: file
		@param verbose: if true, raise an exception if a section is not found
		@type verbose: Boolean
		@return: list of sections which were printed
		@rtype: list of L{SpecSection}
		@raise SpecNotFound: if no section was printed
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
		Find a definition and print/render it
		@param defs: definitions to print from
		@type defs: list of L{SpecSection}
		@param definition: definition to be printed
		@type defs: re
		@param packages: packages from definitions should be printed
		@type packages: list of strings
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
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

	def provides_show(self, packages, f = sys.stdout):
		'''
		Show provides for a specific package
		@param packages: list of packages to show provides for
		@type packages: list of strings
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('Provides:'), packages, f)

	def requires_show(self, packages, f = sys.stdout):
		'''
		Show requires for a specific package
		@param packages: list of packages to show requires for
		@type packages: list of strings
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('Requires:'), packages, f)

	def buildrequires_show(self, packages, f = sys.stdout):
		'''
		Show buildrequires for a specific package
		@param packages: list of packages to show buildrequires for
		@type packages: list of strings
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		defs = self.find_definitions_all(self.model.getSections())
		self.print_definitions(defs, re.compile('BuildRequires:'), packages, f)

	def changelog_show(self, f = sys.stdout):
		'''
		Show changelog section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStChangelog, f)

	def description_show(self, packages = None, f = sys.stdout):
		'''
		Show description section
		@param packages: a file to render to
		@type packages: file
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		# TODO: do this for a specific package
		return self.find_section_print(SpecStDescription, f)

	def build_show(self, f = sys.stdout):
		'''
		Show build section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStBuild, f)

	def check_show(self, f = sys.stdout):
		'''
		Show check section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStCheck, f)

	def clean_show(self, f = sys.stdout):
		'''
		Show clean section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStClean, f)

	def files_show(self, f = sys.stdout):
		'''
		Show files section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		self.find_section_print(SpecStFiles, f)

	def install_show(self, f = sys.stdout):
		'''
		Show install section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStInstall, f)

	def package_show(self, f = sys.stdout):
		'''
		Show package section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		# TODO: do this for specific packages
		return self.find_section_print(SpecStPackage, f)

	def prep_show(self, f = sys.stdout):
		'''
		Show prep section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPrep, f)

	def pre_show(self, f = sys.stdout):
		'''
		Show pre section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPre, f)

	def post_show(self, f = sys.stdout):
		'''
		Show post section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPost, f)

	def preun_show(self, f = sys.stdout):
		'''
		Show preun section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPreun, f)

	def postun_show(self, f = sys.stdout):
		'''
		Show postun section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPostun, f)

	def pretrans_show(self, f = sys.stdout):
		'''
		Show pretrans section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPretrans, f)

	def posttrans_show(self, f = sys.stdout):
		'''
		Show posttrans section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPosttrans, f)

	def triggerin_show(self, f = sys.stdout):
		'''
		Show triggerin section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStTriggerin, f)

	def triggerprein_show(self, f = sys.stdout):
		'''
		Show triggerprein section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStTriggerprein, f)

	def triggerun_show(self, f = sys.stdout):
		'''
		Show triggerun section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStTriggerun, f)

	def triggerpostun_show(self, f = sys.stdout):
		'''
		Show triggerpostun section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStPostun, f)

	def verifyscript_show(self, f = sys.stdout):
		'''
		Show verifyscript section
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		return self.find_section_print(SpecStVerifyscript, f)

class SpecSectionRenderer(object):
	'''
	Generic section renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStSection

	def __init__(self, section):
		'''
		Init
		@param section: section to be rendered
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.section = section

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
		'''
		self.section.getTokenSection().write(f)
		self.section.getTokens().write(f)

class SpecExpressionRenderer(object):
	'''
	Expression renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStExpression

	def __init__(self, section):
		'''
		Init
		@param section: section to be rendered
		@type section: L{SpecSection}
		@return: None
		@rtype: None
		'''
		self.section = section

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
		'''
		for token in self.section.getTokens():
			token.write(f)

class SpecIfRenderer(SpecSectionRenderer):
	'''
	%if renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStIf

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
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
	%global renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStGlobal

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
		'''
		self.section.getGlobalToken().write(f)
		self.section.getVariable().write(f)
		SpecExpressionRenderer(self.section.getValue()).render(f, ctx)

class SpecBuildRenderer(SpecSectionRenderer):
	'''
	%build renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStBuild

class SpecChangelogRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStChangelog

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
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
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStCheck

class SpecCleanRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStClean

class SpecDescriptionRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStDescription

class SpecFilesRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStFiles

class SpecInstallRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStInstall

class SpecPackageRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPackage

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
		'''
		self.section.getTokenSection().write(f)
		if self.section.getPackage():
			self.section.getPackage().write(f)
		ctx.render_list(self.section.getDefs(), f)

class SpecPrepRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPrep

class SpecPreRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPre

class SpecPostRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPost

class SpecPreunRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPreun

class SpecPostunRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPostun

class SpecPretransRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPretrans

class SpecPosttransRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStPosttrans

class SpecDefinitionRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStDefinition

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecRenderer}
		@return: None
		@rtype: None
		'''
		self.section.getName().write(f)
		self.section.getValue().write(f)

class SpecTriggerRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTrigger

class SpecTriggerinRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTriggerin

class SpecTriggerpreinRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTriggerprein

class SpecTriggerunRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTriggerun

class SpecTriggerpostunRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTriggerpostun

class SpecVerifyscriptRenderer(SpecSectionRenderer):
	'''
	%changelog renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStVerifyscript

