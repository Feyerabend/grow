l   3
 ent   1   l   4
 ent   2   l   5
 loda  0       5
 inda          0
 ldcn
 equa
 fjp       l   6
i   10
 loda  0       5
 ldci          3
 csp         new
 loda  0       5
 inda          0
 chka  1   32767
 stra  0       7
 loda  0       7
 lodi  0       6
 stoi
i   20
 loda  0       7
 inca          2
 ldcn
 chka  0   32767
 stoa
 loda  0       7
 inca          1
 ldcn
 chka  0   32767
 stoa
i   30
 ujp       l   7
l   6
 lodi  0       6
 loda  0       5
 inda          0
 chka  1   32767
 indi          0
 lesi
 fjp       l   8
 mst           1
 loda  0       5
i   40
 inda          0
 chka  1   32767
 inca          2
 lodi  0       6
 cup   2   l   3
 ujp       l   9
l   8
 mst           1
 loda  0       5
 inda          0
 chka  1   32767
i   50
 inca          1
 lodi  0       6
 cup   2   l   3
l   9
l   7
 retp
l   4=         8
l   5=         9
l  10
 ent   1   l  11
 ent   2   l  12
 loda  0       5
 ldcn
 neqa
 fjp       l  13
i   60
 mst           1
 loda  0       5
 chka  1   32767
 inda          2
 cup   1   l  10
 loda  0       5
 chka  1   32767
 indi          0
 ldci          4
 lda   1       6
i   70
 csp         wri
 mst           1
 loda  0       5
 chka  1   32767
 inda          1
 cup   1   l  10
l  13
 retp
l  11=         6
l  12=         9
l  14
 ent   1   l  15
 ent   2   l  16
 ldcn
i   80
 chka  0   32767
 sroa         12
 ldci          1
 sroi         14
 ldci         10
 stri  0      19
l  17
 ldoi         14
 lodi  0      19
 leqi
 fjp       l  18
i   90
 lao          11
 ldci          2
 csp         new
 ldoa         11
 chka  1   32767
 ldoi         14
 ldoi         14
 mpi
 stoi
 ldoa         11
i  100
 chka  1   32767
 inca          1
 ldoa         12
 chka  0   32767
 stoa
 ldoa         11
 chka  0   32767
 sroa         12
 ldoi         14
 inci          1
i  110
 sroi         14
 ujp       l  17
l  18
 ldoa         12
 chka  0   32767
 sroa         11
l  19
 ldoa         11
 ldcn
 neqa
 fjp       l  20
 ldoa         11
i  120
 chka  1   32767
 indi          0
 ldci          4
 lda   0       6
 csp         wri
 ldoa         11
 chka  1   32767
 inda          1
 chka  0   32767
 sroa         11
i  130
 ujp       l  19
l  20
 lda   0       6
 csp         wln
 ldcn
 chka  0   32767
 sroa         10
 ldoa         12
 chka  0   32767
 sroa         11
l  21
 ldoa         11
i  140
 ldcn
 neqa
 fjp       l  22
 ldoa         11
 chka  1   32767
 inda          1
 chka  0   32767
 sroa          9
 ldoa         11
 chka  1   32767
i  150
 inca          1
 ldoa         10
 chka  0   32767
 stoa
 ldoa         11
 chka  0   32767
 sroa         10
 ldoa          9
 chka  0   32767
 sroa         11
i  160
 ujp       l  21
l  22
 ldoa         10
 chka  0   32767
 sroa         12
 ldoa         12
 chka  0   32767
 sroa         11
l  23
 ldoa         11
 ldcn
 neqa
i  170
 fjp       l  24
 ldoa         11
 chka  1   32767
 indi          0
 ldci          4
 lda   0       6
 csp         wri
 ldoa         11
 chka  1   32767
 inda          1
i  180
 chka  0   32767
 sroa         11
 ujp       l  23
l  24
 lda   0       6
 csp         wln
 ldcn
 chka  0   32767
 sroa         13
 ldci         17
 sroi         14
l  25
i  190
 mst           0
 lao          13
 ldoi         14
 cup   2   l   3
 ldoi         14
 ldci          7
 mpi
 ldci          3
 adi
 ldci         31
i  200
 mod
 sroi         14
 ldoi         14
 ldci         17
 equi
 fjp       l  25
 mst           0
 ldoa         13
 cup   1   l  10
 lda   0       6
i  210
 csp         wln
 ldcc 'c'
 chkc  0     127
 sroc         15
 ldcb          1
 chkb  0       1
 srob         16
 ldci          5
 sroi         17
 ldob         16
i  220
 fjp       l  26
 ldoc         15
 ldci          1
 lda   0       6
 csp         wrc
 lca' radius         '
 ldci          8
 ldci          8
 lda   0       6
 csp         wrs
i  230
 ldoi         17
 ldci          1
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
l  26
 ldcc 'r'
 chkc  0     127
 sroc         15
 ldcb          0
i  240
 chkb  0       1
 srob         16
 ldci          3
 sroi         18
 ldci          4
 sroi         17
 ldob         16
 not
 fjp       l  27
 ldoc         15
i  250
 ldci          1
 lda   0       6
 csp         wrc
 lca' area           '
 ldci          6
 ldci          6
 lda   0       6
 csp         wrs
 ldoi         18
 ldoi         17
i  260
 mpi
 ldci          1
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
l  27
 retp
l  15=        20
l  16=        12
q
i    0
 mst           0
 cup   0   l  14
 stp
q
