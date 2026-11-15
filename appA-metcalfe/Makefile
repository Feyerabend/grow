# Appendix A: Metcalfe's syntax machine and editor.  make check
PYTHON ?= python3

# Each sample, run on its lines, says what it says in its .out file; the
# English sentence is also traced, as in Metcalfe's report. Then the worked
# answers to the appendix's exercises.
check:
	@$(PYTHON) metcalfe.py -w samples/sentence.syn < samples/sentence.in | diff -u samples/sentence.out -
	@echo "THE BOY SEES A TREE" | $(PYTHON) metcalfe.py -w -t samples/sentence.syn | diff -u samples/sentence-trace.out -
	@$(PYTHON) metcalfe.py -w samples/german.syn < samples/german.in | diff -u samples/german.out -
	@$(PYTHON) metcalfe.py samples/reverse.syn < samples/reverse.in | diff -u samples/reverse.out -
	@$(PYTHON) metcalfe.py samples/expr.syn < samples/expr.in | diff -u samples/expr.out -
	@sh answers/check.sh
	@echo "appendix A: ok"

.PHONY: check
