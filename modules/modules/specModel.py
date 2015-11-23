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

class SpecModel(object):
	# Default section order in a spec file
	SPEC_SECTION_ORDER = [
				SpecStDescription,
				SpecStPackage,
				SpecStPrep,
				SpecStBuild,
				SpecStClean,
				SpecStInstall,
				SpecStCheck,
				SpecStPost,
				SpecStPreun,
				SpecStPostun,
				SpecStPre,
				SpecStPretrans,
				SpecStPosttrans,
				SpecStTrigger,
				SpecStTriggerin,
				SpecStTriggerprein,
				SpecStTriggerun,
				SpecStTriggerpostun,
				SpecStVerifyscript,
				SpecStFiles,
				SpecStChangelog
			]

	def __init__(self):
		self.sections = []

	def append(self, section):
		self.sections.append(section)

	def remove(self, section):
		self.sections.remove(section)

	def append_items(self, array):
		for item in array:
			self.sections.append(item)

	def add(self, section):
		# add section based on order
		raise ValueError("Not Implemented")

	def getSections(self):
		return self.sections

	def find_section(self, section):
		ret = None
		for s in self.sections:
			if issubclass(s.__class__, section):
				if not ret:
					ret = []
				ret.append(s)
		return ret

