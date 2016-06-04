#! /usr/bin/env python

from __future__ import print_function
import getopt
import os
from textwrap import dedent, wrap
import string
import sys
from jinja2 import Environment, FileSystemLoader
from jinja2.exceptions import TemplateNotFound
import yaml

def main(file_name, outfile_name, **options):
    with open(file_name, "r") as f:
        data = yaml.load(f)
    junk, ext = os.path.splitext(outfile_name)
    if ext == '.tex':
        write_latex(data, outfile_name)
    elif ext == '.html':
        write_html(data, outfile_name, **options)
    elif ext == '.txt':
        write_text(data, outfile_name)
    else:
        print("Unknown output format, '{0}'.".format(ext), file=sys.stderr)
        sys.exit(1)

def get_template_folder():
    """
    Return the path to the template folder.
    """
    thisdir = os.path.dirname(__file__)
    return os.path.join(thisdir, "templates")

def write_html(data, outfile_name, **options):
    """
    Produce HTML output.
    """
    loader = FileSystemLoader(get_template_folder())
    env = Environment()
    try:
        templ = loader.load(env, "html.jinja2")
    except TemplateNotFound:
        raise ViewNotImplementedError("The template '%s' was not found." % name)
    symbols = {'data': data}
    symbols.update(options)
    with open(outfile_name, "w") as fout:
        fout.write(templ.render(symbols))

def escape_latex(expr):
    return unicode(expr).replace("#", "\#")


def usage():
    print("Usage: {0} <data.yaml> <outfile>".format(sys.argv[0]), file=sys.stderr)
    print(dedent("""\
-- Options --
-h, --help
-V, --version
-p, --public                            ; Output is to be published on a public
                                        ; web site.  Some personal information
                                        ; will be excluded.

""".strip()), file=sys.stderr)

if __name__ == "__main__":
    #Defaults
    public_flag = False
    #Process command line options and arguments.
    try:
        opts, argv = getopt.gnu_getopt(sys.argv[1:],
                'hVp', [
                    'help',
                    'version',
                    'public',])
    except getopt.GetoptError, e:
        print >> sys.stderr, e.msg
        usage(sys.argv[0])
        sys.exit(STATUS_ERROR)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-V', '--version'):
            print >> sys.stderr, '1.0'
            sys.exit(0)
        elif opt in ('-p', '--public'):
            public_flag = True
        else:
            print >> sys.stderr, "Unknown option, %s." % opt
            usage()
            sys.exit(1)
            
    if len(argv) != 2:
        usage()
        sys.exit(1)
    file_name = argv[0]
    outfile_name = argv[1]
    main(file_name, outfile_name, 
        public_flag=public_flag)


