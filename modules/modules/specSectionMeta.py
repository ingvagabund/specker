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

class SpecSectionMeta(type):
	def __repr__(c):
		return "generic spec Section"

class SpecStIfMeta(SpecSectionMeta):
	def __repr__(c):
		return "%if"

class SpecStDefinitionMeta(SpecSectionMeta):
	def __repr__(c):
		return "spec definition"

class SpecStGlobalMeta(SpecSectionMeta):
	def __repr__(c):
		return "%global"

class SpecStEofMeta(SpecSectionMeta):
	def __repr__(c):
		return "<EOF>"

class SpecStExpressionMeta(SpecSectionMeta):
	def __repr__(c):
		return "spec expression"

class SpecStSectionMeta(SpecSectionMeta):
	def __repr__(c):
		return "generic spec section"

class SpecStDescriptionMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%description"

class SpecStBuildMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%build"

class SpecStChangelogEntryMeta(SpecStSectionMeta):
	def __repr__(c):
		return "spec changelog entry"

class SpecStChangelogMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%changelog"

class SpecStCheckMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%check"

class SpecStCleanMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%clean"

class SpecStFilesMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%files"

class SpecStInstallMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%install"

class SpecStPackageMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%package"

class SpecStPrepMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%prep"

class SpecStPreMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%pre"

class SpecStPostMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%post"

class SpecStPreunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%preun"

class SpecStPostunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%postun"

class SpecStPretransMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%pretrans"

class SpecStPosttransMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%posttrans"

class SpecStTriggerMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerin"

class SpecStTriggerinMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerin"

class SpecStTriggerpreinMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerprein"

class SpecStTriggerunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerpreun"

class SpecStTriggerpostunMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%triggerpostun"

class SpecStVerifyscriptMeta(SpecStSectionMeta):
	def __repr__(c):
		return "%verifyscript"


