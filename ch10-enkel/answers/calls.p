{ Exercise 10.2: calls as expressions }
procedure gcd[a, b];
    begin
        if b = 0 then return a;
        return gcd[b, a % b]
    end;
procedure fib[n];
    begin
        if n < 2 then return n;
        return fib[n - 1] + fib[n - 2]
    end;
begin
    print gcd[15, 6];
    print gcd[1071, 462] * 2;
    print fib[20];
    call fib[10]                { as a statement, its value dropped }
end.
