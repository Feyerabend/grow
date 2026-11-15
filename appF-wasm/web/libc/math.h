/* What wasm.c needs of math.h. Each is one WebAssembly instruction, and
 * clang's builtins make it so: f32.ceil, f64.sqrt, f32.nearest and the
 * rest. */
#ifndef WEB_MATH_H
#define WEB_MATH_H
#define isnan(x)   __builtin_isnan(x)
#define signbit(x) __builtin_signbit(x)
#define ceil(x)    __builtin_ceil(x)
#define ceilf(x)   __builtin_ceilf(x)
#define floor(x)   __builtin_floor(x)
#define floorf(x)  __builtin_floorf(x)
#define trunc(x)   __builtin_trunc(x)
#define truncf(x)  __builtin_truncf(x)
#define rint(x)    __builtin_rint(x)
#define rintf(x)   __builtin_rintf(x)
#define sqrt(x)    __builtin_sqrt(x)
#define sqrtf(x)   __builtin_sqrtf(x)
#endif
