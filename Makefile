# Growing a Machine: the code.  make check runs all of it.

CHAPTERS   := $(sort $(wildcard ch*))
APPENDICES := $(sort $(wildcard app*))

check:
	@for d in $(CHAPTERS); do \
	    if [ -f $$d/Makefile ] && grep -q '^test:' $$d/Makefile; then \
	        $(MAKE) -s -C $$d test || exit 1; \
	    fi; \
	    if [ -f $$d/answers/Makefile ]; then \
	        $(MAKE) -s -C $$d/answers check || exit 1; \
	    fi; \
	done
	@for d in $(APPENDICES); do \
	    if [ -f $$d/Makefile ]; then $(MAKE) -s -C $$d check || exit 1; fi; \
	done
	@echo "all: ok"

.PHONY: check
