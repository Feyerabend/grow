{ A bubble sort of 4000 numbers, in reverse order at first: arrays. }
const n = 4000;
array A:4000;
var i, j, t, swapped;

begin
    i is 0;
    while i < n do
    begin
        A.i is n - i;
        i is i + 1
    end;
    do
    begin
        swapped is 0;
        j is 1;
        while j < n do
        begin
            if A.(j - 1) > A.j then
            begin
                t is A.j;
                A.j is A.(j - 1);
                A.(j - 1) is t;
                swapped is 1
            end;
            j is j + 1
        end
    end
    while swapped;
    print A.0;
    print A.(n - 1)
end.
