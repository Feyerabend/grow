l   3
 ent   1   l   4
 ent   2   l   5
 ldci          1
 stri  0       5
 ldci          8
 stri  0       6
l   6
 lodi  0       5
i   10
 lodi  0       6
 leqi
 fjp       l   7
 lao           9
 lodi  0       5
 chki  1       8
 deci          1
 ixa           1
 indi          0
 ldci          2
i   20
 lda   1       6
 csp         wri
 lodi  0       5
 inci          1
 stri  0       5
 ujp       l   6
l   7
 lda   1       6
 csp         wln
 retp
l   4=         7
l   5=         8
l   8
 ent   1   l   9
i   30
 ent   2   l  10
 ldci          1
 stri  0       6
 ldci          8
 stri  0       7
l  11
 lodi  0       6
 lodi  0       7
 leqi
 fjp       l  12
 lao          17
i   40
 lodi  0       6
 chki  1       8
 deci          1
 ixa           1
 indb          0
 lao          25
 lodi  0       6
 lodi  0       5
 adi
 chki  2      16
i   50
 deci          2
 ixa           1
 indb          0
 and
 lao          40
 lodi  0       6
 lodi  0       5
 sbi
 chki -7       7
 inci          7
i   60
 ixa           1
 indb          0
 and
 fjp       l  13
 lao           9
 lodi  0       5
 chki  1       8
 deci          1
 ixa           1
 lodi  0       6
i   70
 stoi
 lao          17
 lodi  0       6
 chki  1       8
 deci          1
 ixa           1
 ldcb          0
 chkb  0       1
 stob
 lao          25
i   80
 lodi  0       6
 lodi  0       5
 adi
 chki  2      16
 deci          2
 ixa           1
 ldcb          0
 chkb  0       1
 stob
 lao          40
i   90
 lodi  0       6
 lodi  0       5
 sbi
 chki -7       7
 inci          7
 ixa           1
 ldcb          0
 chkb  0       1
 stob
 lodi  0       5
i  100
 ldci          8
 lesi
 fjp       l  14
 mst           1
 lodi  0       5
 ldci          1
 adi
 cup   1   l   8
 ujp       l  15
l  14
 ldoi         55
i  110
 ldci          1
 adi
 sroi         55
 ldoi         55
 ldci          3
 leqi
 fjp       l  16
 mst           1
 cup   0   l   3
l  16
l  15
 lao          17
i  120
 lodi  0       6
 chki  1       8
 deci          1
 ixa           1
 ldcb          1
 chkb  0       1
 stob
 lao          25
 lodi  0       6
 lodi  0       5
i  130
 adi
 chki  2      16
 deci          2
 ixa           1
 ldcb          1
 chkb  0       1
 stob
 lao          40
 lodi  0       6
 lodi  0       5
i  140
 sbi
 chki -7       7
 inci          7
 ixa           1
 ldcb          1
 chkb  0       1
 stob
l  13
 lodi  0       6
 inci          1
 stri  0       6
i  150
 ujp       l  11
l  12
 retp
l   9=         8
l  10=         9
l  17
 ent   1   l  18
 ent   2   l  19
 ldci          1
 sroi         56
 ldci          8
 stri  0      57
l  20
 ldoi         56
 lodi  0      57
i  160
 leqi
 fjp       l  21
 lao          17
 ldoi         56
 chki  1       8
 deci          1
 ixa           1
 ldcb          1
 chkb  0       1
 stob
i  170
 ldoi         56
 inci          1
 sroi         56
 ujp       l  20
l  21
 ldci          2
 sroi         56
 ldci         16
 stri  0      57
l  22
 ldoi         56
 lodi  0      57
i  180
 leqi
 fjp       l  23
 lao          25
 ldoi         56
 chki  2      16
 deci          2
 ixa           1
 ldcb          1
 chkb  0       1
 stob
i  190
 ldoi         56
 inci          1
 sroi         56
 ujp       l  22
l  23
 ldci          7
 ngi
 sroi         56
 ldci          7
 stri  0      57
l  24
 ldoi         56
i  200
 lodi  0      57
 leqi
 fjp       l  25
 lao          40
 ldoi         56
 chki -7       7
 inci          7
 ixa           1
 ldcb          1
 chkb  0       1
i  210
 stob
 ldoi         56
 inci          1
 sroi         56
 ujp       l  24
l  25
 ldci          0
 sroi         55
 mst           0
 ldci          1
 cup   1   l   8
i  220
 ldoi         55
 ldci          1
 lda   0       6
 csp         wri
 lca' solutions      '
 ldci         10
 ldci         10
 lda   0       6
 csp         wrs
 lda   0       6
i  230
 csp         wln
 retp
l  18=        58
l  19=        10
q
i    0
 mst           0
 cup   0   l  17
 stp
q
