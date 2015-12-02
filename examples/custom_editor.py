# -*- coding: utf-8 -*-
'''
Example of a custom editor

C{./specker --custom-editor="examples/custom_editor.py" examples/custom_editor.spec --install-edit="777"}

@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
'''

from modules.specDefaultEditor import SpecInstallEditor
from modules.specToken import SpecToken

# This is only an example, it does not cover all possible positions, it is only
# for demostrating purposes - how to use specker-lib
class MyChangelogEditor(SpecInstallEditor):
	@classmethod
	def edit(cls, section, replacement):
		tokens = section.get_tokens()

		idx = 0
		while idx < len(tokens):
			if str(tokens[idx]) == 'install':
				while idx + 1 < len(tokens) and tokens[idx].same_line(tokens[idx + 1]):
					idx += 1
					if str(tokens[idx]) == '-m':
						idx_rep = idx + 1
						while (idx + 1 < len(tokens) and tokens[idx].same_line(tokens[idx + 1])) \
								or str(tokens[idx]) == 'tcsh.man':
							if str(tokens[idx]) == 'tcsh.man':
								tokens[idx_rep] = SpecToken.create(replacement)
								return
							idx += 1
			else:
				idx += 1

custom_editors = [ MyChangelogEditor ]

