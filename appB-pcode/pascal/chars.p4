l   3
 ent   1   l   4
 ent   2   l   5
 ldcc 'a'
 sroc          9
 ldcc 'z'
 ordc
 stri  0      11
l   6
i   10
 ldoc          9
 ordc
 lodi  0      11
 leqi
 fjp       l   7
 ldoc          9
 ldci          1
 lda   0       6
 csp         wrc
 ldoc          9
i   20
 incc          1
 sroc          9
 ujp       l   6
l   7
 lda   0       6
 csp         wln
 ldcc 'Z'
 sroc          9
 ldcc 'A'
 ordc
 stri  0      11
l   8
i   30
 ldoc          9
 ordc
 lodi  0      11
 geqi
 fjp       l   9
 ldoc          9
 ldci          1
 lda   0       6
 csp         wrc
 ldoc          9
i   40
 decc          1
 sroc          9
 ujp       l   8
l   9
 lda   0       6
 csp         wln
 ldcc 'A'
 ordc
 ldci          1
 lda   0       6
 csp         wri
i   50
 ldcc ' '
 ldci          1
 lda   0       6
 csp         wrc
 ldci         97
 chr
 ldci          1
 lda   0       6
 csp         wrc
 ldcc ' '
i   60
 ldci          1
 lda   0       6
 csp         wrc
 ldcc 'm'
 incc          1
 ldci          1
 lda   0       6
 csp         wrc
 ldcc 'n'
 decc          1
i   70
 ldci          1
 lda   0       6
 csp         wrc
 ldcc ' '
 ldci          1
 lda   0       6
 csp         wrc
 ldcb          1
 ordb
 ldci          1
i   80
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
 ldcc 'a'
 ldcc 'b'
 lesc
 chkb  0       1
 srob         10
 ldob         10
i   90
 ordb
 ldci          1
 lda   0       6
 csp         wri
 ldcc ' '
 ldci          1
 lda   0       6
 csp         wrc
 ldob         10
 not
i  100
 ordb
 ldci          1
 lda   0       6
 csp         wri
 ldcc ' '
 ldci          1
 lda   0       6
 csp         wrc
 ldci          7
 odd
i  110
 ordb
 ldci          6
 lda   0       6
 csp         wri
 ldcc '|'
 ldci          1
 lda   0       6
 csp         wrc
 ldcc 'x'
 ldci          3
i  120
 lda   0       6
 csp         wrc
 ldcc '|'
 ldci          1
 lda   0       6
 csp         wrc
 lca''quoted'        '
 ldci          8
 ldci          8
 lda   0       6
i  130
 csp         wrs
 lda   0       6
 csp         wln
 lca'a string that is'
 ldci         16
 ldci         16
 lda   0       6
 csp         wrs
 lca' longer than    '
 ldci         13
i  140
 ldci         13
 lda   0       6
 csp         wrs
 lca'sixteen         '
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lca'characters,     '
 ldci         12
i  150
 ldci         12
 lda   0       6
 csp         wrs
 lca'written in      '
 ldci         11
 ldci         11
 lda   0       6
 csp         wrs
 lca'pieces          '
 ldci          6
i  160
 ldci          6
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
 retp
l   4=        12
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
