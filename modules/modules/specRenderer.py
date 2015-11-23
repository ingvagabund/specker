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

from specSection import *
from specManipulator import SpecManipulator

class SpecRenderer(SpecManipulator):
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

	def render_list(self, l, f):
		for section in l:
			found = False
			for renderer in self.RENDERERS:
				if issubclass(section.__class__, renderer.obj):
					found = True
					renderer(section).render(f, self)
			if not found:
				raise NotImplementedError("Not implemented renderer")

	def render(self, f):
		self.render_list(self.model.getSections(), f)

	def setModel(self, model):
		self.model = model

	def getModel(self):
		return self.model

class SpecSectionRenderer(object):
	obj = SpecStSection

	def __init__(self, section):
		self.section = section

	def render(self, f, ctx):
		self.section.getTokenSection().write(f)
		self.section.getTokens().write(f)

class SpecIfRenderer(SpecSectionRenderer):
	obj = SpecStIf

	def render(self, f, ctx):
		self.section.getIfToken().write(f)
		self.section.getExpr().write(f)
		ctx.render_list(self.section.getTrueBranch(), f)
		if self.section.getElseToken():
			self.section.getElseToken().write(f)
			ctx.render_list(self.section.getFalseBranch(), f)
		self.section.getEndifToken().write(f)

class SpecGlobalRenderer(SpecSectionRenderer):
	obj = SpecStGlobal

	def render(self, f, ctx):
		self.section.getGlobalToken().write(f)
		self.section.getVariable().write(f)
		self.section.getValue().write(f)

class SpecBuildRenderer(SpecSectionRenderer):
	obj = SpecStBuild

class SpecChangelogRenderer(SpecSectionRenderer):
	obj = SpecStChangelog

	def render(self, f, ctx):
		self.section.getTokenSection().write(f)

		for item in self.section.getItems():
			item.getStar().write(f)
			item.getDate().write(f) # TODO
			item.getUser().write(f) # TODO
			item.getUserEmail().write(f)
			item.getVersionDelim().write(f)
			item.getVersion().write(f)
			item.getMessage().write(f)

class SpecCheckRenderer(SpecSectionRenderer):
	obj = SpecStCheck

class SpecCleanRenderer(SpecSectionRenderer):
	obj = SpecStClean

class SpecDescriptionRenderer(SpecSectionRenderer):
	obj = SpecStDescription

class SpecFilesRenderer(SpecSectionRenderer):
	obj = SpecStFiles

class SpecInstallRenderer(SpecSectionRenderer):
	obj = SpecStInstall

class SpecPackageRenderer(SpecSectionRenderer):
	obj = SpecStPackage

	def render(self, f, ctx):
		self.section.getTokenSection().write(f)
		if self.section.getPackage():
			self.section.getPackage().write(f)
		ctx.render_list(self.section.getDefs(), f)

class SpecPrepRenderer(SpecSectionRenderer):
	obj = SpecStPrep

class SpecPreRenderer(SpecSectionRenderer):
	obj = SpecStPre

class SpecPostRenderer(SpecSectionRenderer):
	obj = SpecStPost

class SpecPreunRenderer(SpecSectionRenderer):
	obj = SpecStPreun

class SpecPostunRenderer(SpecSectionRenderer):
	obj = SpecStPostun

class SpecPretransRenderer(SpecSectionRenderer):
	obj = SpecStPretrans

class SpecPosttransRenderer(SpecSectionRenderer):
	obj = SpecStPosttrans

class SpecDefinitionRenderer(SpecSectionRenderer):
	obj = SpecStDefinition

	def render(self, f, ctx):
		self.section.getName().write(f)
		self.section.getValue().write(f)

class SpecTriggerRenderer(SpecSectionRenderer):
	obj = SpecStTrigger

class SpecTriggerinRenderer(SpecSectionRenderer):
	obj = SpecStTriggerin

class SpecTriggerpreinRenderer(SpecSectionRenderer):
	obj = SpecStTriggerprein

class SpecTriggerunRenderer(SpecSectionRenderer):
	obj = SpecStTriggerun

class SpecTriggerpostunRenderer(SpecSectionRenderer):
	obj = SpecStTriggerpostun

class SpecVerifyscriptRenderer(SpecSectionRenderer):
	obj = SpecStVerifyscript

