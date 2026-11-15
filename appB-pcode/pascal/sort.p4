l   3
 ent   1   l   4
 ent   2   l   5
 loda  0       5
 indi          0
 stri  0       7
 loda  0       5
 loda  0       6
i   10
 indi          0
 stoi
 loda  0       6
 lodi  0       7
 stoi
 retp
l   4=         8
l   5=         7
l   6
 ent   1   l   7
 ent   2   l   8
 ldci          1
 stri  0       7
i   20
 ldci          7
 stri  0       8
l   9
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l  10
 ldci          8
 stri  0       6
 lodi  0       7
 ldci          1
i   30
 adi
 stri  0       9
l  11
 lodi  0       6
 lodi  0       9
 geqi
 fjp       l  12
 loda  0       5
 lodi  0       6
 chki  1       8
 deci          1
i   40
 ixa           1
 indi          0
 loda  0       5
 lodi  0       6
 ldci          1
 sbi
 chki  1       8
 deci          1
 ixa           1
 indi          0
i   50
 lesi
 fjp       l  13
 mst           1
 loda  0       5
 lodi  0       6
 chki  1       8
 deci          1
 ixa           1
 loda  0       5
 lodi  0       6
i   60
 ldci          1
 sbi
 chki  1       8
 deci          1
 ixa           1
 cup   2   l   3
l  13
 lodi  0       6
 deci          1
 stri  0       6
 ujp       l  11
l  12
i   70
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l   9
l  10
 retp
l   7=        10
l   8=         9
l  14
 ent   1   l  15
 ent   2   l  16
 ldci          1
 stri  0       6
 ldci          8
i   80
 stri  0       7
l  17
 lodi  0       6
 lodi  0       7
 leqi
 fjp       l  18
 loda  0       5
 lodi  0       6
 chki  1       8
 deci          1
 ixa           1
i   90
 indi          0
 ldci          4
 lda   1       6
 csp         wri
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l  17
l  18
 lda   1       6
 csp         wln
i  100
 retp
l  15=         8
l  16=         8
l  19
 ent   1   l  20
 ent   2   l  21
 lao           9
 ldci          1
 chki  1       8
 deci          1
 ixa           1
 ldci         31
 stoi
i  110
 lao           9
 ldci          2
 chki  1       8
 deci          1
 ixa           1
 ldci          4
 stoi
 lao           9
 ldci          3
 chki  1       8
i  120
 deci          1
 ixa           1
 ldci         15
 stoi
 lao           9
 ldci          4
 chki  1       8
 deci          1
 ixa           1
 ldci          9
i  130
 ngi
 stoi
 lao           9
 ldci          5
 chki  1       8
 deci          1
 ixa           1
 ldci         26
 stoi
 lao           9
i  140
 ldci          6
 chki  1       8
 deci          1
 ixa           1
 ldci          5
 stoi
 lao           9
 ldci          7
 chki  1       8
 deci          1
i  150
 ixa           1
 ldci          3
 stoi
 lao           9
 ldci          8
 chki  1       8
 deci          1
 ixa           1
 ldci          0
 stoi
i  160
 mst           0
 lao           9
 cup   1   l  14
 mst           0
 lao           9
 cup   1   l   6
 mst           0
 lao           9
 cup   1   l  14
 retp
l  20=        18
l  21=         8
q
i    0
 mst           0
 cup   0   l  19
 stp
q
