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

import re
import sys
import cStringIO
from specDebug import SpecDebug
from specError import SpecNotFound, SpecNotImplemented
from specModelRenderer import SpecModelRenderer
from specSection import *

class SpecFileRenderer(SpecModelRenderer):
	'''
	A spec renderer
	'''
	def __init__(self, reader):
		self.set_model_reader(reader)
		self.MANIPULATORS = [
				SpecIfRenderer,
				SpecTagRenderer,
				SpecDefinitionRenderer,
				SpecGlobalRenderer,
				SpecDefineRenderer,
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
		self.render_list(self.get_model_reader().get_sections(), f)

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
		for renderer in self.MANIPULATORS:
			if issubclass(s.__class__, renderer.obj):
				found = True
				SpecDebug.debug("- rendering section '%s'" % type(s))
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
		s = self.get_model_reader().find_section(section_type)

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
		@type definition: re
		@param packages: packages from definitions should be printed
		@type packages: list of strings
		@param f: a file to render to
		@type f: file
		@return: None
		@rtype: None
		'''
		for d in defs:
			if definition.match(str(d.name)):
				pkg = d.get_package()
				if pkg:
					pkg = pkg.get_package()
				if str(pkg) in packages or (pkg is None and '-' in packages) or '*' in packages:
					if pkg is None:
						f.write('-:')
					else:
						pkg.write(f, raw = True)
						f.write(':') # add delim since raw

					d.get_value().write(f, raw = True)
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
		defs = self.get_model_reader().find_definitions_all()
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
		defs = self.get_model_reader().find_definitions_all()
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
		defs = self.get_model_reader().find_definitions_all()
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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_token_section().write(f)
		self.section.get_tokens().write(f)

	def raw_string(self, ctx):
		'''
		Get raw section representation
		@param ctx: a rendering context
		@type ctx: L{SpecModelRenderer}
		@return: raw string of a section
		@rtype: string
		'''
		output = cStringIO.StringIO()
		self.render(output, ctx)
		ret = ret.getvalue()
		output.close()
		return ret

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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		for token in self.section.get_tokens():
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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_if_token().write(f)
		SpecExpressionRenderer(self.section.get_expr()).render(f, ctx)
		ctx.render_list(self.section.get_true_branch(), f)
		if self.section.get_else_token():
			self.section.get_else_token().write(f)
			ctx.render_list(self.section.get_false_branch(), f)
		self.section.get_endif_token().write(f)

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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_global_token().write(f)
		self.section.get_variable().write(f)
		SpecExpressionRenderer(self.section.get_value()).render(f, ctx)

class SpecDefineRenderer(SpecSectionRenderer):
	'''
	%define renderer
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStDefine

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_define_token().write(f)
		self.section.get_variable().write(f)
		SpecExpressionRenderer(self.section.get_value()).render(f, ctx)

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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_token_section().write(f)

		for entry in self.section.get_entries():
			entry.get_star().write(f)
			entry.get_date().write(f)
			entry.get_user().write(f)
			entry.get_user_email().write(f)
			if entry.get_version_delim():
				entry.get_version_delim().write(f)
			entry.get_version().write(f)
			entry.get_message().write(f)

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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_token_section().write(f)
		if self.section.get_package():
			self.section.get_package().write(f)
		ctx.render_list(self.section.get_defs(), f)

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

class SpecTagRenderer(SpecSectionRenderer):
	'''
	tag renderer (%license, %doc, ...)
	@cvar obj: sections rendered by this renderer
	'''
	obj = SpecStTag

	def render(self, f, ctx):
		'''
		Render section
		@param f: a file to render to
		@type f: file
		@param ctx: a rendering context
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_name().write(f)
		self.section.get_value().write(f)

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
		@type ctx: L{SpecModelRenderer}
		@return: None
		@rtype: None
		'''
		self.section.get_name().write(f)
		self.section.get_value().write(f)

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

