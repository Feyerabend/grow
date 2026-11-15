(* Sets: of a range of integers, and of an enumeration. P4's sets hold
   0 to 47 when it compiles them, and a set is written out element by
   element: [3..6] is a range P4 does not take. *)
program sets(output);
type colour = (red, orange, yellow, green, blue, indigo, violet);
var s, t, u: set of 0..47;
    warm, cool, all: set of colour;
    c: colour;
    i, n: integer;
begin
    s := [1, 3, 5, 7, 9];
    t := [3, 4, 5, 6];
    u := s + t;
    for i := 0 to 47 do if i in u then write(i:3);
    writeln;
    u := s * t;
    for i := 0 to 47 do if i in u then write(i:3);
    writeln;
    u := s - t;
    for i := 0 to 47 do if i in u then write(i:3);
    writeln;
    if [3, 5] <= s then writeln('subset');
    if s >= [1, 9] then writeln('superset');
    if s <> t then writeln('not equal');
    if s * t = [3, 5] then writeln('equal');
    i := 40;
    u := [i, i + 1, 47];
    n := 0;
    for i := 0 to 47 do if i in u then n := n + 1;
    writeln(n:1, ' elements');
    warm := [red, orange, yellow];
    cool := [green, blue, indigo, violet];
    all := warm + cool;
    for c := red to violet do
        if c in warm then write('w') else if c in all then write('c');
    writeln;
    if not (blue in warm) then writeln('blue is cool')
end.
