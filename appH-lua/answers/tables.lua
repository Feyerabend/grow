-- Exercise H.4: a table's array part, growing and shrinking. Lua has
-- no function that says how big the array part is, so this watches the
-- memory each assignment takes, with the collector stopped. Nothing
-- else here allocates between the two readings of the count.
collectgarbage("stop")
local count = collectgarbage
local grow = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}
local shrink = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0}

-- t[1] to t[17], one at a time.
local t = {}
for i = 1, 17 do
  local before = count("count")
  t[i] = true
  grow[i] = (count("count") - before) * 1024
end

-- t[1] to t[16], then t[1] to t[15] set to nil, then a new key, 100.
local u = {}
for i = 1, 16 do u[i] = true end
for i = 1, 15 do
  local before = count("count")
  u[i] = nil
  shrink[i] = (count("count") - before) * 1024
end
local before = count("count")
u[100] = true
shrink[16] = (count("count") - before) * 1024

-- The same, but the new key is a string.
local v = {}
for i = 1, 16 do v[i] = true end
for i = 1, 15 do v[i] = nil end
before = count("count")
v.x = true
shrink[17] = (count("count") - before) * 1024

for i = 1, 17 do print("t[" .. i .. "] = true", grow[i]) end
local nils = 0
for i = 1, 15 do nils = nils + shrink[i] end
print("u[1..15] = nil", nils)
print("u[100] = true", shrink[16])
print("v[1..15] = nil, v.x = true", shrink[17])
