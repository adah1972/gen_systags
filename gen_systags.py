#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from glob import glob
import os
import re
import subprocess
import sys


def detect_linux_x86_64_generic_include_path(incl_paths):
    linux_x86_64_generic_include_path = '/usr/include/x86_64-linux-gnu'
    if os.path.isdir(linux_x86_64_generic_include_path):
        incl_paths.append(linux_x86_64_generic_include_path)
    gcc_paths = sorted(glob('/usr/lib/gcc/x86_64-linux-gnu/*'),
                       reverse=True)
    for path in gcc_paths:
        if os.path.isdir(path + '/include'):
            incl_paths.append(path + '/include')
            if os.path.isdir(path + '/include-fixed'):
                incl_paths.append(path + '/include-fixed')
            break


def detect_linux_x86_64_redhat_include_path(incl_paths):
    gcc_paths = sorted(glob('/usr/lib/gcc/x86_64-redhat-linux/*'),
                       reverse=True)
    for path in gcc_paths:
        if os.path.isdir(path + '/include'):
            incl_paths.append(path + '/include')
            break


def detect_macos_include_path(incl_paths):
    cmd_line_tool_paths = sorted(
        glob('/Library/Developer/CommandLineTools/usr/lib/clang/*'),
        reverse=True)
    for path in cmd_line_tool_paths:
        if os.path.isdir(path + '/include'):
            incl_paths.append(path + '/include')
            break


def find_file(filename, possible_paths):
    """
    Finds the file path given a file name and a list of possible paths.
    """
    for path in possible_paths:
        full_path = path + '/' + filename
        if os.path.isfile(full_path):
            return full_path
    return False


def find_included_files(hdr_file_path):
    """
    Finds files included by a given header file.
    """
    included_files = set()
    with open(hdr_file_path) as f:
        for line in f:
            match = re.match(r'\s*#\s*include\s*<([^>]+)>', line)
            if match:
                included_files.add(match.group(1))
    return included_files


def find_header_files(hdr_files, incl_paths):
    """
    Finds all header files passed in as well as the header files they
    include.  A list of full paths of header files is returned.
    """
    result = []
    processed_files = set()
    new_files = set()
    included_src = {}
    while True:
        for hdr_file in hdr_files:
            if hdr_file in processed_files:
                continue
            processed_files.add(hdr_file)
            full_path = find_file(hdr_file, incl_paths)
            if full_path:
                result.append(full_path)
                included_files = find_included_files(full_path)
                for included_file in included_files:
                    if included_file not in included_src:
                        included_src[included_file] = hdr_file
                new_files.update(included_files)
            else:
                if hdr_file in included_src:
                    print('%s (first included by %s) is not found' %
                          (hdr_file, included_src[hdr_file]),
                          file=sys.stderr)
                else:
                    print(hdr_file, "is not found", file=sys.stderr)
        if not new_files:
            break
        hdr_files = list(new_files)
        new_files = set()
    return result


def gen_systags(hdr_files, incl_paths):
    """
    Generates a systags file from header files.  Given a list of header
    files and the system include paths, find out all header files
    included in those header files recursively, and invoke Exuberant
    Ctags to generate the systags file.

    The systags file is often used with Vim, and one normally does
    something like `set tags+=/usr/local/etc/systags' in .vimrc.  The
    built-in omni-completion (invoked by CTRL-X CTRL-O) should be
    helpful, and I personally enjoy using it with the echofunc plugin:

    https://github.com/mbbill/echofunc
    """
    hdr_files_with_path = find_header_files(hdr_files, incl_paths)
    ctags_cmd = [
        'ctags',
        '-I __DARWIN_ALIAS+',
        '-I __DARWIN_ALIAS_C+',
        '-I __THROW',
        '-I __THROWNL',
        '-I __dead2',
        '-I __printflike+',
        '-I __pure2',
        '-I __result_use_check',
        '-I __swift_unavailable+',
        '--c-kinds=+p',
        '--extra=+q',
        '--fields=+iaS',
        '-o /usr/local/etc/systags'
    ]
    ctags_cmd.extend(hdr_files_with_path)
    subprocess.check_call(ctags_cmd)


def main():
    """
    Generates the header file list using the standard C99/POSIX header
    files and Linux/macOS include paths.  Actually, POSIX header files
    include the C99 header files, but the duplication does not matter.
    """
    incl_paths = [
        '/usr/include',
    ]
    detect_linux_x86_64_generic_include_path(incl_paths)
    detect_linux_x86_64_redhat_include_path(incl_paths)
    detect_macos_include_path(incl_paths)
    print('The following include paths are used:')
    for incl_path in incl_paths:
        print(' ', incl_path)
    hdr_files = [
        # Standard C99 header files
        "assert.h",
        "complex.h",
        "ctype.h",
        "errno.h",
        "fenv.h",
        "float.h",
        "inttypes.h",
        "iso646.h",
        "limits.h",
        "locale.h",
        "math.h",
        "setjmp.h",
        "signal.h",
        "stdarg.h",
        "stdbool.h",
        "stddef.h",
        "stdint.h",
        "stdio.h",
        "stdlib.h",
        "string.h",
        "tgmath.h",
        "time.h",
        "wchar.h",
        "wctype.h",

        # POSIX header files
        "aio.h",
        "arpa/inet.h",
        "assert.h",
        "complex.h",
        "cpio.h",
        "ctype.h",
        "dirent.h",
        "dlfcn.h",
        "errno.h",
        "fcntl.h",
        "fenv.h",
        "float.h",
        "fmtmsg.h",
        "fnmatch.h",
        "ftw.h",
        "glob.h",
        "grp.h",
        "iconv.h",
        "inttypes.h",
        "iso646.h",
        "langinfo.h",
        "libgen.h",
        "limits.h",
        "locale.h",
        "math.h",
        "monetary.h",
        "mqueue.h",
        "ndbm.h",
        "net/if.h",
        "netdb.h",
        "netinet/in.h",
        "netinet/tcp.h",
        "nl_types.h",
        "poll.h",
        "pthread.h",
        "pwd.h",
        "regex.h",
        "sched.h",
        "search.h",
        "semaphore.h",
        "setjmp.h",
        "signal.h",
        "spawn.h",
        "stdarg.h",
        "stdbool.h",
        "stddef.h",
        "stdint.h",
        "stdio.h",
        "stdlib.h",
        "string.h",
        "strings.h",
        "stropts.h",
        "sys/ipc.h",
        "sys/mman.h",
        "sys/msg.h",
        "sys/resource.h",
        "sys/select.h",
        "sys/sem.h",
        "sys/shm.h",
        "sys/socket.h",
        "sys/stat.h",
        "sys/statvfs.h",
        "sys/time.h",
        "sys/times.h",
        "sys/types.h",
        "sys/uio.h",
        "sys/un.h",
        "sys/utsname.h",
        "sys/wait.h",
        "syslog.h",
        "tar.h",
        "termios.h",
        "tgmath.h",
        "time.h",
        "trace.h",
        "ulimit.h",
        "unistd.h",
        "utime.h",
        "utmpx.h",
        "wchar.h",
        "wctype.h",
        "wordexp.h",
    ]
    gen_systags(hdr_files, incl_paths)


if __name__ == '__main__':
    main()
