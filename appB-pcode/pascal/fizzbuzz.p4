l   3
 ent   1   l   4
 ent   2   l   5
 ldci          1
 sroi          9
 ldci         20
 stri  0      10
l   6
 ldoi          9
i   10
 lodi  0      10
 leqi
 fjp       l   7
 ldoi          9
 ldci         15
 mod
 ujp       l   8
l  10
 lca'FizzBuzz        '
 ldci          8
 ldci          8
i   20
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
 ujp       l   9
l  11
 lca'Fizz            '
 ldci          4
 ldci          4
 lda   0       6
 csp         wrs
i   30
 lda   0       6
 csp         wln
 ujp       l   9
l  12
 lca'Buzz            '
 ldci          4
 ldci          4
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
i   40
 ujp       l   9
l  13
 ldoi          9
 ldci          1
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
 ujp       l   9
l   8
 chki  0      14
 ldci          0
i   50
 sbi
 xjp       l  14
l  14
 ujp       l  10
 ujp       l  13
 ujp       l  13
 ujp       l  11
 ujp       l  13
 ujp       l  12
 ujp       l  11
 ujp       l  13
i   60
 ujp       l  13
 ujp       l  11
 ujp       l  12
 ujp       l  13
 ujp       l  11
 ujp       l  13
 ujp       l  13
l   9
 ldoi          9
 inci          1
 sroi          9
i   70
 ujp       l   6
l   7
 retp
l   4=        11
l   5=        10
q
i    0
 mst           0
 cup   0   l   3
 stp
q
