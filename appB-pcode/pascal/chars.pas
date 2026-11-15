program chars(output);
var c: char;
    b: boolean;
begin
    for c := 'a' to 'z' do write(c);
    writeln;
    for c := 'Z' downto 'A' do write(c);
    writeln;
    writeln(ord('A'):1, ' ', chr(97), ' ', succ('m'), pred('n'), ' ', ord(true):1);
    b := 'a' < 'b';
    writeln(ord(b):1, ' ', ord(not b):1, ' ', ord(odd(7)):6, '|', 'x':3, '|', '''quoted''');
    (* P4 cannot write a boolean, or a string of more than 16
       characters: errors/limits.pas. So the long string is written in
       pieces. *)
    write('a string that is', ' longer than ', 'sixteen ');
    writeln('characters, ', 'written in ', 'pieces')
end.
