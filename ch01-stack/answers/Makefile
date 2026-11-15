# Chapter 1's answers: each one built and run, its output compared with
# the .out file beside it.  make check
CC ?= cc
CFLAGS ?= -std=c99 -O0 -w

ANSWERS := div depth rsub

# div.out holds 0 for 1 / 0, which is what the M1 gives; C does not say,
# and an x86 PC stops the program instead.  start1 has no .out: it reads
# and writes outside the stack, and is only checked not to finish well.
check: $(ANSWERS) start1
	@for a in $(ANSWERS); do ./$$a > $$a.got; diff -u $$a.out $$a.got || exit 1; done
	@if ./start1 > /dev/null 2>&1; then echo "start1 finished normally"; fi
	@python3 ershov.py > ershov.got && diff -u ershov.out ershov.got
	@rm -f *.got
	@echo "ch01 answers: ok"

%: %.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(ANSWERS) start1 start1-asan start1-o2 *.got

.PHONY: check clean
