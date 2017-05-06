# gen_systags.py

I used to run a command line as follows to generate a systag file for
Vim code completion (omni-completion and [echofunc][1]):

```bash
ctags -R --c-kinds=+p --extra=+q --fields=+iaS -I … \
      -o /usr/local/etc/systags /usr/include …
```

I made small scripts on machines I work on, but now I feel there is
simply too much noise if I include whole directories recursively. Heck,
I currently can see `fprintf` declared in
*/usr/include/php/ext/standard/basic_functions.h*, and I know I
definitely do not want to see Vim show function prototypes from *that*
file.

So I adopted an alternative method. I’ll start from the standard C
header files, and include in the **ctags** command line only header
files that I want or need (i.e. included by the header files I want). My
little script does exactly that.

I have not put in the C++ header files, as **ctags** probably is not a
good tool for C++ code completion. For that purpose, I use
[**clang_complete**][2]. Also be noted that it is normal for the script
to complain about some missing header files, as it is not a true C
preprocessor and does not deal with conditions. It is possible that it
tries to find a header file that exists only on another platform.

The default include paths work for macOS Sierra (with command line
tools) and some Linux flavours (tested on Ubuntu 16.04 LTS and CentOS
7). You may need to adjust them in other environments. Also be noted the
best order is probably not the one as recognized by your compiler. This
script does not support `include_next`, so it is probably a better idea
to put */usr/include* before your compiler-specific include paths.

[1]: https://github.com/mbbill/fencview
[2]: https://github.com/Rip-Rip/clang_complete

## Licence

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors of
this software dedicate any and all copyright interest in the software to
the public domain. We make this dedication for the benefit of the public
at large and to the detriment of our heirs and successors.  We intend
this dedication to be an overt act of relinquishment in perpetuity of
all present and future rights to this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
