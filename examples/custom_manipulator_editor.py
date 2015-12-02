# -*- coding: utf-8 -*-
'''
Example of a custom editor manipulator

C{./specker --custom-manipulator-renderer="examples/custom_manipulator_editor.py" examples/custom_manipulator_editor.spec --provides-show="*"}

@author: Fridolin Pokorny
@contact: fpokorny@redhat.com
'''

import StringIO
from modules.specFileRenderer import SpecFileRenderer

# There are plenty of methods how to do this, even in better way. This is only
# for demonstration purposes, could be improved as well...
class MyFileRenderer(SpecFileRenderer):
	def print_definitions(self, defs, definition, packages, f):
		output = StringIO.StringIO()
		SpecFileRenderer.print_definitions(self, defs, definition, packages, output)
		f.write(' Package\t\t| Value    \n ')
		f.write(output.getvalue().replace(':', '\t\t\t| ').replace('\n', '\n '))

custom_manipulator_renderer = MyFileRenderer
