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
Metadata of L{SpecSection} and derived classes
@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
@organization: Red Hat Inc.
@license: GPL 2.0
'''

class SpecSectionMeta(type):
	'''
	metaclass for L{SpecSection}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "generic spec Section"

class SpecStIfMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStIf}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%if"

class SpecStDefinitionMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStDefinition}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec definition"

class SpecStGlobalMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStGlobal}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%global"

class SpecStDefineMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStDefine}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%define"

class SpecStEofMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStEof}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "<EOF>"

class SpecStExpressionMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStExpression}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec expression"

class SpecStSectionMeta(SpecSectionMeta):
	'''
	metaclass for L{SpecStSection}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "generic spec section"

class SpecStDescriptionMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStDescription}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%description"

class SpecStBuildMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStBuild}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%build"

class SpecStChangelogEntryMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStChangelog} entry
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "spec changelog entry"

class SpecStChangelogMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStChangelog}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%changelog"

class SpecStCheckMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStCheck}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%check"

class SpecStCleanMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStClean}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%clean"

class SpecStFilesMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStFiles}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%files"

class SpecStInstallMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStInstall}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%install"

class SpecStPackageMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPackage}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%package"

class SpecStPrepMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPrep}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%prep"

class SpecStPreMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPre}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%pre"

class SpecStPostMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPost}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%post"

class SpecStPreunMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPreun}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%preun"

class SpecStPostunMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPostun}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%postun"

class SpecStPretransMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPretrans}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%pretrans"

class SpecStPosttransMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStPosttrans}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%posttrans"

class SpecStTriggerMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStTrigger}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerin"

class SpecStTriggerinMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStTriggerin}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerin"

class SpecStTriggerpreinMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStTriggerprein}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerprein"

class SpecStTriggerunMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStTriggerun}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerpreun"

class SpecStTriggerpostunMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStTriggerpostun}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%triggerpostun"

class SpecStVerifyscriptMeta(SpecStSectionMeta):
	'''
	metaclass for L{SpecStVerifyscript}
	'''
	def __repr__(c):
		'''
		section representation
		'''
		return "%verifyscript"

