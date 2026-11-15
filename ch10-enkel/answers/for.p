{ Exercise 10.4: for loops, made into while loops by the parser }
var i, j, n;
begin
    for i is 1 to 5 do print i * i;
    for i is 5 to 1 do print 0 - 1;     { never runs }
    n is 3;
    for i is 1 to n do
        for j is 1 to i do print 10 * i + j;
    for i is 1 to n do n is n - 1;      { the limit is read each round }
    print i
end.
