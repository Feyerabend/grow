/* Exercise 22.4: no clock in WebAssembly without a host; collecting takes 0 seconds. */
#ifndef TIME_H
#define TIME_H
typedef long clock_t;
#define CLOCKS_PER_SEC 1000000
clock_t clock(void);
#endif
