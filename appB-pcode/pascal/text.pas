(* Reading text: characters and lines, numbers, eoln and eof. It counts
   the lines, words and characters of its input, and adds up the
   numbers on the lines that start with a #. *)
program text(input, output);
var c: char;
    lines, words, chars, total, n: integer;
    inword: boolean;
begin
    lines := 0; words := 0; chars := 0; total := 0;
    while not eof do begin
        if input^ = '#' then begin
            get(input);
            while not eoln do begin
                read(n);
                total := total + n
            end
        end;
        inword := false;
        while not eoln do begin
            read(c);
            chars := chars + 1;
            if c = ' ' then inword := false
            else if not inword then begin
                inword := true;
                words := words + 1
            end
        end;
        readln;
        lines := lines + 1
    end;
    writeln(lines:1, ' lines, ', words:1, ' words, ', chars:1, ' characters');
    writeln('the numbers add ', 'up to ', total:1)
end.
