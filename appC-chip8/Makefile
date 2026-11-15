# Appendix C: CHIP-8, as the VIP ran it and as CHIP-48 did.  make check
PYTHON ?= python3

# Each sample leaves the screen it should; quirks.hex on both machines.
# Then the worked answers to the appendix's exercises; and, with Node.js,
# the page's machine (web/chip8.js) held to chip8.py.
check:
	@$(PYTHON) chip8.py samples/answer.hex | diff -u samples/answer.out -
	@$(PYTHON) chip8.py samples/collide.hex | diff -u samples/collide.out -
	@$(PYTHON) chip8.py -m vip samples/quirks.hex | diff -u samples/quirks-vip.out -
	@$(PYTHON) chip8.py -m chip48 samples/quirks.hex | diff -u samples/quirks-chip48.out -
	@sh answers/check.sh
	@if command -v node > /dev/null; then sh web/check.sh; \
	 else echo "appendix C: no Node.js, the page's machine not checked"; fi
	@echo "appendix C: ok"

.PHONY: check
