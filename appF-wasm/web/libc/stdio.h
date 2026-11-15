/* wasm.c writes to stderr only when it runs out of memory, just before
 * exit(2); on the page that message is the page's, so it goes nowhere. */
#ifndef WEB_STDIO_H
#define WEB_STDIO_H
typedef struct FILE FILE;
#define stderr ((FILE *)0)
#define fprintf(f, ...) ((void)(f), 0)
#endif
