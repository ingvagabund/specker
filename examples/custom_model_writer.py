# -*- coding: utf-8 -*-
'''
Example of a custom model writer

C{./specker examples/custom_model_writer.spec --provides-remove="/bin/cp" --custom-model-writer=examples/custom_model_writer.py}

@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
'''

import cStringIO
from modules.specToken import SpecTokenList
from modules.specSection import SpecStDefinition, SpecStFiles
from modules.specModelTransformator import SpecModelWriter

class MySpecModelWriter(SpecModelWriter):
	def remove(self, section):
		def remove_from_files(what):
			files = self.model.find_section(SpecStFiles)
			if len(files) > 1:
				raise SpecNotImplemented("Cannot remove from multiple %files sections")
			if len(files) == 0:
				return

			files_section = files[0]

			output = cStringIO.StringIO()
			new_tokens = SpecTokenList()
			token_list = files_section.get_tokens()

			line = token_list.get_line()
			while line:
				line.write(output)
				print what
				print output.getvalue()
				if what not in output.getvalue():
					new_tokens.token_list_append_items(line)
				line = token_list.get_line()
				output.truncate(0)

			files_section.set_tokens(new_tokens)
			output.close()

		if issubclass(section.__class__, SpecStDefinition):
			remove_from_files(section.get_value().get_raw().split('/')[-1])

custom_model_writer = MySpecModelWriter

