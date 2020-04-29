from os import getcwd, listdir, sep
from os.path import basename, isdir, isfile, join, normpath, splitext
import sys

class Options(object):
    def __init__(self):
        self.dirs = None

def process_args(argv):
    options = Options()
    if len(argv) == 1:
        options.dirs = ['.']
    else:
        options.dirs = [a for a in argv[1:]]
    return options

def modify_sys_path():
    sys.path.insert(0, getcwd())

def analyse_class(klass):
    return dict([
        (name, value)
        for name, value in klass.__dict__.iteritems()
    ])

def is_a_module(fullname, base):
    return fullname.endswith('.py') and base != '__init__.py'

def get_attr(obj, name):
    if hasattr(obj, name):
        return getattr(obj, name)

def analyse_module(filename):
    # TODO: doesn't work with directory specified as '.'
    modulename = splitext(filename)[0].replace(sep, '.')
    __import__(modulename)
    module = sys.modules[modulename]
    contents = []
    for name, value in module.__dict__.iteritems():
        if (
            not name.startswith('_') and
            hasattr(value, '__module__') and
            getattr(value, '__module__') == modulename
        ):
            contents.append((name, value))
    return contents

def is_a_package(filename):
    return isdir(filename) and isfile(join(filename, '__init__.py'))

def analyse_package(dirname):
    contents = {}
    for filename in listdir(dirname):
        fullname = normpath(join(dirname, filename))
        base = basename(filename)
        if is_a_module(fullname, base):
            contents[base] = analyse_module(fullname)
        if is_a_package(fullname):
            contents[base] = analyse_package(fullname)
    return contents

def display(contents, indent=0):
    if isinstance(contents, dict):
        for name, value in sorted(contents.items()):
            print '%s%s' % ('    ' * indent, name)
            display(value, indent=indent+1)
    elif isinstance(contents, (list, set)):
        for value in sorted(contents):
            display(value, indent=indent)
    else:
        name, value = contents
        if isinstance(value, type):
            print '%s%s' % ('    ' * indent, name)

def main():
    options = process_args(sys.argv)
    modify_sys_path()
    contents = {}
    for dirname in options.dirs:
        contents.update({dirname: analyse_package(dirname)})
    display(contents)

if __name__ == '__main__':
    main()

