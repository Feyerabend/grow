(* Exercise B.5: readln(prd) must move on a line of prd, not of input.
  prd is what follows the program's P4 code in its file: here "ab" and
  "cd", put there by check.sh. input is "xy" and "zw". *)
program readprd(input, output, prd);
var c: char;
begin
  read(prd, c); write(c);
  readln(prd);
  read(prd, c); write(c);
  read(input, c); writeln(' ', c)
end.
