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

from specStatement import *

class SpecManipulator:
	class ChunkParser:
		def __init__(self, token, manipulator):
			self.token = token
			self.setManipulator(manipulator)

		def __str__(self):
			return self.token

		def __eq__(self, other):
			return self.token == other.token

		def parse(self, token_list, parent, allowed, disallowed):
			return self.manipulator.parse(token_list, parent, allowed, disallowed)

		def getManipulator(self):
			return self.manipulator

		def setManipulator(self, manipulator):
			self.manipulator = manipulator

	BUILD_T 				= ChunkParser('%build', SpecStBuild)
	CHANGELOG_T 		= ChunkParser('%changelog', SpecStChangelog)
	CHECK_T 				= ChunkParser('%check', SpecStCheck)
	CLEAN_T 				= ChunkParser('%clean', SpecStClean)
	DESCRIPTION_T 		= ChunkParser('%description', SpecStDescription)
	FILES_T 				= ChunkParser('%files', SpecStFiles)
	INSTALL_T 			= ChunkParser('%install', SpecStInstall)
	PACKAGE_T 			= ChunkParser('%package', SpecStPackage)
	PREP_T 				= ChunkParser('%prep', SpecStPrep)
	PRE_T 				= ChunkParser('%pre', SpecStPre)
	POST_T 				= ChunkParser('%post', SpecStPost)
	PREUN_T 				= ChunkParser('%preun', SpecStPreun)
	POSTUN_T 			= ChunkParser('%postun', SpecStPostun)
	PRETRANS_T 			= ChunkParser('%pretrans', SpecStPretrans)
	POSTTRANS_T			= ChunkParser('%posttrans', SpecStPosttrans)
	TRIGGER_T 			= ChunkParser('%trigger', SpecStTrigger)
	TRIGGERIN_T 		= ChunkParser('%triggerin', SpecStTriggerin)
	TRIGGERPREIN_T 	= ChunkParser('%triggerprein', SpecStTriggerprein)
	TRIGGERUN_T 		= ChunkParser('%triggerun', SpecStTriggerun)
	TRIGGERPOSTUN_T 	= ChunkParser('%triggerpostun', SpecStTriggerpostun)
	VERIFYSCRIPT_T 	= ChunkParser('%verifyscript', SpecStVerifyscript)
	SECTION_TS			= [
						BUILD_T, CHANGELOG_T, CHECK_T, CLEAN_T, DESCRIPTION_T,
						FILES_T, INSTALL_T, PACKAGE_T, PREP_T, PRE_T, POST_T,
						PREUN_T, POSTUN_T, PRETRANS_T, POSTTRANS_T, TRIGGER_T,
						TRIGGERIN_T, TRIGGERPREIN_T, TRIGGERUN_T, TRIGGERPOSTUN_T,
						VERIFYSCRIPT_T
						]
	#
	IF_T					= ChunkParser('%if', SpecStIf)
	GLOBAL_T				= ChunkParser('%global', SpecStGlobal)
	# Definitions
	NAME_T				= ChunkParser('Name:', SpecStDefinition)
	VERSION_T			= ChunkParser('Version:', SpecStDefinition)
	RELEASE_T			= ChunkParser('Release:', SpecStDefinition)
	SUMMARY_T			= ChunkParser('Summary:', SpecStDefinition)
	LICENSE_T			= ChunkParser('License:', SpecStDefinition)
	URL_T					= ChunkParser('URL:', SpecStDefinition)
	SOURCE_T				= ChunkParser('Source:', SpecStDefinition)
	EXCLUSIVEARCH_T	= ChunkParser('ExclusiveArch:', SpecStDefinition)
	BUILDREQUIRES_T	= ChunkParser('BuildRequires:', SpecStDefinition)
	REQUIRES_T			= ChunkParser('Requires:', SpecStDefinition)
	PROVIDES_T			= ChunkParser('Provides:', SpecStDefinition)
	DEFINITION_TS		= [
						NAME_T, VERSION_T, RELEASE_T, SUMMARY_T, LICENSE_T, URL_T,
						SOURCE_T, EXCLUSIVEARCH_T, BUILDREQUIRES_T, REQUIRES_T,
						PROVIDES_T
						]

	ALL_TS				= SECTION_TS + [IF_T, GLOBAL_T] + DEFINITION_TS

	logger = None

	def __init__(self):
		pass

	def setLoggingLevel(self, level):
		SpecManipulator.logger.setLevel(level)

	def register_manipulator(self, manipulator):
		for cp in self.ALL_TS:
			if issubclass(manipulator, cp.getManipulator()):
				cp.setManipulator(manipulator)
				break

	def print_str(self):
		ret = ""
		for s in self.statements:
			ret += s.print_str()
		return ret

	def print_file(self, f):
		for s in self.statements:
			s.print_file(f)

