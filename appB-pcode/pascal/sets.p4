l   3
 ent   1   l   4
 ent   2   l   5
 ldc(  1  3  5  7  9)
 sros         11
 ldc(  3  4  5  6)
 sros         10
 ldos         11
i   10
 ldos         10
 uni
 sros          9
 ldci          0
 sroi         17
 ldci         47
 stri  0      18
l   6
 ldoi         17
 lodi  0      18
 leqi
i   20
 fjp       l   7
 ldoi         17
 ldos          9
 inn
 fjp       l   8
 ldoi         17
 ldci          3
 lda   0       6
 csp         wri
l   8
 ldoi         17
i   30
 inci          1
 sroi         17
 ujp       l   6
l   7
 lda   0       6
 csp         wln
 ldos         11
 ldos         10
 int
 sros          9
 ldci          0
i   40
 sroi         17
 ldci         47
 stri  0      18
l   9
 ldoi         17
 lodi  0      18
 leqi
 fjp       l  10
 ldoi         17
 ldos          9
 inn
i   50
 fjp       l  11
 ldoi         17
 ldci          3
 lda   0       6
 csp         wri
l  11
 ldoi         17
 inci          1
 sroi         17
 ujp       l   9
l  10
 lda   0       6
i   60
 csp         wln
 ldos         11
 ldos         10
 dif
 sros          9
 ldci          0
 sroi         17
 ldci         47
 stri  0      18
l  12
 ldoi         17
i   70
 lodi  0      18
 leqi
 fjp       l  13
 ldoi         17
 ldos          9
 inn
 fjp       l  14
 ldoi         17
 ldci          3
 lda   0       6
i   80
 csp         wri
l  14
 ldoi         17
 inci          1
 sroi         17
 ujp       l  12
l  13
 lda   0       6
 csp         wln
 ldc(  3  5)
 ldos         11
 leqs
i   90
 fjp       l  15
 lca'subset          '
 ldci          6
 ldci          6
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l  15
 ldos         11
 ldc(  1  9)
i  100
 geqs
 fjp       l  16
 lca'superset        '
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l  16
 ldos         11
i  110
 ldos         10
 neqs
 fjp       l  17
 lca'not equal       '
 ldci          9
 ldci          9
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l  17
i  120
 ldos         11
 ldos         10
 int
 ldc(  3  5)
 equs
 fjp       l  18
 lca'equal           '
 ldci          5
 ldci          5
 lda   0       6
i  130
 csp         wrs
 lda   0       6
 csp         wln
l  18
 ldci         40
 sroi         17
 ldoi         17
 sgs
 ldoi         17
 ldci          1
 adi
i  140
 sgs
 uni
 ldc( 47)
 uni
 sros          9
 ldci          0
 sroi         16
 ldci          0
 sroi         17
 ldci         47
i  150
 stri  0      18
l  19
 ldoi         17
 lodi  0      18
 leqi
 fjp       l  20
 ldoi         17
 ldos          9
 inn
 fjp       l  21
 ldoi         16
i  160
 ldci          1
 adi
 sroi         16
l  21
 ldoi         17
 inci          1
 sroi         17
 ujp       l  19
l  20
 ldoi         16
 ldci          1
 lda   0       6
i  170
 csp         wri
 lca' elements       '
 ldci          9
 ldci          9
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
 ldc(  0  1  2)
 sros         14
i  180
 ldc(  3  4  5  6)
 sros         13
 ldos         14
 ldos         13
 uni
 sros         12
 ldci          0
 sroi         15
 ldci          6
 ordi
i  190
 stri  0      18
l  22
 ldoi         15
 ordi
 lodi  0      18
 leqi
 fjp       l  23
 ldoi         15
 ordi
 ldos         14
 inn
i  200
 fjp       l  24
 ldcc 'w'
 ldci          1
 lda   0       6
 csp         wrc
 ujp       l  25
l  24
 ldoi         15
 ordi
 ldos         12
 inn
i  210
 fjp       l  26
 ldcc 'c'
 ldci          1
 lda   0       6
 csp         wrc
l  26
l  25
 ldoi         15
 inci          1
 sroi         15
 ujp       l  22
l  23
 lda   0       6
i  220
 csp         wln
 ldci          4
 ordi
 ldos         14
 inn
 not
 fjp       l  27
 lca'blue is cool    '
 ldci         12
 ldci         12
i  230
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l  27
 retp
l   4=        19
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
