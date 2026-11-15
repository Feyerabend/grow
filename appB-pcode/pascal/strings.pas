(* Strings are packed arrays of char: compared a word at a time, by
   equm and lesm, and moved by mov. *)
program strings(output);
type name = packed array [1..8] of char;
var a, b, c: name;
    words: array [1..5] of name;
    i, j: integer;
    t: name;
begin
    a := 'pascal  ';
    b := 'p-code  ';
    c := a;
    if a = c then writeln('a = c');
    if a <> b then writeln('a <> b');
    if b < a then writeln(b, ' < ', a);
    if a >= b then writeln(a, ' >= ', b);
    words[1] := 'zurich  '; words[2] := 'machine ';
    words[3] := 'compiler'; words[4] := 'portable';
    words[5] := 'abstract';
    for i := 2 to 5 do
        for j := 5 downto i do
            if words[j] < words[j - 1] then begin
                t := words[j]; words[j] := words[j - 1]; words[j - 1] := t
            end;
    for i := 1 to 5 do writeln(words[i]:10);
    writeln(a[1], b[2], c[8], '|')
end.
