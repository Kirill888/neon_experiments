What is this?
----------------------

This is a place where I experiment with ARM's NEON technology. NEON is
ARM's SIMD (single instruction multiple data) instruction set, if you
know SSE2/SSE/MMX of x86 world, NEON is ARM's take on the same
concept.

Gcc/clang and I'm sure other compiler that target armv7+ architectures
provide intrinsics to make writing NEON code easier for the
programmer. These are meant to work with "C" as well as C++, as such
they lack certain niceties C++ programmers, like myself, expect. Since
C lacks support for overloads each intrinsic function needs to have a
unique name. NEON designers resolved this problem by coming up with a
predictable naming scheme, for instance to add two SIMD vectors one
says c = vadd_u8(a,b) to add 8-wide unsigned 8 bit integers, if you
work with 16 wide unsigned 8 bit values, you say vaddq_u8(a,b), if you
want signed you say vaddq_s8(a,b), if you want other bit depth you say
vadd(q|)_(s|u|f|p)(8|16|32|64), and so forth...

This in itself is not too much of a hassle once you learned the naming
convention, but it makes it impossible to write generic code without
resorting to some ugly c pre-processor tricks.

With this project I attempt to create a C++ shim to neon intrinsics
that would allow them to be seamlessly used with C++ templates.

Approach
--------------------------

1. Provide some basic traits via hand-written C++
2. Auto generate overloads for related functions, so that one can say
   "c = vadd(a,b)" and get that compiled for all valid types of a,b,c.


Status
--------------------------

Still in the experimenting stage. I have some python code that
consumes arm_neon.h header and converts it to json data (this is using
clang python bindings). And I have some python code that process that
data and outputs a C++ header with overloads where possible and
templates where necessary.

There are still some problems to address

1. Handling of immediate values

   Generated code for neon intrinsics that use immediate values will
   not compile with -O0 settings by gcc, since constants don't get
   propagated through C++ shim boundary. Annoyingly it does compile
   fine with -O1 and higher. Solution is to treat intrinsics with
   immediate values in a special way and to generate "template<int N>
   func(...)" kind of code for that case.

2. Tests

   There are none, which is obviously a problem. Given that there are
   1870 intrinsics in 159 groups it's not exactly clear how to go
   about testing this thing beyond simple manual inspection of
   generated code.
