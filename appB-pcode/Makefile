CC ?= cc
CFLAGS ?= -std=c99 -O2 -Wall -Wextra
PYTHON ?= python3
FPC ?= fpc
FPCFLAGS = -Miso -v0

PROGRAMS := $(basename $(notdir $(wildcard pascal/*.pas)))
TRAPS := $(basename $(notdir $(wildcard pascal/traps/*.pas)))
ERRORS := $(basename $(notdir $(wildcard pascal/errors/*.pas)))

# Programs whose output has reals, and may differ from pint's in the
# last figure of one (lastdigit.py).
REALS := reals
# Traps pint does not catch: it divides by zero as Free Pascal does, with
# its runtime error 200, and has no check for a variable without a value.
PINT_SILENT := divide undefined

build/p4: p4.c
	mkdir -p build
	$(CC) $(CFLAGS) -o $@ p4.c -lm

build/self.p: p4/pcom.p p4/adapt.py
	mkdir -p build
	$(PYTHON) p4/adapt.py self < p4/pcom.p > $@

# Without Free Pascal:
# 1. pcom, as P4 code, compiles itself on this machine, and makes the
#    same P4 code again, to the character.
# 2. It compiles each program to the P4 code kept beside it, and that
#    code prints what pint printed, and ends with status 0.
# 3. Each trap stops with a message, and status 1, as kept beside it.
# 4. pcom refuses each program in errors/, with the listing kept.
# With Free Pascal, also:
# 5. pcom and pint, compiled by Free Pascal, make the same P4 code and
#    print the same output, and stop each trap the same way.
# 6. Each program, compiled by Free Pascal itself, prints the same.
check: build/p4 build/self.p
	build/p4 p4/pcom.p4 build/pcom.p4 < build/self.p > build/pcom.lst
	cmp p4/pcom.p4 build/pcom.p4
	@echo "pcom compiles itself"
	for s in $(PROGRAMS); do \
	    in=/dev/null; [ -f pascal/$$s.in ] && in=pascal/$$s.in; \
	    build/p4 p4/pcom.p4 build/$$s.p4 < pascal/$$s.pas > build/$$s.lst || exit 1; \
	    cmp pascal/$$s.p4 build/$$s.p4 || exit 1; \
	    build/p4 -u build/$$s.p4 < $$in > build/$$s.out || exit 1; \
	    case " $(REALS) " in \
	        *" $$s "*) $(PYTHON) lastdigit.py pascal/$$s.out build/$$s.out || exit 1;; \
	        *) cmp pascal/$$s.out build/$$s.out || exit 1;; \
	    esac; \
	done
	@echo "$(words $(PROGRAMS)) programs"
	for s in $(TRAPS); do \
	    build/p4 p4/pcom.p4 build/$$s.p4 < pascal/traps/$$s.pas > build/$$s.lst || exit 1; \
	    cmp pascal/traps/$$s.p4 build/$$s.p4 || exit 1; \
	    { build/p4 -u build/$$s.p4 < /dev/null; echo "status $$?"; } > build/$$s.out; \
	    cmp pascal/traps/$$s.out build/$$s.out || exit 1; \
	done
	@echo "$(words $(TRAPS)) traps"
	for s in $(ERRORS); do \
	    build/p4 p4/pcom.p4 build/$$s.p4 < pascal/errors/$$s.pas > build/$$s.lst || exit 1; \
	    cmp pascal/errors/$$s.lst build/$$s.lst || exit 1; \
	    grep -q '\*\*\*\*' build/$$s.lst || exit 1; \
	done
	@echo "$(words $(ERRORS)) refused"
	if command -v $(FPC) > /dev/null; then $(MAKE) --no-print-directory referee; fi
	@sh answers/check.sh
	@echo "appendix b: ok"

# pcom and pint, compiled by Free Pascal: the referees.
build/pcom: p4/pcom.p p4/adapt.py
	mkdir -p build
	$(PYTHON) p4/adapt.py pcom < p4/pcom.p > build/pcom.p
	$(FPC) $(FPCFLAGS) -FEbuild -o$@ build/pcom.p > build/pcom.log 2>&1 || { cat build/pcom.log; exit 1; }

build/pint: p4/pint.p p4/adapt.py
	mkdir -p build
	$(PYTHON) p4/adapt.py pint < p4/pint.p > build/pint.p
	$(FPC) $(FPCFLAGS) -FEbuild -o$@ build/pint.p > build/pint.log 2>&1 || { cat build/pint.log; exit 1; }

# pint's messages are padded with spaces, tabs and NUL bytes, and it
# goes on to dump the store; the message and the line of registers are
# compared.
FIRST3 = tr -d '\000' | sed -n '1,3s/[[:space:]]*$$//p'

referee: build/p4 build/self.p build/pcom build/pint
	build/pcom build/native.p4 < build/self.p > /dev/null
	tr -s ' ' < build/native.p4 > build/a; tr -s ' ' < p4/pcom.p4 > build/b; cmp build/a build/b
	build/pint p4/pcom.p4 build/pint.p4 < build/self.p > /dev/null
	cmp p4/pcom.p4 build/pint.p4
	@echo "Free Pascal's pcom and pint agree on pcom"
	for s in $(PROGRAMS); do \
	    in=/dev/null; [ -f pascal/$$s.in ] && in=pascal/$$s.in; \
	    build/pcom build/$$s.native.p4 < pascal/$$s.pas > /dev/null; \
	    tr -s ' ' < build/$$s.native.p4 > build/a; tr -s ' ' < pascal/$$s.p4 > build/b; \
	    cmp build/a build/b || exit 1; \
	    build/pint pascal/$$s.p4 < $$in > build/$$s.pint; \
	    cmp pascal/$$s.out build/$$s.pint || exit 1; \
	    $(FPC) $(FPCFLAGS) -Cr -FEbuild -obuild/$$s.fpc pascal/$$s.pas > build/$$s.log 2>&1 || { cat build/$$s.log; exit 1; }; \
	    build/$$s.fpc < $$in > build/$$s.fpcout; \
	    cmp pascal/$$s.out build/$$s.fpcout || exit 1; \
	done
	@echo "pint and Free Pascal agree on $(words $(PROGRAMS)) programs"
	for s in $(filter-out $(PINT_SILENT),$(TRAPS)); do \
	    build/pint pascal/traps/$$s.p4 < /dev/null | $(FIRST3) > build/a; \
	    cat pascal/traps/$$s.out | $(FIRST3) > build/b; \
	    cmp build/a build/b || exit 1; \
	done
	@echo "pint stops the traps it can"

# The expected P4 code, listings and output, made again by the referees:
# pcom compiled by itself on pint, and pint. The traps' output is this
# machine's, since pint goes on to dump its store. Read the differences
# before keeping them.
expect: build/p4 build/self.p build/pcom build/pint
	build/pcom build/native.p4 < build/self.p > /dev/null
	build/pint build/native.p4 p4/pcom.p4 < build/self.p > /dev/null
	for s in $(PROGRAMS); do \
	    in=/dev/null; [ -f pascal/$$s.in ] && in=pascal/$$s.in; \
	    build/pint p4/pcom.p4 pascal/$$s.p4 < pascal/$$s.pas > /dev/null; \
	    build/pint pascal/$$s.p4 < $$in > pascal/$$s.out; \
	done
	for s in $(TRAPS); do \
	    build/pint p4/pcom.p4 pascal/traps/$$s.p4 < pascal/traps/$$s.pas > /dev/null; \
	    { build/p4 -u pascal/traps/$$s.p4 < /dev/null; echo "status $$?"; } > pascal/traps/$$s.out; \
	done
	for s in $(ERRORS); do \
	    build/pint p4/pcom.p4 build/$$s.p4 < pascal/errors/$$s.pas > pascal/errors/$$s.lst; \
	done

clean:
	rm -rf build __pycache__

.PHONY: check referee expect clean
