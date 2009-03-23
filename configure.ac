#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(multiprocessing, 0.0, http://code.google.com/p/python-multiprocessing)
AC_CONFIG_HEADER([mpconfig.h])

# We don't use PACKAGE_ variables, and they cause conflicts
# with other autoconf-based packages that include Python.h
grep -v 'define PACKAGE_' <confdefs.h >confdefs.h.new
rm confdefs.h
mv confdefs.h.new confdefs.h

# Checks for programs.
AC_PROG_CC

# Checks for functions and macros
AC_DEFINE(HAVE_BROKEN_SEM_UNLINK, 0, Define if 'sem_unlink' is broken on your platform)
AC_DEFINE(HAVE_BROKEN_SEM_GETVALUE, 0, Define if 'sem_getvalue' is broken on your platform)

AC_MSG_CHECKING(for sem_open)
AC_TRY_COMPILE([#include <semaphore.h>], void *x=sem_open,
  AC_DEFINE(HAVE_SEM_OPEN, 1, Define if you have the 'sem_open' function.)
  AC_MSG_RESULT(yes),
  AC_DEFINE(HAVE_SEM_OPEN, 0, Define if you have the 'sem_open' function.)
  AC_MSG_RESULT(no)
)

AC_MSG_CHECKING(for sem_timedwait)
AC_TRY_COMPILE([#include <semaphore.h>], void *x=sem_timedwait,
  AC_DEFINE(HAVE_SEM_TIMEDWAIT, 1, Define if you have the 'sem_timedwait' function.)
  AC_MSG_RESULT(yes),
  AC_DEFINE(HAVE_SEM_TIMEDWAIT, 0, Define if you have the 'sem_timedwait' function.)
  AC_MSG_RESULT(no)
)

AC_MSG_CHECKING(for fd transfer feature)
AC_TRY_COMPILE([#include <sys/socket.h>], 
  void *x; size_t s; struct msghdr msg;  struct cmsghdr *cmsg;
  x=sendmsg; 
  s = CMSG_SPACE(CMSG_LEN(sizeof(int)));
  cmsg = CMSG_FIRSTHDR(&msg);
  ,
  AC_DEFINE(HAVE_FD_TRANSER, 1, Define if you have the 'sendmsg' function for fd transfer.)
  AC_MSG_RESULT(yes),
  AC_DEFINE(HAVE_FD_TRANSER, 0, Define if you have the 'sendmsg' function for fd transfer.)
  AC_MSG_RESULT(no)
)

case $ac_sys_system/$ac_sys_release in
    FreeBSD/4.*|FreeBSD/5.*|FreeBSD/6.*|FreeBSD/7.*|FreeBSD/8.*)
        # FreeBSD's P1003.1b semaphore support is very experimental
        # and has many known problems. (as of June 2008)
        AC_DEFINE(HAVE_SEM_OPEN, 0)
        AC_DEFINE(HAVE_SEM_TIMEDWAIT, 0)  
    ;;
esac

case $ac_sys_system in
    CYGWIN*)
        AC_DEFINE(HAVE_BROKEN_SEM_UNLINK, 1)
        ;;
    Darwin*)
        AC_DEFINE(HAVE_BROKEN_SEM_GETVALUE, 1)
        ;;
esac

AC_OUTPUT
