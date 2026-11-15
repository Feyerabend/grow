(* Records and pointers: a list built with new, reversed, and a tree
   that sorts. with, nil, and variant records. *)
program heap(output);
type link = ^node;
     node = record value: integer; next: link end;
     tree = ^branch;
     branch = record key: integer; left, right: tree end;
     shape = record
         name: char;
         case round: boolean of
             true: (radius: integer);
             false: (width, height: integer)
     end;
var list, p, q, r: link;
    root: tree;
    i: integer;
    s: shape;

    procedure insert(var t: tree; k: integer);
    begin
        if t = nil then begin
            new(t);
            with t^ do begin key := k; left := nil; right := nil end
        end
        else if k < t^.key then insert(t^.left, k)
        else insert(t^.right, k)
    end;

    procedure walk(t: tree);
    begin
        if t <> nil then begin
            walk(t^.left);
            write(t^.key:4);
            walk(t^.right)
        end
    end;

begin
    list := nil;
    for i := 1 to 10 do begin
        new(p);
        p^.value := i * i;
        p^.next := list;
        list := p
    end;
    p := list;
    while p <> nil do begin write(p^.value:4); p := p^.next end;
    writeln;
    (* reverse it *)
    q := nil;
    p := list;
    while p <> nil do begin r := p^.next; p^.next := q; q := p; p := r end;
    list := q;
    p := list;
    while p <> nil do begin write(p^.value:4); p := p^.next end;
    writeln;
    root := nil;
    i := 17;
    repeat
        insert(root, i);
        i := (i * 7 + 3) mod 31
    until i = 17;
    walk(root);
    writeln;
    with s do begin
        name := 'c'; round := true; radius := 5;
        if round then writeln(name, ' radius ', radius:1);
        name := 'r'; round := false; width := 3; height := 4;
        if not round then writeln(name, ' area ', width * height:1)
    end
end.
