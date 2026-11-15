CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra -Wno-unused-parameter
SOURCES = cek.c tree.c main.c
# Lark's front end needs Python 3.10 or later: the newest one found.
PYTHON ?= $(shell for p in python3.13 python3.12 python3.11 python3.10 python3; do \
    command -v $$p > /dev/null && $$p -c 'import sys; sys.exit(sys.version_info < (3, 10))' \
    2> /dev/null && echo $$p && break; done)
# The fuzzer needs Hypothesis: build/venv has it, if made by make venv.
FUZZPY = $(if $(wildcard build/venv/bin/python),build/venv/bin/python,$(PYTHON))

PROGRAMS = $(sort $(wildcard lark/tests/[0-9][0-9]_*.lark)) lark/tests/09_modules/main.lark \
    $(sort $(wildcard lark/tests/errors/*.lark)) $(sort $(wildcard lark/samples/*.lark))
BENCH = fib loop sort

build/lark: $(SOURCES) cek.h tree.h
	mkdir -p build
	$(CC) $(CFLAGS) -o $@ $(SOURCES)

# The same machine, checking itself: every variable's depth against the
# name of the cell it reaches, and a collection before every step, so
# that a pointer the collector did not know of would be used at once.
build/lark-checked: $(SOURCES) cek.h tree.h
	mkdir -p build
	$(CC) $(CFLAGS) -DLARK_CHECK_DEPTH -DLARK_COLLECT_ALWAYS -o $@ $(SOURCES)

# 1. Every test and sample of Lark's, written out by emit.py and run on
#    the checking machine, prints what Lark's own CEK machine printed,
#    with the same messages and status; the refused ones are refused alike.
# 2. Each benchmark prints the answer bench/answers.py works out.
# 3. With Hypothesis: random well-typed programs from Lark's generator
#    print the same on this machine and on Lark's.
check: build/lark build/lark-checked
	@test -n "$(PYTHON)" || { echo "Lark needs Python 3.10 or later"; exit 1; }
	for f in $(PROGRAMS); do \
	    n=$$(echo $$f | sed 's|^lark/||; s|\.lark$$||; s|/|_|g'); \
	    { $(PYTHON) emit.py $$f > build/$$n.tree && build/lark-checked build/$$n.tree; echo "status $$?"; } \
	        > build/$$n.out 2>&1; \
	    cmp expected/$$n.out build/$$n.out || exit 1; \
	done
	@echo "$(words $(PROGRAMS)) programs"
	for b in $(BENCH); do \
	    $(PYTHON) emit.py bench/$$b.lark > build/$$b.tree || exit 1; \
	    build/lark build/$$b.tree > build/$$b.out || exit 1; \
	    cmp bench/$$b.out build/$$b.out || exit 1; \
	done
	@echo "$(words $(BENCH)) benchmarks"
	if $(FUZZPY) -c 'import hypothesis' 2> /dev/null; then $(FUZZPY) fuzz.py 300; fi
	@PYTHON=$(PYTHON) sh answers/check.sh
	@echo "appendix g: ok"

# A virtual environment with Hypothesis and pytest, for the fuzzer.
venv:
	$(PYTHON) -m venv build/venv
	build/venv/bin/pip install -q pytest hypothesis

# What each program prints, from Lark's own CEK machine (lark/src/cek.py),
# and each benchmark's answer, from bench/answers.py. Read the differences
# before keeping them.
expect:
	mkdir -p expected
	for f in $(PROGRAMS); do \
	    n=$$(echo $$f | sed 's|^lark/||; s|\.lark$$||; s|/|_|g'); \
	    { $(PYTHON) lark/src/cek.py $$f; echo "status $$?"; } > expected/$$n.out 2>&1; \
	done
	for b in $(BENCH); do $(PYTHON) bench/answers.py $$b > bench/$$b.out; done

clean:
	rm -rf build/lark build/lark-checked build/*.tree build/*.out __pycache__ \
	    bench/__pycache__ lark/src/__pycache__ lark/tests/__pycache__

.PHONY: check venv expect clean
