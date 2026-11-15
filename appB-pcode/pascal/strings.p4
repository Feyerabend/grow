l   3
 ent   1   l   4
 ent   2   l   5
 lao          25
 lca'pascal          '
 mov           8
 lao          17
 lca'p-code          '
i   10
 mov           8
 lao           9
 lao          25
 mov           8
 lao          25
 lao           9
 equm          8
 fjp       l   6
 lca'a = c           '
 ldci          5
i   20
 ldci          5
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   6
 lao          25
 lao          17
 neqm          8
 fjp       l   7
 lca'a <> b          '
i   30
 ldci          6
 ldci          6
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   7
 lao          17
 lao          25
 lesm          8
 fjp       l   8
i   40
 lao          17
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lca' <              '
 ldci          3
 ldci          3
 lda   0       6
 csp         wrs
i   50
 lao          25
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   8
 lao          25
 lao          17
 geqm          8
i   60
 fjp       l   9
 lao          25
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lca' >=             '
 ldci          4
 ldci          4
 lda   0       6
i   70
 csp         wrs
 lao          17
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   9
 lao          33
 ldci          1
i   80
 chki  1       5
 deci          1
 ixa           8
 lca'zurich          '
 mov           8
 lao          33
 ldci          2
 chki  1       5
 deci          1
 ixa           8
i   90
 lca'machine         '
 mov           8
 lao          33
 ldci          3
 chki  1       5
 deci          1
 ixa           8
 lca'compiler        '
 mov           8
 lao          33
i  100
 ldci          4
 chki  1       5
 deci          1
 ixa           8
 lca'portable        '
 mov           8
 lao          33
 ldci          5
 chki  1       5
 deci          1
i  110
 ixa           8
 lca'abstract        '
 mov           8
 ldci          2
 sroi         74
 ldci          5
 stri  0      83
l  10
 ldoi         74
 lodi  0      83
 leqi
i  120
 fjp       l  11
 ldci          5
 sroi         73
 ldoi         74
 stri  0      84
l  12
 ldoi         73
 lodi  0      84
 geqi
 fjp       l  13
 lao          33
i  130
 ldoi         73
 chki  1       5
 deci          1
 ixa           8
 lao          33
 ldoi         73
 ldci          1
 sbi
 chki  1       5
 deci          1
i  140
 ixa           8
 lesm          8
 fjp       l  14
 lao          75
 lao          33
 ldoi         73
 chki  1       5
 deci          1
 ixa           8
 mov           8
i  150
 lao          33
 ldoi         73
 chki  1       5
 deci          1
 ixa           8
 lao          33
 ldoi         73
 ldci          1
 sbi
 chki  1       5
i  160
 deci          1
 ixa           8
 mov           8
 lao          33
 ldoi         73
 ldci          1
 sbi
 chki  1       5
 deci          1
 ixa           8
i  170
 lao          75
 mov           8
l  14
 ldoi         73
 deci          1
 sroi         73
 ujp       l  12
l  13
 ldoi         74
 inci          1
 sroi         74
 ujp       l  10
l  11
i  180
 ldci          1
 sroi         74
 ldci          5
 stri  0      83
l  15
 ldoi         74
 lodi  0      83
 leqi
 fjp       l  16
 lao          33
 ldoi         74
i  190
 chki  1       5
 deci          1
 ixa           8
 ldci         10
 ldci          8
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
 ldoi         74
i  200
 inci          1
 sroi         74
 ujp       l  15
l  16
 lao          25
 ldci          1
 chki  1       8
 deci          1
 ixa           1
 indc          0
 ldci          1
i  210
 lda   0       6
 csp         wrc
 lao          17
 ldci          2
 chki  1       8
 deci          1
 ixa           1
 indc          0
 ldci          1
 lda   0       6
i  220
 csp         wrc
 lao           9
 ldci          8
 chki  1       8
 deci          1
 ixa           1
 indc          0
 ldci          1
 lda   0       6
 csp         wrc
i  230
 ldcc '|'
 ldci          1
 lda   0       6
 csp         wrc
 lda   0       6
 csp         wln
 retp
l   4=        85
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
