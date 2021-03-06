# $Id: __init__.py 4564 2006-05-21 20:44:42Z wiemann $
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
PSEP HTML Writer.
"""

__docformat__ = 'reStructuredText'


import sys
import os
import os.path
import codecs
import docutils
from docutils import frontend, nodes, utils, writers
from docutils.writers import html4css1


class Writer(html4css1.Writer):

    default_stylesheet = 'psep.css'

    default_stylesheet_path = utils.relative_path(
        os.path.join(os.getcwd(), 'dummy'),
        os.path.join(os.path.dirname(__file__), default_stylesheet))

    default_template = 'template.txt'

    default_template_path = utils.relative_path(
        os.path.join(os.getcwd(), 'dummy'),
        os.path.join(os.path.dirname(__file__), default_template))

    settings_spec = html4css1.Writer.settings_spec + (
        'PSEP/HTML-Specific Options',
        'For the PSEP/HTML writer, the default value for the --stylesheet-path '
        'option is "%s", and the default value for --template is "%s". '
        'See HTML-Specific Options above.'
        % (default_stylesheet_path, default_template_path),
        (('Python\'s home URL.  Default is "http://www.python.org".',
          ['--python-home'],
          {'default': 'http://www.pyside.org', 'metavar': '<URL>'}),
         ('Home URL prefix for PSEPs.  Default is "." (current directory).',
          ['--psep-home'],
          {'default': '.', 'metavar': '<URL>'}),
         # For testing.
         (frontend.SUPPRESS_HELP,
          ['--no-random'],
          {'action': 'store_true', 'validator': frontend.validate_boolean}),))

    settings_default_overrides = {'stylesheet_path': default_stylesheet_path,
                                  'template': default_template_path,}

    relative_path_settings = (html4css1.Writer.relative_path_settings
                              + ('template',))

    config_section = 'psep_html writer'
    config_section_dependencies = ('writers', 'html4css1 writer')

    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator

    def interpolation_dict(self):
        subs = html4css1.Writer.interpolation_dict(self)
        settings = self.document.settings
        pyhome = settings.python_home
        subs['pyhome'] = pyhome
        subs['psephome'] = settings.psep_home
        if pyhome == '..':
            subs['psepindex'] = '.'
        else:
            subs['psepindex'] = pyhome + '/docs/pseps'
        index = self.document.first_child_matching_class(nodes.field_list)
        header = self.document[index]
        self.psepnum = header[0][1].astext()
        subs['psep'] = self.psepnum
        if settings.no_random:
            subs['banner'] = 0
        else:
            import random
            subs['banner'] = random.randrange(64)
        try:
            subs['psepnum'] = '%04i' % int(self.psepnum)
        except ValueError:
            subs['psepnum'] = psepnum
        self.title = header[1][1].astext()
        subs['title'] = self.title
        subs['body'] = ''.join(
            self.body_pre_docinfo + self.docinfo + self.body)
        return subs

    def assemble_parts(self):
        html4css1.Writer.assemble_parts(self)
        self.parts['title'] = [self.title]
        self.parts['psepnum'] = self.psepnum


class HTMLTranslator(html4css1.HTMLTranslator):

    def depart_field_list(self, node):
        html4css1.HTMLTranslator.depart_field_list(self, node)
        if 'rfc2822' in node['classes']:
             self.body.append('<hr />\n')
