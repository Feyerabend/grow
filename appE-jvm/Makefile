CC ?= cc
CFLAGS ?= -std=c11 -O2 -Wall -Wextra
PYTHON ?= python3
JAVAC ?= javac
SOURCES = class.c verify.c run.c main.c

# Java, if there is one that runs: macOS has a java that only says no
# Java is installed. make check JAVA= leaves it out.
JAVA ?= $(shell java -version > /dev/null 2>&1 && echo java)
# Without its helpful messages, a NullPointerException says only its name.
JAVAFLAGS = -XX:-ShowCodeDetailsInExceptionMessages

CLASSES = $(basename $(notdir $(wildcard java/*.java)))
ENKEL = ../ch10-enkel
SAMPLES = $(basename $(notdir $(wildcard $(ENKEL)/samples/*.p)))

build/jvm: $(SOURCES) jvm.h
	mkdir -p build
	$(CC) $(CFLAGS) -o $@ $(SOURCES)

# The same machine, built to catch any read or write outside what it owns,
# and any undefined behaviour of C: for mutate.py.
build/jvm-checked: $(SOURCES) jvm.h
	mkdir -p build
	$(CC) -std=c11 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=undefined \
	    -o $@ $(SOURCES)

# 1. Every class javac made, from java/, prints on this machine what Java
#    printed, in tests/: its output, its trace and its status; and with Java,
#    Java prints it again.
# 2. Chapter 10's samples, compiled by enkelj.py, print what they print on
#    chapter 10's machine, here and with Java; so do 300 of chapter 9's
#    random expressions, and an enkel/0 program that traps.
# 3. Class files broken on purpose by break.py are refused, here and with
#    Java, but for the differences break.py lists.
# 4. 1000 random breakages of javac's classes: whatever the verifier takes
#    runs on build/jvm-checked, and must not crash it.
# 5. The answers to the exercises.
check: build/jvm build/jvm-checked
	@test -n "$(JAVA)" || echo "no java: the real JVM is left out"
	for c in $(CLASSES); do \
	    { build/jvm classes/$$c.class 2>&1; echo "status $$?"; } | diff -u tests/$$c.out - || exit 1; \
	    if [ -n "$(JAVA)" ]; then \
	        { env -u JAVA_TOOL_OPTIONS $(JAVA) $(JAVAFLAGS) -cp classes $$c 2>&1; echo "status $$?"; } \
	            | diff -u tests/$$c.out - || exit 1; \
	    fi; \
	done
	@echo "$(words $(CLASSES)) classes from javac$(if $(JAVA), on both machines)"
	$(MAKE) -s -C $(ENKEL) vm $(SAMPLES:%=samples/%.vm) > /dev/null
	mkdir -p build/enkel
	for s in $(SAMPLES); do \
	    $(ENKEL)/vm $(ENKEL)/samples/$$s.vm | cmp -s - $(ENKEL)/samples/$$s.out || { echo "$$s: chapter 10"; exit 1; }; \
	    $(PYTHON) enkelj.py $(ENKEL)/samples/$$s.p build/enkel || exit 1; \
	    c=$$($(PYTHON) enkelj.py -name $$s); \
	    build/jvm build/enkel/$$c.class | diff -u $(ENKEL)/samples/$$s.out - || exit 1; \
	    if [ -n "$(JAVA)" ]; then \
	        env -u JAVA_TOOL_OPTIONS $(JAVA) -cp build/enkel $$c | diff -u $(ENKEL)/samples/$$s.out - || exit 1; \
	    fi; \
	done
	@echo "$(words $(SAMPLES)) samples of chapter 10, the same on its machine and here$(if $(JAVA), and on Java)"
	$(PYTHON) $(ENKEL)/fuzz.py 2 300 build/enkel/fuzz.p build/enkel/fuzz.expected
	$(PYTHON) enkelj.py build/enkel/fuzz.p build/enkel
	build/jvm build/enkel/Fuzz.class | cmp - build/enkel/fuzz.expected
	if [ -n "$(JAVA)" ]; then \
	    env -u JAVA_TOOL_OPTIONS $(JAVA) -cp build/enkel Fuzz | cmp - build/enkel/fuzz.expected || exit 1; \
	fi
	$(PYTHON) enkelj.py tests/share.p build/enkel
	{ build/jvm build/enkel/Share.class 2>&1; echo "status $$?"; } | diff -u tests/share.out -
	if [ -n "$(JAVA)" ]; then \
	    { env -u JAVA_TOOL_OPTIONS $(JAVA) -cp build/enkel Share 2>&1; echo "status $$?"; } \
	        | diff -u tests/share.out - || exit 1; \
	fi
	@echo "300 random expressions and a trap"
	rm -rf build/broken
	$(PYTHON) break.py classes build/broken
	$(PYTHON) verifycmp.py build/broken $(JAVA) > build/verify.txt || { cat build/verify.txt; exit 1; }
	@tail -1 build/verify.txt
	$(PYTHON) mutate.py 1000 1 build/jvm-checked > build/mutate.txt || { cat build/mutate.txt; exit 1; }
	@head -1 build/mutate.txt
	@JAVA="$(JAVA)" PYTHON=$(PYTHON) sh answers/check.sh
	@echo "appendix e: ok"

# What each class prints, from Java, and the classes again, from javac,
# for Java SE 21: class files of version 65. Read the differences before
# keeping them.
expect:
	for c in $(CLASSES); do \
	    { env -u JAVA_TOOL_OPTIONS java $(JAVAFLAGS) -cp classes $$c 2>&1; echo "status $$?"; } > tests/$$c.out; \
	done
	$(PYTHON) enkelj.py tests/share.p build/enkel
	{ env -u JAVA_TOOL_OPTIONS java -cp build/enkel Share 2>&1; echo "status $$?"; } > tests/share.out

classes:
	$(JAVAC) --release 21 -d classes java/*.java

clean:
	rm -rf build __pycache__

.PHONY: check expect classes clean
