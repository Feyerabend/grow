(* Two of P4's limits, both error 399, an implementation restriction:
   it cannot write a boolean, and a string has at most 16 characters. *)
program limits(output);
var b: boolean;
begin
    b := true;
    writeln(b);
    writeln('a string that is longer than sixteen characters')
end.
