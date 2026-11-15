-- Exercise H.2: two closures, one variable. inc and get both use n.
-- They are called after counter has returned, so n has moved off the
-- stack into its upvalue. If each closure had an upvalue of its own,
-- inc would add to one copy and get would read the other: 0, not 2.
local function counter()
  local n = 0
  local function inc() n = n + 1 end
  local function get() return n end
  return inc, get
end

local inc, get = counter()
inc()
inc()
print(get())
