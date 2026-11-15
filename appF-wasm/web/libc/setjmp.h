/* WebAssembly 1.0 cannot jump back up the stack, so on the page a jump
 * back is a JavaScript exception: longjmp asks the page to throw, with
 * the machine's own message, and the page makes a new machine for the
 * next run. setjmp is then always 0, the first return. (host.c) */
#ifndef WEB_SETJMP_H
#define WEB_SETJMP_H
typedef int jmp_buf[1];
#define setjmp(b) ((void)(b), 0)
__attribute__((noreturn)) void web_longjmp(int *b);
#define longjmp(b, v) web_longjmp(b)
#endif
