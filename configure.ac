#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT(multiprocessing, 0.0, http://code.google.com/p/python-multiprocessing)
AC_CONFIG_HEADER([Modules/_multiprocessing/mpconfig.h])

# We don't use PACKAGE_ variables, and they cause conflicts
# with other autoconf-based packages that include Python.h
grep -v 'define PACKAGE_' <confdefs.h >confdefs.h.new
rm confdefs.h
mv confdefs.h.new confdefs.h

# Checks for programs.
AC_PROG_CC

# Checks for functions and macros
# TODO: add checks for HAVE_BROKEN_SEM_UNLINK and  HAVE_BROKEN_SEM_UNLINK

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

AC_OUTPUT
