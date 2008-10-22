# Autodetecting setup.py script for building the Python extensions
#

__version__ = "$Revision$"

import os
import sys
import glob

from distutils.core import setup, Extension

if sys.version_info < (2, 4):
    raise ValueError("Versions of Python before 2.4 are not supported")

if sys.platform == 'win32': # Windows
    macros = dict()
    libraries = ['ws2_32']

elif sys.platform.startswith('darwin'): # Mac OSX
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
        HAVE_BROKEN_SEM_GETVALUE=1
        )
    libraries = []

elif sys.platform.startswith('cygwin'): # Cygwin
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=1,
        HAVE_FD_TRANSFER=0,
        HAVE_BROKEN_SEM_UNLINK=1
        )
    libraries = []

elif sys.platform in ('freebsd5', 'freebsd6', 'freebsd7', 'freebsd8'):
    # FreeBSD's P1003.1b semaphore support is very experimental
    # and has many known problems. (as of June 2008)
    macros = dict(                  # FreeBSD
        HAVE_SEM_OPEN=0,
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
        )
    libraries = []

elif sys.platform.startswith('openbsd'):
    macros = dict(                  # OpenBSD
        HAVE_SEM_OPEN=0,            # Not implemented
        HAVE_SEM_TIMEDWAIT=0,
        HAVE_FD_TRANSFER=1,
        )
    libraries = []

else:                                   # Linux and other unices
    macros = dict(
        HAVE_SEM_OPEN=1,
        HAVE_SEM_TIMEDWAIT=1,
        HAVE_FD_TRANSFER=1
        )
    libraries = ['rt']

if sys.platform == 'win32':
    multiprocessing_srcs = ['Modules/_multiprocessing/multiprocessing.c',
                            'Modules/_multiprocessing/semaphore.c',
                            'Modules/_multiprocessing/pipe_connection.c',
                            'Modules/_multiprocessing/socket_connection.c',
                            'Modules/_multiprocessing/win32_functions.c'
                           ]

else:
    multiprocessing_srcs = ['Modules/_multiprocessing/multiprocessing.c',
                            'Modules/_multiprocessing/socket_connection.c'
                           ]

    if macros.get('HAVE_SEM_OPEN', False):
        multiprocessing_srcs.append('Modules/_multiprocessing/semaphore.c')


print 'Macros:'
for name, value in sorted(macros.iteritems()):
    print '\t%s = %r' % (name, value)
print '\nLibraries:\n\t%r\n' % ', '.join(libraries)
print '\Sources:\n\t%r\n' % ', '.join(multiprocessing_srcs)


extensions = [
    Extension('multiprocessing._multiprocessing',
              sources=multiprocessing_srcs,
              define_macros=macros.items(),
              include_dirs=["Modules/_multiprocessing"],
              depends=(glob.glob('Modules/_multiprocessing/*.h') +
                       glob.glob('Modules/_multiprocessing/*.c') + 
                       ['setup.py'])
              ),
    ]

packages = [
    'multiprocessing',
    'multiprocessing.dummy',
    ]

package_dir = {
    'multiprocessing': 'Lib/multiprocessing',
    #'processing.doc': 'doc',
    #'processing.tests': 'tests',
    #'processing.examples': 'examples'
    }

setup(
    name='multiprocessing',
    version="XXX",
    description=('Package for using processes which mimics ' +
                 'the threading module'),
    #long_description=long_description,
    packages=packages,
    package_dir=package_dir,
    #package_data=package_data,
    ext_modules=extensions,
    #author='R Oudkerk',
    #author_email='roudkerk at users.berlios.de',
    #url='http://developer.berlios.de/projects/pyprocessing',
    #license='BSD Licence',
    platforms='Unix and Windows',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        ]
    )
