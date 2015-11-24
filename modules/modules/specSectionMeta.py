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
specker-lib - metadata of L{SpecSection} and inherited classes
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

class SpecSectionMeta(type):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "generic spec Section"

class SpecStIfMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%if"

class SpecStDefinitionMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec definition"

class SpecStGlobalMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%global"

class SpecStEofMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "<EOF>"

class SpecStExpressionMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec expression"

class SpecStSectionMeta(SpecSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "generic spec section"

class SpecStDescriptionMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%description"

class SpecStBuildMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%build"

class SpecStChangelogEntryMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec changelog entry"

class SpecStChangelogMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%changelog"

class SpecStCheckMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%check"

class SpecStCleanMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%clean"

class SpecStFilesMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%files"

class SpecStInstallMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%install"

class SpecStPackageMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%package"

class SpecStPrepMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%prep"

class SpecStPreMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%pre"

class SpecStPostMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%post"

class SpecStPreunMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%preun"

class SpecStPostunMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%postun"

class SpecStPretransMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%pretrans"

class SpecStPosttransMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%posttrans"

class SpecStTriggerMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerin"

class SpecStTriggerinMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerin"

class SpecStTriggerpreinMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerprein"

class SpecStTriggerunMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerpreun"

class SpecStTriggerpostunMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerpostun"

class SpecStVerifyscriptMeta(SpecStSectionMeta):
	'''
	TODO
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%verifyscript"


