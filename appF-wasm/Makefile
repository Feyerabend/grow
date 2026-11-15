CC ?= cc
CFLAGS ?= -std=c99 -O2 -Wall -Wextra
CLANG ?= clang
NODE ?= node
PYTHON ?= python3
WAST2JSON ?= wast2json

SOURCES = wasm.c spec.c main.c program.c
PROGRAMS := $(basename $(notdir $(wildcard programs/*.c)))
WASM32 = --target=wasm32 -mcpu=mvp -std=c99 -O2 -Wall -Wextra -nostdlib -Wl,--no-entry

# Everything after 1.0 is switched off, but for mutable globals, which
# 1.0 has.
FEATURES = --disable-exceptions --disable-saturating-float-to-int \
    --disable-sign-extension --disable-simd --disable-multi-value \
    --disable-tail-call --disable-bulk-memory --disable-reference-types \
    --disable-annotations --disable-memory64 --disable-multi-memory \
    --disable-extended-const --disable-relaxed-simd
# The five files whose NaN assertions are in 1.0's form (nan.py).
OLDNAN = f32 f64 conversions float_exprs float_misc

build/wasm: $(SOURCES) wasm.h spec.h
	mkdir -p build
	$(CC) $(CFLAGS) -D_POSIX_C_SOURCE=200809L -o $@ $(SOURCES) -lm

# 1. Each program prints what it should, and ends with status 0.
# 2. Chapter 23's machine, compiled to WebAssembly 1.0, passes the
#    book's conformance suite on this machine, with each collector.
# With WABT: 3. the specification's own tests, all of them that are of
#    the binary format or of execution.
# With Node.js: 4. each program prints the same under Node; and the
#    page's programs, in web/, print the same on Node's engine and on this
#    machine compiled to WebAssembly and running inside it.
check: build/wasm
	for p in $(PROGRAMS); do \
	    { build/wasm programs/$$p.wasm; echo "status $$?"; } > build/$$p.out 2>&1; \
	    cmp programs/$$p.out build/$$p.out || exit 1; \
	done
	@echo "$(words $(PROGRAMS)) programs"
	cd ../ch23-wasm && $(PYTHON) conform.py ../appF-wasm/build/wasm -m ../appF-wasm/programs/vm.wasm
	cd ../ch23-wasm && $(PYTHON) conform.py ../appF-wasm/build/wasm -m ../appF-wasm/programs/vm.wasm -g copy -S
	if command -v $(WAST2JSON) > /dev/null; then $(MAKE) --no-print-directory suite; fi
	if command -v $(NODE) > /dev/null; then $(MAKE) --no-print-directory referee; fi
	@sh answers/check.sh
	@echo "appendix f: ok"

suite: build/wasm
	mkdir -p build/suite
	for w in suite/*.wast; do \
	    n=$$(basename $$w .wast); \
	    case " $(OLDNAN) " in \
	        *" $$n "*) t=f32; [ $$n = f64 ] && t=f64; \
	            $(PYTHON) nan.py $$t < $$w > build/suite/$$n.wast;; \
	        *) cp $$w build/suite/$$n.wast;; \
	    esac; \
	    $(WAST2JSON) $(FEATURES) -o build/suite/$$n.json build/suite/$$n.wast || exit 1; \
	done
	build/wasm -s build/suite/*.json

referee:
	for p in $(PROGRAMS); do \
	    { $(NODE) run.mjs programs/$$p.wasm; echo "status $$?"; } > build/$$p.node 2>&1; \
	    cmp programs/$$p.out build/$$p.node || exit 1; \
	done
	@echo "Node.js agrees on $(words $(PROGRAMS)) programs"
	$(NODE) web/check.cjs

# The programs compiled again, chapter 23's machine with them, and
# what each prints, from Node.js; and the page's web/data.js, with this
# machine compiled to WebAssembly in it. Read the differences before
# keeping them.
expect:
	for p in $(PROGRAMS); do \
	    $(CLANG) $(WASM32) -Wl,--export=main -Wl,--allow-undefined \
	        -o programs/$$p.wasm programs/$$p.c || exit 1; \
	    { $(NODE) run.mjs programs/$$p.wasm; echo "status $$?"; } > programs/$$p.out 2>&1; \
	done
	$(CLANG) $(WASM32) -o programs/vm.wasm ../ch23-wasm/core.c
	mkdir -p build
	$(CLANG) $(WASM32) -nostdlibinc -isystem web/libc -o build/appf.wasm web/host.c
	$(PYTHON) web/data.py build/appf.wasm > web/data.js

clean:
	rm -rf build

.PHONY: check suite referee expect clean
