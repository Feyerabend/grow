{ A trap in enkel/0: division by zero, two calls deep. On the JVM it is
  an ArithmeticException, and the trace names the lines of this file. }
var people;

procedure share[total, n];
begin
    return total / n
end;

procedure round[total];
begin
    call share[total, people];
    print rval
end;

begin
    people is 3;
    while people >= 0 do
    begin
        call round[100];
        people is people - 1
    end
end.
