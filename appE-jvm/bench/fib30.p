{ The 30th Fibonacci number, by recursion: calls. }
procedure fib[n];
var a;
begin
    if n < 2 then return n;
    call fib[n - 1];
    a is rval;
    call fib[n - 2];
    return a + rval
end;

begin
    call fib[30];
    print rval
end.
