-- Exercise H.3: a loop that runs a million times, as a while loop and
-- as a numeric for loop.
local i = 0
while i < 1000000 do
  i = i + 1
end
local n = 0
for j = 1, 1000000 do
  n = n + 1
end
print(i, n)
