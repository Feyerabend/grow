# Appendix A: the Metcalfe parsing machine

Howard Metcalfe's syntax machine and editor machine, as his report of
1964 defines them, in one Python program, `metcalfe.py`. The book's
appendix A describes them; this is the machine to run.

    make check
    python3 metcalfe.py -w samples/sentence.syn < samples/sentence.in
    echo "THE BOY SEES A TREE" | python3 metcalfe.py -w -t samples/sentence.syn
    python3 metcalfe.py samples/expr.syn < samples/expr.in

`-w` reads words, as in his English examples; without it, characters,
with blanks left out, as in his programming language. `-t` traces every
instruction as his report does: the trace of the English sentence is the
one he prints, location for location.

The samples:

- `sentence.syn`: his first syntax program, the grammar of "The boy sees
  a tree", 28 instructions.
- `german.syn`: English to German, with marks to choose der, den, ein or
  einen, and the editor to join each article to its ending.
- `reverse.syn`: his first use of the editor, reversing a string.
- `expr.syn`: a statement of his small language, compiled to the code of
  his stack computer; the first three lines give the code his report
  prints for the same statements.

The grammars of `german.syn` and `expr.syn` are ours, written from his.
Two things are ours, not his: W empties the editor's stack after writing
it, as his section on tape movement does after each statement; and each
line also says where the machine stopped reading, if it stopped before
the end, where his machine shows only the flag.

`answers/` holds the worked answers to the appendix's exercises, which
`make check` runs too.
