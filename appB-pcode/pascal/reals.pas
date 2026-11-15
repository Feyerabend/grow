(* Reals: arithmetic, the standard functions, and write(x:w), in the
   form Free Pascal gives it. P4 keeps at most three real constants in
   its table, so the rest are made from integers. *)
program reals(output);
var x, y, z: real;
    i: integer;
begin
    x := 3 / 2;
    y := 1 / 3;
    z := 0.1;
    writeln(x:12, x:1, -x:20, x:9, x:10, x:30);
    writeln(y:24, y * 1e30:15, sqrt(2):9);
    writeln(z + 2 * z:25, x * y:12, x - y:12, -y:12);
    i := trunc(-x);
    writeln(i:3, trunc(x):3, trunc(y * 1000):5);
    writeln(sin(1):24, cos(1):24);
    writeln(exp(1):24, ln(2):24, arctan(1):24);
    writeln(abs(-x):8, sqr(x):8, 7 / 2:8, 2.5e-3:12);
    if x > y then writeln('x > y');
    if x * 2 = 3 then writeln('x * 2 = 3');
    if y + y + y <> 3 / 3 then writeln('thirds: not 1')
end.
