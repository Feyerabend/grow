{ enkel/0 does not check an index computed while the program runs:
  A.i with i = 3 is the word after A, which is B.0. }
array A:3, B:3;
var i;
begin
    B.0 is 99;
    i is 3;
    print A.i
end.
