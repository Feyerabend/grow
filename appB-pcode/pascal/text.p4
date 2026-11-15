l   3
 ent   1   l   4
 ent   2   l   5
 ldci          0
 sroi         14
 ldci          0
 sroi         13
 ldci          0
i   10
 sroi         12
 ldci          0
 sroi         11
l   6
 lao           5
 eof
 not
 fjp       l   7
 ldoc          5
 ldcc '#'
 equc
i   20
 fjp       l   8
 lao           5
 csp         get
l   9
 lao           5
 csp         eln
 not
 fjp       l  10
 lao          10
 lda   0       5
 csp         rdi
i   30
 ldoi         11
 ldoi         10
 adi
 sroi         11
 ujp       l   9
l  10
l   8
 ldcb          0
 chkb  0       1
 srob         15
l  11
 lao           5
 csp         eln
i   40
 not
 fjp       l  12
 lao           9
 lda   0       5
 csp         rdc
 ldoi         12
 ldci          1
 adi
 sroi         12
 ldoc          9
i   50
 ldcc ' '
 equc
 fjp       l  13
 ldcb          0
 chkb  0       1
 srob         15
 ujp       l  14
l  13
 ldob         15
 not
 fjp       l  15
i   60
 ldcb          1
 chkb  0       1
 srob         15
 ldoi         13
 ldci          1
 adi
 sroi         13
l  15
l  14
 ujp       l  11
l  12
 lda   0       5
 csp         rln
i   70
 ldoi         14
 ldci          1
 adi
 sroi         14
 ujp       l   6
l   7
 ldoi         14
 ldci          1
 lda   0       6
 csp         wri
 lca' lines,         '
i   80
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 ldoi         13
 ldci          1
 lda   0       6
 csp         wri
 lca' words,         '
 ldci          8
i   90
 ldci          8
 lda   0       6
 csp         wrs
 ldoi         12
 ldci          1
 lda   0       6
 csp         wri
 lca' characters     '
 ldci         11
 ldci         11
i  100
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
 lca'the numbers add '
 ldci         16
 ldci         16
 lda   0       6
 csp         wrs
 lca'up to           '
i  110
 ldci          6
 ldci          6
 lda   0       6
 csp         wrs
 ldoi         11
 ldci          1
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
i  120
 retp
l   4=        16
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
