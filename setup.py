__version__ = "$Revision$"

import os
import sys
import glob

try:
    from setuptools import setup, Extension
except ImportError:
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
elif sys.platform in ('freebsd4', 'freebsd5', 'freebsd6', 'freebsd7', 'freebsd8'):
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


if 0:
    print 'Macros:'
    for name, value in sorted(macros.iteritems()):
        print '\t%s = %r' % (name, value)
    print '\nLibraries:\n\t%r\n' % ', '.join(libraries)
    print '\Sources:\n\t%r\n' % ', '.join(multiprocessing_srcs)


extensions = [
    Extension('multiprocessing._multiprocessing',
              sources=multiprocessing_srcs,
              define_macros=macros.items(),
              libraries=libraries,
              include_dirs=["Modules/_multiprocessing"],
              depends=(glob.glob('Modules/_multiprocessing/*.h') +
                       ['setup.py'])
              ),
    ]

if sys.version_info < (2, 5):
    # Python 2.4's mmap doesn't support anonymous memory
    extensions.append(
        Extension('multiprocessing._mmap25', 
	          sources=["Modules/mmapmodule.c"])
        )

packages = [
    'multiprocessing',
    'multiprocessing.dummy',
    'multiprocessing.examples',
    ]

package_dir = {
    'multiprocessing': 'Lib/multiprocessing',
    'multiprocessing.examples': 'examples'
    }

here = os.path.dirname(os.path.abspath(__file__))

setup(
    name='multiprocessing',
    version="2.6.0-0.1",
    description=('Backport of the multiprocessing package to '
                 'Python 2.4 and 2.5'),
    long_description=open(os.path.join(here, 'README.txt')).read(),
    packages=packages,
    package_dir=package_dir,
    #package_data=package_data,
    ext_modules=extensions,
    author='R Oudkerk / Python Software Foundation',
    author_email='python-dev@python.org',
    maintainer='Christian Heimes',
    maintainer_email="christian at cheimes dot de",
    url='http://code.google.com/p/python-multiprocessing',
    license='BSD Licence',
    platforms='Unix and Windows',
    keywords="",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )

