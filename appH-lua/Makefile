# Appendix H: Lua.  make check
# The appendix is described, not built: this folder holds only the
# worked answers to its exercises.

check:
	@if command -v lua > /dev/null && command -v luac > /dev/null; then \
	    sh answers/check.sh; \
	else \
	    echo "appendix H: Lua 5.5 not found, the answers not checked"; \
	fi
	@echo "appendix H: ok"

.PHONY: check
