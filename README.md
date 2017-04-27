# gen_systags.py

I used to run a command line as follows to generate a systag file for Vim code completion (omni-completion and [echofunc](https://github.com/mbbill/fencview)):

```bash
ctags -R --c-kinds=+p --extra=+q --fields=+iaS -I … \
      -o /usr/local/etc/systags /usr/include …
```

I made small scripts on machines I work on, but now I feel there is simply too much noise if I include whole directories recursively. Heck, I currently can see `fprintf` declared in */usr/include/php/ext/standard/basic_functions.h*, and I know I definitely do not want to see Vim show function prototypes from *that* file.

So I adopted an alternative method. I’ll start from the standard C header files, and include in the **ctags** command line only header files that I want or need (i.e. included by the header files I want). My little script does exactly that.

I have not put in the C++ header files, as **ctags** probably is not a good tool for C++ code completion. For that purpose, I use [**clang_complete**](https://github.com/Rip-Rip/clang_complete). Also be noted that it is normal for the script to complain about some missing header files, as it is not a true C preprocessor and does not deal with conditions. It is possible that it tries to find a header file that exists only on another platform.

The default include paths work for macOS with command line tools. You will need to adjust them in other environments. Also be noted the best order is probably not the one as recognized by your compiler. This script does not support `include_next`, so it is probably a better idea to put */usr/include* before your compiler-specific include paths.
