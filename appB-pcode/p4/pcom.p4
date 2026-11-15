l   3
 ent   1   l   4
 ent   2   l   5
 ldoi        159
 ldci          0
 grti
 fjp       l   6
 ldoi         28
i   10
 ldci          6
 lda   1       6
 csp         wri
 lca' ****           '
 ldci          9
 ldci          7
 lda   1       6
 csp         wrs
 ldci          0
 stri  0      10
i   20
 ldci          1
 stri  0       9
 ldci          1
 stri  0       5
 ldoi        159
 stri  0      11
l   7
 lodi  0       5
 lodi  0      11
 leqi
 fjp       l   8
i   30
 lao         160
 lodi  0       5
 deci          1
 ixa           2
 stra  0      12
 loda  0      12
 indi          0
 stri  0       8
 loda  0      12
 indi          1
i   40
 stri  0       7
 lodi  0       8
 lodi  0      10
 equi
 fjp       l   9
 ldcc ','
 ldci          1
 lda   1       6
 csp         wrc
 ujp       l  10
l   9
l  11
i   50
 lodi  0       9
 lodi  0       8
 lesi
 fjp       l  12
 ldcc ' '
 ldci          1
 lda   1       6
 csp         wrc
 lodi  0       9
 ldci          1
i   60
 adi
 stri  0       9
 ujp       l  11
l  12
 ldcc '^'
 ldci          1
 lda   1       6
 csp         wrc
 lodi  0       8
 stri  0      10
l  10
 lodi  0       7
i   70
 ldci         10
 lesi
 fjp       l  13
 ldci          1
 stri  0       6
 ujp       l  14
l  13
 lodi  0       7
 ldci        100
 lesi
 fjp       l  15
i   80
 ldci          2
 stri  0       6
 ujp       l  16
l  15
 ldci          3
 stri  0       6
l  16
l  14
 lodi  0       7
 lodi  0       6
 lda   1       6
 csp         wri
 lodi  0       9
i   90
 lodi  0       6
 adi
 ldci          1
 adi
 stri  0       9
 lodi  0       5
 inci          1
 stri  0       5
 ujp       l   7
l   8
 lda   1       6
i  100
 csp         wln
 ldci          0
 sroi        159
l   6
 ldoi         28
 ldci          1
 adi
 sroi         28
 ldob         31
 lao           5
 eof
i  110
 not
 and
 fjp       l  17
 ldoi         28
 ldci          6
 lda   1       6
 csp         wri
 lca'                '
 ldci          2
 ldci          2
i  120
 lda   1       6
 csp         wrs
 ldob         33
 fjp       l  18
 ldoi         27
 ldci          7
 lda   1       6
 csp         wri
 ujp       l  19
l  18
 ldoi         26
i  130
 ldci          7
 lda   1       6
 csp         wri
l  19
 ldcc ' '
 ldci          1
 lda   1       6
 csp         wrc
l  17
 ldci          0
 sroi         25
 retp
l   4=        13
l   5=         9
l  20
i  140
 ent   1   l  21
 ent   2   l  22
 ldoi        159
 ldci          9
 geqi
 fjp       l  23
 lao         160
 ldci         10
 deci          1
 ixa           2
i  150
 inca          1
 ldci        255
 stoi
 ldci         10
 sroi        159
 ujp       l  24
l  23
 ldoi        159
 ldci          1
 adi
 sroi        159
i  160
 lao         160
 ldoi        159
 deci          1
 ixa           2
 inca          1
 lodi  0       5
 stoi
l  24
 lao         160
 ldoi        159
 deci          1
i  170
 ixa           2
 ldoi         25
 stoi
 retp
l  21=         6
l  22=         7
l  29
 ent   1   l  30
 ent   2   l  31
 ldob         24
 fjp       l  32
 ldob         31
 fjp       l  33
i  180
 lda   2       6
 csp         wln
l  33
 mst           2
 cup   0   l   3
l  32
 lao           5
 eof
 not
 fjp       l  34
 lao           5
 csp         eln
i  190
 srob         24
 lao          23
 lda   2       5
 csp         rdc
 ldob         31
 fjp       l  35
 ldoc         23
 ldci          1
 lda   2       6
 csp         wrc
l  35
i  200
 ldoi         25
 ldci          1
 adi
 sroi         25
 ujp       l  36
l  34
 lca'   *** eof      '
 ldci         11
 ldci         11
 lda   2       6
 csp         wrs
i  210
 lca'encountered     '
 ldci         11
 ldci         11
 lda   2       6
 csp         wrs
 lda   2       6
 csp         wln
 ldcb          0
 strb  1      40
l  36
 retp
l  30=         5
l  31=         9
l  37
i  220
 ent   1   l  38
 ent   2   l  39
l  40
 mst           1
 cup   0   l  29
 ldoc         23
 ldcc '*'
 neqc
 fjp       l  41
 ldoc         23
 ldcc 't'
i  230
 equc
 fjp       l  42
 mst           1
 cup   0   l  29
 ldoc         23
 ldcc '+'
 equc
 srob         29
 ujp       l  43
l  42
 ldoc         23
i  240
 ldcc 'l'
 equc
 fjp       l  44
 mst           1
 cup   0   l  29
 ldoc         23
 ldcc '+'
 equc
 srob         31
 ldob         31
i  250
 not
 fjp       l  45
 lda   2       6
 csp         wln
l  45
 ujp       l  46
l  44
 ldoc         23
 ldcc 'd'
 equc
 fjp       l  47
 mst           1
i  260
 cup   0   l  29
 ldoc         23
 ldcc '+'
 equc
 srob         34
 ujp       l  48
l  47
 ldoc         23
 ldcc 'c'
 equc
 fjp       l  49
i  270
 mst           1
 cup   0   l  29
 ldoc         23
 ldcc '+'
 equc
 srob         30
l  49
l  48
l  46
l  43
 mst           1
 cup   0   l  29
l  41
 ldoc         23
 ldcc ','
i  280
 neqc
 fjp       l  40
 retp
l  38=         5
l  39=         7
l  25
 ent   1   l  50
 ent   2   l  51
l  26
l  52
l  53
 ldoc         23
 ldcc ' '
 equc
 ldoc         23
 ldcc '	'
i  290
 equc
 ior
 ldob         24
 not
 and
 fjp       l  54
 mst           0
 cup   0   l  29
 ujp       l  53
l  54
 ldob         24
i  300
 strb  0      40
 lodb  0      40
 fjp       l  55
 mst           0
 cup   0   l  29
l  55
 lodb  0      40
 not
 fjp       l  52
 lao         193
 ldoc         23
i  310
 ordc
 ixa           1
 indi          0
 ldci          3
 equi
 fjp       l  56
 ldci         47
 sroi          9
 ldci         15
 sroi         10
i  320
 mst           1
 ldci        399
 cup   1   l  20
 mst           0
 cup   0   l  29
 ujp       l  57
l  56
 lao         193
 ldoc         23
 ordc
 ixa           1
i  330
 indi          0
 ordi
 ujp       l  58
l  60
 ldci          0
 stri  0       5
l  61
 lodi  0       5
 ldci          8
 lesi
 fjp       l  62
 lodi  0       5
i  340
 ldci          1
 adi
 stri  0       5
 lao          14
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  62
 mst           0
i  350
 cup   0   l  29
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ordi
 ldc(  2  3  4  5  6  7  8  9 10)
 inn
 fjp       l  61
i  360
 lodi  0       5
 ldoi         22
 geqi
 fjp       l  63
 lodi  0       5
 sroi         22
 ujp       l  64
l  63
l  65
 lao          14
 ldoi         22
 deci          1
i  370
 ixa           1
 ldcc ' '
 stoc
 ldoi         22
 ldci          1
 sbi
 sroi         22
 ldoi         22
 lodi  0       5
 equi
i  380
 fjp       l  65
l  64
 lao         601
 lodi  0       5
 deci          1
 ixa           1
 indi          0
 stri  0       6
 lao         601
 lodi  0       5
 ldci          1
i  390
 adi
 deci          1
 ixa           1
 indi          0
 ldci          1
 sbi
 stri  0      41
l  66
 lodi  0       6
 lodi  0      41
 leqi
i  400
 fjp       l  67
 lao         321
 lodi  0       6
 deci          1
 ixa           8
 lao          14
 equm          8
 fjp       l  68
 lao         610
 lodi  0       6
i  410
 deci          1
 ixa           1
 indi          0
 sroi          9
 lao         773
 lodi  0       6
 deci          1
 ixa           1
 indi          0
 sroi         10
i  420
 ujp       l  27
l  68
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l  66
l  67
 ldci          0
 sroi          9
 ldci         15
 sroi         10
l  27
 ujp       l  59
l  69
i  430
 ldci         15
 sroi         10
 ldci          0
 stri  0       6
l  70
 lodi  0       6
 ldci          1
 adi
 stri  0       6
 lodi  0       6
 ldoi       1764
i  440
 leqi
 fjp       l  71
 lda   0       7
 lodi  0       6
 deci          1
 ixa           1
 ldoc         23
 stoc
l  71
 mst           0
 cup   0   l  29
i  450
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ldci          1
 neqi
 fjp       l  70
 ldoc         23
 ldcc '.'
i  460
 equc
 ldoc          5
 ldcc '.'
 neqc
 and
 ldoc         23
 ldcc 'e'
 equc
 ior
 fjp       l  72
i  470
 lodi  0       6
 stri  0       5
 ldoc         23
 ldcc '.'
 equc
 fjp       l  73
 lodi  0       5
 ldci          1
 adi
 stri  0       5
i  480
 lodi  0       5
 ldoi       1764
 leqi
 fjp       l  74
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  74
i  490
 mst           0
 cup   0   l  29
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ldci          1
 neqi
 fjp       l  75
i  500
 mst           1
 ldci        201
 cup   1   l  20
 ujp       l  76
l  75
l  77
 lodi  0       5
 ldci          1
 adi
 stri  0       5
 lodi  0       5
 ldoi       1764
i  510
 leqi
 fjp       l  78
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  78
 mst           0
 cup   0   l  29
i  520
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ldci          1
 neqi
 fjp       l  77
l  76
l  73
 ldoc         23
 ldcc 'e'
i  530
 equc
 fjp       l  79
 lodi  0       5
 ldci          1
 adi
 stri  0       5
 lodi  0       5
 ldoi       1764
 leqi
 fjp       l  80
i  540
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  80
 mst           0
 cup   0   l  29
 ldoc         23
 ldcc '+'
i  550
 equc
 ldoc         23
 ldcc '-'
 equc
 ior
 fjp       l  81
 lodi  0       5
 ldci          1
 adi
 stri  0       5
i  560
 lodi  0       5
 ldoi       1764
 leqi
 fjp       l  82
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  82
i  570
 mst           0
 cup   0   l  29
l  81
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ldci          1
 neqi
 fjp       l  83
i  580
 mst           1
 ldci        201
 cup   1   l  20
 ujp       l  84
l  83
l  85
 lodi  0       5
 ldci          1
 adi
 stri  0       5
 lodi  0       5
 ldoi       1764
i  590
 leqi
 fjp       l  86
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 ldoc         23
 stoc
l  86
 mst           0
 cup   0   l  29
i  600
 lao         193
 ldoc         23
 ordc
 ixa           1
 indi          0
 ldci          1
 neqi
 fjp       l  85
l  84
l  79
 lda   0      39
 ldci         17
i  610
 csp         new
 ldci          2
 sroi          9
 loda  0      39
 ldci          0
 stoi
 loda  0      39
 stra  0      41
 ldci          1
 stri  0       6
i  620
 ldci         16
 stri  0      42
l  87
 lodi  0       6
 lodi  0      42
 leqi
 fjp       l  88
 loda  0      41
 inca          1
 lodi  0       6
 deci          1
i  630
 ixa           1
 ldcc ' '
 stoc
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l  87
l  88
 lodi  0       5
 ldoi       1764
 leqi
i  640
 fjp       l  89
 ldci          2
 stri  0       6
 lodi  0       5
 ldci          1
 adi
 stri  0      42
l  90
 lodi  0       6
 lodi  0      42
 leqi
i  650
 fjp       l  91
 loda  0      41
 inca          1
 lodi  0       6
 deci          1
 ixa           1
 lda   0       7
 lodi  0       6
 ldci          1
 sbi
i  660
 deci          1
 ixa           1
 indc          0
 stoc
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l  90
l  91
 ujp       l  92
l  89
 mst           1
i  670
 ldci        203
 cup   1   l  20
 loda  0      41
 inca          1
 ldci          2
 deci          1
 ixa           1
 ldcc '0'
 stoc
 loda  0      41
i  680
 inca          1
 ldci          3
 deci          1
 ixa           1
 ldcc '.'
 stoc
 loda  0      41
 inca          1
 ldci          4
 deci          1
i  690
 ixa           1
 ldcc '0'
 stoc
l  92
 loda  0      39
 sroa         12
 ujp       l  93
l  72
l  28
 lodi  0       6
 ldoi       1764
 grti
 fjp       l  94
i  700
 mst           1
 ldci        203
 cup   1   l  20
 ldci          0
 sroi         12
 ujp       l  95
l  94
 ldci          0
 sroi         12
 ldci          1
 stri  0       5
i  710
 lodi  0       6
 stri  0      41
l  96
 lodi  0       5
 lodi  0      41
 leqi
 fjp       l  97
 ldoi         12
 ldoi       1765
 leqi
 fjp       l  98
i  720
 ldoi         12
 ldci         10
 mpi
 lao        1636
 lda   0       7
 lodi  0       5
 deci          1
 ixa           1
 indc          0
 ordc
i  730
 ixa           1
 indi          0
 adi
 sroi         12
 ujp       l  99
l  98
 mst           1
 ldci        203
 cup   1   l  20
 ldci          0
 sroi         12
l  99
i  740
 lodi  0       5
 inci          1
 stri  0       5
 ujp       l  96
l  97
 ldci          1
 sroi          9
l  95
l  93
 ujp       l  59
l 100
 ldci          0
 sroi         13
 ldci          3
i  750
 sroi          9
 ldci         15
 sroi         10
l 101
l 102
 mst           0
 cup   0   l  29
 ldoi         13
 ldci          1
 adi
 sroi         13
 ldoi         13
i  760
 ldci         16
 leqi
 fjp       l 103
 lda   0      23
 ldoi         13
 deci          1
 ixa           1
 ldoc         23
 stoc
l 103
 ldob         24
i  770
 ldoc         23
 ldcc '''
 equc
 ior
 fjp       l 102
 ldob         24
 fjp       l 104
 mst           1
 ldci        202
 cup   1   l  20
i  780
 ujp       l 105
l 104
 mst           0
 cup   0   l  29
l 105
 ldoc         23
 ldcc '''
 neqc
 fjp       l 101
 ldoi         13
 ldci          1
 sbi
i  790
 sroi         13
 ldoi         13
 ldci          0
 equi
 fjp       l 106
 mst           1
 ldci        205
 cup   1   l  20
 ujp       l 107
l 106
 ldoi         13
i  800
 ldci          1
 equi
 fjp       l 108
 lda   0      23
 ldci          1
 deci          1
 ixa           1
 indc          0
 ordc
 sroi         12
i  810
 ujp       l 109
l 108
 lda   0      39
 ldci         18
 csp         new
 loda  0      39
 ldci          2
 stoi
 ldoi         13
 ldci         16
 grti
i  820
 fjp       l 110
 mst           1
 ldci        399
 cup   1   l  20
 ldci         16
 sroi         13
l 110
 loda  0      39
 stra  0      41
 loda  0      41
 inca          1
i  830
 ldoi         13
 stoi
 ldci          1
 stri  0       6
 ldoi         13
 stri  0      42
l 111
 lodi  0       6
 lodi  0      42
 leqi
 fjp       l 112
i  840
 loda  0      41
 inca          2
 lodi  0       6
 deci          1
 ixa           1
 lda   0      23
 lodi  0       6
 deci          1
 ixa           1
 indc          0
i  850
 stoc
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l 111
l 112
 loda  0      39
 sroa         12
l 109
l 107
 ujp       l  59
l 113
 ldci         15
 sroi         10
i  860
 mst           0
 cup   0   l  29
 ldoc         23
 ldcc '='
 equc
 fjp       l 114
 ldci         17
 sroi          9
 mst           0
 cup   0   l  29
i  870
 ujp       l 115
l 114
 ldci         16
 sroi          9
l 115
 ujp       l  59
l 116
 ldci         15
 sroi         10
 mst           0
 cup   0   l  29
 ldoc         23
 ldcc '.'
i  880
 equc
 fjp       l 117
 ldci         16
 sroi          9
 mst           0
 cup   0   l  29
 ujp       l 118
l 117
 ldci         14
 sroi          9
l 118
 ujp       l  59
l 119
i  890
 mst           0
 cup   0   l  29
 ldci          7
 sroi          9
 ldoc         23
 ldcc '='
 equc
 fjp       l 120
 ldci          9
 sroi         10
i  900
 mst           0
 cup   0   l  29
 ujp       l 121
l 120
 ldoc         23
 ldcc '>'
 equc
 fjp       l 122
 ldci         12
 sroi         10
 mst           0
i  910
 cup   0   l  29
 ujp       l 123
l 122
 ldci          8
 sroi         10
l 123
l 121
 ujp       l  59
l 124
 mst           0
 cup   0   l  29
 ldci          7
 sroi          9
 ldoc         23
i  920
 ldcc '='
 equc
 fjp       l 125
 ldci         10
 sroi         10
 mst           0
 cup   0   l  29
 ujp       l 126
l 125
 ldci         11
 sroi         10
l 126
i  930
 ujp       l  59
l 127
 mst           0
 cup   0   l  29
 ldoc         23
 ldcc '*'
 equc
 fjp       l 128
 mst           0
 cup   0   l  29
 ldoc         23
i  940
 ldcc '$'
 equc
 fjp       l 129
 mst           0
 cup   0   l  37
l 129
l 130
l 131
 ldoc         23
 ldcc '*'
 neqc
 lao           5
 eof
i  950
 not
 and
 fjp       l 132
 mst           0
 cup   0   l  29
 ujp       l 131
l 132
 mst           0
 cup   0   l  29
 ldoc         23
 ldcc ')'
i  960
 equc
 lao           5
 eof
 ior
 fjp       l 130
 mst           0
 cup   0   l  29
 ujp       l  26
l 128
 ldci          8
 sroi          9
i  970
 ldci         15
 sroi         10
 ujp       l  59
l 133
 lao         645
 ldoc         23
 ordc
 ixa           1
 indi          0
 sroi          9
 lao         808
i  980
 ldoc         23
 ordc
 ixa           1
 indi          0
 sroi         10
 mst           0
 cup   0   l  29
 ujp       l  59
l 134
 ldci         47
 sroi          9
i  990
 ujp       l  59
l  58
 chki  0      10
 ldci          0
 sbi
 xjp       l 135
l 135
 ujp       l  60
 ujp       l  69
 ujp       l 133
 ujc
 ujp       l 100
i 1000
 ujp       l 113
 ujp       l 116
 ujp       l 119
 ujp       l 124
 ujp       l 127
 ujp       l 134
l  59
l  57
 retp
l  50=        43
l  51=        18
l 136
 ent   1   l 137
 ent   2   l 138
 lda   0       6
i 1010
 loda  0       5
 mov           8
 lao          54
 ldoi         52
 ixa           5
 inda          0
 stra  0      15
 loda  0      15
 ldcn
 equa
i 1020
 fjp       l 139
 lao          54
 ldoi         52
 ixa           5
 loda  0       5
 stoa
 ujp       l 140
l 139
l 141
 loda  0      15
 stra  0      14
 loda  0      15
i 1030
 lda   0       6
 equm          8
 fjp       l 142
 mst           1
 ldci        101
 cup   1   l  20
 loda  0      15
 inda          8
 stra  0      15
 ldcb          0
i 1040
 strb  0      16
 ujp       l 143
l 142
 loda  0      15
 lda   0       6
 lesm          8
 fjp       l 144
 loda  0      15
 inda          8
 stra  0      15
 ldcb          0
i 1050
 strb  0      16
 ujp       l 145
l 144
 loda  0      15
 inda          9
 stra  0      15
 ldcb          1
 strb  0      16
l 145
l 143
 loda  0      15
 ldcn
 equa
i 1060
 fjp       l 141
 lodb  0      16
 fjp       l 146
 loda  0      14
 inca          9
 loda  0       5
 stoa
 ujp       l 147
l 146
 loda  0      14
 inca          8
i 1070
 loda  0       5
 stoa
l 147
l 140
 loda  0       5
 inca          9
 ldcn
 stoa
 loda  0       5
 inca          8
 ldcn
 stoa
i 1080
 retp
l 137=        17
l 138=         8
l 148
 ent   1   l 150
 ent   2   l 151
l 152
 loda  0       5
 ldcn
 neqa
 fjp       l 153
 loda  0       5
 lao          14
 equm          8
i 1090
 fjp       l 154
 ujp       l 149
 ujp       l 155
l 154
 loda  0       5
 lao          14
 lesm          8
 fjp       l 156
 loda  0       5
 inda          8
 stra  0       5
i 1100
 ujp       l 157
l 156
 loda  0       5
 inda          9
 stra  0       5
l 157
l 155
 ujp       l 152
l 153
l 149
 loda  0       6
 loda  0       5
 stoa
 retp
l 150=         7
l 151=         7
l 158
 ent   1   l 160
i 1110
 ent   2   l 161
 ldoi         52
 sroi         53
 ldci          0
 stri  0       8
l 162
 ldoi         53
 lodi  0       8
 geqi
 fjp       l 163
 lao          54
i 1120
 ldoi         53
 ixa           5
 inda          0
 stra  0       7
l 164
 loda  0       7
 ldcn
 neqa
 fjp       l 165
 loda  0       7
 lao          14
i 1130
 equm          8
 fjp       l 166
 loda  0       7
 indi         12
 ordi
 lods  0       5
 inn
 fjp       l 167
 ujp       l 159
 ujp       l 168
l 167
i 1140
 ldob         32
 fjp       l 169
 mst           1
 ldci        103
 cup   1   l  20
l 169
 loda  0       7
 inda          8
 stra  0       7
l 168
 ujp       l 170
l 166
 loda  0       7
i 1150
 lao          14
 lesm          8
 fjp       l 171
 loda  0       7
 inda          8
 stra  0       7
 ujp       l 172
l 171
 loda  0       7
 inda          9
 stra  0       7
l 172
l 170
i 1160
 ujp       l 164
l 165
 ldoi         53
 deci          1
 sroi         53
 ujp       l 162
l 163
 ldob         32
 fjp       l 173
 mst           1
 ldci        104
 cup   1   l  20
i 1170
 ldci          0
 ordi
 lods  0       5
 inn
 fjp       l 174
 ldoa         48
 stra  0       7
 ujp       l 175
l 174
 ldci          2
 ordi
i 1180
 lods  0       5
 inn
 fjp       l 176
 ldoa         46
 stra  0       7
 ujp       l 177
l 176
 ldci          3
 ordi
 lods  0       5
 inn
i 1190
 fjp       l 178
 ldoa         45
 stra  0       7
 ujp       l 179
l 178
 ldci          1
 ordi
 lods  0       5
 inn
 fjp       l 180
 ldoa         47
i 1200
 stra  0       7
 ujp       l 181
l 180
 ldci          4
 ordi
 lods  0       5
 inn
 fjp       l 182
 ldoa         44
 stra  0       7
 ujp       l 183
l 182
i 1210
 ldoa         43
 stra  0       7
l 183
l 181
l 179
l 177
l 175
l 173
l 159
 loda  0       6
 loda  0       7
 stoa
 retp
l 160=         9
l 161=         9
l 184
 ent   1   l 185
 ent   2   l 186
 loda  0       6
 ldci          0
i 1220
 stoi
 loda  0       7
 ldci          0
 stoi
 loda  0       5
 ldcn
 neqa
 fjp       l 187
 loda  0       5
 stra  0       8
i 1230
 loda  0       8
 indi          2
 ldci          1
 equi
 fjp       l 188
 loda  0       6
 loda  0       8
 indi          7
 stoi
 loda  0       7
i 1240
 loda  0       8
 indi          5
 stoi
 ujp       l 189
l 188
 loda  0       5
 ldoa         38
 equa
 fjp       l 190
 loda  0       6
 ldci          0
i 1250
 stoi
 loda  0       7
 ldci        127
 stoi
 ujp       l 191
l 190
 loda  0       8
 inda          4
 ldcn
 neqa
 fjp       l 192
i 1260
 loda  0       7
 loda  0       8
 inda          4
 indi         14
 stoi
l 192
l 191
l 189
l 187
 retp
l 185=         9
l 186=         7
l 193
 ent   1   l 194
 ent   2   l 195
 ldci          1
 stri  0       0
i 1270
 loda  0       5
 ldcn
 neqa
 fjp       l 196
 loda  0       5
 stra  0       6
 loda  0       6
 indi          2
 ordi
 ujp       l 197
l 199
i 1280
 loda  0       5
 ldoa         40
 equa
 fjp       l 200
 ldci          1
 stri  0       0
 ujp       l 201
l 200
 loda  0       5
 ldoa         37
 equa
i 1290
 fjp       l 202
 ldci          1
 stri  0       0
 ujp       l 203
l 202
 loda  0       6
 indi          3
 ldci          1
 equi
 fjp       l 204
 ldci          1
i 1300
 stri  0       0
 ujp       l 205
l 204
 loda  0       5
 ldoa         38
 equa
 fjp       l 206
 ldci          1
 stri  0       0
 ujp       l 207
l 206
 loda  0       5
i 1310
 ldoa         39
 equa
 fjp       l 208
 ldci          1
 stri  0       0
 ujp       l 209
l 208
 ldci          1
 stri  0       0
l 209
l 207
l 205
l 203
l 201
 ujp       l 198
l 210
 mst           1
i 1320
 loda  0       6
 inda          3
 cup   1   l 193
 stri  0       0
 ujp       l 198
l 211
 ldci          1
 stri  0       0
 ujp       l 198
l 212
 ldci          1
 stri  0       0
i 1330
 ujp       l 198
l 213
 ldci          1
 stri  0       0
 ujp       l 198
l 214
 mst           1
 loda  0       6
 inda          4
 cup   1   l 193
 stri  0       0
 ujp       l 198
l 215
i 1340
 ldci          1
 stri  0       0
 ujp       l 198
l 216
 mst           1
 ldci        501
 cup   1   l  20
 ujp       l 198
l 197
 chki  0       8
 ldci          0
 sbi
i 1350
 xjp       l 217
l 217
 ujp       l 199
 ujp       l 210
 ujp       l 211
 ujp       l 212
 ujp       l 214
 ujp       l 215
 ujp       l 213
 ujp       l 216
 ujp       l 216
l 198
l 196
i 1360
 reti
l 194=         7
l 195=         8
l 218
 ent   1   l 219
 ent   2   l 220
 mst           1
 loda  0       5
 cup   1   l 193
 stri  0       8
 loda  0       6
 indi          0
 ldci          1
i 1370
 sbi
 stri  0       7
 loda  0       6
 lodi  0       7
 lodi  0       8
 adi
 lodi  0       8
 lodi  0       7
 adi
 lodi  0       8
i 1380
 mod
 sbi
 stoi
 retp
l 219=         9
l 220=         9
l 224
 ent   1   l 225
 ent   2   l 226
 loda  0       5
 ldcn
 neqa
 fjp       l 227
i 1390
 loda  0       5
 stra  0       6
 loda  0       6
 ldcb          1
 stob
 loda  0       6
 indi          2
 ordi
 ujp       l 228
l 230
 ujp       l 229
l 231
i 1400
 mst           1
 loda  0       6
 inda          3
 cup   1   l 224
 ujp       l 229
l 232
 ujp       l 229
l 233
 mst           1
 loda  0       6
 inda          3
 cup   1   l 224
i 1410
 ujp       l 229
l 234
 mst           1
 loda  0       6
 inda          4
 cup   1   l 224
 mst           1
 loda  0       6
 inda          3
 cup   1   l 224
 ujp       l 229
l 235
i 1420
 mst           1
 loda  0       6
 inda          3
 cup   1   l 223
 mst           1
 loda  0       6
 inda          4
 cup   1   l 224
 ujp       l 229
l 236
 mst           1
i 1430
 loda  0       6
 inda          3
 cup   1   l 224
 ujp       l 229
l 237
 mst           1
 loda  0       6
 inda          4
 cup   1   l 224
 ujp       l 229
l 238
 mst           1
i 1440
 loda  0       6
 inda          4
 cup   1   l 224
 mst           1
 loda  0       6
 inda          3
 cup   1   l 224
 ujp       l 229
l 228
 chki  0       8
 ldci          0
i 1450
 sbi
 xjp       l 239
l 239
 ujp       l 230
 ujp       l 231
 ujp       l 232
 ujp       l 233
 ujp       l 234
 ujp       l 235
 ujp       l 236
 ujp       l 237
i 1460
 ujp       l 238
l 229
l 227
 retp
l 225=         7
l 226=        17
l 223
 ent   1   l 240
 ent   2   l 241
 loda  0       5
 ldcn
 neqa
 fjp       l 242
 loda  0       5
 stra  0       6
i 1470
 mst           1
 loda  0       6
 inda          9
 cup   1   l 223
 mst           1
 loda  0       6
 inda          8
 cup   1   l 223
 mst           1
 loda  0       6
i 1480
 inda         10
 cup   1   l 224
l 242
 retp
l 240=         7
l 241=         8
l 222
 ent   1   l 243
 ent   2   l 244
 ldoi         52
 stri  0       5
 lodi  1       6
 stri  0       6
l 245
 lodi  0       5
i 1490
 lodi  0       6
 geqi
 fjp       l 246
 mst           0
 lao          54
 lodi  0       5
 ixa           5
 inda          0
 cup   1   l 223
 lodi  0       5
i 1500
 deci          1
 stri  0       5
 ujp       l 245
l 246
 retp
l 243=         7
l 244=         7
l 248
 ent   1   l 249
 ent   2   l 250
 loda  0       5
 ldcn
 neqa
 fjp       l 251
i 1510
 loda  0       5
 stra  0       6
 loda  0       6
 indb          0
 fjp       l 252
 loda  0       6
 ldcb          0
 stob
 ldcc ' '
 ldci          4
i 1520
 lda   2       6
 csp         wrc
 loda  0       5
 orda
 ldci          6
 lda   2       6
 csp         wri
 loda  0       6
 indi          1
 ldci         10
i 1530
 lda   2       6
 csp         wri
 loda  0       6
 indi          2
 ordi
 ujp       l 253
l 255
 lca'scalar          '
 ldci         10
 ldci          6
 lda   2       6
i 1540
 csp         wrs
 loda  0       6
 indi          3
 ldci          0
 equi
 fjp       l 256
 lca'standard        '
 ldci         10
 ldci          8
 lda   2       6
i 1550
 csp         wrs
 ujp       l 257
l 256
 lca'declared        '
 ldci         10
 ldci          8
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
i 1560
 csp         wrc
 loda  0       6
 inda          4
 orda
 ldci          6
 lda   2       6
 csp         wri
l 257
 lda   2       6
 csp         wln
 ujp       l 254
l 258
i 1570
 lca'subrange        '
 ldci         10
 ldci          8
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
i 1580
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 loda  0       6
 inda          3
 ldoa         39
 neqa
 fjp       l 259
i 1590
 loda  0       6
 indi          7
 ldci         10
 lda   2       6
 csp         wri
 loda  0       6
 indi          5
 ldci         10
 lda   2       6
 csp         wri
i 1600
 ujp       l 260
l 259
 loda  0       6
 inda          7
 ldcn
 neqa
 loda  0       6
 inda          5
 ldcn
 neqa
 and
i 1610
 fjp       l 261
 ldcc ' '
 ldci          1
 lda   2       6
 csp         wrc
 loda  0       6
 inda          7
 inca          1
 ldci          9
 ldci         16
i 1620
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          1
 lda   2       6
 csp         wrc
 loda  0       6
 inda          5
 inca          1
 ldci          9
i 1630
 ldci         16
 lda   2       6
 csp         wrs
l 261
l 260
 lda   2       6
 csp         wln
 mst           1
 loda  0       6
 inda          3
 cup   1   l 248
 ujp       l 254
l 262
i 1640
 lca'pointer         '
 ldci         10
 ldci          7
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
i 1650
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 ujp       l 254
l 263
 lca'set             '
 ldci         10
i 1660
 ldci          3
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
 inda          3
 orda
i 1670
 ldci          6
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 mst           1
 loda  0       6
 inda          3
 cup   1   l 248
 ujp       l 254
l 264
i 1680
 lca'array           '
 ldci         10
 ldci          5
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
i 1690
 inda          4
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
i 1700
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 mst           1
 loda  0       6
 inda          4
i 1710
 cup   1   l 248
 mst           1
 loda  0       6
 inda          3
 cup   1   l 248
 ujp       l 254
l 265
 lca'record          '
 ldci         10
 ldci          6
 lda   2       6
i 1720
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
 inda          3
 orda
 ldci          6
 lda   2       6
i 1730
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
 inda          4
 orda
 ldci          6
 lda   2       6
i 1740
 csp         wri
 lda   2       6
 csp         wln
 mst           1
 loda  0       6
 inda          3
 cup   1   l 247
 mst           1
 loda  0       6
 inda          4
i 1750
 cup   1   l 248
 ujp       l 254
l 266
 lca'file            '
 ldci         10
 ldci          4
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
i 1760
 csp         wrc
 loda  0       6
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 mst           1
 loda  0       6
 inda          3
i 1770
 cup   1   l 248
 ujp       l 254
l 267
 lca'tagfld          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
i 1780
 csp         wrc
 loda  0       6
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
i 1790
 csp         wrc
 loda  0       6
 inda          4
 orda
 ldci          6
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 mst           1
i 1800
 loda  0       6
 inda          4
 cup   1   l 248
 ujp       l 254
l 268
 lca'variant         '
 ldci         10
 ldci          7
 lda   2       6
 csp         wrs
 ldcc ' '
i 1810
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
 inda          4
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
i 1820
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       6
 inda          3
 orda
 ldci          6
 lda   2       6
 csp         wri
 loda  0       6
i 1830
 indi          6
 ldci         10
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 mst           1
 loda  0       6
 inda          4
 cup   1   l 248
i 1840
 mst           1
 loda  0       6
 inda          3
 cup   1   l 248
 ujp       l 254
l 253
 chki  0       8
 ldci          0
 sbi
 xjp       l 269
l 269
 ujp       l 255
i 1850
 ujp       l 258
 ujp       l 262
 ujp       l 263
 ujp       l 264
 ujp       l 265
 ujp       l 266
 ujp       l 267
 ujp       l 268
l 254
l 252
l 251
 retp
l 249=         7
l 250=        18
l 247
 ent   1   l 270
i 1860
 ent   2   l 271
 loda  0       5
 ldcn
 neqa
 fjp       l 272
 loda  0       5
 stra  0       7
 ldcc ' '
 ldci          4
 lda   2       6
i 1870
 csp         wrc
 loda  0       5
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          1
 lda   2       6
 csp         wrc
i 1880
 loda  0       7
 ldci          9
 ldci          8
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 1890
 inda          9
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 1900
 inda          8
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 1910
 inda         10
 orda
 ldci          6
 lda   2       6
 csp         wri
 loda  0       7
 indi         12
 ordi
 ujp       l 273
l 275
 lca'type            '
i 1920
 ldci         10
 ldci          4
 lda   2       6
 csp         wrs
 ujp       l 274
l 276
 lca'constant        '
 ldci         10
 ldci          8
 lda   2       6
 csp         wrs
i 1930
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
 inda         11
 orda
 ldci          6
 lda   2       6
 csp         wri
i 1940
 loda  0       7
 inda         10
 ldcn
 neqa
 fjp       l 277
 loda  0       7
 inda         10
 ldoa         39
 equa
 fjp       l 278
i 1950
 loda  0       7
 inda         14
 ldcn
 neqa
 fjp       l 279
 ldcc ' '
 ldci          1
 lda   2       6
 csp         wrc
 loda  0       7
i 1960
 inda         14
 inca          1
 ldci          9
 ldci         16
 lda   2       6
 csp         wrs
l 279
 ujp       l 280
l 278
 loda  0       7
 inda         10
 indi          2
i 1970
 ldci          4
 equi
 fjp       l 281
 loda  0       7
 inda         14
 ldcn
 neqa
 fjp       l 282
 ldcc ' '
 ldci          1
i 1980
 lda   2       6
 csp         wrc
 loda  0       7
 inda         14
 stra  0       8
 ldci          1
 stri  0       6
 loda  0       8
 indi          1
 stri  0       9
l 283
i 1990
 lodi  0       6
 lodi  0       9
 leqi
 fjp       l 284
 loda  0       8
 inca          2
 lodi  0       6
 deci          1
 ixa           1
 indc          0
i 2000
 ldci          1
 lda   2       6
 csp         wrc
 lodi  0       6
 inci          1
 stri  0       6
 ujp       l 283
l 284
l 282
 ujp       l 285
l 281
 loda  0       7
 indi         14
i 2010
 ldci         10
 lda   2       6
 csp         wri
l 285
l 280
l 277
 ujp       l 274
l 286
 lca'variable        '
 ldci         10
 ldci          8
 lda   2       6
 csp         wrs
 loda  0       7
i 2020
 indi         13
 ldci          0
 equi
 fjp       l 287
 lca'actual          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
 ujp       l 288
l 287
i 2030
 lca'formal          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
l 288
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 2040
 inda         11
 orda
 ldci          6
 lda   2       6
 csp         wri
 loda  0       7
 indi         14
 ldci         10
 lda   2       6
 csp         wri
i 2050
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
 indi         15
 ldci          6
 lda   2       6
 csp         wri
 ujp       l 274
l 289
i 2060
 lca'field           '
 ldci         10
 ldci          5
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 2070
 inda         11
 orda
 ldci          6
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
i 2080
 indi         13
 ldci          6
 lda   2       6
 csp         wri
 ujp       l 274
l 290
 loda  0       7
 indi         12
 ldci          4
 equi
 fjp       l 291
i 2090
 lca'procedure       '
 ldci         10
 ldci          9
 lda   2       6
 csp         wrs
 ujp       l 292
l 291
 lca'function        '
 ldci         10
 ldci          8
 lda   2       6
i 2100
 csp         wrs
l 292
 loda  0       7
 indi         13
 ldci          0
 equi
 fjp       l 293
 lca'standard        '
 ldci         10
 ldci          8
 lda   2       6
i 2110
 csp         wrs
 loda  0       7
 indi         14
 ldci         10
 lda   2       6
 csp         wri
 ujp       l 294
l 293
 lca'declared        '
 ldci         10
 ldci          8
i 2120
 lda   2       6
 csp         wrs
 ldcc ' '
 ldci          4
 lda   2       6
 csp         wrc
 loda  0       7
 inda         11
 orda
 ldci          6
i 2130
 lda   2       6
 csp         wri
 loda  0       7
 indi         14
 ldci         10
 lda   2       6
 csp         wri
 ldcc ' '
 ldci          4
 lda   2       6
i 2140
 csp         wrc
 loda  0       7
 indi         15
 ldci          6
 lda   2       6
 csp         wri
 loda  0       7
 indi         16
 ldci          0
 equi
i 2150
 fjp       l 295
 lca'actual          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
 loda  0       7
 indb         18
 fjp       l 296
 lca'forward         '
i 2160
 ldci         10
 ldci          7
 lda   2       6
 csp         wrs
 ujp       l 297
l 296
 lca'notforward      '
 ldci         10
 ldci         10
 lda   2       6
 csp         wrs
l 297
i 2170
 loda  0       7
 indb         17
 fjp       l 298
 lca'extern          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
 ujp       l 299
l 298
 lca'not extern      '
i 2180
 ldci         10
 ldci         10
 lda   2       6
 csp         wrs
l 299
 ujp       l 300
l 295
 lca'formal          '
 ldci         10
 ldci          6
 lda   2       6
 csp         wrs
l 300
l 294
i 2190
 ujp       l 274
l 273
 chki  0       5
 ldci          0
 sbi
 xjp       l 301
l 301
 ujp       l 275
 ujp       l 276
 ujp       l 286
 ujp       l 289
 ujp       l 290
i 2200
 ujp       l 290
l 274
 lda   2       6
 csp         wln
 mst           1
 loda  0       7
 inda          9
 cup   1   l 247
 mst           1
 loda  0       7
 inda          8
i 2210
 cup   1   l 247
 mst           1
 loda  0       7
 inda         10
 cup   1   l 248
l 272
 retp
l 270=        10
l 271=        10
l 221
 ent   1   l 302
 ent   2   l 303
 lda   1       6
 csp         wln
i 2220
 lda   1       6
 csp         wln
 lda   1       6
 csp         wln
 lodb  0       5
 fjp       l 304
 ldci          0
 stri  0       6
 ujp       l 305
l 304
 ldoi         52
i 2230
 stri  0       6
 lca' local          '
 ldci          6
 ldci          6
 lda   1       6
 csp         wrs
l 305
 lca' tables         '
 ldci          8
 ldci          8
 lda   1       6
i 2240
 csp         wrs
 lda   1       6
 csp         wln
 lda   1       6
 csp         wln
 mst           0
 cup   0   l 222
 ldoi         52
 stri  0       7
 lodi  0       6
i 2250
 stri  0       8
l 306
 lodi  0       7
 lodi  0       8
 geqi
 fjp       l 307
 mst           0
 lao          54
 lodi  0       7
 ixa           5
 inda          0
i 2260
 cup   1   l 247
 lodi  0       7
 deci          1
 stri  0       7
 ujp       l 306
l 307
 lda   1       6
 csp         wln
 ldob         24
 not
 fjp       l 308
i 2270
 ldcc ' '
 ldoi         25
 ldci         16
 adi
 lda   1       6
 csp         wrc
l 308
 retp
l 302=         9
l 303=         9
l 309
 ent   1   l 310
 ent   2   l 311
 ldoi       1766
i 2280
 ldci          1
 adi
 sroi       1766
 loda  0       5
 ldoi       1766
 stoi
 retp
l 310=         6
l 311=         7
l 313
 ent   1   l 314
 ent   2   l 315
 lao           5
i 2290
 eof
 not
 fjp       l 316
l 317
 ldoi          9
 ordi
 lods  0       5
 inn
 not
 lao           5
 eof
i 2300
 not
 and
 fjp       l 318
 mst           2
 cup   0   l  25
 ujp       l 317
l 318
 ldoi          9
 ordi
 lods  0       5
 inn
i 2310
 not
 fjp       l 319
 mst           2
 cup   0   l  25
l 319
l 316
 retp
l 314=         6
l 315=         7
l 320
 ent   1   l 321
 ent   2   l 322
 ldcn
 stra  0       8
 loda  0       7
i 2320
 inca          1
 ldci          0
 stoi
 ldoi          9
 ordi
 ldos        192
 inn
 not
 fjp       l 323
 mst           2
i 2330
 ldci         50
 cup   1   l  20
 mst           1
 lods  0       5
 ldos        192
 uni
 cup   1   l 313
l 323
 ldoi          9
 ordi
 ldos        192
i 2340
 inn
 fjp       l 324
 ldoi          9
 ldci          3
 equi
 fjp       l 325
 ldoi         13
 ldci          1
 equi
 fjp       l 326
i 2350
 ldoa         38
 stra  0       8
 ujp       l 327
l 326
 lda   0       8
 ldci          5
 csp         new
 loda  0       8
 stra  0      13
 loda  0      13
 inca          4
i 2360
 ldoa         38
 stoa
 loda  0      13
 inca          3
 ldcn
 stoa
 loda  0      13
 inca          1
 ldoi         13
 ldci          1
i 2370
 mpi
 stoi
 loda  0      13
 inca          2
 ldci          4
 stoi
l 327
 loda  0       7
 lao          11
 mov           2
 mst           2
i 2380
 cup   0   l  25
 ujp       l 328
l 325
 ldci          0
 stri  0      10
 ldoi          9
 ldci          6
 equi
 ldoi         10
 ordi
 ldc(  5  6)
i 2390
 inn
 and
 fjp       l 329
 ldoi         10
 ldci          5
 equi
 fjp       l 330
 ldci          1
 stri  0      10
 ujp       l 331
l 330
i 2400
 ldci          2
 stri  0      10
l 331
 mst           2
 cup   0   l  25
l 329
 ldoi          9
 ldci          0
 equi
 fjp       l 332
 mst           2
 ldc(  1)
i 2410
 lda   0       9
 cup   2   l 158
 loda  0       9
 stra  0      13
 loda  0      13
 inda         10
 stra  0       8
 loda  0       7
 loda  0      13
 inca         13
i 2420
 mov           2
 lodi  0      10
 ldci          0
 neqi
 fjp       l 333
 loda  0       8
 ldoa         40
 equa
 fjp       l 334
 lodi  0      10
i 2430
 ldci          2
 equi
 fjp       l 335
 loda  0       7
 inca          1
 loda  0       7
 indi          1
 ngi
 stoi
l 335
 ujp       l 336
l 334
i 2440
 loda  0       8
 ldoa         39
 equa
 fjp       l 337
 lodi  0      10
 ldci          2
 equi
 fjp       l 338
 lda   0      11
 ldci         17
i 2450
 csp         new
 loda  0       7
 inda          1
 inca          1
 ldci          1
 deci          1
 ixa           1
 indc          0
 ldcc '-'
 equc
i 2460
 fjp       l 339
 loda  0      11
 inca          1
 ldci          1
 deci          1
 ixa           1
 ldcc '+'
 stoc
 ujp       l 340
l 339
 loda  0      11
i 2470
 inca          1
 ldci          1
 deci          1
 ixa           1
 ldcc '-'
 stoc
l 340
 ldci          2
 stri  0      12
 ldci         16
 stri  0      13
l 341
i 2480
 lodi  0      12
 lodi  0      13
 leqi
 fjp       l 342
 loda  0      11
 inca          1
 lodi  0      12
 deci          1
 ixa           1
 loda  0       7
i 2490
 inda          1
 inca          1
 lodi  0      12
 deci          1
 ixa           1
 indc          0
 stoc
 lodi  0      12
 inci          1
 stri  0      12
i 2500
 ujp       l 341
l 342
 loda  0       7
 inca          1
 loda  0      11
 stoa
l 338
 ujp       l 343
l 337
 mst           2
 ldci        105
 cup   1   l  20
l 343
l 336
l 333
 mst           2
i 2510
 cup   0   l  25
 ujp       l 344
l 332
 ldoi          9
 ldci          1
 equi
 fjp       l 345
 lodi  0      10
 ldci          2
 equi
 fjp       l 346
i 2520
 ldoi         12
 ngi
 sroi         12
l 346
 ldoa         40
 stra  0       8
 loda  0       7
 lao          11
 mov           2
 mst           2
 cup   0   l  25
i 2530
 ujp       l 347
l 345
 ldoi          9
 ldci          2
 equi
 fjp       l 348
 lodi  0      10
 ldci          2
 equi
 fjp       l 349
 ldoa         12
i 2540
 inca          1
 ldci          1
 deci          1
 ixa           1
 ldcc '-'
 stoc
l 349
 ldoa         39
 stra  0       8
 loda  0       7
 lao          11
i 2550
 mov           2
 mst           2
 cup   0   l  25
 ujp       l 350
l 348
 mst           2
 ldci        106
 cup   1   l  20
 mst           1
 lods  0       5
 cup   1   l 313
l 350
l 347
l 344
l 328
i 2560
 ldoi          9
 ordi
 lods  0       5
 inn
 not
 fjp       l 351
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
i 2570
 lods  0       5
 cup   1   l 313
l 351
l 324
 loda  0       6
 loda  0       8
 stoa
 retp
l 321=        14
l 322=        16
l 352
 ent   1   l 353
 ent   2   l 354
 loda  0       5
 ldcn
i 2580
 equa
 loda  0       6
 ldcn
 equa
 ior
 fjp       l 355
 ldcb          1
 strb  0       0
 ujp       l 356
l 355
 mst           2
i 2590
 loda  0       5
 lda   0      10
 lda   0       8
 cup   3   l 184
 mst           2
 loda  0       6
 lda   0       9
 lda   0       7
 cup   3   l 184
 lodi  0      10
i 2600
 lodi  0       9
 equi
 lodi  0       8
 lodi  0       7
 equi
 and
 strb  0       0
l 356
 retb
l 353=        11
l 354=        14
l 357
 ent   1   l 358
 ent   2   l 359
i 2610
 loda  0       5
 loda  0       6
 equa
 fjp       l 360
 ldcb          1
 strb  0       0
 ujp       l 361
l 360
 loda  0       5
 ldcn
 neqa
i 2620
 loda  0       6
 ldcn
 neqa
 and
 fjp       l 362
 loda  0       5
 indi          2
 loda  0       6
 indi          2
 equi
i 2630
 fjp       l 363
 loda  0       5
 indi          2
 ordi
 ujp       l 364
l 366
 ldcb          0
 strb  0       0
 ujp       l 365
l 367
 mst           1
 loda  0       5
i 2640
 inda          3
 loda  0       6
 inda          3
 cup   2   l 357
 strb  0       0
 ujp       l 365
l 368
 ldcb          0
 strb  0       9
 ldoa         50
 stra  0      11
i 2650
 ldoa         50
 stra  0      10
l 369
 loda  0      11
 ldcn
 neqa
 fjp       l 370
 loda  0      11
 stra  0      12
 loda  0      12
 inda          1
i 2660
 loda  0       5
 inda          3
 equa
 loda  0      12
 inda          0
 loda  0       6
 inda          3
 equa
 and
 fjp       l 371
i 2670
 ldcb          1
 strb  0       9
l 371
 loda  0      12
 inda          2
 stra  0      11
 ujp       l 369
l 370
 lodb  0       9
 not
 fjp       l 372
 lda   0      11
i 2680
 ldci          3
 csp         new
 loda  0      11
 stra  0      12
 loda  0      12
 inca          1
 loda  0       5
 inda          3
 stoa
 loda  0      12
i 2690
 loda  0       6
 inda          3
 stoa
 loda  0      12
 inca          2
 ldoa         50
 stoa
 loda  0      11
 sroa         50
 mst           1
i 2700
 loda  0       5
 inda          3
 loda  0       6
 inda          3
 cup   2   l 357
 strb  0       9
l 372
 lodb  0       9
 strb  0       0
 loda  0      10
 sroa         50
i 2710
 ujp       l 365
l 373
 mst           1
 loda  0       5
 inda          3
 loda  0       6
 inda          3
 cup   2   l 357
 strb  0       0
 ujp       l 365
l 374
 mst           1
i 2720
 loda  0       5
 inda          4
 loda  0       6
 inda          4
 cup   2   l 357
 mst           1
 loda  0       5
 inda          3
 loda  0       6
 inda          3
i 2730
 cup   2   l 357
 and
 strb  0       9
 lodb  0       9
 loda  0       5
 indi          1
 loda  0       6
 indi          1
 equi
 and
i 2740
 mst           1
 loda  0       5
 inda          3
 loda  0       6
 inda          3
 cup   2   l 352
 and
 strb  0       0
 ujp       l 365
l 375
 loda  0       5
i 2750
 inda          3
 stra  0       8
 loda  0       6
 inda          3
 stra  0       7
 ldcb          1
 strb  0       9
l 376
 loda  0       8
 ldcn
 neqa
i 2760
 loda  0       7
 ldcn
 neqa
 and
 fjp       l 377
 lodb  0       9
 mst           1
 loda  0       8
 inda         10
 loda  0       7
i 2770
 inda         10
 cup   2   l 357
 and
 strb  0       9
 loda  0       8
 inda         11
 stra  0       8
 loda  0       7
 inda         11
 stra  0       7
i 2780
 ujp       l 376
l 377
 lodb  0       9
 loda  0       8
 ldcn
 equa
 and
 loda  0       7
 ldcn
 equa
 and
i 2790
 loda  0       5
 inda          4
 ldcn
 equa
 and
 loda  0       6
 inda          4
 ldcn
 equa
 and
i 2800
 strb  0       0
 ujp       l 365
l 378
 mst           1
 loda  0       5
 inda          3
 loda  0       6
 inda          3
 cup   2   l 357
 strb  0       0
 ujp       l 365
l 364
i 2810
 chki  0       6
 ldci          0
 sbi
 xjp       l 379
l 379
 ujp       l 366
 ujp       l 367
 ujp       l 368
 ujp       l 373
 ujp       l 374
 ujp       l 375
i 2820
 ujp       l 378
l 365
 ujp       l 380
l 363
 loda  0       5
 indi          2
 ldci          1
 equi
 fjp       l 381
 mst           1
 loda  0       5
 inda          3
i 2830
 loda  0       6
 cup   2   l 357
 strb  0       0
 ujp       l 382
l 381
 loda  0       6
 indi          2
 ldci          1
 equi
 fjp       l 383
 mst           1
i 2840
 loda  0       5
 loda  0       6
 inda          3
 cup   2   l 357
 strb  0       0
 ujp       l 384
l 383
 ldcb          0
 strb  0       0
l 384
l 382
l 380
 ujp       l 385
l 362
 ldcb          1
i 2850
 strb  0       0
l 385
l 361
 retb
l 358=        13
l 359=        16
l 386
 ent   1   l 387
 ent   2   l 388
 ldcb          0
 strb  0       0
 loda  0       5
 ldcn
 neqa
 fjp       l 389
i 2860
 loda  0       5
 indi          2
 ldci          4
 equi
 fjp       l 390
 mst           1
 loda  0       5
 inda          4
 ldoa         38
 cup   2   l 357
i 2870
 fjp       l 391
 ldcb          1
 strb  0       0
l 391
l 390
l 389
 retb
l 387=         6
l 388=         7
l 393
 ent   1   l 394
 ent   2   l 395
 loda  0       7
 ldci          1
 stoi
 ldoi          9
i 2880
 ordi
 ldos        191
 inn
 not
 fjp       l 396
 mst           3
 ldci          1
 cup   1   l  20
 mst           2
 lods  0       5
i 2890
 ldos        191
 uni
 cup   1   l 313
l 396
 ldoi          9
 ordi
 ldos        191
 inn
 fjp       l 397
 ldoi          9
 ldci          8
i 2900
 equi
 fjp       l 398
 ldoi         52
 stri  0      12
l 399
 lao          54
 ldoi         52
 ixa           5
 indi          2
 ldci          0
 neqi
i 2910
 fjp       l 400
 ldoi         52
 ldci          1
 sbi
 sroi         52
 ujp       l 399
l 400
 lda   0       9
 ldci          5
 csp         new
 loda  0       9
i 2920
 stra  0      16
 loda  0      16
 inca          1
 ldci          1
 stoi
 loda  0      16
 inca          2
 ldci          0
 stoi
 loda  0      16
i 2930
 inca          3
 ldci          1
 stoi
 ldcn
 stra  0      10
 ldci          0
 stri  0      13
l 401
 mst           3
 cup   0   l  25
 ldoi          9
i 2940
 ldci          0
 equi
 fjp       l 402
 lda   0      11
 ldci         15
 csp         new
 loda  0      11
 stra  0      16
 loda  0      16
 lao          14
i 2950
 mov           8
 loda  0      16
 inca         10
 loda  0       9
 stoa
 loda  0      16
 inca         11
 loda  0      10
 stoa
 loda  0      16
i 2960
 inca         14
 lodi  0      13
 stoi
 loda  0      16
 inca         12
 ldci          1
 stoi
 mst           3
 loda  0      11
 cup   1   l 136
i 2970
 lodi  0      13
 ldci          1
 adi
 stri  0      13
 loda  0      11
 stra  0      10
 mst           3
 cup   0   l  25
 ujp       l 403
l 402
 mst           3
i 2980
 ldci          2
 cup   1   l  20
l 403
 ldoi          9
 ordi
 lods  0       5
 ldc(  9 12)
 uni
 inn
 not
 fjp       l 404
i 2990
 mst           3
 ldci          6
 cup   1   l  20
 mst           2
 lods  0       5
 ldc(  9 12)
 uni
 cup   1   l 313
l 404
 ldoi          9
 ldci         12
i 3000
 neqi
 fjp       l 401
 loda  0       9
 inca          4
 loda  0      10
 stoa
 lodi  0      12
 sroi         52
 ldoi          9
 ldci          9
i 3010
 equi
 fjp       l 405
 mst           3
 cup   0   l  25
 ujp       l 406
l 405
 mst           3
 ldci          4
 cup   1   l  20
l 406
 ujp       l 407
l 398
 ldoi          9
i 3020
 ldci          0
 equi
 fjp       l 408
 mst           3
 ldc(  0  1)
 lda   0      11
 cup   2   l 158
 mst           3
 cup   0   l  25
 loda  0      11
i 3030
 indi         12
 ldci          1
 equi
 fjp       l 409
 lda   0       9
 ldci          8
 csp         new
 loda  0       9
 stra  0      16
 loda  0      11
i 3040
 stra  0      17
 loda  0      16
 inca          3
 loda  0      17
 inda         10
 stoa
 loda  0      16
 inca          2
 ldci          1
 stoi
i 3050
 mst           2
 loda  0      16
 inda          3
 cup   1   l 386
 fjp       l 410
 mst           3
 ldci        148
 cup   1   l  20
 loda  0      16
 inca          3
i 3060
 ldcn
 stoa
l 410
 loda  0      16
 inca          6
 loda  0      17
 inca         13
 mov           2
 loda  0      16
 inca          1
 ldci          1
i 3070
 stoi
 ldoi          9
 ldci         16
 equi
 fjp       l 411
 mst           3
 cup   0   l  25
 ujp       l 412
l 411
 mst           3
 ldci          5
i 3080
 cup   1   l  20
l 412
 mst           2
 lods  0       5
 lda   0       8
 lda   0      14
 cup   3   l 320
 loda  0       9
 inca          4
 lda   0      14
 mov           2
i 3090
 loda  0       9
 inda          3
 loda  0       8
 neqa
 fjp       l 413
 mst           3
 ldci        107
 cup   1   l  20
l 413
 ujp       l 414
l 409
 loda  0      11
i 3100
 inda         10
 stra  0       9
 loda  0       9
 ldcn
 neqa
 fjp       l 415
 loda  0       7
 loda  0       9
 indi          1
 stoi
l 415
l 414
i 3110
 ujp       l 416
l 408
 lda   0       9
 ldci          8
 csp         new
 loda  0       9
 inca          2
 ldci          1
 stoi
 mst           2
 lods  0       5
i 3120
 ldc( 16)
 uni
 lda   0       8
 lda   0      14
 cup   3   l 320
 mst           2
 loda  0       8
 cup   1   l 386
 fjp       l 417
 mst           3
i 3130
 ldci        148
 cup   1   l  20
 ldcn
 stra  0       8
l 417
 loda  0       9
 stra  0      16
 loda  0      16
 inca          3
 loda  0       8
 stoa
i 3140
 loda  0      16
 inca          6
 lda   0      14
 mov           2
 loda  0      16
 inca          1
 ldci          1
 stoi
 ldoi          9
 ldci         16
i 3150
 equi
 fjp       l 418
 mst           3
 cup   0   l  25
 ujp       l 419
l 418
 mst           3
 ldci          5
 cup   1   l  20
l 419
 mst           2
 lods  0       5
i 3160
 lda   0       8
 lda   0      14
 cup   3   l 320
 loda  0       9
 inca          4
 lda   0      14
 mov           2
 loda  0       9
 inda          3
 loda  0       8
i 3170
 neqa
 fjp       l 420
 mst           3
 ldci        107
 cup   1   l  20
l 420
l 416
 loda  0       9
 ldcn
 neqa
 fjp       l 421
 loda  0       9
i 3180
 stra  0      16
 loda  0      16
 indi          2
 ldci          1
 equi
 fjp       l 422
 loda  0      16
 inda          3
 ldcn
 neqa
i 3190
 fjp       l 423
 loda  0      16
 inda          3
 ldoa         39
 equa
 fjp       l 424
 mst           3
 ldci        399
 cup   1   l  20
 ujp       l 425
l 424
i 3200
 loda  0      16
 indi          7
 loda  0      16
 indi          5
 grti
 fjp       l 426
 mst           3
 ldci        102
 cup   1   l  20
l 426
l 425
l 423
l 422
l 421
l 407
 loda  0       6
i 3210
 loda  0       9
 stoa
 ldoi          9
 ordi
 lods  0       5
 inn
 not
 fjp       l 427
 mst           3
 ldci          6
i 3220
 cup   1   l  20
 mst           2
 lods  0       5
 cup   1   l 313
l 427
 ujp       l 428
l 397
 loda  0       6
 ldcn
 stoa
l 428
 retp
l 394=        18
l 395=        35
l 429
 ent   1   l 430
i 3230
 ent   2   l 431
 ldcn
 stra  0       7
 ldcn
 stra  0      15
 ldoi          9
 ordi
 lods  0       5
 ldc(  0 33)
 uni
i 3240
 inn
 not
 fjp       l 432
 mst           3
 ldci         19
 cup   1   l  20
 mst           2
 lods  0       5
 ldc(  0 33)
 uni
i 3250
 cup   1   l 313
l 432
l 433
 ldoi          9
 ldci          0
 equi
 fjp       l 434
 loda  0       7
 stra  0       8
l 435
 ldoi          9
 ldci          0
 equi
i 3260
 fjp       l 436
 lda   0      10
 ldci         14
 csp         new
 loda  0      10
 stra  0      21
 loda  0      21
 lao          14
 mov           8
 loda  0      21
i 3270
 inca         10
 ldcn
 stoa
 loda  0      21
 inca         11
 loda  0       8
 stoa
 loda  0      21
 inca         12
 ldci          3
i 3280
 stoi
 loda  0      10
 stra  0       8
 mst           3
 loda  0      10
 cup   1   l 136
 mst           3
 cup   0   l  25
 ujp       l 437
l 436
 mst           3
i 3290
 ldci          2
 cup   1   l  20
l 437
 ldoi          9
 ordi
 ldc( 12 16)
 inn
 not
 fjp       l 438
 mst           3
 ldci          6
i 3300
 cup   1   l  20
 mst           2
 lods  0       5
 ldc( 12 13 16 33)
 uni
 cup   1   l 313
l 438
 ldoi          9
 ldci         12
 neqi
 strb  2       9
i 3310
 lodb  2       9
 not
 fjp       l 439
 mst           3
 cup   0   l  25
l 439
 lodb  2       9
 fjp       l 435
 ldoi          9
 ldci         16
 equi
i 3320
 fjp       l 440
 mst           3
 cup   0   l  25
 ujp       l 441
l 440
 mst           3
 ldci          5
 cup   1   l  20
l 441
 mst           2
 lods  0       5
 ldc( 13 33)
i 3330
 uni
 lda   0      15
 lda   0      16
 cup   3   l 392
l 442
 loda  0       8
 loda  0       7
 neqa
 fjp       l 443
 loda  0       8
 stra  0      21
i 3340
 mst           3
 loda  0      15
 lda   1      13
 cup   2   l 218
 loda  0      21
 inca         10
 loda  0      15
 stoa
 loda  0      21
 inca         13
i 3350
 lodi  1      13
 stoi
 loda  0      21
 inda         11
 stra  0       8
 lodi  1      13
 lodi  0      16
 adi
 stri  1      13
 ujp       l 442
l 443
i 3360
 loda  0      10
 stra  0       7
l 444
 ldoi          9
 ldci         13
 equi
 fjp       l 445
 mst           3
 cup   0   l  25
 ldoi          9
 ordi
i 3370
 lods  0       5
 ldc(  0 13 33)
 uni
 inn
 not
 fjp       l 446
 mst           3
 ldci         19
 cup   1   l  20
 mst           2
i 3380
 lods  0       5
 ldc(  0 33)
 uni
 cup   1   l 313
l 446
 ujp       l 444
l 445
 ujp       l 433
l 434
 ldcn
 stra  0       8
l 447
 loda  0       7
 ldcn
i 3390
 neqa
 fjp       l 448
 loda  0       7
 stra  0      21
 loda  0      21
 inda         11
 stra  0      10
 loda  0      21
 inca         11
 loda  0       8
i 3400
 stoa
 loda  0       7
 stra  0       8
 loda  0      10
 stra  0       7
 ujp       l 447
l 448
 ldoi          9
 ldci         33
 equi
 fjp       l 449
i 3410
 lda   0      15
 ldci          5
 csp         new
 loda  0      15
 stra  0      21
 loda  0      21
 inca          3
 ldcn
 stoa
 loda  0      21
i 3420
 inca          4
 ldcn
 stoa
 loda  0      21
 inca          2
 ldci          7
 stoi
 loda  0       6
 loda  0      15
 stoa
i 3430
 mst           3
 cup   0   l  25
 ldoi          9
 ldci          0
 equi
 fjp       l 450
 lda   0      10
 ldci         14
 csp         new
 loda  0      10
i 3440
 stra  0      21
 loda  0      21
 lao          14
 mov           8
 loda  0      21
 inca         10
 ldcn
 stoa
 loda  0      21
 inca         12
i 3450
 ldci          3
 stoi
 loda  0      21
 inca         11
 ldcn
 stoa
 loda  0      21
 inca         13
 lodi  1      13
 stoi
i 3460
 mst           3
 loda  0      10
 cup   1   l 136
 mst           3
 cup   0   l  25
 ldoi          9
 ldci         16
 equi
 fjp       l 451
 mst           3
i 3470
 cup   0   l  25
 ujp       l 452
l 451
 mst           3
 ldci          5
 cup   1   l  20
l 452
 ldoi          9
 ldci          0
 equi
 fjp       l 453
 mst           3
i 3480
 ldc(  0)
 lda   0       9
 cup   2   l 158
 loda  0       9
 inda         10
 stra  0      14
 loda  0      14
 ldcn
 neqa
 fjp       l 454
i 3490
 mst           3
 loda  0      14
 lda   1      13
 cup   2   l 218
 loda  0      10
 inca         13
 lodi  1      13
 stoi
 lodi  1      13
 loda  0      14
i 3500
 indi          1
 adi
 stri  1      13
 loda  0      14
 indi          2
 ldci          1
 leqi
 mst           2
 loda  0      14
 cup   1   l 386
i 3510
 ior
 fjp       l 455
 mst           2
 ldoa         39
 loda  0      14
 cup   2   l 357
 fjp       l 456
 mst           3
 ldci        109
 cup   1   l  20
i 3520
 ujp       l 457
l 456
 mst           2
 loda  0      14
 cup   1   l 386
 fjp       l 458
 mst           3
 ldci        399
 cup   1   l  20
l 458
l 457
 loda  0      10
 inca         10
i 3530
 loda  0      14
 stoa
 loda  0      15
 inca          3
 loda  0      10
 stoa
 ujp       l 459
l 455
 mst           3
 ldci        110
 cup   1   l  20
l 459
l 454
i 3540
 mst           3
 cup   0   l  25
 ujp       l 460
l 453
 mst           3
 ldci          2
 cup   1   l  20
 mst           2
 lods  0       5
 ldc(  8 42)
 uni
i 3550
 cup   1   l 313
l 460
 ujp       l 461
l 450
 mst           3
 ldci          2
 cup   1   l  20
 mst           2
 lods  0       5
 ldc(  8 42)
 uni
 cup   1   l 313
l 461
i 3560
 loda  0      15
 inca          1
 lodi  1      13
 stoi
 ldoi          9
 ldci         42
 equi
 fjp       l 462
 mst           3
 cup   0   l  25
i 3570
 ujp       l 463
l 462
 mst           3
 ldci          8
 cup   1   l  20
l 463
 ldcn
 stra  0      14
 lodi  1      13
 stri  0      18
 lodi  1      13
 stri  0      17
l 464
i 3580
 ldcn
 stra  0      13
 ldoi          9
 ordi
 lods  0       5
 ldc( 13)
 uni
 inn
 not
 fjp       l 465
l 466
i 3590
 mst           2
 lods  0       5
 ldc(  8 12 16)
 uni
 lda   0      12
 lda   0      19
 cup   3   l 320
 loda  0      15
 inda          3
 ldcn
i 3600
 neqa
 fjp       l 467
 mst           2
 loda  0      15
 inda          3
 inda         10
 loda  0      12
 cup   2   l 357
 not
 fjp       l 468
i 3610
 mst           3
 ldci        111
 cup   1   l  20
l 468
l 467
 lda   0      12
 ldci          7
 csp         new
 loda  0      12
 stra  0      21
 loda  0      21
 inca          4
i 3620
 loda  0      14
 stoa
 loda  0      21
 inca          3
 loda  0      13
 stoa
 loda  0      21
 inca          5
 lda   0      19
 mov           2
i 3630
 loda  0      21
 inca          2
 ldci          8
 stoi
 loda  0      14
 stra  0      11
l 469
 loda  0      11
 ldcn
 neqa
 fjp       l 470
i 3640
 loda  0      11
 stra  0      21
 loda  0      21
 indi          6
 lodi  0      20
 equi
 fjp       l 471
 mst           3
 ldci        178
 cup   1   l  20
l 471
i 3650
 loda  0      21
 inda          4
 stra  0      11
 ujp       l 469
l 470
 loda  0      12
 stra  0      14
 loda  0      12
 stra  0      13
 ldoi          9
 ldci         12
i 3660
 neqi
 strb  2       9
 lodb  2       9
 not
 fjp       l 472
 mst           3
 cup   0   l  25
l 472
 lodb  2       9
 fjp       l 466
 ldoi          9
i 3670
 ldci         16
 equi
 fjp       l 473
 mst           3
 cup   0   l  25
 ujp       l 474
l 473
 mst           3
 ldci          5
 cup   1   l  20
l 474
 ldoi          9
i 3680
 ldci          8
 equi
 fjp       l 475
 mst           3
 cup   0   l  25
 ujp       l 476
l 475
 mst           3
 ldci          9
 cup   1   l  20
l 476
 mst           1
i 3690
 lods  0       5
 ldc(  9 13)
 uni
 lda   0      13
 cup   2   l 429
 lodi  1      13
 lodi  0      17
 grti
 fjp       l 477
 lodi  1      13
i 3700
 stri  0      17
l 477
l 478
 loda  0      12
 ldcn
 neqa
 fjp       l 479
 loda  0      12
 inda          3
 stra  0      11
 loda  0      12
 inca          3
i 3710
 loda  0      13
 stoa
 loda  0      12
 inca          1
 lodi  1      13
 stoi
 loda  0      11
 stra  0      12
 ujp       l 478
l 479
 ldoi          9
i 3720
 ldci          9
 equi
 fjp       l 480
 mst           3
 cup   0   l  25
 ldoi          9
 ordi
 lods  0       5
 ldc( 13)
 uni
i 3730
 inn
 not
 fjp       l 481
 mst           3
 ldci          6
 cup   1   l  20
 mst           2
 lods  0       5
 ldc( 13)
 uni
i 3740
 cup   1   l 313
l 481
 ujp       l 482
l 480
 mst           3
 ldci          4
 cup   1   l  20
l 482
l 465
 ldoi          9
 ldci         13
 neqi
 strb  2       9
 lodb  2       9
i 3750
 not
 fjp       l 483
 lodi  0      18
 stri  1      13
 mst           3
 cup   0   l  25
l 483
 lodb  2       9
 fjp       l 464
 lodi  0      17
 stri  1      13
i 3760
 loda  0      15
 inca          4
 loda  0      14
 stoa
 ujp       l 484
l 449
 loda  0       6
 ldcn
 stoa
l 484
 retp
l 430=        22
l 431=        49
l 392
 ent   1   l 485
i 3770
 ent   2   l 486
 ldoi          9
 ordi
 ldos        190
 inn
 not
 fjp       l 487
 mst           2
 ldci         10
 cup   1   l  20
i 3780
 mst           1
 lods  0       5
 ldos        190
 uni
 cup   1   l 313
l 487
 ldoi          9
 ordi
 ldos        190
 inn
 fjp       l 488
i 3790
 ldoi          9
 ordi
 ldos        191
 inn
 fjp       l 489
 mst           0
 lods  0       5
 loda  0       6
 loda  0       7
 cup   3   l 393
i 3800
 ujp       l 490
l 489
 ldoi          9
 ldci         15
 equi
 fjp       l 491
 lda   0      10
 ldci          4
 csp         new
 loda  0       6
 loda  0      10
i 3810
 stoa
 loda  0      10
 stra  0      17
 loda  0      17
 inca          3
 ldcn
 stoa
 loda  0      17
 inca          1
 ldci          1
i 3820
 stoi
 loda  0      17
 inca          2
 ldci          2
 stoi
 mst           2
 cup   0   l  25
 ldoi          9
 ldci          0
 equi
i 3830
 fjp       l 492
 ldcb          0
 srob         32
 mst           2
 ldc(  0)
 lda   0      12
 cup   2   l 158
 ldcb          1
 srob         32
 loda  0      12
i 3840
 ldcn
 equa
 fjp       l 493
 lda   0      12
 ldci         13
 csp         new
 loda  0      12
 stra  0      17
 loda  0      17
 lao          14
i 3850
 mov           8
 loda  0      17
 inca         10
 loda  0      10
 stoa
 loda  0      17
 inca         11
 ldoa         42
 stoa
 loda  0      17
i 3860
 inca         12
 ldci          0
 stoi
 loda  0      12
 sroa         42
 ujp       l 494
l 493
 loda  0      12
 inda         10
 ldcn
 neqa
i 3870
 fjp       l 495
 loda  0      12
 inda         10
 indi          2
 ldci          6
 equi
 fjp       l 496
 mst           2
 ldci        108
 cup   1   l  20
i 3880
 ujp       l 497
l 496
 loda  0      10
 inca          3
 loda  0      12
 inda         10
 stoa
l 497
l 495
l 494
 mst           2
 cup   0   l  25
 ujp       l 498
l 492
 mst           2
i 3890
 ldci          2
 cup   1   l  20
l 498
 ujp       l 499
l 491
 ldoi          9
 ldci         26
 equi
 fjp       l 500
 mst           2
 cup   0   l  25
 ldoi          9
i 3900
 ordi
 ldos        185
 inn
 not
 fjp       l 501
 mst           2
 ldci         10
 cup   1   l  20
 mst           1
 lods  0       5
i 3910
 ldos        185
 uni
 cup   1   l 313
l 501
l 500
 ldoi          9
 ldci         27
 equi
 fjp       l 502
 mst           2
 cup   0   l  25
 ldoi          9
i 3920
 ldci         10
 equi
 fjp       l 503
 mst           2
 cup   0   l  25
 ujp       l 504
l 503
 mst           2
 ldci         11
 cup   1   l  20
l 504
 ldcn
i 3930
 stra  0       9
l 505
 lda   0      10
 ldci          5
 csp         new
 loda  0      10
 stra  0      17
 loda  0      17
 inca          4
 loda  0       9
 stoa
i 3940
 loda  0      17
 inca          3
 ldcn
 stoa
 loda  0      17
 inca          2
 ldci          4
 stoi
 loda  0      10
 stra  0       9
i 3950
 mst           0
 lods  0       5
 ldc( 11 12 42)
 uni
 lda   0       8
 lda   0      14
 cup   3   l 393
 loda  0       9
 inca          1
 lodi  0      14
i 3960
 stoi
 loda  0       8
 ldcn
 neqa
 fjp       l 506
 loda  0       8
 indi          2
 ldci          1
 leqi
 fjp       l 507
i 3970
 loda  0       8
 ldoa         39
 equa
 fjp       l 508
 mst           2
 ldci        109
 cup   1   l  20
 ldcn
 stra  0       8
 ujp       l 509
l 508
i 3980
 loda  0       8
 ldoa         40
 equa
 fjp       l 510
 mst           2
 ldci        149
 cup   1   l  20
 ldcn
 stra  0       8
l 510
l 509
 loda  0      10
i 3990
 inca          3
 loda  0       8
 stoa
 ujp       l 511
l 507
 mst           2
 ldci        113
 cup   1   l  20
 ldcn
 stra  0       8
l 511
l 506
 ldoi          9
i 4000
 ldci         12
 neqi
 strb  1       9
 lodb  1       9
 not
 fjp       l 512
 mst           2
 cup   0   l  25
l 512
 lodb  1       9
 fjp       l 505
i 4010
 ldoi          9
 ldci         11
 equi
 fjp       l 513
 mst           2
 cup   0   l  25
 ujp       l 514
l 513
 mst           2
 ldci         12
 cup   1   l  20
l 514
i 4020
 ldoi          9
 ldci         42
 equi
 fjp       l 515
 mst           2
 cup   0   l  25
 ujp       l 516
l 515
 mst           2
 ldci          8
 cup   1   l  20
l 516
i 4030
 mst           1
 lods  0       5
 lda   0      10
 lda   0      14
 cup   3   l 392
l 517
 loda  0       9
 stra  0      17
 loda  0      17
 inda          4
 stra  0       8
i 4040
 loda  0      17
 inca          4
 loda  0      10
 stoa
 loda  0      17
 inda          3
 ldcn
 neqa
 fjp       l 518
 mst           2
i 4050
 loda  0      17
 inda          3
 lda   0      16
 lda   0      15
 cup   3   l 184
 mst           2
 loda  0      10
 lda   0      14
 cup   2   l 218
 lodi  0      14
i 4060
 lodi  0      15
 lodi  0      16
 sbi
 ldci          1
 adi
 mpi
 stri  0      14
 loda  0      17
 inca          1
 lodi  0      14
i 4070
 stoi
l 518
 loda  0       9
 stra  0      10
 loda  0       8
 stra  0       9
 loda  0       9
 ldcn
 equa
 fjp       l 517
 ujp       l 519
l 502
i 4080
 ldoi          9
 ldci         28
 equi
 fjp       l 520
 mst           2
 cup   0   l  25
 ldoi         52
 stri  0      11
 ldoi         52
 ldci         20
i 4090
 lesi
 fjp       l 521
 ldoi         52
 ldci          1
 adi
 sroi         52
 lao          54
 ldoi         52
 ixa           5
 stra  0      17
i 4100
 loda  0      17
 ldcn
 stoa
 loda  0      17
 inca          1
 ldcn
 stoa
 loda  0      17
 inca          2
 ldci          3
i 4110
 stoi
 ujp       l 522
l 521
 mst           2
 ldci        250
 cup   1   l  20
l 522
 ldci          0
 stri  0      13
 mst           0
 lods  0       5
 ldc( 13)
i 4120
 dif
 ldc( 39)
 uni
 lda   0       9
 cup   2   l 429
 lda   0      10
 ldci          5
 csp         new
 loda  0      10
 stra  0      17
i 4130
 loda  0      17
 inca          3
 lao          54
 ldoi         52
 ixa           5
 inda          0
 stoa
 loda  0      17
 inca          4
 loda  0       9
i 4140
 stoa
 loda  0      17
 inca          1
 lodi  0      13
 stoi
 loda  0      17
 inca          2
 ldci          5
 stoi
 lodi  0      11
i 4150
 sroi         52
 ldoi          9
 ldci         39
 equi
 fjp       l 523
 mst           2
 cup   0   l  25
 ujp       l 524
l 523
 mst           2
 ldci         13
i 4160
 cup   1   l  20
l 524
 ujp       l 525
l 520
 ldoi          9
 ldci         25
 equi
 fjp       l 526
 mst           2
 cup   0   l  25
 ldoi          9
 ldci         42
i 4170
 equi
 fjp       l 527
 mst           2
 cup   0   l  25
 ujp       l 528
l 527
 mst           2
 ldci          8
 cup   1   l  20
l 528
 mst           0
 lods  0       5
i 4180
 lda   0       9
 lda   0      14
 cup   3   l 393
 loda  0       9
 ldcn
 neqa
 fjp       l 529
 loda  0       9
 indi          2
 ldci          1
i 4190
 grti
 fjp       l 530
 mst           2
 ldci        115
 cup   1   l  20
 ldcn
 stra  0       9
 ujp       l 531
l 530
 loda  0       9
 ldoa         39
i 4200
 equa
 fjp       l 532
 mst           2
 ldci        114
 cup   1   l  20
 ldcn
 stra  0       9
 ujp       l 533
l 532
 loda  0       9
 ldoa         40
i 4210
 equa
 fjp       l 534
 mst           2
 ldci        169
 cup   1   l  20
 ldcn
 stra  0       9
 ujp       l 535
l 534
 mst           2
 loda  0       9
i 4220
 lda   0      16
 lda   0      15
 cup   3   l 184
 lodi  0      16
 ldci          0
 lesi
 lodi  0      15
 ldci         47
 grti
 ior
i 4230
 fjp       l 536
 mst           2
 ldci        169
 cup   1   l  20
l 536
l 535
l 533
l 531
l 529
 lda   0      10
 ldci          4
 csp         new
 loda  0      10
 stra  0      17
 loda  0      17
i 4240
 inca          3
 loda  0       9
 stoa
 loda  0      17
 inca          1
 ldci          1
 stoi
 loda  0      17
 inca          2
 ldci          3
i 4250
 stoi
 ujp       l 537
l 526
 ldoi          9
 ldci         29
 equi
 fjp       l 538
 mst           2
 cup   0   l  25
 mst           2
 ldci        399
i 4260
 cup   1   l  20
 mst           1
 lods  0       5
 cup   1   l 313
 ldcn
 stra  0      10
l 538
l 537
l 525
l 519
 loda  0       6
 loda  0      10
 stoa
l 499
l 490
 ldoi          9
i 4270
 ordi
 lods  0       5
 inn
 not
 fjp       l 539
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
 lods  0       5
i 4280
 cup   1   l 313
l 539
 ujp       l 540
l 488
 loda  0       6
 ldcn
 stoa
l 540
 loda  0       6
 inda          0
 ldcn
 equa
 fjp       l 541
i 4290
 loda  0       7
 ldci          1
 stoi
 ujp       l 542
l 541
 loda  0       7
 loda  0       6
 inda          0
 indi          1
 stoi
l 542
 retp
l 485=        18
l 486=        54
l 543
i 4300
 ent   1   l 544
 ent   2   l 545
l 546
 ldoi          9
 ldci          1
 equi
 fjp       l 547
 lao          54
 ldoi         52
 ixa           5
 stra  0       8
i 4310
 loda  0       8
 inda          1
 stra  0       5
 ldcb          0
 strb  0       6
l 548
 loda  0       5
 ldcn
 neqa
 lodb  0       6
 not
i 4320
 and
 fjp       l 549
 loda  0       5
 indi          3
 ldoi         12
 neqi
 fjp       l 550
 loda  0       5
 inda          0
 stra  0       5
i 4330
 ujp       l 551
l 550
 ldcb          1
 strb  0       6
 mst           2
 ldci        166
 cup   1   l  20
l 551
 ujp       l 548
l 549
 lodb  0       6
 not
 fjp       l 552
i 4340
 lda   0       5
 ldci          4
 csp         new
 loda  0       5
 stra  0       9
 loda  0       9
 inca          3
 ldoi         12
 stoi
 mst           2
i 4350
 lda   0       7
 cup   1   l 309
 loda  0       9
 inca          1
 ldcb          0
 stob
 loda  0       9
 loda  0       8
 inda          1
 stoa
i 4360
 loda  0       9
 inca          2
 lodi  0       7
 stoi
 loda  0       8
 inca          1
 loda  0       5
 stoa
l 552
 mst           2
 cup   0   l  25
i 4370
 ujp       l 553
l 547
 mst           2
 ldci         15
 cup   1   l  20
l 553
 ldoi          9
 ordi
 lods  1       5
 ldc( 12 13)
 uni
 inn
i 4380
 not
 fjp       l 554
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
 lods  1       5
 ldc( 12 13)
 uni
 cup   1   l 313
l 554
i 4390
 ldoi          9
 ldci         12
 neqi
 strb  1       9
 lodb  1       9
 not
 fjp       l 555
 mst           2
 cup   0   l  25
l 555
 lodb  1       9
i 4400
 fjp       l 546
 ldoi          9
 ldci         13
 equi
 fjp       l 556
 mst           2
 cup   0   l  25
 ujp       l 557
l 556
 mst           2
 ldci         14
i 4410
 cup   1   l  20
l 557
 retp
l 544=        10
l 545=        12
l 558
 ent   1   l 559
 ent   2   l 560
 ldoi          9
 ldci          0
 neqi
 fjp       l 561
 mst           2
 ldci          2
i 4420
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  0)
 uni
 cup   1   l 313
l 561
l 562
 ldoi          9
 ldci          0
 equi
 fjp       l 563
i 4430
 lda   0       5
 ldci         15
 csp         new
 loda  0       5
 stra  0       9
 loda  0       9
 lao          14
 mov           8
 loda  0       9
 inca         10
i 4440
 ldcn
 stoa
 loda  0       9
 inca         11
 ldcn
 stoa
 loda  0       9
 inca         12
 ldci          1
 stoi
i 4450
 mst           2
 cup   0   l  25
 ldoi          9
 ldci          7
 equi
 ldoi         10
 ldci         13
 equi
 and
 fjp       l 564
i 4460
 mst           2
 cup   0   l  25
 ujp       l 565
l 564
 mst           2
 ldci         16
 cup   1   l  20
l 565
 mst           1
 lods  1       5
 ldc( 13)
 uni
i 4470
 lda   0       6
 lda   0       7
 cup   3   l 320
 mst           2
 loda  0       5
 cup   1   l 136
 loda  0       5
 inca         10
 loda  0       6
 stoa
i 4480
 loda  0       5
 inca         13
 lda   0       7
 mov           2
 ldoi          9
 ldci         13
 equi
 fjp       l 566
 mst           2
 cup   0   l  25
i 4490
 ldoi          9
 ordi
 lods  1       5
 ldc(  0)
 uni
 inn
 not
 fjp       l 567
 mst           2
 ldci          6
i 4500
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  0)
 uni
 cup   1   l 313
l 567
 ujp       l 568
l 566
 mst           2
 ldci         14
 cup   1   l  20
l 568
i 4510
 ujp       l 562
l 563
 retp
l 559=        10
l 560=        15
l 569
 ent   1   l 570
 ent   2   l 571
 ldoi          9
 ldci          0
 neqi
 fjp       l 572
 mst           2
 ldci          2
i 4520
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  0)
 uni
 cup   1   l 313
l 572
l 573
 ldoi          9
 ldci          0
 equi
 fjp       l 574
i 4530
 lda   0       7
 ldci         13
 csp         new
 loda  0       7
 stra  0      10
 loda  0      10
 lao          14
 mov           8
 loda  0      10
 inca         10
i 4540
 ldcn
 stoa
 loda  0      10
 inca         12
 ldci          0
 stoi
 mst           2
 cup   0   l  25
 ldoi          9
 ldci          7
i 4550
 equi
 ldoi         10
 ldci         13
 equi
 and
 fjp       l 575
 mst           2
 cup   0   l  25
 ujp       l 576
l 575
 mst           2
i 4560
 ldci         16
 cup   1   l  20
l 576
 mst           1
 lods  1       5
 ldc( 13)
 uni
 lda   0       8
 lda   0       9
 cup   3   l 392
 mst           2
i 4570
 loda  0       7
 cup   1   l 136
 loda  0       7
 inca         10
 loda  0       8
 stoa
 ldoa         42
 stra  0       6
l 577
 loda  0       6
 ldcn
i 4580
 neqa
 fjp       l 578
 loda  0       6
 loda  0       7
 equm          8
 fjp       l 579
 loda  0       6
 inda         10
 inca          3
 loda  0       7
i 4590
 inda         10
 stoa
 loda  0       6
 ldoa         42
 neqa
 fjp       l 580
 loda  0       5
 inca         11
 loda  0       6
 inda         11
i 4600
 stoa
 ujp       l 581
l 580
 loda  0       6
 inda         11
 sroa         42
l 581
 ujp       l 582
l 579
 loda  0       6
 stra  0       5
l 582
 loda  0       6
 inda         11
i 4610
 stra  0       6
 ujp       l 577
l 578
 ldoi          9
 ldci         13
 equi
 fjp       l 583
 mst           2
 cup   0   l  25
 ldoi          9
 ordi
i 4620
 lods  1       5
 ldc(  0)
 uni
 inn
 not
 fjp       l 584
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
i 4630
 lods  1       5
 ldc(  0)
 uni
 cup   1   l 313
l 584
 ujp       l 585
l 583
 mst           2
 ldci         14
 cup   1   l  20
l 585
 ujp       l 573
l 574
 ldoa         42
i 4640
 ldcn
 neqa
 fjp       l 586
 mst           2
 ldci        117
 cup   1   l  20
 lda   2       6
 csp         wln
l 587
 lca' type-id        '
 ldci          9
i 4650
 ldci          9
 lda   2       6
 csp         wrs
 ldoa         42
 ldci          8
 ldci          8
 lda   2       6
 csp         wrs
 lda   2       6
 csp         wln
i 4660
 ldoa         42
 inda         11
 sroa         42
 ldoa         42
 ldcn
 equa
 fjp       l 587
 ldob         24
 not
 fjp       l 588
i 4670
 ldcc ' '
 ldoi         25
 ldci         16
 adi
 lda   2       6
 csp         wrc
l 588
l 586
 retp
l 570=        11
l 571=        20
l 589
 ent   1   l 590
 ent   2   l 591
 ldcn
i 4680
 stra  0       5
l 592
l 593
 ldoi          9
 ldci          0
 equi
 fjp       l 594
 lda   0       6
 ldci         16
 csp         new
 loda  0       6
 stra  0       9
i 4690
 loda  0       9
 lao          14
 mov           8
 loda  0       9
 inca         11
 loda  0       5
 stoa
 loda  0       9
 inca         12
 ldci          2
i 4700
 stoi
 loda  0       9
 inca         10
 ldcn
 stoa
 loda  0       9
 inca         13
 ldci          0
 stoi
 loda  0       9
i 4710
 inca         14
 ldoi         51
 stoi
 mst           2
 loda  0       6
 cup   1   l 136
 loda  0       6
 stra  0       5
 mst           2
 cup   0   l  25
i 4720
 ujp       l 595
l 594
 mst           2
 ldci          2
 cup   1   l  20
l 595
 ldoi          9
 ordi
 lods  1       5
 ldc( 12 16)
 uni
 ldos        185
i 4730
 uni
 inn
 not
 fjp       l 596
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
 lods  1       5
 ldc( 12 13 16)
i 4740
 uni
 ldos        185
 uni
 cup   1   l 313
l 596
 ldoi          9
 ldci         12
 neqi
 strb  1       9
 lodb  1       9
 not
i 4750
 fjp       l 597
 mst           2
 cup   0   l  25
l 597
 lodb  1       9
 fjp       l 593
 ldoi          9
 ldci         16
 equi
 fjp       l 598
 mst           2
i 4760
 cup   0   l  25
 ujp       l 599
l 598
 mst           2
 ldci          5
 cup   1   l  20
l 599
 mst           1
 lods  1       5
 ldc( 13)
 uni
 ldos        185
i 4770
 uni
 lda   0       7
 lda   0       8
 cup   3   l 392
l 600
 loda  0       5
 ldcn
 neqa
 fjp       l 601
 loda  0       5
 stra  0       9
i 4780
 mst           2
 loda  0       7
 lao          27
 cup   2   l 218
 loda  0       9
 inca         10
 loda  0       7
 stoa
 loda  0       9
 inca         15
i 4790
 ldoi         27
 stoi
 ldoi         27
 lodi  0       8
 adi
 sroi         27
 loda  0       9
 inda         11
 stra  0       5
 ujp       l 600
l 601
i 4800
 ldoi          9
 ldci         13
 equi
 fjp       l 602
 mst           2
 cup   0   l  25
 ldoi          9
 ordi
 lods  1       5
 ldc(  0)
i 4810
 uni
 inn
 not
 fjp       l 603
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  0)
i 4820
 uni
 cup   1   l 313
l 603
 ujp       l 604
l 602
 mst           2
 ldci         14
 cup   1   l  20
l 604
 ldoi          9
 ldci          0
 neqi
 ldoi          9
i 4830
 ordi
 ldos        185
 inn
 not
 and
 fjp       l 592
 ldoa         42
 ldcn
 neqa
 fjp       l 605
i 4840
 mst           2
 ldci        117
 cup   1   l  20
 lda   2       6
 csp         wln
l 606
 lca' type-id        '
 ldci          9
 ldci          9
 lda   2       6
 csp         wrs
i 4850
 ldoa         42
 ldci          8
 ldci          8
 lda   2       6
 csp         wrs
 lda   2       6
 csp         wln
 ldoa         42
 inda         11
 sroa         42
i 4860
 ldoa         42
 ldcn
 equa
 fjp       l 606
 ldob         24
 not
 fjp       l 607
 ldcc ' '
 ldoi         25
 ldci         16
i 4870
 adi
 lda   2       6
 csp         wrc
l 607
l 605
 retp
l 590=        10
l 591=        23
l 609
 ent   1   l 610
 ent   2   l 611
 ldcn
 stra  0       9
 ldoi          9
 ordi
i 4880
 lods  0       5
 ldc(  8)
 uni
 inn
 not
 fjp       l 612
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
i 4890
 lods  2       5
 lods  0       5
 uni
 ldc(  8)
 uni
 cup   1   l 313
l 612
 ldoi          9
 ldci          8
 equi
 fjp       l 613
i 4900
 lodb  1      10
 fjp       l 614
 mst           3
 ldci        119
 cup   1   l  20
l 614
 mst           3
 cup   0   l  25
 ldoi          9
 ordi
 ldc(  0 21 22 24)
i 4910
 inn
 not
 fjp       l 615
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  0  9)
 uni
i 4920
 cup   1   l 313
l 615
l 616
 ldoi          9
 ordi
 ldc(  0 21 22 24)
 inn
 fjp       l 617
 ldoi          9
 ldci         24
 equi
 fjp       l 618
i 4930
 mst           3
 ldci        399
 cup   1   l  20
l 619
 mst           3
 cup   0   l  25
 ldoi          9
 ldci          0
 equi
 fjp       l 620
 lda   0      10
i 4940
 ldci         17
 csp         new
 loda  0      10
 stra  0      16
 loda  0      16
 lao          14
 mov           8
 loda  0      16
 inca         10
 ldcn
i 4950
 stoa
 loda  0      16
 inca         11
 loda  0       9
 stoa
 loda  0      16
 inca         14
 ldoi         51
 stoi
 loda  0      16
i 4960
 inca         12
 ldci          4
 stoi
 loda  0      16
 inca         13
 ldci          1
 stoi
 loda  0      16
 inca         16
 ldci          1
i 4970
 stoi
 mst           3
 loda  0      10
 cup   1   l 136
 loda  0      10
 stra  0       9
 mst           3
 ldoa         41
 lao          27
 cup   2   l 218
i 4980
 mst           3
 cup   0   l  25
 ujp       l 621
l 620
 mst           3
 ldci          2
 cup   1   l  20
l 621
 ldoi          9
 ordi
 lods  2       5
 ldc(  9 12 13)
i 4990
 uni
 inn
 not
 fjp       l 622
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  9 12 13)
i 5000
 uni
 cup   1   l 313
l 622
 ldoi          9
 ldci         12
 neqi
 fjp       l 619
 ujp       l 623
l 618
 ldoi          9
 ldci         22
 equi
i 5010
 fjp       l 624
 mst           3
 ldci        399
 cup   1   l  20
 ldcn
 stra  0       8
l 625
 mst           3
 cup   0   l  25
 ldoi          9
 ldci          0
i 5020
 equi
 fjp       l 626
 lda   0      10
 ldci         17
 csp         new
 loda  0      10
 stra  0      16
 loda  0      16
 lao          14
 mov           8
i 5030
 loda  0      16
 inca         10
 ldcn
 stoa
 loda  0      16
 inca         11
 loda  0       8
 stoa
 loda  0      16
 inca         14
i 5040
 ldoi         51
 stoi
 loda  0      16
 inca         12
 ldci          5
 stoi
 loda  0      16
 inca         13
 ldci          1
 stoi
i 5050
 loda  0      16
 inca         16
 ldci          1
 stoi
 mst           3
 loda  0      10
 cup   1   l 136
 loda  0      10
 stra  0       8
 mst           3
i 5060
 ldoa         41
 lao          27
 cup   2   l 218
 mst           3
 cup   0   l  25
l 626
 ldoi          9
 ordi
 ldc( 12 16)
 lods  2       5
 uni
i 5070
 inn
 not
 fjp       l 627
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  9 12 13)
 uni
i 5080
 cup   1   l 313
l 627
 ldoi          9
 ldci         12
 neqi
 fjp       l 625
 ldoi          9
 ldci         16
 equi
 fjp       l 628
 mst           3
i 5090
 cup   0   l  25
 ldoi          9
 ldci          0
 equi
 fjp       l 629
 mst           3
 ldc(  0)
 lda   0      10
 cup   2   l 158
 loda  0      10
i 5100
 inda         10
 stra  0      11
 loda  0      11
 ldcn
 neqa
 fjp       l 630
 loda  0      11
 indi          2
 ordi
 ldc(  0  1  2)
i 5110
 inn
 not
 fjp       l 631
 mst           3
 ldci        120
 cup   1   l  20
 ldcn
 stra  0      11
l 631
l 630
 loda  0       8
 stra  0       7
l 632
i 5120
 loda  0       8
 ldcn
 neqa
 fjp       l 633
 loda  0       8
 inca         10
 loda  0      11
 stoa
 loda  0       8
 stra  0      10
i 5130
 loda  0       8
 inda         11
 stra  0       8
 ujp       l 632
l 633
 loda  0      10
 inca         11
 loda  0       9
 stoa
 loda  0       7
 stra  0       9
i 5140
 mst           3
 cup   0   l  25
 ujp       l 634
l 629
 mst           3
 ldci          2
 cup   1   l  20
l 634
 ldoi          9
 ordi
 lods  2       5
 ldc(  9 13)
i 5150
 uni
 inn
 not
 fjp       l 635
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  9 13)
i 5160
 uni
 cup   1   l 313
l 635
 ujp       l 636
l 628
 mst           3
 ldci          5
 cup   1   l  20
l 636
 ujp       l 637
l 624
 ldoi          9
 ldci         21
 equi
i 5170
 fjp       l 638
 ldci          1
 stri  0      12
 mst           3
 cup   0   l  25
 ujp       l 639
l 638
 ldci          0
 stri  0      12
l 639
 ldcn
 stra  0       8
i 5180
 ldci          0
 stri  0      15
l 640
 ldoi          9
 ldci          0
 equi
 fjp       l 641
 lda   0      10
 ldci         16
 csp         new
 loda  0      10
i 5190
 stra  0      16
 loda  0      16
 lao          14
 mov           8
 loda  0      16
 inca         10
 ldcn
 stoa
 loda  0      16
 inca         12
i 5200
 ldci          2
 stoi
 loda  0      16
 inca         13
 lodi  0      12
 stoi
 loda  0      16
 inca         11
 loda  0       8
 stoa
i 5210
 loda  0      16
 inca         14
 ldoi         51
 stoi
 mst           3
 loda  0      10
 cup   1   l 136
 loda  0      10
 stra  0       8
 lodi  0      15
i 5220
 ldci          1
 adi
 stri  0      15
 mst           3
 cup   0   l  25
l 641
 ldoi          9
 ordi
 ldc( 12 16)
 lods  2       5
 uni
i 5230
 inn
 not
 fjp       l 642
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  9 12 13)
 uni
i 5240
 cup   1   l 313
l 642
 ldoi          9
 ldci         12
 neqi
 strb  2       9
 lodb  2       9
 not
 fjp       l 643
 mst           3
 cup   0   l  25
l 643
i 5250
 lodb  2       9
 fjp       l 640
 ldoi          9
 ldci         16
 equi
 fjp       l 644
 mst           3
 cup   0   l  25
 ldoi          9
 ldci          0
i 5260
 equi
 fjp       l 645
 mst           3
 ldc(  0)
 lda   0      10
 cup   2   l 158
 loda  0      10
 inda         10
 stra  0      11
 ldci          1
i 5270
 stri  0      13
 loda  0      11
 ldcn
 neqa
 fjp       l 646
 lodi  0      12
 ldci          0
 equi
 fjp       l 647
 loda  0      11
i 5280
 indi          2
 ldci          3
 leqi
 fjp       l 648
 loda  0      11
 indi          1
 stri  0      13
 ujp       l 649
l 648
 loda  0      11
 indi          2
i 5290
 ldci          6
 equi
 fjp       l 650
 mst           3
 ldci        121
 cup   1   l  20
l 650
l 649
l 647
l 646
 mst           3
 ldoa         41
 lda   0      13
 cup   2   l 218
i 5300
 loda  0       8
 stra  0       7
 mst           3
 ldoa         41
 lao          27
 cup   2   l 218
 ldoi         27
 lodi  0      15
 lodi  0      13
 mpi
i 5310
 adi
 sroi         27
 ldoi         27
 stri  0      14
l 651
 loda  0       8
 ldcn
 neqa
 fjp       l 652
 loda  0       8
 stra  0      10
i 5320
 loda  0       8
 stra  0      16
 loda  0      16
 inca         10
 loda  0      11
 stoa
 lodi  0      14
 lodi  0      13
 sbi
 stri  0      14
i 5330
 loda  0      16
 inca         15
 lodi  0      14
 stoi
 loda  0       8
 inda         11
 stra  0       8
 ujp       l 651
l 652
 loda  0      10
 inca         11
i 5340
 loda  0       9
 stoa
 loda  0       7
 stra  0       9
 mst           3
 cup   0   l  25
 ujp       l 653
l 645
 mst           3
 ldci          2
 cup   1   l  20
l 653
i 5350
 ldoi          9
 ordi
 lods  2       5
 ldc(  9 13)
 uni
 inn
 not
 fjp       l 654
 mst           3
 ldci          7
i 5360
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  9 13)
 uni
 cup   1   l 313
l 654
 ujp       l 655
l 644
 mst           3
 ldci          5
 cup   1   l  20
l 655
l 637
l 623
i 5370
 ldoi          9
 ldci         13
 equi
 fjp       l 656
 mst           3
 cup   0   l  25
 ldoi          9
 ordi
 lods  2       5
 ldc(  0 21 22 24)
i 5380
 uni
 inn
 not
 fjp       l 657
 mst           3
 ldci          7
 cup   1   l  20
 mst           2
 lods  2       5
 ldc(  0  9)
i 5390
 uni
 cup   1   l 313
l 657
l 656
 ujp       l 616
l 617
 ldoi          9
 ldci          9
 equi
 fjp       l 658
 mst           3
 cup   0   l  25
 ldoi          9
i 5400
 ordi
 lods  0       5
 lods  2       5
 uni
 inn
 not
 fjp       l 659
 mst           3
 ldci          6
 cup   1   l  20
i 5410
 mst           2
 lods  0       5
 lods  2       5
 uni
 cup   1   l 313
l 659
 ujp       l 660
l 658
 mst           3
 ldci          4
 cup   1   l  20
l 660
 ldcn
i 5420
 stra  0       7
l 661
 loda  0       9
 ldcn
 neqa
 fjp       l 662
 loda  0       9
 stra  0      16
 loda  0      16
 inda         11
 stra  0       8
i 5430
 loda  0      16
 inca         11
 loda  0       7
 stoa
 loda  0      16
 indi         12
 ldci          2
 equi
 fjp       l 663
 loda  0      16
i 5440
 inda         10
 ldcn
 neqa
 fjp       l 664
 loda  0      16
 indi         13
 ldci          0
 equi
 loda  0      16
 inda         10
i 5450
 indi          2
 ldci          3
 grti
 and
 fjp       l 665
 mst           3
 loda  0      16
 inda         10
 lao          27
 cup   2   l 218
i 5460
 loda  0      16
 inca         15
 ldoi         27
 stoi
 ldoi         27
 loda  0      16
 inda         10
 indi          1
 adi
 sroi         27
l 665
l 664
l 663
i 5470
 loda  0       9
 stra  0       7
 loda  0       8
 stra  0       9
 ujp       l 661
l 662
 loda  0       6
 loda  0       7
 stoa
 ujp       l 666
l 613
 loda  0       6
i 5480
 ldcn
 stoa
l 666
 retp
l 610=        17
l 611=        53
l 608
 ent   1   l 667
 ent   2   l 668
 ldoi         27
 stri  0      13
 ldci          5
 sroi         27
 ldcb          0
i 5490
 strb  0      10
 ldoi          9
 ldci          0
 equi
 fjp       l 669
 mst           2
 lao          54
 ldoi         52
 ixa           5
 inda          0
i 5500
 lda   0       8
 cup   2   l 148
 loda  0       8
 ldcn
 neqa
 fjp       l 670
 loda  0       8
 indi         12
 ldci          4
 equi
i 5510
 fjp       l 671
 loda  0       8
 indb         18
 lodi  0       5
 ldci         24
 equi
 and
 loda  0       8
 indi         16
 ldci          0
i 5520
 equi
 and
 strb  0      10
 ujp       l 672
l 671
 loda  0       8
 indi         12
 ldci          5
 equi
 fjp       l 673
 loda  0       8
i 5530
 indb         18
 lodi  0       5
 ldci         22
 equi
 and
 loda  0       8
 indi         16
 ldci          0
 equi
 and
i 5540
 strb  0      10
 ujp       l 674
l 673
 ldcb          0
 strb  0      10
l 674
l 672
 lodb  0      10
 not
 fjp       l 675
 mst           2
 ldci        160
 cup   1   l  20
l 675
l 670
i 5550
 lodb  0      10
 not
 fjp       l 676
 lodi  0       5
 ldci         24
 equi
 fjp       l 677
 lda   0       8
 ldci         19
 csp         new
i 5560
 ujp       l 678
l 677
 lda   0       8
 ldci         19
 csp         new
l 678
 loda  0       8
 stra  0      16
 loda  0      16
 lao          14
 mov           8
 loda  0      16
i 5570
 inca         10
 ldcn
 stoa
 loda  0      16
 inca         17
 ldcb          0
 stob
 loda  0      16
 inca         14
 ldoi         51
i 5580
 stoi
 mst           2
 lda   0      14
 cup   1   l 309
 loda  0      16
 inca         13
 ldci          1
 stoi
 loda  0      16
 inca         16
i 5590
 ldci          0
 stoi
 loda  0      16
 inca         15
 lodi  0      14
 stoi
 lodi  0       5
 ldci         24
 equi
 fjp       l 679
i 5600
 loda  0      16
 inca         12
 ldci          4
 stoi
 ujp       l 680
l 679
 loda  0      16
 inca         12
 ldci          5
 stoi
l 680
 mst           2
i 5610
 loda  0       8
 cup   1   l 136
 ujp       l 681
l 676
 loda  0       8
 inda         11
 stra  0       7
l 682
 loda  0       7
 ldcn
 neqa
 fjp       l 683
i 5620
 loda  0       7
 stra  0      16
 loda  0      16
 indi         12
 ldci          2
 equi
 fjp       l 684
 loda  0      16
 inda         10
 ldcn
i 5630
 neqa
 fjp       l 685
 loda  0      16
 indi         15
 loda  0      16
 inda         10
 indi          1
 adi
 stri  0      12
 lodi  0      12
i 5640
 ldoi         27
 grti
 fjp       l 686
 lodi  0      12
 sroi         27
l 686
l 685
l 684
 loda  0       7
 inda         11
 stra  0       7
 ujp       l 682
l 683
l 681
 mst           2
i 5650
 cup   0   l  25
 ujp       l 687
l 669
 mst           2
 ldci          2
 cup   1   l  20
 ldoa         43
 stra  0       8
l 687
 ldoi         51
 stri  0       6
 ldoi         52
i 5660
 stri  0      11
 ldoi         51
 ldci         10
 lesi
 fjp       l 688
 ldoi         51
 ldci          1
 adi
 sroi         51
 ujp       l 689
l 688
i 5670
 mst           2
 ldci        251
 cup   1   l  20
l 689
 ldoi         52
 ldci         20
 lesi
 fjp       l 690
 ldoi         52
 ldci          1
 adi
i 5680
 sroi         52
 lao          54
 ldoi         52
 ixa           5
 stra  0      16
 lodb  0      10
 fjp       l 691
 loda  0      16
 loda  0       8
 inda         11
i 5690
 stoa
 ujp       l 692
l 691
 loda  0      16
 ldcn
 stoa
l 692
 loda  0      16
 inca          1
 ldcn
 stoa
 loda  0      16
i 5700
 inca          2
 ldci          0
 stoi
 ujp       l 693
l 690
 mst           2
 ldci        250
 cup   1   l  20
l 693
 lodi  0       5
 ldci         24
 equi
i 5710
 fjp       l 694
 mst           0
 ldc( 13)
 lda   0       7
 cup   2   l 609
 lodb  0      10
 not
 fjp       l 695
 loda  0       8
 inca         11
i 5720
 loda  0       7
 stoa
l 695
 ujp       l 696
l 694
 mst           0
 ldc( 13 16)
 lda   0       7
 cup   2   l 609
 lodb  0      10
 not
 fjp       l 697
i 5730
 loda  0       8
 inca         11
 loda  0       7
 stoa
l 697
 ldoi          9
 ldci         16
 equi
 fjp       l 698
 mst           2
 cup   0   l  25
i 5740
 ldoi          9
 ldci          0
 equi
 fjp       l 699
 lodb  0      10
 fjp       l 700
 mst           2
 ldci        122
 cup   1   l  20
l 700
 mst           2
i 5750
 ldc(  0)
 lda   0       7
 cup   2   l 158
 loda  0       7
 inda         10
 stra  0       9
 loda  0       8
 inca         10
 loda  0       9
 stoa
i 5760
 loda  0       9
 ldcn
 neqa
 fjp       l 701
 loda  0       9
 indi          2
 ordi
 ldc(  0  1  2)
 inn
 not
i 5770
 fjp       l 702
 mst           2
 ldci        120
 cup   1   l  20
 loda  0       8
 inca         10
 ldcn
 stoa
l 702
l 701
 mst           2
 cup   0   l  25
i 5780
 ujp       l 703
l 699
 mst           2
 ldci          2
 cup   1   l  20
 mst           1
 lods  1       5
 ldc( 13)
 uni
 cup   1   l 313
l 703
 ujp       l 704
l 698
i 5790
 lodb  0      10
 not
 fjp       l 705
 mst           2
 ldci        123
 cup   1   l  20
l 705
l 704
l 696
 ldoi          9
 ldci         13
 equi
 fjp       l 706
i 5800
 mst           2
 cup   0   l  25
 ujp       l 707
l 706
 mst           2
 ldci         14
 cup   1   l  20
l 707
 ldoi          9
 ldci         30
 equi
 fjp       l 708
i 5810
 lodb  0      10
 fjp       l 709
 mst           2
 ldci        161
 cup   1   l  20
 ujp       l 710
l 709
 loda  0       8
 inca         18
 ldcb          1
 stob
l 710
i 5820
 mst           2
 cup   0   l  25
 ldoi          9
 ldci         13
 equi
 fjp       l 711
 mst           2
 cup   0   l  25
 ujp       l 712
l 711
 mst           2
i 5830
 ldci         14
 cup   1   l  20
l 712
 ldoi          9
 ordi
 lods  1       5
 inn
 not
 fjp       l 713
 mst           2
 ldci          6
i 5840
 cup   1   l  20
 mst           1
 lods  1       5
 cup   1   l 313
l 713
 ujp       l 714
l 708
 loda  0       8
 inca         18
 ldcb          0
 stob
 lda   0      15
i 5850
 csp         sav
l 715
 mst           2
 lods  1       5
 ldci         13
 loda  0       8
 cup   3   l 312
 ldoi          9
 ldci         13
 equi
 fjp       l 716
i 5860
 ldob         29
 fjp       l 717
 mst           2
 ldcb          0
 cup   1   l 221
l 717
 mst           2
 cup   0   l  25
 ldoi          9
 ordi
 ldc( 22 24 31)
i 5870
 inn
 not
 fjp       l 718
 mst           2
 ldci          6
 cup   1   l  20
 mst           1
 lods  1       5
 cup   1   l 313
l 718
 ujp       l 719
l 716
i 5880
 mst           2
 ldci         14
 cup   1   l  20
l 719
 ldoi          9
 ordi
 ldc( 22 24 31)
 inn
 lao           5
 eof
 ior
i 5890
 fjp       l 715
 loda  0      15
 csp         rst
l 714
 lodi  0       6
 sroi         51
 lodi  0      11
 sroi         52
 lodi  0      13
 sroi         27
 retp
l 667=        17
l 668=        38
l 721
i 5900
 ent   1   l 722
 ent   2   l 723
 lodi  1      84
 lao        1552
 lodi  0       5
 ixa           1
 indi          0
 ldci          1
 mpi
 adi
i 5910
 stri  1      84
 lodi  1      84
 lodi  1      83
 grti
 fjp       l 724
 lodi  1      84
 stri  1      83
l 724
 retp
l 722=         6
l 723=         8
l 725
 ent   1   l 726
 ent   2   l 727
i 5920
 ldoi         26
 ldci         10
 mod
 ldci          0
 equi
 fjp       l 728
 ldcc 'i'
 ldci          1
 lda   3       8
 csp         wrc
i 5930
 ldoi         26
 ldci          5
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 728
 retp
l 726=         5
l 727=         8
l 729
 ent   1   l 730
 ent   2   l 731
 ldob         30
i 5940
 fjp       l 732
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
i 5950
 lda   3       8
 csp         wln
l 732
 ldoi         26
 ldci          1
 adi
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 730=         6
l 731=         9
l 733
i 5960
 ent   1   l 734
 ent   2   l 735
 ldob         30
 fjp       l 736
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
i 5970
 ldci          4
 lda   3       8
 csp         wrs
 lodi  0       5
 ldci         30
 equi
 fjp       l 737
 lao        1460
 lodi  0       6
 deci          1
i 5980
 ixa           4
 ldci         12
 ldci          4
 lda   3       8
 csp         wrs
 lda   3       8
 csp         wln
 lodi  1      84
 lao        1613
 lodi  0       6
i 5990
 deci          1
 ixa           1
 indi          0
 ldci          1
 mpi
 adi
 stri  1      84
 lodi  1      84
 lodi  1      83
 grti
i 6000
 fjp       l 738
 lodi  1      84
 stri  1      83
l 738
 ujp       l 739
l 737
 lodi  0       5
 ldci         38
 equi
 fjp       l 740
 ldcc '''
 ldci          1
i 6010
 lda   3       8
 csp         wrc
 lda   1      15
 lodi  0       6
 deci          1
 ixa           1
 inda          0
 stra  0       8
 ldci          1
 stri  0       7
i 6020
 loda  0       8
 indi          1
 stri  0       9
l 741
 lodi  0       7
 lodi  0       9
 leqi
 fjp       l 742
 loda  0       8
 inca          2
 lodi  0       7
i 6030
 deci          1
 ixa           1
 indc          0
 ldci          1
 lda   3       8
 csp         wrc
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l 741
l 742
i 6040
 loda  0       8
 indi          1
 ldci          1
 adi
 stri  0       7
 ldci         16
 stri  0       9
l 743
 lodi  0       7
 lodi  0       9
 leqi
i 6050
 fjp       l 744
 ldcc ' '
 ldci          1
 lda   3       8
 csp         wrc
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l 743
l 744
 ldcc '''
i 6060
 ldci          1
 lda   3       8
 csp         wrc
 lda   3       8
 csp         wln
 ujp       l 745
l 740
 lodi  0       5
 ldci         42
 equi
 fjp       l 746
i 6070
 lodi  0       6
 chr
 ldci          1
 lda   3       8
 csp         wrc
 lda   3       8
 csp         wln
 ujp       l 747
l 746
 lodi  0       6
 ldci         12
i 6080
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 747
l 745
 mst           1
 lodi  0       5
 cup   1   l 721
l 739
l 736
 ldoi         26
 ldci          1
 adi
i 6090
 sroi         26
 retp
l 734=        10
l 735=         9
l 748
 ent   1   l 749
 ent   2   l 750
 ldob         30
 fjp       l 751
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
i 6100
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
 lodi  0       5
 ujp       l 752
l 754
 ldcc ' '
 ldci          1
 lda   3       8
i 6110
 csp         wrc
 lodi  0       6
 ldci          3
 lda   3       8
 csp         wri
 lodi  0       7
 ldci          8
 lda   3       8
 csp         wri
 lda   3       8
i 6120
 csp         wln
 ujp       l 753
l 755
 lodi  0       6
 chr
 ldci          1
 lda   3       8
 csp         wrc
 lodi  0       6
 chr
 ldcc 'm'
i 6130
 equc
 fjp       l 756
 lodi  0       7
 ldci         11
 lda   3       8
 csp         wri
l 756
 lda   3       8
 csp         wln
 ujp       l 753
l 757
 lodi  0       6
i 6140
 ujp       l 758
l 760
 lca'i               '
 ldci          2
 ldci          2
 lda   3       8
 csp         wrs
 lodi  0       7
 ldci         10
 lda   3       8
 csp         wri
i 6150
 lda   3       8
 csp         wln
 ujp       l 759
l 761
 lca'r               '
 ldci          2
 ldci          2
 lda   3       8
 csp         wrs
 lda   1      15
 lodi  0       7
i 6160
 deci          1
 ixa           1
 inda          0
 stra  0       9
 ldci          1
 stri  0       8
 ldci         16
 stri  0      10
l 762
 lodi  0       8
 lodi  0      10
i 6170
 leqi
 fjp       l 763
 loda  0       9
 inca          1
 lodi  0       8
 deci          1
 ixa           1
 indc          0
 ldci          1
 lda   3       8
i 6180
 csp         wrc
 lodi  0       8
 inci          1
 stri  0       8
 ujp       l 762
l 763
 lda   3       8
 csp         wln
 ujp       l 759
l 764
 lca'b               '
 ldci          2
i 6190
 ldci          2
 lda   3       8
 csp         wrs
 lodi  0       7
 ldci         10
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
 ujp       l 759
l 765
i 6200
 ldcc 'n'
 ldci          1
 lda   3       8
 csp         wrc
 lda   3       8
 csp         wln
 ujp       l 759
l 766
 lca'c '             '
 ldci          3
 ldci          3
i 6210
 lda   3       8
 csp         wrs
 lodi  0       7
 chr
 ldci          1
 lda   3       8
 csp         wrc
 ldcc '''
 ldci          1
 lda   3       8
i 6220
 csp         wrc
 lda   3       8
 csp         wln
 ujp       l 759
l 767
 ldcc '('
 ldci          1
 lda   3       8
 csp         wrc
 lda   1      15
 lodi  0       7
i 6230
 deci          1
 ixa           1
 inda          0
 stra  0       9
 ldci          0
 stri  0       8
 ldci         47
 stri  0      10
l 768
 lodi  0       8
 lodi  0      10
i 6240
 leqi
 fjp       l 769
 lodi  0       8
 loda  0       9
 inds          1
 inn
 fjp       l 770
 lodi  0       8
 ldci          3
 lda   3       8
i 6250
 csp         wri
l 770
 lodi  0       8
 inci          1
 stri  0       8
 ujp       l 768
l 769
 ldcc ')'
 ldci          1
 lda   3       8
 csp         wrc
 lda   3       8
i 6260
 csp         wln
 ujp       l 759
l 758
 chki  1       6
 ldci          1
 sbi
 xjp       l 771
l 771
 ujp       l 760
 ujp       l 761
 ujp       l 764
 ujp       l 765
i 6270
 ujp       l 767
 ujp       l 766
l 759
 ujp       l 753
l 752
 chki 45      56
 ldci         45
 sbi
 xjp       l 772
l 772
 ujp       l 754
 ujc
 ujp       l 755
i 6280
 ujp       l 755
 ujp       l 755
 ujp       l 754
 ujp       l 757
 ujp       l 755
 ujp       l 755
 ujp       l 754
 ujp       l 755
 ujp       l 754
l 753
l 751
 ldoi         26
i 6290
 ldci          1
 adi
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 749=        11
l 750=        11
l 773
 ent   1   l 774
 ent   2   l 775
 loda  0       5
i 6300
 ldcn
 neqa
 fjp       l 776
 loda  0       5
 stra  0       6
 loda  0       6
 indi          2
 ordi
 ujp       l 777
l 779
 loda  0       5
i 6310
 ldoa         40
 equa
 fjp       l 780
 ldcc 'i'
 ldci          1
 lda   3       8
 csp         wrc
 ujp       l 781
l 780
 loda  0       5
 ldoa         37
i 6320
 equa
 fjp       l 782
 ldcc 'b'
 ldci          1
 lda   3       8
 csp         wrc
 ujp       l 783
l 782
 loda  0       5
 ldoa         38
 equa
i 6330
 fjp       l 784
 ldcc 'c'
 ldci          1
 lda   3       8
 csp         wrc
 ujp       l 785
l 784
 loda  0       6
 indi          3
 ldci          1
 equi
i 6340
 fjp       l 786
 ldcc 'i'
 ldci          1
 lda   3       8
 csp         wrc
 ujp       l 787
l 786
 ldcc 'r'
 ldci          1
 lda   3       8
 csp         wrc
l 787
l 785
l 783
l 781
i 6350
 ujp       l 778
l 788
 mst           1
 loda  0       6
 inda          3
 cup   1   l 773
 ujp       l 778
l 789
 ldcc 'a'
 ldci          1
 lda   3       8
 csp         wrc
i 6360
 ujp       l 778
l 790
 ldcc 's'
 ldci          1
 lda   3       8
 csp         wrc
 ujp       l 778
l 791
 ldcc 'm'
 ldci          1
 lda   3       8
 csp         wrc
i 6370
 ujp       l 778
l 792
 mst           3
 ldci        500
 cup   1   l  20
 ujp       l 778
l 777
 chki  0       8
 ldci          0
 sbi
 xjp       l 793
l 793
 ujp       l 779
i 6380
 ujp       l 788
 ujp       l 789
 ujp       l 790
 ujp       l 791
 ujp       l 791
 ujp       l 792
 ujp       l 792
 ujp       l 792
l 778
l 776
 retp
l 774=         7
l 775=        10
l 794
 ent   1   l 795
i 6390
 ent   2   l 796
 ldob         30
 fjp       l 797
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
i 6400
 lda   3       8
 csp         wrs
 mst           1
 loda  0       6
 cup   1   l 773
 lda   3       8
 csp         wln
l 797
 ldoi         26
 ldci          1
 adi
i 6410
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 795=         7
l 796=         9
l 798
 ent   1   l 799
 ent   2   l 800
 ldob         30
 fjp       l 801
 mst           1
i 6420
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
 mst           1
 loda  0       7
i 6430
 cup   1   l 773
 lodi  0       6
 ldci         11
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 801
 ldoi         26
 ldci          1
 adi
i 6440
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 799=         8
l 800=         9
l 802
 ent   1   l 803
 ent   2   l 804
 ldob         30
 fjp       l 805
 mst           1
i 6450
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
 mst           1
 loda  0       8
i 6460
 cup   1   l 773
 lodi  0       6
 ldci          3
 ldci          5
 lodi  0       6
 abi
 ldci         99
 grti
 ordb
 mpi
i 6470
 adi
 lda   3       8
 csp         wri
 lodi  0       7
 ldci          8
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 805
 ldoi         26
i 6480
 ldci          1
 adi
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 803=         9
l 804=        11
l 806
 ent   1   l 807
 ent   2   l 808
 ldoa        180
i 6490
 ldcn
 neqa
 fjp       l 809
 ldoi        181
 ordi
 ujp       l 810
l 812
 ldoa        180
 indi          2
 ldci          0
 equi
i 6500
 ldoa        180
 ldoa         39
 neqa
 and
 fjp       l 813
 ldoa        180
 ldoa         37
 equa
 fjp       l 814
 mst           1
i 6510
 ldci         51
 ldci          3
 ldoi        183
 cup   3   l 748
 ujp       l 815
l 814
 ldoa        180
 ldoa         38
 equa
 fjp       l 816
 mst           1
i 6520
 ldci         51
 ldci          6
 ldoi        183
 cup   3   l 748
 ujp       l 817
l 816
 mst           1
 ldci         51
 ldci          1
 ldoi        183
 cup   3   l 748
l 817
l 815
i 6530
 ujp       l 818
l 813
 ldoa        180
 ldoa         36
 equa
 fjp       l 819
 mst           1
 ldci         51
 ldci          4
 ldci          0
 cup   3   l 748
i 6540
 ujp       l 820
l 819
 lodi  1      80
 ldci         65
 geqi
 fjp       l 821
 mst           3
 ldci        254
 cup   1   l  20
 ujp       l 822
l 821
 lodi  1      80
i 6550
 ldci          1
 adi
 stri  1      80
 lda   1      15
 lodi  1      80
 deci          1
 ixa           1
 ldoa        183
 stoa
 ldoa        180
i 6560
 ldoa         39
 equa
 fjp       l 823
 mst           1
 ldci         51
 ldci          2
 lodi  1      80
 cup   3   l 748
 ujp       l 824
l 823
 mst           1
i 6570
 ldci         51
 ldci          5
 lodi  1      80
 cup   3   l 748
l 824
l 822
l 820
l 818
 ujp       l 811
l 825
 ldoi        182
 ordi
 ujp       l 826
l 828
 ldoi        183
 ldci          1
i 6580
 leqi
 fjp       l 829
 mst           1
 ldci         39
 ldoi        184
 ldoa        180
 cup   3   l 798
 ujp       l 830
l 829
 mst           1
 ldci         54
i 6590
 ldoi         51
 ldoi        183
 sbi
 ldoi        184
 ldoa        180
 cup   4   l 802
l 830
 ujp       l 827
l 831
 mst           1
 ldci         35
 ldoi        183
i 6600
 ldoa        180
 cup   3   l 798
 ujp       l 827
l 832
 mst           3
 ldci        400
 cup   1   l  20
 ujp       l 827
l 826
 chki  0       2
 ldci          0
 sbi
i 6610
 xjp       l 833
l 833
 ujp       l 828
 ujp       l 831
 ujp       l 832
l 827
 ujp       l 811
l 834
 ujp       l 811
l 810
 chki  0       2
 ldci          0
 sbi
 xjp       l 835
l 835
i 6620
 ujp       l 812
 ujp       l 825
 ujp       l 834
l 811
 ldci          2
 sroi        181
l 809
 retp
l 807=         5
l 808=        38
l 836
 ent   1   l 837
 ent   2   l 838
 loda  0       5
 stra  0       6
i 6630
 loda  0       6
 inda          0
 ldcn
 neqa
 fjp       l 839
 loda  0       6
 indi          2
 ordi
 ujp       l 840
l 842
 loda  0       6
i 6640
 indi          3
 ldci          1
 leqi
 fjp       l 843
 mst           1
 ldci         43
 loda  0       6
 indi          4
 loda  0       6
 inda          0
i 6650
 cup   3   l 798
 ujp       l 844
l 843
 mst           1
 ldci         56
 ldoi         51
 loda  0       6
 indi          3
 sbi
 loda  0       6
 indi          4
i 6660
 loda  0       6
 inda          0
 cup   4   l 802
l 844
 ujp       l 841
l 845
 loda  0       6
 indi          3
 ldci          0
 neqi
 fjp       l 846
 mst           3
i 6670
 ldci        400
 cup   1   l  20
 ujp       l 847
l 846
 mst           1
 ldci         26
 loda  0       6
 inda          0
 cup   2   l 794
l 847
 ujp       l 841
l 848
 mst           3
i 6680
 ldci        400
 cup   1   l  20
 ujp       l 841
l 840
 chki  0       2
 ldci          0
 sbi
 xjp       l 849
l 849
 ujp       l 842
 ujp       l 845
 ujp       l 848
l 841
l 839
i 6690
 retp
l 837=         7
l 838=        18
l 850
 ent   1   l 851
 ent   2   l 852
 ldoa        180
 ldcn
 neqa
 fjp       l 853
 ldoi        181
 ordi
 ujp       l 854
l 856
i 6700
 mst           2
 ldoa        180
 cup   1   l 386
 fjp       l 857
 lodi  1      80
 ldci         65
 geqi
 fjp       l 858
 mst           3
 ldci        254
i 6710
 cup   1   l  20
 ujp       l 859
l 858
 lodi  1      80
 ldci          1
 adi
 stri  1      80
 lda   1      15
 lodi  1      80
 deci          1
 ixa           1
i 6720
 ldoa        183
 stoa
 mst           1
 ldci         38
 lodi  1      80
 cup   2   l 733
l 859
 ujp       l 860
l 857
 mst           3
 ldci        400
 cup   1   l  20
l 860
i 6730
 ujp       l 855
l 861
 ldoi        182
 ordi
 ujp       l 862
l 864
 ldoi        183
 ldci          1
 leqi
 fjp       l 865
 mst           1
 ldci         37
i 6740
 ldoi        184
 cup   2   l 733
 ujp       l 866
l 865
 mst           1
 ldci         50
 ldoi         51
 ldoi        183
 sbi
 ldoi        184
 cup   3   l 748
l 866
i 6750
 ujp       l 863
l 867
 ldoi        183
 ldci          0
 neqi
 fjp       l 868
 mst           1
 ldci         34
 ldoi        183
 ldoa         36
 cup   3   l 798
l 868
i 6760
 ujp       l 863
l 869
 mst           3
 ldci        400
 cup   1   l  20
 ujp       l 863
l 862
 chki  0       2
 ldci          0
 sbi
 xjp       l 870
l 870
 ujp       l 864
i 6770
 ujp       l 867
 ujp       l 869
l 863
 ujp       l 855
l 871
 mst           3
 ldci        400
 cup   1   l  20
 ujp       l 855
l 854
 chki  0       2
 ldci          0
 sbi
i 6780
 xjp       l 872
l 872
 ujp       l 856
 ujp       l 861
 ujp       l 871
l 855
 ldci          1
 sroi        181
 ldci          1
 sroi        182
 ldci          0
 sroi        183
l 853
i 6790
 retp
l 851=         5
l 852=        21
l 873
 ent   1   l 874
 ent   2   l 875
 mst           1
 cup   0   l 806
 ldoa        180
 ldcn
 neqa
 fjp       l 876
 ldoa        180
i 6800
 ldoa         37
 neqa
 fjp       l 877
 mst           3
 ldci        144
 cup   1   l  20
l 877
l 876
 ldob         30
 fjp       l 878
 mst           1
 cup   0   l 725
i 6810
 lao        1216
 ldci         33
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
 lca' l              '
 ldci          8
 ldci          2
i 6820
 lda   3       8
 csp         wrs
 lodi  0       5
 ldci          4
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 878
 ldoi         26
 ldci          1
i 6830
 adi
 sroi         26
 mst           1
 ldci         33
 cup   1   l 721
 retp
l 874=         6
l 875=        10
l 879
 ent   1   l 880
 ent   2   l 881
 ldob         30
 fjp       l 882
i 6840
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
 csp         wrs
 lca' l              '
i 6850
 ldci          8
 ldci          2
 lda   3       8
 csp         wrs
 lodi  0       6
 ldci          4
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 882
i 6860
 ldoi         26
 ldci          1
 adi
 sroi         26
 mst           1
 lodi  0       5
 cup   1   l 721
 retp
l 880=         7
l 881=         9
l 883
 ent   1   l 884
 ent   2   l 885
i 6870
 ldob         30
 fjp       l 886
 mst           1
 cup   0   l 725
 lao        1216
 lodi  0       5
 ixa           4
 ldci          4
 ldci          4
 lda   3       8
i 6880
 csp         wrs
 lodi  0       6
 ldci          4
 lda   3       8
 csp         wri
 ldcc 'l'
 ldci          4
 lda   3       8
 csp         wrc
 lodi  0       7
i 6890
 ldci          4
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 886
 ldoi         26
 ldci          1
 adi
 sroi         26
 mst           1
i 6900
 lodi  0       5
 cup   1   l 721
 retp
l 884=         8
l 885=         9
l 887
 ent   1   l 888
 ent   2   l 889
 loda  0       5
 ldcn
 neqa
 fjp       l 890
 loda  0       5
i 6910
 ldoa         40
 neqa
 fjp       l 891
 loda  0       5
 ldoa         39
 neqa
 fjp       l 892
 loda  0       5
 indi          2
 ldci          1
i 6920
 leqi
 fjp       l 893
 mst           3
 loda  0       5
 lda   0       7
 lda   0       6
 cup   3   l 184
 mst           1
 ldci         45
 lodi  0       7
i 6930
 lodi  0       6
 loda  0       5
 cup   4   l 802
l 893
l 892
l 891
l 890
 retp
l 888=         8
l 889=        12
l 894
 ent   1   l 895
 ent   2   l 896
 ldob         30
 fjp       l 897
 ldcc 'l'
 ldci          1
i 6940
 lda   3       8
 csp         wrc
 lodi  0       5
 ldci          4
 lda   3       8
 csp         wri
 lda   3       8
 csp         wln
l 897
 retp
l 895=         6
l 896=         8
l 901
 ent   1   l 902
i 6950
 ent   2   l 903
 loda  0       6
 stra  0      16
 loda  0      16
 inda         10
 sroa        180
 ldci          1
 sroi        181
 loda  0      16
 indi         12
i 6960
 ordi
 ujp       l 904
l 906
 loda  0      16
 indi         13
 ldci          0
 equi
 fjp       l 907
 ldci          0
 sroi        182
 loda  0      16
i 6970
 indi         14
 sroi        183
 loda  0      16
 indi         15
 sroi        184
 ujp       l 908
l 907
 mst           2
 ldci         54
 ldoi         51
 loda  0      16
i 6980
 indi         14
 sbi
 loda  0      16
 indi         15
 ldoa         36
 cup   4   l 802
 ldci          1
 sroi        182
 ldci          0
 sroi        183
l 908
i 6990
 ujp       l 905
l 909
 lao          54
 ldoi         53
 ixa           5
 stra  0      17
 loda  0      17
 indi          2
 ldci          1
 equi
 fjp       l 910
i 7000
 ldci          0
 sroi        182
 loda  0      17
 indi          3
 sroi        183
 loda  0      17
 indi          4
 loda  0      16
 indi         13
 adi
i 7010
 sroi        184
 ujp       l 911
l 910
 ldoi         51
 ldci          1
 equi
 fjp       l 912
 mst           2
 ldci         39
 loda  0      17
 indi          3
i 7020
 ldoa         36
 cup   3   l 798
 ujp       l 913
l 912
 mst           2
 ldci         54
 ldci          0
 loda  0      17
 indi          3
 ldoa         36
 cup   4   l 802
l 913
i 7030
 ldci          1
 sroi        182
 loda  0      16
 indi         13
 sroi        183
l 911
 ujp       l 905
l 914
 loda  0      16
 indi         13
 ldci          0
 equi
i 7040
 fjp       l 915
 mst           4
 ldci        150
 cup   1   l  20
 ldcn
 sroa        180
 ujp       l 916
l 915
 loda  0      16
 indi         16
 ldci          1
i 7050
 equi
 fjp       l 917
 mst           4
 ldci        151
 cup   1   l  20
 ujp       l 918
l 917
 loda  0      16
 indi         14
 ldci          1
 adi
i 7060
 ldoi         51
 neqi
 loda  3       7
 loda  0       6
 neqa
 ior
 fjp       l 919
 mst           4
 ldci        177
 cup   1   l  20
l 919
l 918
i 7070
 ldci          0
 sroi        182
 loda  0      16
 indi         14
 ldci          1
 adi
 sroi        183
 ldci          0
 sroi        184
l 916
 ujp       l 905
l 904
i 7080
 chki  2       5
 ldci          2
 sbi
 xjp       l 920
l 920
 ujp       l 906
 ujp       l 909
 ujc
 ujp       l 914
l 905
 ldoi          9
 ordi
i 7090
 ldos        188
 lods  0       5
 uni
 inn
 not
 fjp       l 921
 mst           4
 ldci         59
 cup   1   l  20
 mst           3
i 7100
 ldos        188
 lods  0       5
 uni
 cup   1   l 313
l 921
l 922
 ldoi          9
 ordi
 ldos        188
 inn
 fjp       l 923
 ldoi          9
i 7110
 ldci         10
 equi
 fjp       l 924
l 925
 lda   0       7
 lao         180
 mov           5
 loda  0       7
 ldcn
 neqa
 fjp       l 926
i 7120
 loda  0       7
 indi          2
 ldci          4
 neqi
 fjp       l 927
 mst           4
 ldci        138
 cup   1   l  20
 ldcn
 stra  0       7
l 927
l 926
i 7130
 mst           2
 cup   0   l 850
 mst           4
 cup   0   l  25
 mst           1
 lods  0       5
 ldc( 11 12)
 uni
 cup   1   l 900
 mst           2
i 7140
 cup   0   l 806
 ldoa        180
 ldcn
 neqa
 fjp       l 928
 ldoa        180
 indi          2
 ldci          0
 neqi
 fjp       l 929
i 7150
 mst           4
 ldci        113
 cup   1   l  20
 ujp       l 930
l 929
 mst           3
 ldoa        180
 ldoa         40
 cup   2   l 357
 not
 fjp       l 931
i 7160
 mst           2
 ldci         58
 ldoa        180
 cup   2   l 794
l 931
l 930
l 928
 loda  0       7
 ldcn
 neqa
 fjp       l 932
 loda  0       7
 stra  0      16
i 7170
 mst           3
 loda  0      16
 inda          3
 ldoa        180
 cup   2   l 357
 fjp       l 933
 loda  0      16
 inda          3
 ldcn
 neqa
i 7180
 fjp       l 934
 mst           4
 loda  0      16
 inda          3
 lda   0      15
 lda   0      14
 cup   3   l 184
 ldob         34
 fjp       l 935
 mst           2
i 7190
 ldci         45
 lodi  0      15
 lodi  0      14
 ldoa         40
 cup   4   l 802
l 935
 lodi  0      15
 ldci          0
 grti
 fjp       l 936
 mst           2
i 7200
 ldci         31
 lodi  0      15
 ldoa         40
 cup   3   l 798
 ujp       l 937
l 936
 lodi  0      15
 ldci          0
 lesi
 fjp       l 938
 mst           2
i 7210
 ldci         34
 lodi  0      15
 ngi
 ldoa         40
 cup   3   l 798
l 938
l 937
l 934
 ujp       l 939
l 933
 mst           4
 ldci        139
 cup   1   l  20
l 939
 loda  0      16
i 7220
 inda          4
 sroa        180
 ldci          1
 sroi        181
 ldci          1
 sroi        182
 ldci          0
 sroi        183
 ldoa        180
 ldcn
i 7230
 neqa
 fjp       l 940
 ldoa        180
 indi          1
 stri  0      13
 mst           4
 ldoa        180
 lda   0      13
 cup   2   l 218
 mst           2
i 7240
 ldci         36
 lodi  0      13
 cup   2   l 733
l 940
l 932
 ldoi          9
 ldci         12
 neqi
 fjp       l 925
 ldoi          9
 ldci         11
 equi
i 7250
 fjp       l 941
 mst           4
 cup   0   l  25
 ujp       l 942
l 941
 mst           4
 ldci         12
 cup   1   l  20
l 942
 ujp       l 943
l 924
 ldoi          9
 ldci         14
i 7260
 equi
 fjp       l 944
 ldoa        180
 ldcn
 neqa
 fjp       l 945
 ldoa        180
 indi          2
 ldci          5
 neqi
i 7270
 fjp       l 946
 mst           4
 ldci        140
 cup   1   l  20
 ldcn
 sroa        180
l 946
l 945
 mst           4
 cup   0   l  25
 ldoi          9
 ldci          0
i 7280
 equi
 fjp       l 947
 ldoa        180
 ldcn
 neqa
 fjp       l 948
 mst           4
 ldoa        180
 inda          3
 lda   0      12
i 7290
 cup   2   l 148
 loda  0      12
 ldcn
 equa
 fjp       l 949
 mst           4
 ldci        152
 cup   1   l  20
 ldcn
 sroa        180
i 7300
 ujp       l 950
l 949
 loda  0      12
 stra  0      16
 loda  0      16
 inda         10
 sroa        180
 ldoi        182
 ordi
 ujp       l 951
l 953
 ldoi        184
i 7310
 loda  0      16
 indi         13
 adi
 sroi        184
 ujp       l 952
l 954
 ldoi        183
 loda  0      16
 indi         13
 adi
 sroi        183
i 7320
 ujp       l 952
l 955
 mst           4
 ldci        400
 cup   1   l  20
 ujp       l 952
l 951
 chki  0       2
 ldci          0
 sbi
 xjp       l 956
l 956
 ujp       l 953
i 7330
 ujp       l 954
 ujp       l 955
l 952
l 950
l 948
 mst           4
 cup   0   l  25
 ujp       l 957
l 947
 mst           4
 ldci          2
 cup   1   l  20
l 957
 ujp       l 958
l 944
 ldoa        180
i 7340
 ldcn
 neqa
 fjp       l 959
 ldoa        180
 stra  0      16
 loda  0      16
 indi          2
 ldci          2
 equi
 fjp       l 960
i 7350
 mst           2
 cup   0   l 806
 loda  0      16
 inda          3
 sroa        180
 ldob         34
 fjp       l 961
 mst           2
 ldci         45
 ldci          1
i 7360
 ldci      32767
 ldoa         36
 cup   4   l 802
l 961
 ldci          1
 sroi        181
 ldci          1
 sroi        182
 ldci          0
 sroi        183
 ujp       l 962
l 960
i 7370
 loda  0      16
 indi          2
 ldci          6
 equi
 fjp       l 963
 loda  0      16
 inda          3
 sroa        180
 ujp       l 964
l 963
 mst           4
i 7380
 ldci        141
 cup   1   l  20
l 964
l 962
l 959
 mst           4
 cup   0   l  25
l 958
l 943
 ldoi          9
 ordi
 lods  0       5
 ldos        188
 uni
 inn
i 7390
 not
 fjp       l 965
 mst           4
 ldci          6
 cup   1   l  20
 mst           3
 lods  0       5
 ldos        188
 uni
 cup   1   l 313
l 965
i 7400
 ujp       l 922
l 923
 retp
l 902=        18
l 903=        61
l 967
 ent   1   l 968
 ent   2   l 969
 ldoi          9
 ldci          0
 equi
 fjp       l 970
 mst           5
 ldc(  2  3)
i 7410
 lda   0       6
 cup   2   l 158
 mst           5
 cup   0   l  25
 ujp       l 971
l 970
 mst           5
 ldci          2
 cup   1   l  20
 ldoa         46
 stra  0       6
l 971
i 7420
 mst           2
 lods  0       5
 loda  0       6
 cup   2   l 901
 retp
l 968=         7
l 969=        10
l 972
 ent   1   l 973
 ent   2   l 974
 mst           1
 lods  1       5
 ldc(  9)
i 7430
 uni
 cup   1   l 967
 mst           3
 cup   0   l 850
 ldoa        180
 ldcn
 neqa
 fjp       l 975
 ldoa        180
 indi          2
i 7440
 ldci          6
 neqi
 fjp       l 976
 mst           5
 ldci        116
 cup   1   l  20
l 976
l 975
 lodi  1       7
 ldci          2
 leqi
 fjp       l 977
i 7450
 mst           3
 ldci         30
 lodi  1       7
 cup   2   l 733
 ujp       l 978
l 977
 mst           5
 ldci        399
 cup   1   l  20
l 978
 retp
l 973=         5
l 974=        10
l 979
 ent   1   l 980
i 7460
 ent   2   l 981
 ldci          1
 stri  0       5
 ldci          5
 stri  0       6
 ldoi          9
 ldci          8
 equi
 fjp       l 982
 mst           5
i 7470
 cup   0   l  25
 mst           1
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 967
 ldoa        180
 stra  0       7
 ldcb          0
 strb  4       9
i 7480
 loda  0       7
 ldcn
 neqa
 fjp       l 983
 loda  0       7
 indi          2
 ldci          6
 equi
 fjp       l 984
 loda  0       7
i 7490
 stra  0       8
 loda  0       8
 inda          3
 ldoa         38
 equa
 fjp       l 985
 ldoi        183
 stri  0       5
 ldoi        184
 stri  0       6
i 7500
 ujp       l 986
l 985
 mst           5
 ldci        399
 cup   1   l  20
l 986
 ldoi          9
 ldci          9
 equi
 fjp       l 987
 lodi  1       7
 ldci          5
i 7510
 equi
 fjp       l 988
 mst           5
 ldci        116
 cup   1   l  20
l 988
 ldcb          1
 strb  4       9
 ujp       l 989
l 987
 ldoi          9
 ldci         12
i 7520
 neqi
 fjp       l 990
 mst           5
 ldci        116
 cup   1   l  20
 mst           4
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 313
l 990
l 989
i 7530
 ldoi          9
 ldci         12
 equi
 fjp       l 991
 mst           5
 cup   0   l  25
 mst           1
 lods  1       5
 ldc(  9 12)
 uni
i 7540
 cup   1   l 967
 ujp       l 992
l 991
 ldcb          1
 strb  4       9
l 992
l 984
l 983
 lodb  4       9
 not
 fjp       l 993
l 994
 mst           3
 cup   0   l 850
 mst           3
i 7550
 ldci         50
 ldoi         51
 lodi  0       5
 sbi
 lodi  0       6
 cup   3   l 748
 ldoa        180
 ldcn
 neqa
 fjp       l 995
i 7560
 ldoa        180
 indi          2
 ldci          1
 leqi
 fjp       l 996
 mst           4
 ldoa         40
 ldoa        180
 cup   2   l 357
 fjp       l 997
i 7570
 mst           3
 ldci         30
 ldci          3
 cup   2   l 733
 ujp       l 998
l 997
 mst           4
 ldoa         39
 ldoa        180
 cup   2   l 357
 fjp       l 999
i 7580
 mst           3
 ldci         30
 ldci          4
 cup   2   l 733
 ujp       l1000
l 999
 mst           4
 ldoa         38
 ldoa        180
 cup   2   l 357
 fjp       l1001
i 7590
 mst           3
 ldci         30
 ldci          5
 cup   2   l 733
 ujp       l1002
l1001
 mst           5
 ldci        399
 cup   1   l  20
l1002
l1000
l 998
 ujp       l1003
l 996
 mst           5
i 7600
 ldci        116
 cup   1   l  20
l1003
l 995
 ldoi          9
 ldci         12
 neqi
 strb  4       9
 lodb  4       9
 not
 fjp       l1004
 mst           5
i 7610
 cup   0   l  25
 mst           1
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 967
l1004
 lodb  4       9
 fjp       l 994
l 993
 ldoi          9
 ldci          9
i 7620
 equi
 fjp       l1005
 mst           5
 cup   0   l  25
 ujp       l1006
l1005
 mst           5
 ldci          4
 cup   1   l  20
l1006
 ujp       l1007
l 982
 lodi  1       7
i 7630
 ldci          5
 equi
 fjp       l1008
 mst           5
 ldci        116
 cup   1   l  20
l1008
l1007
 lodi  1       7
 ldci         11
 equi
 fjp       l1009
i 7640
 mst           3
 ldci         50
 ldoi         51
 lodi  0       5
 sbi
 lodi  0       6
 cup   3   l 748
 mst           3
 ldci         30
 ldci         21
i 7650
 cup   2   l 733
l1009
 retp
l 980=         9
l 981=        33
l1010
 ent   1   l1011
 ent   2   l1012
 lodi  1       7
 stri  0       7
 ldci          1
 stri  0       8
 ldci          5
 ldci          1
i 7660
 adi
 stri  0      10
 ldoi          9
 ldci          8
 equi
 fjp       l1013
 mst           5
 cup   0   l  25
 mst           2
 lods  1       5
i 7670
 ldc(  9 12 16)
 uni
 cup   1   l 900
 ldoa        180
 stra  0       5
 ldcb          0
 strb  4       9
 loda  0       5
 ldcn
 neqa
i 7680
 fjp       l1014
 loda  0       5
 indi          2
 ldci          6
 equi
 fjp       l1015
 loda  0       5
 stra  0      11
 loda  0      11
 inda          3
i 7690
 ldoa         38
 equa
 fjp       l1016
 ldoi        183
 stri  0       8
 ldoi        184
 stri  0      10
 ujp       l1017
l1016
 mst           5
 ldci        399
i 7700
 cup   1   l  20
l1017
 ldoi          9
 ldci          9
 equi
 fjp       l1018
 lodi  0       7
 ldci          6
 equi
 fjp       l1019
 mst           5
i 7710
 ldci        116
 cup   1   l  20
l1019
 ldcb          1
 strb  4       9
 ujp       l1020
l1018
 ldoi          9
 ldci         12
 neqi
 fjp       l1021
 mst           5
i 7720
 ldci        116
 cup   1   l  20
 mst           4
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 313
l1021
l1020
 ldoi          9
 ldci         12
 equi
i 7730
 fjp       l1022
 mst           5
 cup   0   l  25
 mst           2
 lods  1       5
 ldc(  9 12 16)
 uni
 cup   1   l 900
 ujp       l1023
l1022
 ldcb          1
i 7740
 strb  4       9
l1023
l1015
l1014
 lodb  4       9
 not
 fjp       l1024
l1025
 ldoa        180
 stra  0       5
 loda  0       5
 ldcn
 neqa
 fjp       l1026
i 7750
 loda  0       5
 indi          2
 ldci          1
 leqi
 fjp       l1027
 mst           3
 cup   0   l 806
 ujp       l1028
l1027
 mst           3
 cup   0   l 850
l1028
l1026
i 7760
 ldoi          9
 ldci         16
 equi
 fjp       l1029
 mst           5
 cup   0   l  25
 mst           2
 lods  1       5
 ldc(  9 12 16)
 uni
i 7770
 cup   1   l 900
 ldoa        180
 ldcn
 neqa
 fjp       l1030
 ldoa        180
 ldoa         40
 neqa
 fjp       l1031
 mst           5
i 7780
 ldci        116
 cup   1   l  20
l1031
l1030
 mst           3
 cup   0   l 806
 ldcb          0
 strb  0       6
 ujp       l1032
l1029
 ldcb          1
 strb  0       6
l1032
 ldoi          9
i 7790
 ldci         16
 equi
 fjp       l1033
 mst           5
 cup   0   l  25
 mst           2
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 900
i 7800
 ldoa        180
 ldcn
 neqa
 fjp       l1034
 ldoa        180
 ldoa         40
 neqa
 fjp       l1035
 mst           5
 ldci        116
i 7810
 cup   1   l  20
l1035
l1034
 loda  0       5
 ldoa         39
 neqa
 fjp       l1036
 mst           5
 ldci        124
 cup   1   l  20
l1036
 mst           3
 cup   0   l 806
i 7820
 mst           5
 ldci        399
 cup   1   l  20
 ujp       l1037
l1033
 loda  0       5
 ldoa         40
 equa
 fjp       l1038
 lodb  0       6
 fjp       l1039
i 7830
 mst           3
 ldci         51
 ldci          1
 ldci         10
 cup   3   l 748
l1039
 mst           3
 ldci         50
 ldoi         51
 lodi  0       8
 sbi
i 7840
 lodi  0      10
 cup   3   l 748
 mst           3
 ldci         30
 ldci          6
 cup   2   l 733
 ujp       l1040
l1038
 loda  0       5
 ldoa         39
 equa
i 7850
 fjp       l1041
 lodb  0       6
 fjp       l1042
 mst           3
 ldci         51
 ldci          1
 ldci         20
 cup   3   l 748
l1042
 mst           3
 ldci         50
i 7860
 ldoi         51
 lodi  0       8
 sbi
 lodi  0      10
 cup   3   l 748
 mst           3
 ldci         30
 ldci          8
 cup   2   l 733
 ujp       l1043
l1041
i 7870
 loda  0       5
 ldoa         38
 equa
 fjp       l1044
 lodb  0       6
 fjp       l1045
 mst           3
 ldci         51
 ldci          1
 ldci          1
i 7880
 cup   3   l 748
l1045
 mst           3
 ldci         50
 ldoi         51
 lodi  0       8
 sbi
 lodi  0      10
 cup   3   l 748
 mst           3
 ldci         30
i 7890
 ldci          9
 cup   2   l 733
 ujp       l1046
l1044
 loda  0       5
 ldcn
 neqa
 fjp       l1047
 loda  0       5
 indi          2
 ldci          0
i 7900
 equi
 fjp       l1048
 mst           5
 ldci        399
 cup   1   l  20
 ujp       l1049
l1048
 mst           4
 loda  0       5
 cup   1   l 386
 fjp       l1050
i 7910
 loda  0       5
 indi          1
 ldci          1
 dvi
 stri  0       9
 lodb  0       6
 fjp       l1051
 mst           3
 ldci         51
 ldci          1
i 7920
 lodi  0       9
 cup   3   l 748
l1051
 mst           3
 ldci         51
 ldci          1
 lodi  0       9
 cup   3   l 748
 mst           3
 ldci         50
 ldoi         51
i 7930
 lodi  0       8
 sbi
 lodi  0      10
 cup   3   l 748
 mst           3
 ldci         30
 ldci         10
 cup   2   l 733
 ujp       l1052
l1050
 mst           5
i 7940
 ldci        116
 cup   1   l  20
l1052
l1049
l1047
l1046
l1043
l1040
l1037
 ldoi          9
 ldci         12
 neqi
 strb  4       9
 lodb  4       9
 not
 fjp       l1053
 mst           5
i 7950
 cup   0   l  25
 mst           2
 lods  1       5
 ldc(  9 12 16)
 uni
 cup   1   l 900
l1053
 lodb  4       9
 fjp       l1025
l1024
 ldoi          9
 ldci          9
i 7960
 equi
 fjp       l1054
 mst           5
 cup   0   l  25
 ujp       l1055
l1054
 mst           5
 ldci          4
 cup   1   l  20
l1055
 ujp       l1056
l1013
 lodi  1       7
i 7970
 ldci          6
 equi
 fjp       l1057
 mst           5
 ldci        116
 cup   1   l  20
l1057
l1056
 lodi  0       7
 ldci         12
 equi
 fjp       l1058
i 7980
 mst           3
 ldci         50
 ldoi         51
 lodi  0       8
 sbi
 lodi  0      10
 cup   3   l 748
 mst           3
 ldci         30
 ldci         22
i 7990
 cup   2   l 733
l1058
 retp
l1011=        12
l1012=        62
l1059
 ent   1   l1060
 ent   2   l1061
 mst           5
 ldci        399
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  9 12)
i 8000
 uni
 cup   1   l 967
 ldcn
 stra  0       6
 ldcn
 stra  0       5
 ldoa        180
 ldcn
 neqa
 fjp       l1062
i 8010
 ldoa        180
 stra  0       7
 loda  0       7
 indi          2
 ldci          4
 equi
 fjp       l1063
 loda  0       7
 inda          3
 stra  0       6
i 8020
 loda  0       7
 inda          4
 stra  0       5
 ujp       l1064
l1063
 mst           5
 ldci        116
 cup   1   l  20
l1064
l1062
 ldoi          9
 ldci         12
 equi
i 8030
 fjp       l1065
 mst           5
 cup   0   l  25
 ujp       l1066
l1065
 mst           5
 ldci         20
 cup   1   l  20
l1066
 mst           2
 lods  1       5
 ldc(  9 12)
i 8040
 uni
 cup   1   l 900
 ldoa        180
 ldcn
 neqa
 fjp       l1067
 ldoa        180
 indi          2
 ldci          0
 neqi
i 8050
 fjp       l1068
 mst           5
 ldci        116
 cup   1   l  20
 ujp       l1069
l1068
 mst           4
 loda  0       6
 ldoa        180
 cup   2   l 357
 not
i 8060
 fjp       l1070
 mst           5
 ldci        116
 cup   1   l  20
l1070
l1069
l1067
 ldoi          9
 ldci         12
 equi
 fjp       l1071
 mst           5
 cup   0   l  25
i 8070
 ujp       l1072
l1071
 mst           5
 ldci         20
 cup   1   l  20
l1072
 mst           1
 lods  1       5
 ldc(  9)
 uni
 cup   1   l 967
 ldoa        180
i 8080
 ldcn
 neqa
 fjp       l1073
 ldoa        180
 stra  0       7
 loda  0       7
 indi          2
 ldci          4
 equi
 fjp       l1074
i 8090
 mst           4
 loda  0       7
 inda          4
 loda  0       5
 cup   2   l 357
 not
 mst           4
 loda  0       7
 inda          3
 loda  0       6
i 8100
 cup   2   l 357
 not
 ior
 fjp       l1075
 mst           5
 ldci        116
 cup   1   l  20
l1075
 ujp       l1076
l1074
 mst           5
 ldci        116
i 8110
 cup   1   l  20
l1076
l1073
 retp
l1060=         8
l1061=        19
l1077
 ent   1   l1078
 ent   2   l1079
 mst           5
 ldci        399
 cup   1   l  20
 mst           1
 lods  1       5
 ldc(  9 12)
i 8120
 uni
 cup   1   l 967
 ldcn
 stra  0       6
 ldcn
 stra  0       5
 ldoa        180
 ldcn
 neqa
 fjp       l1080
i 8130
 ldoa        180
 stra  0       7
 loda  0       7
 indi          2
 ldci          4
 equi
 fjp       l1081
 loda  0       7
 inda          3
 stra  0       6
i 8140
 loda  0       7
 inda          4
 stra  0       5
 ujp       l1082
l1081
 mst           5
 ldci        116
 cup   1   l  20
l1082
l1080
 ldoi          9
 ldci         12
 equi
i 8150
 fjp       l1083
 mst           5
 cup   0   l  25
 ujp       l1084
l1083
 mst           5
 ldci         20
 cup   1   l  20
l1084
 mst           1
 lods  1       5
 ldc(  9 12)
i 8160
 uni
 cup   1   l 967
 ldoa        180
 ldcn
 neqa
 fjp       l1085
 ldoa        180
 stra  0       7
 loda  0       7
 indi          2
i 8170
 ldci          4
 equi
 fjp       l1086
 mst           4
 loda  0       7
 inda          4
 loda  0       5
 cup   2   l 357
 not
 mst           4
i 8180
 loda  0       7
 inda          3
 loda  0       6
 cup   2   l 357
 not
 ior
 fjp       l1087
 mst           5
 ldci        116
 cup   1   l  20
l1087
i 8190
 ujp       l1088
l1086
 mst           5
 ldci        116
 cup   1   l  20
l1088
l1085
 ldoi          9
 ldci         12
 equi
 fjp       l1089
 mst           5
 cup   0   l  25
i 8200
 ujp       l1090
l1089
 mst           5
 ldci         20
 cup   1   l  20
l1090
 mst           2
 lods  1       5
 ldc(  9)
 uni
 cup   1   l 900
 ldoa        180
i 8210
 ldcn
 neqa
 fjp       l1091
 ldoa        180
 indi          2
 ldci          0
 neqi
 fjp       l1092
 mst           5
 ldci        116
i 8220
 cup   1   l  20
 ujp       l1093
l1092
 mst           4
 loda  0       6
 ldoa        180
 cup   2   l 357
 not
 fjp       l1094
 mst           5
 ldci        116
i 8230
 cup   1   l  20
l1094
l1093
l1091
 retp
l1078=         8
l1079=        19
l1095
 ent   1   l1097
 ent   2   l1098
 mst           1
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 967
 mst           3
i 8240
 cup   0   l 850
 ldcn
 stra  0       6
 ldci          0
 stri  0       7
 ldci          0
 stri  0       8
 ldoa        180
 ldcn
 neqa
i 8250
 fjp       l1099
 ldoa        180
 stra  0      11
 loda  0      11
 indi          2
 ldci          2
 equi
 fjp       l1100
 loda  0      11
 inda          3
i 8260
 ldcn
 neqa
 fjp       l1101
 loda  0      11
 inda          3
 indi          1
 stri  0       8
 loda  0      11
 inda          3
 indi          2
i 8270
 ldci          5
 equi
 fjp       l1102
 loda  0      11
 inda          3
 inda          4
 stra  0       6
l1102
l1101
 ujp       l1103
l1100
 mst           5
 ldci        116
i 8280
 cup   1   l  20
l1103
l1099
l1104
 ldoi          9
 ldci         12
 equi
 fjp       l1105
 mst           5
 cup   0   l  25
 mst           4
 lods  1       5
 ldc(  9 12)
i 8290
 uni
 lda   0       5
 lda   0       9
 cup   3   l 320
 lodi  0       7
 ldci          1
 adi
 stri  0       7
 loda  0       6
 ldcn
i 8300
 equa
 fjp       l1106
 mst           5
 ldci        158
 cup   1   l  20
 ujp       l1107
l1106
 loda  0       6
 indi          2
 ldci          7
 neqi
i 8310
 fjp       l1108
 mst           5
 ldci        162
 cup   1   l  20
 ujp       l1109
l1108
 loda  0       6
 inda          3
 ldcn
 neqa
 fjp       l1110
i 8320
 mst           4
 loda  0       5
 cup   1   l 386
 loda  0       5
 ldoa         39
 equa
 ior
 fjp       l1111
 mst           5
 ldci        159
i 8330
 cup   1   l  20
 ujp       l1112
l1111
 mst           4
 loda  0       6
 inda          3
 inda         10
 loda  0       5
 cup   2   l 357
 fjp       l1113
 loda  0       6
i 8340
 inda          4
 stra  0       5
l1114
 loda  0       5
 ldcn
 neqa
 fjp       l1115
 loda  0       5
 stra  0      11
 loda  0      11
 indi          6
i 8350
 lodi  0      10
 equi
 fjp       l1116
 loda  0      11
 indi          1
 stri  0       8
 loda  0      11
 inda          3
 stra  0       6
 ujp       l1096
i 8360
 ujp       l1117
l1116
 loda  0      11
 inda          4
 stra  0       5
l1117
 ujp       l1114
l1115
 loda  0       6
 indi          1
 stri  0       8
 ldcn
 stra  0       6
i 8370
 ujp       l1118
l1113
 mst           5
 ldci        116
 cup   1   l  20
l1118
l1112
l1110
l1109
l1107
l1096
 ujp       l1104
l1105
 mst           3
 ldci         51
 ldci          1
 lodi  0       8
 cup   3   l 748
i 8380
 mst           3
 ldci         30
 ldci         12
 cup   2   l 733
 retp
l1097=        12
l1098=        20
l1119
 ent   1   l1120
 ent   2   l1121
 mst           1
 lods  1       5
 ldc(  9)
i 8390
 uni
 cup   1   l 967
 ldoa        180
 ldcn
 neqa
 fjp       l1122
 ldoa        180
 indi          2
 ldci          2
 equi
i 8400
 fjp       l1123
 mst           3
 cup   0   l 850
 mst           3
 ldci         30
 ldci         23
 cup   2   l 733
 ujp       l1124
l1123
 mst           5
 ldci        116
i 8410
 cup   1   l  20
l1124
l1122
 retp
l1120=         5
l1121=         9
l1125
 ent   1   l1126
 ent   2   l1127
 mst           1
 lods  1       5
 ldc(  9)
 uni
 cup   1   l 967
 ldoa        180
i 8420
 ldcn
 neqa
 fjp       l1128
 ldoa        180
 indi          2
 ldci          2
 equi
 fjp       l1129
 mst           3
 cup   0   l 806
i 8430
 mst           3
 ldci         30
 ldci         13
 cup   2   l 733
 ujp       l1130
l1129
 mst           5
 ldci        116
 cup   1   l  20
l1130
l1128
 retp
l1126=         5
l1127=         9
l1131
 ent   1   l1132
i 8440
 ent   2   l1133
 ldoa        180
 ldcn
 neqa
 fjp       l1134
 ldoa        180
 ldoa         40
 equa
 fjp       l1135
 mst           3
i 8450
 ldci          0
 cup   1   l 729
 ujp       l1136
l1135
 ldoa        180
 ldoa         39
 equa
 fjp       l1137
 mst           3
 ldci          1
 cup   1   l 729
i 8460
 ujp       l1138
l1137
 mst           5
 ldci        125
 cup   1   l  20
 ldoa         40
 sroa        180
l1138
l1136
l1134
 retp
l1132=         5
l1133=         9
l1139
 ent   1   l1140
 ent   2   l1141
 ldoa        180
i 8470
 ldcn
 neqa
 fjp       l1142
 ldoa        180
 ldoa         40
 equa
 fjp       l1143
 mst           3
 ldci         24
 cup   1   l 729
i 8480
 ujp       l1144
l1143
 ldoa        180
 ldoa         39
 equa
 fjp       l1145
 mst           3
 ldci         25
 cup   1   l 729
 ujp       l1146
l1145
 mst           5
i 8490
 ldci        125
 cup   1   l  20
 ldoa         40
 sroa        180
l1146
l1144
l1142
 retp
l1140=         5
l1141=         9
l1147
 ent   1   l1148
 ent   2   l1149
 ldoa        180
 ldcn
 neqa
i 8500
 fjp       l1150
 ldoa        180
 ldoa         39
 neqa
 fjp       l1151
 mst           5
 ldci        125
 cup   1   l  20
l1151
l1150
 mst           3
 ldci         27
i 8510
 cup   1   l 729
 ldoa         40
 sroa        180
 retp
l1148=         5
l1149=         8
l1152
 ent   1   l1153
 ent   2   l1154
 ldoa        180
 ldcn
 neqa
 fjp       l1155
i 8520
 ldoa        180
 ldoa         40
 neqa
 fjp       l1156
 mst           5
 ldci        125
 cup   1   l  20
l1156
l1155
 mst           3
 ldci         20
 cup   1   l 729
i 8530
 ldoa         37
 sroa        180
 retp
l1153=         5
l1154=         8
l1157
 ent   1   l1158
 ent   2   l1159
 ldoa        180
 ldcn
 neqa
 fjp       l1160
 ldoa        180
i 8540
 indi          2
 ldci          3
 geqi
 fjp       l1161
 mst           5
 ldci        125
 cup   1   l  20
l1161
l1160
 mst           3
 ldci         58
 ldoa        180
i 8550
 cup   2   l 794
 ldoa         40
 sroa        180
 retp
l1158=         5
l1159=         9
l1162
 ent   1   l1163
 ent   2   l1164
 ldoa        180
 ldcn
 neqa
 fjp       l1165
i 8560
 ldoa        180
 ldoa         40
 neqa
 fjp       l1166
 mst           5
 ldci        125
 cup   1   l  20
l1166
l1165
 mst           3
 ldci         59
 cup   1   l 729
i 8570
 ldoa         38
 sroa        180
 retp
l1163=         5
l1164=         8
l1167
 ent   1   l1168
 ent   2   l1169
 ldoa        180
 ldcn
 neqa
 fjp       l1170
 ldoa        180
i 8580
 indi          2
 ldci          0
 neqi
 fjp       l1171
 mst           5
 ldci        125
 cup   1   l  20
l1171
l1170
 lodi  1       7
 ldci          7
 equi
i 8590
 fjp       l1172
 mst           3
 ldci         31
 ldci          1
 ldoa        180
 cup   3   l 798
 ujp       l1173
l1172
 mst           3
 ldci         34
 ldci          1
i 8600
 ldoa        180
 cup   3   l 798
l1173
 retp
l1168=         5
l1169=        12
l1174
 ent   1   l1175
 ent   2   l1176
 ldoi          9
 ldci          8
 equi
 fjp       l1177
 mst           5
i 8610
 cup   0   l  25
 mst           1
 lods  1       5
 ldc(  9)
 uni
 cup   1   l 967
 ldoi          9
 ldci          9
 equi
 fjp       l1178
i 8620
 mst           5
 cup   0   l  25
 ujp       l1179
l1178
 mst           5
 ldci          4
 cup   1   l  20
l1179
 ujp       l1180
l1177
 ldoa         35
 sroa        180
 ldci          1
i 8630
 sroi        181
 ldci          0
 sroi        182
 ldci          1
 sroi        183
 ldci          5
 sroi        184
l1180
 mst           3
 cup   0   l 850
 ldoa        180
i 8640
 ldcn
 neqa
 fjp       l1181
 ldoa        180
 indi          2
 ldci          6
 neqi
 fjp       l1182
 mst           5
 ldci        125
i 8650
 cup   1   l  20
l1182
l1181
 lodi  1       7
 ldci          9
 equi
 fjp       l1183
 mst           3
 ldci          8
 cup   1   l 729
 ujp       l1184
l1183
 mst           3
i 8660
 ldci         30
 ldci         14
 cup   2   l 733
l1184
 ldoa         37
 sroa        180
 retp
l1175=         5
l1176=        12
l1185
 ent   1   l1186
 ent   2   l1187
 ldci          0
 stri  0      11
i 8670
 loda  1       6
 stra  0      12
 loda  0      12
 inda         11
 stra  0       6
 loda  0      12
 indi         16
 stri  0       8
 loda  0      12
 indb         17
i 8680
 not
 fjp       l1188
 mst           3
 ldci         41
 ldoi         51
 loda  0      12
 indi         14
 sbi
 cup   2   l 733
l1188
 ldoi          9
i 8690
 ldci          8
 equi
 fjp       l1189
 ldoi         27
 stri  0      10
l1190
 ldcb          0
 strb  0       9
 lodi  0       8
 ldci          0
 equi
i 8700
 fjp       l1191
 loda  0       6
 ldcn
 equa
 fjp       l1192
 mst           5
 ldci        126
 cup   1   l  20
 ujp       l1193
l1192
 loda  0       6
i 8710
 indi         12
 ordi
 ldc(  4  5)
 inn
 strb  0       9
l1193
 ujp       l1194
l1191
 mst           5
 ldci        399
 cup   1   l  20
l1194
 mst           5
i 8720
 cup   0   l  25
 lodb  0       9
 fjp       l1195
 mst           5
 ldci        399
 cup   1   l  20
 ldoi          9
 ldci          0
 neqi
 fjp       l1196
i 8730
 mst           5
 ldci          2
 cup   1   l  20
 mst           4
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 313
 ujp       l1197
l1196
 loda  0       6
i 8740
 indi         12
 ldci          4
 equi
 fjp       l1198
 mst           5
 ldc(  4)
 lda   0       5
 cup   2   l 158
 ujp       l1199
l1198
 mst           5
i 8750
 ldc(  5)
 lda   0       5
 cup   2   l 158
 mst           4
 loda  0       5
 inda         10
 loda  0       6
 inda         10
 cup   2   l 357
 not
i 8760
 fjp       l1200
 mst           5
 ldci        128
 cup   1   l  20
l1200
l1199
 mst           5
 cup   0   l  25
 ldoi          9
 ordi
 lods  1       5
 ldc(  9 12)
i 8770
 uni
 inn
 not
 fjp       l1201
 mst           5
 ldci          6
 cup   1   l  20
 mst           4
 lods  1       5
 ldc(  9 12)
i 8780
 uni
 cup   1   l 313
l1201
l1197
 ujp       l1202
l1195
 mst           2
 lods  1       5
 ldc(  9 12)
 uni
 cup   1   l 900
 ldoa        180
 ldcn
i 8790
 neqa
 fjp       l1203
 lodi  0       8
 ldci          0
 equi
 fjp       l1204
 loda  0       6
 ldcn
 neqa
 fjp       l1205
i 8800
 loda  0       6
 inda         10
 stra  0       7
 loda  0       7
 ldcn
 neqa
 fjp       l1206
 loda  0       6
 indi         13
 ldci          0
i 8810
 equi
 fjp       l1207
 loda  0       7
 indi          2
 ldci          3
 leqi
 fjp       l1208
 mst           3
 cup   0   l 806
 ldob         34
i 8820
 fjp       l1209
 mst           3
 loda  0       7
 cup   1   l 887
l1209
 mst           4
 ldoa         39
 loda  0       7
 cup   2   l 357
 ldoa        180
 ldoa         40
i 8830
 equa
 and
 fjp       l1210
 mst           3
 ldci         10
 cup   1   l 729
 ldoa         39
 sroa        180
l1210
 lodi  0      11
 loda  0       7
i 8840
 indi          1
 adi
 stri  0      11
 mst           5
 ldoa         41
 lda   0      11
 cup   2   l 218
 ujp       l1211
l1208
 mst           3
 cup   0   l 850
i 8850
 lodi  0      11
 ldci          1
 adi
 stri  0      11
 mst           5
 ldoa         41
 lda   0      11
 cup   2   l 218
l1211
 ujp       l1212
l1207
 ldoi        181
i 8860
 ldci          1
 equi
 fjp       l1213
 mst           3
 cup   0   l 850
 lodi  0      11
 ldci          1
 adi
 stri  0      11
 mst           5
i 8870
 ldoa         41
 lda   0      11
 cup   2   l 218
 ujp       l1214
l1213
 mst           5
 ldci        154
 cup   1   l  20
l1214
l1212
 mst           4
 loda  0       7
 ldoa        180
i 8880
 cup   2   l 357
 not
 fjp       l1215
 mst           5
 ldci        142
 cup   1   l  20
l1215
l1206
l1205
 ujp       l1216
l1204
l1216
l1203
l1202
 lodi  0       8
 ldci          0
 equi
i 8890
 loda  0       6
 ldcn
 neqa
 and
 fjp       l1217
 loda  0       6
 inda         11
 stra  0       6
l1217
 ldoi          9
 ldci         12
i 8900
 neqi
 fjp       l1190
 lodi  0      10
 sroi         27
 ldoi          9
 ldci          9
 equi
 fjp       l1218
 mst           5
 cup   0   l  25
i 8910
 ujp       l1219
l1218
 mst           5
 ldci          4
 cup   1   l  20
l1219
l1189
 lodi  0       8
 ldci          0
 equi
 fjp       l1220
 loda  0       6
 ldcn
i 8920
 neqa
 fjp       l1221
 mst           5
 ldci        126
 cup   1   l  20
l1221
 loda  1       6
 stra  0      12
 loda  0      12
 indb         17
 fjp       l1222
i 8930
 mst           3
 ldci         30
 loda  0      12
 indi         15
 cup   2   l 733
 ujp       l1223
l1222
 mst           3
 ldci         46
 lodi  0      11
 loda  0      12
i 8940
 indi         15
 cup   3   l 883
l1223
l1220
 loda  1       6
 inda         10
 sroa        180
 retp
l1186=        13
l1187=        41
l 966
 ent   1   l1224
 ent   2   l1225
 loda  0       6
 indi         13
i 8950
 ldci          0
 equi
 fjp       l1226
 loda  0       6
 indi         14
 stri  0       7
 loda  0       6
 indi         12
 ldci          4
 equi
i 8960
 fjp       l1227
 lodi  0       7
 ldc(  5  6 11 12)
 inn
 not
 fjp       l1228
 ldoi          9
 ldci          8
 equi
 fjp       l1229
i 8970
 mst           4
 cup   0   l  25
 ujp       l1230
l1229
 mst           4
 ldci          9
 cup   1   l  20
l1230
l1228
 lodi  0       7
 ujp       l1231
l1233
 mst           0
 cup   0   l 972
i 8980
 ujp       l1232
l1234
 mst           0
 cup   0   l 979
 ujp       l1232
l1235
 mst           0
 cup   0   l1010
 ujp       l1232
l1236
 mst           0
 cup   0   l1059
 ujp       l1232
l1237
i 8990
 mst           0
 cup   0   l1077
 ujp       l1232
l1238
 mst           0
 cup   0   l1095
 ujp       l1232
l1239
 mst           0
 cup   0   l1125
 ujp       l1232
l1240
 mst           0
i 9000
 cup   0   l1119
 ujp       l1232
l1231
 chki  1      13
 ldci          1
 sbi
 xjp       l1241
l1241
 ujp       l1233
 ujp       l1233
 ujp       l1233
 ujp       l1233
i 9010
 ujp       l1234
 ujp       l1235
 ujp       l1236
 ujp       l1237
 ujp       l1238
 ujp       l1239
 ujp       l1234
 ujp       l1235
 ujp       l1240
l1232
 lodi  0       7
i 9020
 ldc(  5  6 11 12)
 inn
 not
 fjp       l1242
 ldoi          9
 ldci          9
 equi
 fjp       l1243
 mst           4
 cup   0   l  25
i 9030
 ujp       l1244
l1243
 mst           4
 ldci          4
 cup   1   l  20
l1244
l1242
 ujp       l1245
l1227
 lodi  0       7
 ldci          8
 leqi
 fjp       l1246
 ldoi          9
i 9040
 ldci          8
 equi
 fjp       l1247
 mst           4
 cup   0   l  25
 ujp       l1248
l1247
 mst           4
 ldci          9
 cup   1   l  20
l1248
 mst           1
i 9050
 lods  0       5
 ldc(  9)
 uni
 cup   1   l 900
 mst           2
 cup   0   l 806
l1246
 lodi  0       7
 ujp       l1249
l1251
 mst           0
 cup   0   l1131
i 9060
 ujp       l1250
l1252
 mst           0
 cup   0   l1139
 ujp       l1250
l1253
 mst           0
 cup   0   l1147
 ujp       l1250
l1254
 mst           0
 cup   0   l1152
 ujp       l1250
l1255
i 9070
 mst           0
 cup   0   l1157
 ujp       l1250
l1256
 mst           0
 cup   0   l1162
 ujp       l1250
l1257
 mst           0
 cup   0   l1167
 ujp       l1250
l1258
 mst           0
i 9080
 cup   0   l1174
 ujp       l1250
l1249
 chki  1      10
 ldci          1
 sbi
 xjp       l1259
l1259
 ujp       l1251
 ujp       l1252
 ujp       l1253
 ujp       l1254
i 9090
 ujp       l1255
 ujp       l1256
 ujp       l1257
 ujp       l1257
 ujp       l1258
 ujp       l1258
l1250
 lodi  0       7
 ldci          8
 leqi
 fjp       l1260
i 9100
 ldoi          9
 ldci          9
 equi
 fjp       l1261
 mst           4
 cup   0   l  25
 ujp       l1262
l1261
 mst           4
 ldci          4
 cup   1   l  20
l1262
l1260
l1245
i 9110
 ujp       l1263
l1226
 mst           0
 cup   0   l1185
l1263
 retp
l1224=         8
l1225=        11
l1266
 ent   1   l1267
 ent   2   l1268
 ldoi          9
 ordi
 ldos        187
 inn
i 9120
 not
 fjp       l1269
 mst           7
 ldci         58
 cup   1   l  20
 mst           6
 lods  0       5
 ldos        187
 uni
 cup   1   l 313
i 9130
 ldcn
 sroa        180
l1269
l1270
 ldoi          9
 ordi
 ldos        187
 inn
 fjp       l1271
 ldoi          9
 ordi
 ujp       l1272
l1274
i 9140
 mst           7
 ldc(  1  2  3  5)
 lda   0       6
 cup   2   l 158
 mst           7
 cup   0   l  25
 loda  0       6
 indi         12
 ldci          5
 equi
i 9150
 fjp       l1275
 mst           4
 lods  0       5
 loda  0       6
 cup   2   l 966
 ldci          2
 sroi        181
 ldoa        180
 ldcn
 neqa
i 9160
 fjp       l1276
 ldoa        180
 indi          2
 ldci          1
 equi
 fjp       l1277
 ldoa        180
 inda          3
 sroa        180
l1277
l1276
 ujp       l1278
l1275
i 9170
 loda  0       6
 indi         12
 ldci          1
 equi
 fjp       l1279
 loda  0       6
 stra  0      11
 loda  0      11
 inda         10
 sroa        180
i 9180
 ldci          0
 sroi        181
 lao         182
 loda  0      11
 inca         13
 mov           2
 ujp       l1280
l1279
 mst           4
 lods  0       5
 loda  0       6
i 9190
 cup   2   l 901
 ldoa        180
 ldcn
 neqa
 fjp       l1281
 ldoa        180
 stra  0      11
 loda  0      11
 indi          2
 ldci          1
i 9200
 equi
 fjp       l1282
 loda  0      11
 inda          3
 sroa        180
l1282
l1281
l1280
l1278
 ujp       l1273
l1283
 ldoa         40
 sroa        180
 ldci          0
 sroi        181
i 9210
 lao         182
 lao          11
 mov           2
 mst           7
 cup   0   l  25
 ujp       l1273
l1284
 ldoa         39
 sroa        180
 ldci          0
 sroi        181
i 9220
 lao         182
 lao          11
 mov           2
 mst           7
 cup   0   l  25
 ujp       l1273
l1285
 ldoi         13
 ldci          1
 equi
 fjp       l1286
i 9230
 ldoa         38
 sroa        180
 ujp       l1287
l1286
 lda   0      10
 ldci          5
 csp         new
 loda  0      10
 stra  0      11
 loda  0      11
 inca          4
i 9240
 ldoa         38
 stoa
 loda  0      11
 inca          2
 ldci          4
 stoi
 loda  0      11
 inca          3
 ldcn
 stoa
i 9250
 loda  0      11
 inca          1
 ldoi         13
 ldci          1
 mpi
 stoi
 loda  0      10
 sroa        180
l1287
 ldci          0
 sroi        181
i 9260
 lao         182
 lao          11
 mov           2
 mst           7
 cup   0   l  25
 ujp       l1273
l1288
 mst           7
 cup   0   l  25
 mst           4
 lods  0       5
i 9270
 ldc(  9)
 uni
 cup   1   l 900
 ldoi          9
 ldci          9
 equi
 fjp       l1289
 mst           7
 cup   0   l  25
 ujp       l1290
l1289
i 9280
 mst           7
 ldci          4
 cup   1   l  20
l1290
 ujp       l1273
l1291
 mst           7
 cup   0   l  25
 mst           1
 lods  0       5
 cup   1   l1266
 mst           5
i 9290
 cup   0   l 806
 mst           5
 ldci         19
 cup   1   l 729
 ldoa        180
 ldcn
 neqa
 fjp       l1292
 ldoa        180
 ldoa         37
i 9300
 neqa
 fjp       l1293
 mst           7
 ldci        135
 cup   1   l  20
 ldcn
 sroa        180
l1293
l1292
 ujp       l1273
l1294
 mst           7
 cup   0   l  25
i 9310
 ldc()
 strs  0       9
 ldcb          0
 strb  0       8
 lda   0      10
 ldci          4
 csp         new
 loda  0      10
 stra  0      11
 loda  0      11
i 9320
 inca          3
 ldcn
 stoa
 loda  0      11
 inca          1
 ldci          1
 stoi
 loda  0      11
 inca          2
 ldci          3
i 9330
 stoi
 ldoi          9
 ldci         11
 equi
 fjp       l1295
 loda  0      10
 sroa        180
 ldci          0
 sroi        181
 mst           7
i 9340
 cup   0   l  25
 ujp       l1296
l1295
l1297
 mst           4
 lods  0       5
 ldc( 11 12)
 uni
 cup   1   l 900
 ldoa        180
 ldcn
 neqa
i 9350
 fjp       l1298
 ldoa        180
 indi          2
 ldci          0
 neqi
 fjp       l1299
 mst           7
 ldci        136
 cup   1   l  20
 ldcn
i 9360
 sroa        180
 ujp       l1300
l1299
 mst           6
 loda  0      10
 inda          3
 ldoa        180
 cup   2   l 357
 fjp       l1301
 ldoi        181
 ldci          0
i 9370
 equi
 fjp       l1302
 ldoi        183
 ldci          0
 lesi
 ldoi        183
 ldci         47
 grti
 ior
 fjp       l1303
i 9380
 mst           7
 ldci        304
 cup   1   l  20
 ujp       l1304
l1303
 lods  0       9
 ldoi        183
 sgs
 uni
 strs  0       9
l1304
 ujp       l1305
l1302
i 9390
 mst           5
 cup   0   l 806
 mst           6
 ldoa        180
 ldoa         40
 cup   2   l 357
 not
 fjp       l1306
 mst           5
 ldci         58
i 9400
 ldoa        180
 cup   2   l 794
l1306
 mst           5
 ldci         23
 cup   1   l 729
 lodb  0       8
 fjp       l1307
 mst           5
 ldci         28
 cup   1   l 729
i 9410
 ujp       l1308
l1307
 ldcb          1
 strb  0       8
l1308
l1305
 loda  0      10
 inca          3
 ldoa        180
 stoa
 loda  0      10
 sroa        180
 ujp       l1309
l1301
i 9420
 mst           7
 ldci        137
 cup   1   l  20
l1309
l1300
l1298
 ldoi          9
 ldci         12
 neqi
 strb  6       9
 lodb  6       9
 not
 fjp       l1310
i 9430
 mst           7
 cup   0   l  25
l1310
 lodb  6       9
 fjp       l1297
 ldoi          9
 ldci         11
 equi
 fjp       l1311
 mst           7
 cup   0   l  25
i 9440
 ujp       l1312
l1311
 mst           7
 ldci         12
 cup   1   l  20
l1312
l1296
 lodb  0       8
 fjp       l1313
 lods  0       9
 ldc()
 neqs
 fjp       l1314
i 9450
 lda   0       7
 ldci          2
 csp         new
 loda  0       7
 inca          1
 lods  0       9
 stos
 loda  0       7
 ldci          1
 stoi
i 9460
 lodi  5      80
 ldci         65
 equi
 fjp       l1315
 mst           7
 ldci        254
 cup   1   l  20
 ujp       l1316
l1315
 lodi  5      80
 ldci          1
i 9470
 adi
 stri  5      80
 lda   5      15
 lodi  5      80
 deci          1
 ixa           1
 loda  0       7
 stoa
 mst           5
 ldci         51
i 9480
 ldci          5
 lodi  5      80
 cup   3   l 748
 mst           5
 ldci         28
 cup   1   l 729
 ldci          2
 sroi        181
l1316
l1314
 ujp       l1317
l1313
 lda   0       7
i 9490
 ldci          2
 csp         new
 loda  0       7
 inca          1
 lods  0       9
 stos
 loda  0       7
 ldci          1
 stoi
 loda  0       7
i 9500
 sroa        183
l1317
 ujp       l1273
l1272
 chki  0      10
 ldci          0
 sbi
 xjp       l1318
l1318
 ujp       l1274
 ujp       l1283
 ujp       l1284
 ujp       l1285
i 9510
 ujp       l1291
 ujc
 ujc
 ujc
 ujp       l1288
 ujc
 ujp       l1294
l1273
 ldoi          9
 ordi
 lods  0       5
i 9520
 inn
 not
 fjp       l1319
 mst           7
 ldci          6
 cup   1   l  20
 mst           6
 lods  0       5
 ldos        187
 uni
i 9530
 cup   1   l 313
l1319
 ujp       l1270
l1271
 retp
l1267=        12
l1268=        37
l1265
 ent   1   l1320
 ent   2   l1321
 mst           0
 lods  0       5
 ldc(  5)
 uni
 cup   1   l1266
l1322
i 9540
 ldoi          9
 ldci          5
 equi
 fjp       l1323
 mst           4
 cup   0   l 806
 lda   0       6
 lao         180
 mov           5
 ldoi         10
i 9550
 stri  0      11
 mst           6
 cup   0   l  25
 mst           0
 lods  0       5
 ldc(  5)
 uni
 cup   1   l1266
 mst           4
 cup   0   l 806
i 9560
 loda  0       6
 ldcn
 neqa
 ldoa        180
 ldcn
 neqa
 and
 fjp       l1324
 lodi  0      11
 ordi
i 9570
 ujp       l1325
l1327
 loda  0       6
 ldoa         40
 equa
 ldoa        180
 ldoa         40
 equa
 and
 fjp       l1328
 mst           4
i 9580
 ldci         15
 cup   1   l 729
 ujp       l1329
l1328
 loda  0       6
 ldoa         40
 equa
 fjp       l1330
 mst           4
 ldci          9
 cup   1   l 729
i 9590
 ldoa         39
 stra  0       6
 ujp       l1331
l1330
 ldoa        180
 ldoa         40
 equa
 fjp       l1332
 mst           4
 ldci         10
 cup   1   l 729
i 9600
 ldoa         39
 sroa        180
l1332
l1331
 loda  0       6
 ldoa         39
 equa
 ldoa        180
 ldoa         39
 equa
 and
 fjp       l1333
i 9610
 mst           4
 ldci         16
 cup   1   l 729
 ujp       l1334
l1333
 loda  0       6
 indi          2
 ldci          3
 equi
 mst           5
 loda  0       6
i 9620
 ldoa        180
 cup   2   l 357
 and
 fjp       l1335
 mst           4
 ldci         12
 cup   1   l 729
 ujp       l1336
l1335
 mst           6
 ldci        134
i 9630
 cup   1   l  20
 ldcn
 sroa        180
l1336
l1334
l1329
 ujp       l1326
l1337
 ldoa        180
 ldoa         40
 equa
 fjp       l1338
 mst           4
 ldci         10
i 9640
 cup   1   l 729
 ldoa         39
 sroa        180
l1338
 loda  0       6
 ldoa         40
 equa
 fjp       l1339
 mst           4
 ldci          9
 cup   1   l 729
i 9650
 ldoa         39
 stra  0       6
l1339
 loda  0       6
 ldoa         39
 equa
 ldoa        180
 ldoa         39
 equa
 and
 fjp       l1340
i 9660
 mst           4
 ldci          7
 cup   1   l 729
 ujp       l1341
l1340
 mst           6
 ldci        134
 cup   1   l  20
 ldcn
 sroa        180
l1341
 ujp       l1326
l1342
i 9670
 loda  0       6
 ldoa         40
 equa
 ldoa        180
 ldoa         40
 equa
 and
 fjp       l1343
 mst           4
 ldci          6
i 9680
 cup   1   l 729
 ujp       l1344
l1343
 mst           6
 ldci        134
 cup   1   l  20
 ldcn
 sroa        180
l1344
 ujp       l1326
l1345
 loda  0       6
 ldoa         40
i 9690
 equa
 ldoa        180
 ldoa         40
 equa
 and
 fjp       l1346
 mst           4
 ldci         14
 cup   1   l 729
 ujp       l1347
l1346
i 9700
 mst           6
 ldci        134
 cup   1   l  20
 ldcn
 sroa        180
l1347
 ujp       l1326
l1348
 loda  0       6
 ldoa         37
 equa
 ldoa        180
i 9710
 ldoa         37
 equa
 and
 fjp       l1349
 mst           4
 ldci          4
 cup   1   l 729
 ujp       l1350
l1349
 mst           6
 ldci        134
i 9720
 cup   1   l  20
 ldcn
 sroa        180
l1350
 ujp       l1326
l1325
 chki  0       4
 ldci          0
 sbi
 xjp       l1351
l1351
 ujp       l1327
 ujp       l1337
i 9730
 ujp       l1348
 ujp       l1342
 ujp       l1345
l1326
 ujp       l1352
l1324
 ldcn
 sroa        180
l1352
 ujp       l1322
l1323
 retp
l1320=        12
l1321=        26
l1264
 ent   1   l1353
 ent   2   l1354
i 9740
 ldcb          0
 strb  0      12
 ldoi          9
 ldci          6
 equi
 ldoi         10
 ordi
 ldc(  5  6)
 inn
 and
i 9750
 fjp       l1355
 ldoi         10
 ldci          6
 equi
 strb  0      12
 mst           5
 cup   0   l  25
l1355
 mst           0
 lods  0       5
 ldc(  6)
i 9760
 uni
 cup   1   l1265
 lodb  0      12
 fjp       l1356
 mst           3
 cup   0   l 806
 ldoa        180
 ldoa         40
 equa
 fjp       l1357
i 9770
 mst           3
 ldci         17
 cup   1   l 729
 ujp       l1358
l1357
 ldoa        180
 ldoa         39
 equa
 fjp       l1359
 mst           3
 ldci         18
i 9780
 cup   1   l 729
 ujp       l1360
l1359
 mst           5
 ldci        134
 cup   1   l  20
 ldcn
 sroa        180
l1360
l1358
l1356
l1361
 ldoi          9
 ldci          6
 equi
i 9790
 fjp       l1362
 mst           3
 cup   0   l 806
 lda   0       6
 lao         180
 mov           5
 ldoi         10
 stri  0      11
 mst           5
 cup   0   l  25
i 9800
 mst           0
 lods  0       5
 ldc(  6)
 uni
 cup   1   l1265
 mst           3
 cup   0   l 806
 loda  0       6
 ldcn
 neqa
i 9810
 ldoa        180
 ldcn
 neqa
 and
 fjp       l1363
 lodi  0      11
 ordi
 ujp       l1364
l1366
 loda  0       6
 ldoa         40
i 9820
 equa
 ldoa        180
 ldoa         40
 equa
 and
 fjp       l1367
 mst           3
 ldci          2
 cup   1   l 729
 ujp       l1368
l1367
i 9830
 loda  0       6
 ldoa         40
 equa
 fjp       l1369
 mst           3
 ldci          9
 cup   1   l 729
 ldoa         39
 stra  0       6
 ujp       l1370
l1369
i 9840
 ldoa        180
 ldoa         40
 equa
 fjp       l1371
 mst           3
 ldci         10
 cup   1   l 729
 ldoa         39
 sroa        180
l1371
l1370
 loda  0       6
i 9850
 ldoa         39
 equa
 ldoa        180
 ldoa         39
 equa
 and
 fjp       l1372
 mst           3
 ldci          3
 cup   1   l 729
i 9860
 ujp       l1373
l1372
 loda  0       6
 indi          2
 ldci          3
 equi
 mst           4
 loda  0       6
 ldoa        180
 cup   2   l 357
 and
i 9870
 fjp       l1374
 mst           3
 ldci         28
 cup   1   l 729
 ujp       l1375
l1374
 mst           5
 ldci        134
 cup   1   l  20
 ldcn
 sroa        180
l1375
l1373
l1368
i 9880
 ujp       l1365
l1376
 loda  0       6
 ldoa         40
 equa
 ldoa        180
 ldoa         40
 equa
 and
 fjp       l1377
 mst           3
i 9890
 ldci         21
 cup   1   l 729
 ujp       l1378
l1377
 loda  0       6
 ldoa         40
 equa
 fjp       l1379
 mst           3
 ldci          9
 cup   1   l 729
i 9900
 ldoa         39
 stra  0       6
 ujp       l1380
l1379
 ldoa        180
 ldoa         40
 equa
 fjp       l1381
 mst           3
 ldci         10
 cup   1   l 729
i 9910
 ldoa         39
 sroa        180
l1381
l1380
 loda  0       6
 ldoa         39
 equa
 ldoa        180
 ldoa         39
 equa
 and
 fjp       l1382
i 9920
 mst           3
 ldci         22
 cup   1   l 729
 ujp       l1383
l1382
 loda  0       6
 indi          2
 ldci          3
 equi
 mst           4
 loda  0       6
i 9930
 ldoa        180
 cup   2   l 357
 and
 fjp       l1384
 mst           3
 ldci          5
 cup   1   l 729
 ujp       l1385
l1384
 mst           5
 ldci        134
i 9940
 cup   1   l  20
 ldcn
 sroa        180
l1385
l1383
l1378
 ujp       l1365
l1386
 loda  0       6
 ldoa         37
 equa
 ldoa        180
 ldoa         37
 equa
i 9950
 and
 fjp       l1387
 mst           3
 ldci         13
 cup   1   l 729
 ujp       l1388
l1387
 mst           5
 ldci        134
 cup   1   l  20
 ldcn
i 9960
 sroa        180
l1388
 ujp       l1365
l1364
 chki  5       7
 ldci          5
 sbi
 xjp       l1389
l1389
 ujp       l1366
 ujp       l1376
 ujp       l1386
l1365
 ujp       l1390
l1363
i 9970
 ldcn
 sroa        180
l1390
 ujp       l1361
l1362
 retp
l1353=        13
l1354=        28
l 900
 ent   1   l1391
 ent   2   l1392
 mst           0
 lods  0       5
 ldc(  7)
 uni
i 9980
 cup   1   l1264
 ldoi          9
 ldci          7
 equi
 fjp       l1393
 ldoa        180
 ldcn
 neqa
 fjp       l1394
 ldoa        180
i 9990
 indi          2
 ldci          3
 leqi
 fjp       l1395
 mst           2
 cup   0   l 806
 ujp       l1396
l1395
 mst           2
 cup   0   l 850
l1396
l1394
 lda   0       6
i10000
 lao         180
 mov           5
 ldoi         10
 stri  0      11
 lodi  0      11
 ldci         14
 equi
 fjp       l1397
 mst           3
 ldoa        180
i10010
 ldoa         40
 cup   2   l 357
 not
 fjp       l1398
 mst           2
 ldci         58
 ldoa        180
 cup   2   l 794
l1398
l1397
 mst           4
 cup   0   l  25
i10020
 mst           0
 lods  0       5
 cup   1   l1264
 ldoa        180
 ldcn
 neqa
 fjp       l1399
 ldoa        180
 indi          2
 ldci          3
i10030
 leqi
 fjp       l1400
 mst           2
 cup   0   l 806
 ujp       l1401
l1400
 mst           2
 cup   0   l 850
l1401
l1399
 loda  0       6
 ldcn
 neqa
i10040
 ldoa        180
 ldcn
 neqa
 and
 fjp       l1402
 lodi  0      11
 ldci         14
 equi
 fjp       l1403
 ldoa        180
i10050
 indi          2
 ldci          3
 equi
 fjp       l1404
 mst           3
 loda  0       6
 ldoa        180
 inda          3
 cup   2   l 357
 fjp       l1405
i10060
 mst           2
 ldci         11
 cup   1   l 729
 ujp       l1406
l1405
 mst           4
 ldci        129
 cup   1   l  20
 ldcn
 sroa        180
l1406
 ujp       l1407
l1404
i10070
 mst           4
 ldci        130
 cup   1   l  20
 ldcn
 sroa        180
l1407
 ujp       l1408
l1403
 loda  0       6
 ldoa        180
 neqa
 fjp       l1409
i10080
 loda  0       6
 ldoa         40
 equa
 fjp       l1410
 mst           2
 ldci          9
 cup   1   l 729
 ldoa         39
 stra  0       6
 ujp       l1411
l1410
i10090
 ldoa        180
 ldoa         40
 equa
 fjp       l1412
 mst           2
 ldci         10
 cup   1   l 729
 ldoa         39
 sroa        180
l1412
l1411
l1409
 mst           3
i10100
 loda  0       6
 ldoa        180
 cup   2   l 357
 fjp       l1413
 loda  0       6
 indi          1
 stri  0      13
 loda  0       6
 indi          2
 ordi
i10110
 ujp       l1414
l1416
 loda  0       6
 ldoa         39
 equa
 fjp       l1417
 ldcc 'r'
 strc  0      12
 ujp       l1418
l1417
 loda  0       6
 ldoa         37
i10120
 equa
 fjp       l1419
 ldcc 'b'
 strc  0      12
 ujp       l1420
l1419
 loda  0       6
 ldoa         38
 equa
 fjp       l1421
 ldcc 'c'
i10130
 strc  0      12
 ujp       l1422
l1421
 ldcc 'i'
 strc  0      12
l1422
l1420
l1418
 ujp       l1415
l1423
 lodi  0      11
 ordi
 ldc(  8  9 10 11)
 inn
 fjp       l1424
i10140
 mst           4
 ldci        131
 cup   1   l  20
l1424
 ldcc 'a'
 strc  0      12
 ujp       l1415
l1425
 lodi  0      11
 ordi
 ldc(  8 11)
 inn
i10150
 fjp       l1426
 mst           4
 ldci        132
 cup   1   l  20
l1426
 ldcc 's'
 strc  0      12
 ujp       l1415
l1427
 mst           3
 loda  0       6
 cup   1   l 386
i10160
 not
 fjp       l1428
 mst           4
 ldci        134
 cup   1   l  20
l1428
 ldcc 'm'
 strc  0      12
 ujp       l1415
l1429
 mst           4
 ldci        134
i10170
 cup   1   l  20
 ldcc 'm'
 strc  0      12
 ujp       l1415
l1430
 mst           4
 ldci        133
 cup   1   l  20
 ldcc 'f'
 strc  0      12
 ujp       l1415
l1414
i10180
 chki  0       6
 ldci          0
 sbi
 xjp       l1431
l1431
 ujp       l1416
 ujc
 ujp       l1423
 ujp       l1425
 ujp       l1427
 ujp       l1429
i10190
 ujp       l1430
l1415
 lodi  0      11
 ordi
 ujp       l1432
l1434
 mst           2
 ldci         53
 lodc  0      12
 ordc
 lodi  0      13
 cup   3   l 748
i10200
 ujp       l1433
l1435
 mst           2
 ldci         52
 lodc  0      12
 ordc
 lodi  0      13
 cup   3   l 748
 ujp       l1433
l1436
 mst           2
 ldci         49
i10210
 lodc  0      12
 ordc
 lodi  0      13
 cup   3   l 748
 ujp       l1433
l1437
 mst           2
 ldci         48
 lodc  0      12
 ordc
 lodi  0      13
i10220
 cup   3   l 748
 ujp       l1433
l1438
 mst           2
 ldci         55
 lodc  0      12
 ordc
 lodi  0      13
 cup   3   l 748
 ujp       l1433
l1439
 mst           2
i10230
 ldci         47
 lodc  0      12
 ordc
 lodi  0      13
 cup   3   l 748
 ujp       l1433
l1432
 chki  8      13
 ldci          8
 sbi
 xjp       l1440
l1440
i10240
 ujp       l1434
 ujp       l1435
 ujp       l1437
 ujp       l1436
 ujp       l1438
 ujp       l1439
l1433
 ujp       l1441
l1413
 mst           4
 ldci        129
 cup   1   l  20
l1441
l1408
l1402
i10250
 ldoa         37
 sroa        180
 ldci          2
 sroi        181
l1393
 retp
l1391=        14
l1392=        42
l1442
 ent   1   l1443
 ent   2   l1444
 mst           1
 lods  1       5
 ldc( 17)
i10260
 uni
 loda  0       5
 cup   2   l 901
 ldoi          9
 ldci         17
 equi
 fjp       l1445
 ldoa        180
 ldcn
 neqa
i10270
 fjp       l1446
 ldoi        182
 ldci          0
 neqi
 ldoa        180
 indi          2
 ldci          3
 grti
 ior
 fjp       l1447
i10280
 mst           2
 cup   0   l 850
l1447
l1446
 lda   0       6
 lao         180
 mov           5
 mst           4
 cup   0   l  25
 mst           1
 lods  1       5
 cup   1   l 900
i10290
 ldoa        180
 ldcn
 neqa
 fjp       l1448
 ldoa        180
 indi          2
 ldci          3
 leqi
 fjp       l1449
 mst           2
i10300
 cup   0   l 806
 ujp       l1450
l1449
 mst           2
 cup   0   l 850
l1450
l1448
 loda  0       6
 ldcn
 neqa
 ldoa        180
 ldcn
 neqa
i10310
 and
 fjp       l1451
 mst           3
 ldoa         39
 loda  0       6
 cup   2   l 357
 ldoa        180
 ldoa         40
 equa
 and
i10320
 fjp       l1452
 mst           2
 ldci         10
 cup   1   l 729
 ldoa         39
 sroa        180
l1452
 mst           3
 loda  0       6
 ldoa        180
 cup   2   l 357
i10330
 fjp       l1453
 loda  0       6
 indi          2
 ordi
 ujp       l1454
l1456
 ldob         34
 fjp       l1457
 mst           2
 loda  0       6
 cup   1   l 887
l1457
i10340
 mst           2
 lda   0       6
 cup   1   l 836
 ujp       l1455
l1458
 ldob         34
 fjp       l1459
 mst           2
 ldci         45
 ldci          0
 ldci      32767
i10350
 ldoa         36
 cup   4   l 802
l1459
 mst           2
 lda   0       6
 cup   1   l 836
 ujp       l1455
l1460
 mst           2
 lda   0       6
 cup   1   l 836
 ujp       l1455
l1461
i10360
 mst           2
 ldci         40
 loda  0       6
 indi          1
 cup   2   l 733
 ujp       l1455
l1462
 mst           4
 ldci        146
 cup   1   l  20
 ujp       l1455
l1454
i10370
 chki  0       6
 ldci          0
 sbi
 xjp       l1463
l1463
 ujp       l1456
 ujp       l1456
 ujp       l1458
 ujp       l1460
 ujp       l1461
 ujp       l1461
i10380
 ujp       l1462
l1455
 ujp       l1464
l1453
 mst           4
 ldci        129
 cup   1   l  20
l1464
l1451
 ujp       l1465
l1445
 mst           4
 ldci         51
 cup   1   l  20
l1465
 retp
l1443=        11
l1444=        24
l1466
i10390
 ent   1   l1467
 ent   2   l1468
 ldoi          9
 ldci          1
 equi
 fjp       l1469
 ldcb          0
 strb  0       6
 ldoi         52
 stri  0       8
l1470
i10400
 lao          54
 lodi  0       8
 ixa           5
 indi          2
 ldci          0
 neqi
 fjp       l1471
 lodi  0       8
 ldci          1
 sbi
i10410
 stri  0       8
 ujp       l1470
l1471
 lodi  0       8
 stri  0       7
l1472
 lao          54
 lodi  0       8
 ixa           5
 inda          1
 stra  0       5
l1473
 loda  0       5
i10420
 ldcn
 neqa
 lodb  0       6
 not
 and
 fjp       l1474
 loda  0       5
 stra  0       9
 loda  0       9
 indi          3
i10430
 ldoi         12
 equi
 fjp       l1475
 ldcb          1
 strb  0       6
 lodi  0       8
 lodi  0       7
 equi
 fjp       l1476
 mst           2
i10440
 ldci         57
 loda  0       9
 indi          2
 cup   2   l 879
 ujp       l1477
l1476
 mst           4
 ldci        399
 cup   1   l  20
l1477
 ujp       l1478
l1475
 loda  0       9
i10450
 inda          0
 stra  0       5
l1478
 ujp       l1473
l1474
 lodi  0       8
 ldci          1
 sbi
 stri  0       8
 lodb  0       6
 lodi  0       8
 ldci          0
i10460
 equi
 ior
 fjp       l1472
 lodb  0       6
 not
 fjp       l1479
 mst           4
 ldci        167
 cup   1   l  20
l1479
 mst           4
i10470
 cup   0   l  25
 ujp       l1480
l1469
 mst           4
 ldci         15
 cup   1   l  20
l1480
 retp
l1467=        10
l1468=        11
l1481
 ent   1   l1482
 ent   2   l1483
l1484
l1485
 mst           2
 lods  1       5
i10480
 ldc( 13 39)
 uni
 cup   1   l 898
 ldoi          9
 ordi
 ldos        186
 inn
 not
 fjp       l1485
 ldoi          9
i10490
 ldci         13
 neqi
 strb  3       9
 lodb  3       9
 not
 fjp       l1486
 mst           4
 cup   0   l  25
l1486
 lodb  3       9
 fjp       l1484
i10500
 ldoi          9
 ldci         39
 equi
 fjp       l1487
 mst           4
 cup   0   l  25
 ujp       l1488
l1487
 mst           4
 ldci         13
 cup   1   l  20
l1488
i10510
 retp
l1482=         5
l1483=         8
l1489
 ent   1   l1490
 ent   2   l1491
 mst           1
 lods  1       5
 ldc( 46)
 uni
 cup   1   l 900
 mst           4
 lda   0       6
i10520
 cup   1   l 309
 mst           2
 lodi  0       6
 cup   1   l 873
 ldoi          9
 ldci         46
 equi
 fjp       l1492
 mst           4
 cup   0   l  25
i10530
 ujp       l1493
l1492
 mst           4
 ldci         52
 cup   1   l  20
l1493
 mst           2
 lods  1       5
 ldc( 40)
 uni
 cup   1   l 898
 ldoi          9
i10540
 ldci         40
 equi
 fjp       l1494
 mst           4
 lda   0       5
 cup   1   l 309
 mst           2
 ldci         57
 lodi  0       5
 cup   2   l 879
i10550
 mst           2
 lodi  0       6
 cup   1   l 894
 mst           4
 cup   0   l  25
 mst           2
 lods  1       5
 cup   1   l 898
 mst           2
 lodi  0       5
i10560
 cup   1   l 894
 ujp       l1495
l1494
 mst           2
 lodi  0       6
 cup   1   l 894
l1495
 retp
l1490=         7
l1491=        17
l1496
 ent   1   l1498
 ent   2   l1499
 mst           1
 lods  1       5
i10570
 ldc( 12 16 42)
 uni
 cup   1   l 900
 mst           2
 cup   0   l 806
 mst           4
 lda   0      16
 cup   1   l 309
 ldoa        180
 stra  0       6
i10580
 loda  0       6
 ldcn
 neqa
 fjp       l1500
 loda  0       6
 indi          2
 ldci          0
 neqi
 loda  0       6
 ldoa         39
i10590
 equa
 ior
 fjp       l1501
 mst           4
 ldci        144
 cup   1   l  20
 ldcn
 stra  0       6
 ujp       l1502
l1501
 mst           3
i10600
 loda  0       6
 ldoa         40
 cup   2   l 357
 not
 fjp       l1503
 mst           2
 ldci         58
 loda  0       6
 cup   2   l 794
l1503
l1502
l1500
 mst           2
i10610
 ldci         57
 lodi  0      16
 cup   2   l 879
 ldoi          9
 ldci         42
 equi
 fjp       l1504
 mst           4
 cup   0   l  25
 ujp       l1505
l1504
i10620
 mst           4
 ldci          8
 cup   1   l  20
l1505
 ldcn
 stra  0      10
 mst           4
 lda   0      17
 cup   1   l 309
l1506
 ldcn
 stra  0       7
i10630
 mst           4
 lda   0      15
 cup   1   l 309
 ldoi          9
 ordi
 ldc( 13 39)
 inn
 not
 fjp       l1507
l1508
 mst           3
i10640
 lods  1       5
 ldc( 12 16)
 uni
 lda   0       5
 lda   0      11
 cup   3   l 320
 loda  0       6
 ldcn
 neqa
 fjp       l1509
i10650
 mst           3
 loda  0       6
 loda  0       5
 cup   2   l 357
 fjp       l1510
 loda  0      10
 stra  0       9
 ldcn
 stra  0       8
l1511
 loda  0       9
i10660
 ldcn
 neqa
 fjp       l1512
 loda  0       9
 stra  0      18
 loda  0      18
 indi          2
 lodi  0      12
 leqi
 fjp       l1513
i10670
 loda  0      18
 indi          2
 lodi  0      12
 equi
 fjp       l1514
 mst           4
 ldci        156
 cup   1   l  20
l1514
 ujp       l1497
l1513
 loda  0       9
i10680
 stra  0       8
 loda  0      18
 inda          0
 stra  0       9
 ujp       l1511
l1512
l1497
 lda   0       7
 ldci          3
 csp         new
 loda  0       7
 stra  0      18
i10690
 loda  0      18
 loda  0       9
 stoa
 loda  0      18
 inca          2
 lodi  0      12
 stoi
 loda  0      18
 inca          1
 lodi  0      15
i10700
 stoi
 loda  0       8
 ldcn
 equa
 fjp       l1515
 loda  0       7
 stra  0      10
 ujp       l1516
l1515
 loda  0       8
 loda  0       7
i10710
 stoa
l1516
 ujp       l1517
l1510
 mst           4
 ldci        147
 cup   1   l  20
l1517
l1509
 ldoi          9
 ldci         12
 neqi
 strb  3       9
 lodb  3       9
i10720
 not
 fjp       l1518
 mst           4
 cup   0   l  25
l1518
 lodb  3       9
 fjp       l1508
 ldoi          9
 ldci         16
 equi
 fjp       l1519
i10730
 mst           4
 cup   0   l  25
 ujp       l1520
l1519
 mst           4
 ldci          5
 cup   1   l  20
l1520
 mst           2
 lodi  0      15
 cup   1   l 894
l1521
 mst           2
i10740
 lods  1       5
 ldc( 13)
 uni
 cup   1   l 898
 ldoi          9
 ordi
 ldos        186
 inn
 not
 fjp       l1521
i10750
 loda  0       7
 ldcn
 neqa
 fjp       l1522
 mst           2
 ldci         57
 lodi  0      17
 cup   2   l 879
l1522
l1507
 ldoi          9
 ldci         13
i10760
 neqi
 strb  3       9
 lodb  3       9
 not
 fjp       l1523
 mst           4
 cup   0   l  25
l1523
 lodb  3       9
 fjp       l1506
 mst           2
i10770
 lodi  0      16
 cup   1   l 894
 loda  0      10
 ldcn
 neqa
 fjp       l1524
 loda  0      10
 indi          2
 stri  0      13
 loda  0      10
i10780
 stra  0       9
 ldcn
 stra  0      10
l1525
 loda  0       9
 inda          0
 stra  0       8
 loda  0       9
 loda  0      10
 stoa
 loda  0       9
i10790
 stra  0      10
 loda  0       8
 stra  0       9
 loda  0       9
 ldcn
 equa
 fjp       l1525
 loda  0      10
 indi          2
 stri  0      14
i10800
 lodi  0      13
 lodi  0      14
 sbi
 ldci       1000
 lesi
 fjp       l1526
 mst           2
 ldci         45
 lodi  0      14
 lodi  0      13
i10810
 ldoa         40
 cup   4   l 802
 mst           2
 ldci         51
 ldci          1
 lodi  0      14
 cup   3   l 748
 mst           2
 ldci         21
 cup   1   l 729
i10820
 mst           4
 lda   0      16
 cup   1   l 309
 mst           2
 ldci         44
 lodi  0      16
 cup   2   l 879
 mst           2
 lodi  0      16
 cup   1   l 894
l1527
i10830
 loda  0      10
 stra  0      18
l1528
 loda  0      18
 indi          2
 lodi  0      14
 grti
 fjp       l1529
 mst           2
 ldci         60
 cup   1   l 729
i10840
 lodi  0      14
 ldci          1
 adi
 stri  0      14
 ujp       l1528
l1529
 mst           2
 ldci         57
 loda  0      18
 indi          1
 cup   2   l 879
i10850
 loda  0      18
 inda          0
 stra  0      10
 lodi  0      14
 ldci          1
 adi
 stri  0      14
 loda  0      10
 ldcn
 equa
i10860
 fjp       l1527
 mst           2
 lodi  0      17
 cup   1   l 894
 ujp       l1530
l1526
 mst           4
 ldci        157
 cup   1   l  20
l1530
l1524
 ldoi          9
 ldci         39
i10870
 equi
 fjp       l1531
 mst           4
 cup   0   l  25
 ujp       l1532
l1531
 mst           4
 ldci         13
 cup   1   l  20
l1532
 retp
l1498=        19
l1499=        47
l1533
 ent   1   l1534
i10880
 ent   2   l1535
 mst           4
 lda   0       5
 cup   1   l 309
 mst           2
 lodi  0       5
 cup   1   l 894
l1536
 mst           2
 lods  1       5
 ldc( 13 41)
i10890
 uni
 cup   1   l 898
 ldoi          9
 ordi
 ldos        186
 inn
 fjp       l1537
 mst           4
 ldci         14
 cup   1   l  20
l1537
i10900
 ldoi          9
 ordi
 ldos        186
 inn
 not
 fjp       l1536
l1538
 ldoi          9
 ldci         13
 equi
 fjp       l1539
i10910
 mst           4
 cup   0   l  25
l1540
 mst           2
 lods  1       5
 ldc( 13 41)
 uni
 cup   1   l 898
 ldoi          9
 ordi
 ldos        186
i10920
 inn
 fjp       l1541
 mst           4
 ldci         14
 cup   1   l  20
l1541
 ldoi          9
 ordi
 ldos        186
 inn
 not
i10930
 fjp       l1540
 ujp       l1538
l1539
 ldoi          9
 ldci         41
 equi
 fjp       l1542
 mst           4
 cup   0   l  25
 mst           1
 lods  1       5
i10940
 cup   1   l 900
 mst           2
 lodi  0       5
 cup   1   l 873
 ujp       l1543
l1542
 mst           4
 ldci         53
 cup   1   l  20
l1543
 retp
l1534=         6
l1535=        14
l1544
 ent   1   l1545
i10950
 ent   2   l1546
 mst           4
 lda   0       6
 cup   1   l 309
 mst           2
 lodi  0       6
 cup   1   l 894
 mst           1
 lods  1       5
 ldc( 43)
i10960
 uni
 cup   1   l 900
 mst           4
 lda   0       5
 cup   1   l 309
 mst           2
 lodi  0       5
 cup   1   l 873
 ldoi          9
 ldci         43
i10970
 equi
 fjp       l1547
 mst           4
 cup   0   l  25
 ujp       l1548
l1547
 mst           4
 ldci         54
 cup   1   l  20
l1548
 mst           2
 lods  1       5
i10980
 cup   1   l 898
 mst           2
 ldci         57
 lodi  0       6
 cup   2   l 879
 mst           2
 lodi  0       5
 cup   1   l 894
 retp
l1545=         7
l1546=        15
l1549
 ent   1   l1550
i10990
 ent   2   l1551
 ldoi         27
 stri  0      13
 ldcn
 stra  0       5
 ldci          1
 stri  0       6
 ldci          0
 stri  0       7
 ldoi         51
i11000
 stri  0       8
 ldci          0
 stri  0       9
 ldoi          9
 ldci          0
 equi
 fjp       l1552
 mst           4
 ldc(  2)
 lda   1       6
i11010
 cup   2   l 158
 loda  1       6
 stra  0      14
 loda  0      14
 inda         10
 stra  0       5
 ldci          1
 stri  0       6
 loda  0      14
 indi         13
i11020
 ldci          0
 equi
 fjp       l1553
 ldci          0
 stri  0       7
 loda  0      14
 indi         14
 stri  0       8
 loda  0      14
 indi         15
i11030
 stri  0       9
 ujp       l1554
l1553
 mst           4
 ldci        155
 cup   1   l  20
 ldcn
 stra  0       5
l1554
 loda  0       5
 ldcn
 neqa
i11040
 fjp       l1555
 loda  0       5
 indi          2
 ldci          1
 grti
 mst           3
 ldoa         39
 loda  0       5
 cup   2   l 357
 ior
i11050
 fjp       l1556
 mst           4
 ldci        143
 cup   1   l  20
 ldcn
 stra  0       5
l1556
l1555
 mst           4
 cup   0   l  25
 ujp       l1557
l1552
 mst           4
i11060
 ldci          2
 cup   1   l  20
 mst           3
 lods  1       5
 ldc( 17 43 44 45)
 uni
 cup   1   l 313
l1557
 ldoi          9
 ldci         17
 equi
i11070
 fjp       l1558
 mst           4
 cup   0   l  25
 mst           1
 lods  1       5
 ldc( 43 44 45)
 uni
 cup   1   l 900
 ldoa        180
 ldcn
i11080
 neqa
 fjp       l1559
 ldoa        180
 indi          2
 ldci          0
 neqi
 fjp       l1560
 mst           4
 ldci        144
 cup   1   l  20
i11090
 ujp       l1561
l1560
 mst           3
 loda  0       5
 ldoa        180
 cup   2   l 357
 fjp       l1562
 mst           2
 cup   0   l 806
 mst           2
 lda   0       5
i11100
 cup   1   l 836
 ujp       l1563
l1562
 mst           4
 ldci        145
 cup   1   l  20
l1563
l1561
l1559
 ujp       l1564
l1558
 mst           4
 ldci         51
 cup   1   l  20
 mst           3
i11110
 lods  1       5
 ldc( 43 44 45)
 uni
 cup   1   l 313
l1564
 ldoi          9
 ordi
 ldc( 44 45)
 inn
 fjp       l1565
 ldoi          9
i11120
 stri  0      10
 mst           4
 cup   0   l  25
 mst           1
 lods  1       5
 ldc( 43)
 uni
 cup   1   l 900
 ldoa        180
 ldcn
i11130
 neqa
 fjp       l1566
 ldoa        180
 indi          2
 ldci          0
 neqi
 fjp       l1567
 mst           4
 ldci        144
 cup   1   l  20
i11140
 ujp       l1568
l1567
 mst           3
 loda  0       5
 ldoa        180
 cup   2   l 357
 fjp       l1569
 mst           2
 cup   0   l 806
 mst           3
 loda  0       5
i11150
 ldoa         40
 cup   2   l 357
 not
 fjp       l1570
 mst           2
 ldci         58
 ldoa        180
 cup   2   l 794
l1570
 mst           4
 ldoa         40
i11160
 lao          27
 cup   2   l 218
 mst           2
 ldci         56
 ldci          0
 ldoi         27
 ldoa         40
 cup   4   l 802
 mst           4
 lda   0      11
i11170
 cup   1   l 309
 mst           2
 lodi  0      11
 cup   1   l 894
 lao         180
 lda   0       5
 mov           5
 mst           2
 cup   0   l 806
 mst           3
i11180
 ldoa        180
 ldoa         40
 cup   2   l 357
 not
 fjp       l1571
 mst           2
 ldci         58
 ldoa        180
 cup   2   l 794
l1571
 mst           2
i11190
 ldci         54
 ldci          0
 ldoi         27
 ldoa         40
 cup   4   l 802
 ldoi         27
 ldci          1
 adi
 sroi         27
 ldoi         27
i11200
 lodi  2      87
 grti
 fjp       l1572
 ldoi         27
 stri  2      87
l1572
 lodi  0      10
 ldci         44
 equi
 fjp       l1573
 mst           2
i11210
 ldci         52
 ldcc 'i'
 ordc
 ldci          1
 cup   3   l 748
 ujp       l1574
l1573
 mst           2
 ldci         48
 ldcc 'i'
 ordc
i11220
 ldci          1
 cup   3   l 748
l1574
 ujp       l1575
l1569
 mst           4
 ldci        145
 cup   1   l  20
l1575
l1568
l1566
 ujp       l1576
l1565
 mst           4
 ldci         55
 cup   1   l  20
i11230
 mst           3
 lods  1       5
 ldc( 43)
 uni
 cup   1   l 313
l1576
 mst           4
 lda   0      12
 cup   1   l 309
 mst           2
 ldci         33
i11240
 lodi  0      12
 cup   2   l 879
 ldoi          9
 ldci         43
 equi
 fjp       l1577
 mst           4
 cup   0   l  25
 ujp       l1578
l1577
 mst           4
i11250
 ldci         54
 cup   1   l  20
l1578
 mst           2
 lods  1       5
 cup   1   l 898
 lao         180
 lda   0       5
 mov           5
 mst           2
 cup   0   l 806
i11260
 lodi  0      10
 ldci         44
 equi
 fjp       l1579
 mst           2
 ldci         34
 ldci          1
 ldoa        180
 cup   3   l 798
 ujp       l1580
l1579
i11270
 mst           2
 ldci         31
 ldci          1
 ldoa        180
 cup   3   l 798
l1580
 mst           2
 lda   0       5
 cup   1   l 836
 mst           2
 ldci         57
i11280
 lodi  0      11
 cup   2   l 879
 mst           2
 lodi  0      12
 cup   1   l 894
 lodi  0      13
 sroi         27
 retp
l1550=        15
l1551=        65
l1581
 ent   1   l1582
 ent   2   l1583
i11290
 ldci          0
 stri  0       6
 ldoi         27
 stri  0       7
l1584
 ldoi          9
 ldci          0
 equi
 fjp       l1585
 mst           4
 ldc(  2  3)
i11300
 lda   0       5
 cup   2   l 158
 mst           4
 cup   0   l  25
 ujp       l1586
l1585
 mst           4
 ldci          2
 cup   1   l  20
 ldoa         46
 stra  0       5
l1586
i11310
 mst           1
 lods  1       5
 ldc( 12 43)
 uni
 loda  0       5
 cup   2   l 901
 ldoa        180
 ldcn
 neqa
 fjp       l1587
i11320
 ldoa        180
 indi          2
 ldci          5
 equi
 fjp       l1588
 ldoi         52
 ldci         20
 lesi
 fjp       l1589
 ldoi         52
i11330
 ldci          1
 adi
 sroi         52
 lodi  0       6
 ldci          1
 adi
 stri  0       6
 lao          54
 ldoi         52
 ixa           5
i11340
 stra  0       8
 loda  0       8
 ldoa        180
 inda          3
 stoa
 loda  0       8
 inca          1
 ldcn
 stoa
 ldoi        182
i11350
 ldci          0
 equi
 fjp       l1590
 lao          54
 ldoi         52
 ixa           5
 stra  0       8
 loda  0       8
 inca          2
 ldci          1
i11360
 stoi
 loda  0       8
 inca          3
 ldoi        183
 stoi
 loda  0       8
 inca          4
 ldoi        184
 stoi
 ujp       l1591
l1590
i11370
 mst           2
 cup   0   l 850
 mst           4
 ldoa         36
 lao          27
 cup   2   l 218
 mst           2
 ldci         56
 ldci          0
 ldoi         27
i11380
 ldoa         36
 cup   4   l 802
 lao          54
 ldoi         52
 ixa           5
 stra  0       8
 loda  0       8
 inca          2
 ldci          2
 stoi
i11390
 loda  0       8
 inca          3
 ldoi         27
 stoi
 ldoi         27
 ldci          1
 adi
 sroi         27
 ldoi         27
 lodi  2      87
i11400
 grti
 fjp       l1592
 ldoi         27
 stri  2      87
l1592
l1591
 ujp       l1593
l1589
 mst           4
 ldci        250
 cup   1   l  20
l1593
 ujp       l1594
l1588
 mst           4
i11410
 ldci        140
 cup   1   l  20
l1594
l1587
 ldoi          9
 ldci         12
 neqi
 strb  3       9
 lodb  3       9
 not
 fjp       l1595
 mst           4
i11420
 cup   0   l  25
l1595
 lodb  3       9
 fjp       l1584
 ldoi          9
 ldci         43
 equi
 fjp       l1596
 mst           4
 cup   0   l  25
 ujp       l1597
l1596
i11430
 mst           4
 ldci         54
 cup   1   l  20
l1597
 mst           2
 lods  1       5
 cup   1   l 898
 ldoi         52
 lodi  0       6
 sbi
 sroi         52
i11440
 lodi  0       7
 sroi         27
 retp
l1582=         9
l1583=        22
l 898
 ent   1   l1598
 ent   2   l1599
 ldoi          9
 ldci          1
 equi
 fjp       l1600
 lao          54
i11450
 ldoi         51
 ixa           5
 inda          1
 stra  0       7
l1601
 loda  0       7
 ldcn
 neqa
 fjp       l1602
 loda  0       7
 stra  0       8
i11460
 loda  0       8
 indi          3
 ldoi         12
 equi
 fjp       l1603
 loda  0       8
 indb          1
 fjp       l1604
 mst           3
 ldci        165
i11470
 cup   1   l  20
l1604
 mst           1
 loda  0       8
 indi          2
 cup   1   l 894
 loda  0       8
 inca          1
 ldcb          1
 stob
 ujp       l 899
i11480
 ujp       l1605
l1603
 loda  0       8
 inda          0
 stra  0       7
l1605
 ujp       l1601
l1602
 mst           3
 ldci        167
 cup   1   l  20
l 899
 mst           3
 cup   0   l  25
i11490
 ldoi          9
 ldci         16
 equi
 fjp       l1606
 mst           3
 cup   0   l  25
 ujp       l1607
l1606
 mst           3
 ldci          5
 cup   1   l  20
l1607
l1600
i11500
 ldoi          9
 ordi
 lods  0       5
 ldc(  0)
 uni
 inn
 not
 fjp       l1608
 mst           3
 ldci          6
i11510
 cup   1   l  20
 mst           2
 lods  0       5
 cup   1   l 313
l1608
 ldoi          9
 ordi
 ldos        186
 ldc(  0)
 uni
 inn
i11520
 fjp       l1609
 ldoi          9
 ordi
 ujp       l1610
l1612
 mst           3
 ldc(  2  3  4  5)
 lda   0       6
 cup   2   l 158
 mst           3
 cup   0   l  25
i11530
 loda  0       6
 indi         12
 ldci          4
 equi
 fjp       l1613
 mst           0
 lods  0       5
 loda  0       6
 cup   2   l 966
 ujp       l1614
l1613
i11540
 mst           0
 loda  0       6
 cup   1   l1442
l1614
 ujp       l1611
l1615
 mst           3
 cup   0   l  25
 mst           0
 cup   0   l1481
 ujp       l1611
l1616
 mst           3
i11550
 cup   0   l  25
 mst           0
 cup   0   l1466
 ujp       l1611
l1617
 mst           3
 cup   0   l  25
 mst           0
 cup   0   l1489
 ujp       l1611
l1618
 mst           3
i11560
 cup   0   l  25
 mst           0
 cup   0   l1496
 ujp       l1611
l1619
 mst           3
 cup   0   l  25
 mst           0
 cup   0   l1544
 ujp       l1611
l1620
 mst           3
i11570
 cup   0   l  25
 mst           0
 cup   0   l1533
 ujp       l1611
l1621
 mst           3
 cup   0   l  25
 mst           0
 cup   0   l1549
 ujp       l1611
l1622
 mst           3
i11580
 cup   0   l  25
 mst           0
 cup   0   l1581
 ujp       l1611
l1610
 chki  0      38
 ldci          0
 sbi
 xjp       l1623
l1623
 ujp       l1612
 ujc
i11590
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
i11600
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
i11610
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujc
 ujp       l1615
i11620
 ujp       l1617
 ujp       l1618
 ujp       l1620
 ujp       l1619
 ujp       l1621
 ujp       l1622
 ujp       l1616
l1611
 ldoi          9
 ordi
 ldc( 13 39 40 41)
i11630
 inn
 not
 fjp       l1624
 mst           3
 ldci          6
 cup   1   l  20
 mst           2
 lods  0       5
 cup   1   l 313
l1624
l1609
 retp
l1598=         9
l1599=        18
l 720
i11640
 ent   1   l1625
 ent   2   l1626
 loda  1       7
 ldcn
 neqa
 fjp       l1627
 loda  1       7
 indi         15
 stri  0      82
 ujp       l1628
l1627
i11650
 mst           2
 lda   0      82
 cup   1   l 309
l1628
 ldci          0
 stri  0      80
 ldci          5
 stri  0      84
 ldci          5
 stri  0      83
 mst           0
i11660
 lodi  0      82
 cup   1   l 894
 mst           2
 lda   0      81
 cup   1   l 309
 mst           2
 lda   0      85
 cup   1   l 309
 mst           0
 ldci         32
i11670
 ldci          1
 lodi  0      81
 cup   3   l 883
 mst           0
 ldci         32
 ldci          2
 lodi  0      85
 cup   3   l 883
 loda  1       7
 ldcn
i11680
 neqa
 fjp       l1629
 ldci          5
 stri  0      86
 loda  1       7
 inda         11
 stra  0      88
l1630
 loda  0      88
 ldcn
 neqa
i11690
 fjp       l1631
 loda  0      88
 stra  0      90
 mst           2
 ldoa         41
 lda   0      86
 cup   2   l 218
 loda  0      90
 indi         12
 ldci          2
i11700
 equi
 fjp       l1632
 loda  0      90
 inda         10
 ldcn
 neqa
 fjp       l1633
 loda  0      90
 inda         10
 indi          2
i11710
 ldci          3
 grti
 fjp       l1634
 loda  0      90
 indi         13
 ldci          0
 equi
 fjp       l1635
 mst           0
 ldci         50
i11720
 ldci          0
 loda  0      90
 indi         15
 cup   3   l 748
 mst           0
 ldci         54
 ldci          0
 lodi  0      86
 ldoa         36
 cup   4   l 802
i11730
 mst           0
 ldci         40
 loda  0      90
 inda         10
 indi          1
 cup   2   l 733
l1635
 lodi  0      86
 ldci          1
 adi
 stri  0      86
i11740
 ujp       l1636
l1634
 lodi  0      86
 loda  0      90
 inda         10
 indi          1
 adi
 stri  0      86
l1636
l1633
l1632
 loda  0      88
 inda         11
 stra  0      88
i11750
 ujp       l1630
l1631
l1629
 ldoi         27
 stri  0      87
l1637
l1638
 mst           0
 lods  0       5
 ldc( 13 39)
 uni
 cup   1   l 898
 ldoi          9
 ordi
i11760
 ldos        186
 inn
 not
 fjp       l1638
 ldoi          9
 ldci         13
 neqi
 strb  1       9
 lodb  1       9
 not
i11770
 fjp       l1639
 mst           2
 cup   0   l  25
l1639
 lodb  1       9
 fjp       l1637
 ldoi          9
 ldci         39
 equi
 fjp       l1640
 mst           2
i11780
 cup   0   l  25
 ujp       l1641
l1640
 mst           2
 ldci         13
 cup   1   l  20
l1641
 lao          54
 ldoi         52
 ixa           5
 inda          1
 stra  0      89
l1642
i11790
 loda  0      89
 ldcn
 neqa
 fjp       l1643
 loda  0      89
 stra  0      90
 loda  0      90
 indb          1
 not
 fjp       l1644
i11800
 mst           2
 ldci        168
 cup   1   l  20
 lda   2       6
 csp         wln
 lca' label          '
 ldci          7
 ldci          7
 lda   2       6
 csp         wrs
i11810
 loda  0      90
 indi          3
 ldci         10
 lda   2       6
 csp         wri
 lda   2       6
 csp         wln
 ldcc ' '
 ldoi         25
 ldci         16
i11820
 adi
 lda   2       6
 csp         wrc
l1644
 loda  0      90
 inda          0
 stra  0      89
 ujp       l1642
l1643
 loda  1       7
 ldcn
 neqa
i11830
 fjp       l1645
 loda  1       7
 inda         10
 ldcn
 equa
 fjp       l1646
 mst           0
 ldci         42
 ldcc 'p'
 ordc
i11840
 cup   2   l 733
 ujp       l1647
l1646
 mst           0
 ldci         42
 loda  1       7
 inda         10
 cup   2   l 794
l1647
 mst           2
 ldoa         41
 lda   0      87
i11850
 cup   2   l 218
 ldob         30
 fjp       l1648
 ldcc 'l'
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      81
 ldci          4
 lda   2       8
i11860
 csp         wri
 ldcc '='
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      87
 ldci         10
 lda   2       8
 csp         wri
 lda   2       8
i11870
 csp         wln
 ldcc 'l'
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      85
 ldci          4
 lda   2       8
 csp         wri
 ldcc '='
i11880
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      83
 ldci         10
 lda   2       8
 csp         wri
 lda   2       8
 csp         wln
l1648
 ujp       l1649
l1645
i11890
 mst           0
 ldci         42
 ldcc 'p'
 ordc
 cup   2   l 733
 mst           2
 ldoa         41
 lda   0      87
 cup   2   l 218
 ldob         30
i11900
 fjp       l1650
 ldcc 'l'
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      81
 ldci          4
 lda   2       8
 csp         wri
 ldcc '='
i11910
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      87
 ldci         10
 lda   2       8
 csp         wri
 lda   2       8
 csp         wln
 ldcc 'l'
i11920
 ldci          1
 lda   2       8
 csp         wrc
 lodi  0      85
 ldci          4
 lda   2       8
 csp         wri
 ldcc '='
 ldci          1
 lda   2       8
i11930
 csp         wrc
 lodi  0      83
 ldci         10
 lda   2       8
 csp         wri
 lda   2       8
 csp         wln
 ldcc 'q'
 ldci          1
 lda   2       8
i11940
 csp         wrc
 lda   2       8
 csp         wln
l1650
 ldci          0
 sroi         26
 mst           0
 ldci         41
 ldci          0
 cup   2   l 733
 mst           0
i11950
 ldci         46
 ldci          0
 lodi  0      82
 cup   3   l 883
 mst           0
 ldci         29
 cup   1   l 729
 ldob         30
 fjp       l1651
 ldcc 'q'
i11960
 ldci          1
 lda   2       8
 csp         wrc
 lda   2       8
 csp         wln
l1651
 lda   0       7
 lao          14
 mov           8
l1652
 ldoa         49
 ldcn
i11970
 neqa
 fjp       l1653
 ldoa         49
 stra  0      90
 loda  0      90
 lca'input           '
 equm          8
 loda  0      90
 lca'output          '
 equm          8
i11980
 ior
 loda  0      90
 lca'prd             '
 equm          8
 ior
 loda  0      90
 lca'prr             '
 equm          8
 ior
 not
i11990
 fjp       l1654
 lao          14
 loda  0      90
 mov           8
 mst           2
 ldc(  2)
 lda   0       6
 cup   2   l 158
 loda  0       6
 inda         10
i12000
 ldcn
 neqa
 fjp       l1655
 loda  0       6
 inda         10
 indi          2
 ldci          6
 neqi
 fjp       l1656
 lda   2       6
i12010
 csp         wln
 ldcc ' '
 ldci          8
 lda   2       6
 csp         wrc
 lca'undeclared      '
 ldci         11
 ldci         11
 lda   2       6
 csp         wrs
i12020
 lca'external        '
 ldci          9
 ldci          9
 lda   2       6
 csp         wrs
 lca'file            '
 ldci          4
 ldci          4
 lda   2       6
 csp         wrs
i12030
 ldoa         49
 ldci          8
 ldci          8
 lda   2       6
 csp         wrs
 lda   2       6
 csp         wln
 ldcc ' '
 ldoi         25
 ldci         16
i12040
 adi
 lda   2       6
 csp         wrc
l1656
l1655
l1654
 ldoa         49
 inda          8
 sroa         49
 ujp       l1652
l1653
 lao          14
 lda   0       7
 mov           8
i12050
 ldob         29
 fjp       l1657
 lda   2       6
 csp         wln
 mst           2
 ldcb          1
 cup   1   l 221
l1657
l1649
 retp
l1625=        91
l1626=        51
l 312
 ent   1   l1658
 ent   2   l1659
i12060
 ldcb          1
 srob         33
l1660
 ldoi          9
 ldci         18
 equi
 fjp       l1661
 mst           1
 cup   0   l  25
 mst           0
 cup   0   l 543
l1661
i12070
 ldoi          9
 ldci         19
 equi
 fjp       l1662
 mst           1
 cup   0   l  25
 mst           0
 cup   0   l 558
l1662
 ldoi          9
 ldci         20
i12080
 equi
 fjp       l1663
 mst           1
 cup   0   l  25
 mst           0
 cup   0   l 569
l1663
 ldoi          9
 ldci         21
 equi
 fjp       l1664
i12090
 mst           1
 cup   0   l  25
 mst           0
 cup   0   l 589
l1664
l1665
 ldoi          9
 ordi
 ldc( 22 24)
 inn
 fjp       l1666
 ldoi          9
i12100
 stri  0       8
 mst           1
 cup   0   l  25
 mst           0
 lodi  0       8
 cup   1   l 608
 ujp       l1665
l1666
 ldoi          9
 ldci         31
 neqi
i12110
 fjp       l1667
 mst           1
 ldci         18
 cup   1   l  20
 mst           0
 lods  0       5
 cup   1   l 313
l1667
 ldoi          9
 ordi
 ldos        186
i12120
 inn
 lao           5
 eof
 ior
 fjp       l1660
 ldcb          0
 srob         33
 ldoi          9
 ldci         31
 equi
i12130
 fjp       l1668
 mst           1
 cup   0   l  25
 ujp       l1669
l1668
 mst           1
 ldci         17
 cup   1   l  20
l1669
l1670
 mst           0
 lods  0       5
 ldc( 33)
i12140
 uni
 cup   1   l 720
 ldoi          9
 lodi  0       6
 neqi
 fjp       l1671
 mst           1
 ldci          6
 cup   1   l  20
 mst           0
i12150
 lods  0       5
 cup   1   l 313
l1671
 ldoi          9
 lodi  0       6
 equi
 ldoi          9
 ordi
 ldos        189
 inn
 ior
i12160
 lao           5
 eof
 ior
 fjp       l1670
 retp
l1658=        10
l1659=        15
l1672
 ent   1   l1673
 ent   2   l1674
 ldoi          9
 ldci         23
 equi
i12170
 fjp       l1675
 mst           1
 cup   0   l  25
 ldoi          9
 ldci          0
 neqi
 fjp       l1676
 mst           1
 ldci          2
 cup   1   l  20
l1676
i12180
 mst           1
 cup   0   l  25
 ldoi          9
 ordi
 ldc(  8 13)
 inn
 not
 fjp       l1677
 mst           1
 ldci         14
i12190
 cup   1   l  20
l1677
 ldoi          9
 ldci          8
 equi
 fjp       l1678
l1679
 mst           1
 cup   0   l  25
 ldoi          9
 ldci          0
 equi
i12200
 fjp       l1680
 lda   0       6
 ldci          9
 csp         new
 loda  0       6
 stra  0       7
 loda  0       7
 lao          14
 mov           8
 loda  0       7
i12210
 inca          8
 ldoa         49
 stoa
 loda  0       6
 sroa         49
 mst           1
 cup   0   l  25
 ldoi          9
 ordi
 ldc(  9 12)
i12220
 inn
 not
 fjp       l1681
 mst           1
 ldci         20
 cup   1   l  20
l1681
 ujp       l1682
l1680
 mst           1
 ldci          2
 cup   1   l  20
l1682
i12230
 ldoi          9
 ldci         12
 neqi
 fjp       l1679
 ldoi          9
 ldci          9
 neqi
 fjp       l1683
 mst           1
 ldci          4
i12240
 cup   1   l  20
l1683
 mst           1
 cup   0   l  25
l1678
 ldoi          9
 ldci         13
 neqi
 fjp       l1684
 mst           1
 ldci         14
 cup   1   l  20
i12250
 ujp       l1685
l1684
 mst           1
 cup   0   l  25
l1685
l1675
l1686
 mst           1
 lods  0       5
 ldci         14
 ldcn
 cup   3   l 312
 ldoi          9
 ldci         14
i12260
 neqi
 fjp       l1687
 mst           1
 ldci         21
 cup   1   l  20
l1687
 ldoi          9
 ldci         14
 equi
 lao           5
 eof
i12270
 ior
 fjp       l1686
 ldob         31
 fjp       l1688
 lda   1       6
 csp         wln
l1688
 ldoi        159
 ldci          0
 neqi
 fjp       l1689
i12280
 ldcb          0
 srob         31
 mst           1
 cup   0   l   3
l1689
 retp
l1673=         8
l1674=        17
l1690
 ent   1   l1691
 ent   2   l1692
 lao         936
 ldci          1
 deci          1
i12290
 ixa           8
 lca'false           '
 mov           8
 lao         936
 ldci          2
 deci          1
 ixa           8
 lca'true            '
 mov           8
 lao         936
i12300
 ldci          3
 deci          1
 ixa           8
 lca'input           '
 mov           8
 lao         936
 ldci          4
 deci          1
 ixa           8
 lca'output          '
i12310
 mov           8
 lao         936
 ldci          5
 deci          1
 ixa           8
 lca'get             '
 mov           8
 lao         936
 ldci          6
 deci          1
i12320
 ixa           8
 lca'put             '
 mov           8
 lao         936
 ldci          7
 deci          1
 ixa           8
 lca'reset           '
 mov           8
 lao         936
i12330
 ldci          8
 deci          1
 ixa           8
 lca'rewrite         '
 mov           8
 lao         936
 ldci          9
 deci          1
 ixa           8
 lca'read            '
i12340
 mov           8
 lao         936
 ldci         10
 deci          1
 ixa           8
 lca'write           '
 mov           8
 lao         936
 ldci         11
 deci          1
i12350
 ixa           8
 lca'pack            '
 mov           8
 lao         936
 ldci         12
 deci          1
 ixa           8
 lca'unpack          '
 mov           8
 lao         936
i12360
 ldci         13
 deci          1
 ixa           8
 lca'new             '
 mov           8
 lao         936
 ldci         14
 deci          1
 ixa           8
 lca'release         '
i12370
 mov           8
 lao         936
 ldci         15
 deci          1
 ixa           8
 lca'readln          '
 mov           8
 lao         936
 ldci         16
 deci          1
i12380
 ixa           8
 lca'writeln         '
 mov           8
 lao         936
 ldci         17
 deci          1
 ixa           8
 lca'abs             '
 mov           8
 lao         936
i12390
 ldci         18
 deci          1
 ixa           8
 lca'sqr             '
 mov           8
 lao         936
 ldci         19
 deci          1
 ixa           8
 lca'trunc           '
i12400
 mov           8
 lao         936
 ldci         20
 deci          1
 ixa           8
 lca'odd             '
 mov           8
 lao         936
 ldci         21
 deci          1
i12410
 ixa           8
 lca'ord             '
 mov           8
 lao         936
 ldci         22
 deci          1
 ixa           8
 lca'chr             '
 mov           8
 lao         936
i12420
 ldci         23
 deci          1
 ixa           8
 lca'pred            '
 mov           8
 lao         936
 ldci         24
 deci          1
 ixa           8
 lca'succ            '
i12430
 mov           8
 lao         936
 ldci         25
 deci          1
 ixa           8
 lca'eof             '
 mov           8
 lao         936
 ldci         26
 deci          1
i12440
 ixa           8
 lca'eoln            '
 mov           8
 lao         936
 ldci         27
 deci          1
 ixa           8
 lca'sin             '
 mov           8
 lao         936
i12450
 ldci         28
 deci          1
 ixa           8
 lca'cos             '
 mov           8
 lao         936
 ldci         29
 deci          1
 ixa           8
 lca'exp             '
i12460
 mov           8
 lao         936
 ldci         30
 deci          1
 ixa           8
 lca'sqrt            '
 mov           8
 lao         936
 ldci         31
 deci          1
i12470
 ixa           8
 lca'ln              '
 mov           8
 lao         936
 ldci         32
 deci          1
 ixa           8
 lca'arctan          '
 mov           8
 lao         936
i12480
 ldci         33
 deci          1
 ixa           8
 lca'prd             '
 mov           8
 lao         936
 ldci         34
 deci          1
 ixa           8
 lca'prr             '
i12490
 mov           8
 lao         936
 ldci         35
 deci          1
 ixa           8
 lca'mark            '
 mov           8
 retp
l1691=         5
l1692=         7
l1693
 ent   1   l1694
 ent   2   l1695
i12500
 lao          40
 ldci          4
 csp         new
 ldoa         40
 stra  0       5
 loda  0       5
 inca          1
 ldci          1
 stoi
 loda  0       5
i12510
 inca          2
 ldci          0
 stoi
 loda  0       5
 inca          3
 ldci          0
 stoi
 lao          39
 ldci          4
 csp         new
i12520
 ldoa         39
 stra  0       5
 loda  0       5
 inca          1
 ldci          1
 stoi
 loda  0       5
 inca          2
 ldci          0
 stoi
i12530
 loda  0       5
 inca          3
 ldci          0
 stoi
 lao          38
 ldci          4
 csp         new
 ldoa         38
 stra  0       5
 loda  0       5
i12540
 inca          1
 ldci          1
 stoi
 loda  0       5
 inca          2
 ldci          0
 stoi
 loda  0       5
 inca          3
 ldci          0
i12550
 stoi
 lao          37
 ldci          5
 csp         new
 ldoa         37
 stra  0       5
 loda  0       5
 inca          1
 ldci          1
 stoi
i12560
 loda  0       5
 inca          2
 ldci          0
 stoi
 loda  0       5
 inca          3
 ldci          1
 stoi
 lao          36
 ldci          4
i12570
 csp         new
 ldoa         36
 stra  0       5
 loda  0       5
 inca          3
 ldcn
 stoa
 loda  0       5
 inca          1
 ldci          1
i12580
 stoi
 loda  0       5
 inca          2
 ldci          2
 stoi
 lao          41
 ldci          4
 csp         new
 ldoa         41
 stra  0       5
i12590
 loda  0       5
 inca          1
 ldci          1
 stoi
 loda  0       5
 inca          2
 ldci          0
 stoi
 loda  0       5
 inca          3
i12600
 ldci          0
 stoi
 lao          35
 ldci          4
 csp         new
 ldoa         35
 stra  0       5
 loda  0       5
 inca          3
 ldoa         38
i12610
 stoa
 loda  0       5
 inca          1
 ldci          1
 stoi
 loda  0       5
 inca          2
 ldci          6
 stoi
 retp
l1694=         6
l1695=         7
l1696
i12620
 ent   1   l1697
 ent   2   l1698
 lda   0       6
 ldci         13
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'integer         '
 mov           8
i12630
 loda  0       8
 inca         10
 ldoa         40
 stoa
 loda  0       8
 inca         12
 ldci          0
 stoi
 mst           1
 loda  0       6
i12640
 cup   1   l 136
 lda   0       6
 ldci         13
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'real            '
 mov           8
 loda  0       8
i12650
 inca         10
 ldoa         39
 stoa
 loda  0       8
 inca         12
 ldci          0
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
i12660
 lda   0       6
 ldci         13
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'char            '
 mov           8
 loda  0       8
 inca         10
i12670
 ldoa         38
 stoa
 loda  0       8
 inca         12
 ldci          0
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 lda   0       6
i12680
 ldci         13
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'boolean         '
 mov           8
 loda  0       8
 inca         10
 ldoa         37
i12690
 stoa
 loda  0       8
 inca         12
 ldci          0
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 ldcn
 stra  0       5
i12700
 ldci          1
 stri  0       7
 ldci          2
 stri  0       8
l1699
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l1700
 lda   0       6
 ldci         15
i12710
 csp         new
 loda  0       6
 stra  0       9
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
 ixa           8
 mov           8
 loda  0       9
i12720
 inca         10
 ldoa         37
 stoa
 loda  0       9
 inca         11
 loda  0       5
 stoa
 loda  0       9
 inca         14
 lodi  0       7
i12730
 ldci          1
 sbi
 stoi
 loda  0       9
 inca         12
 ldci          1
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
i12740
 loda  0       6
 stra  0       5
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l1699
l1700
 ldoa         37
 inca          4
 loda  0       6
 stoa
i12750
 lda   0       6
 ldci         15
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'nil             '
 mov           8
 loda  0       8
 inca         10
i12760
 ldoa         36
 stoa
 loda  0       8
 inca         11
 ldcn
 stoa
 loda  0       8
 inca         14
 ldci          0
 stoi
i12770
 loda  0       8
 inca         12
 ldci          1
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 ldci          3
 stri  0       7
 ldci          4
i12780
 stri  0       8
l1701
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l1702
 lda   0       6
 ldci         16
 csp         new
 loda  0       6
 stra  0       9
i12790
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
 ixa           8
 mov           8
 loda  0       9
 inca         10
 ldoa         35
 stoa
i12800
 loda  0       9
 inca         12
 ldci          2
 stoi
 loda  0       9
 inca         13
 ldci          0
 stoi
 loda  0       9
 inca         11
i12810
 ldcn
 stoa
 loda  0       9
 inca         14
 ldci          1
 stoi
 loda  0       9
 inca         15
 ldci          5
 lodi  0       7
i12820
 ldci          3
 sbi
 ldci          1
 mpi
 adi
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 lodi  0       7
i12830
 inci          1
 stri  0       7
 ujp       l1701
l1702
 ldci         33
 stri  0       7
 ldci         34
 stri  0       8
l1703
 lodi  0       7
 lodi  0       8
 leqi
i12840
 fjp       l1704
 lda   0       6
 ldci         16
 csp         new
 loda  0       6
 stra  0       9
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
i12850
 ixa           8
 mov           8
 loda  0       9
 inca         10
 ldoa         35
 stoa
 loda  0       9
 inca         12
 ldci          2
 stoi
i12860
 loda  0       9
 inca         13
 ldci          0
 stoi
 loda  0       9
 inca         11
 ldcn
 stoa
 loda  0       9
 inca         14
i12870
 ldci          1
 stoi
 loda  0       9
 inca         15
 ldci          5
 lodi  0       7
 ldci         31
 sbi
 ldci          1
 mpi
i12880
 adi
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l1703
l1704
 ldci          5
i12890
 stri  0       7
 ldci         16
 stri  0       8
l1705
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l1706
 lda   0       6
 ldci         15
 csp         new
i12900
 loda  0       6
 stra  0       9
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
 ixa           8
 mov           8
 loda  0       9
 inca         10
i12910
 ldcn
 stoa
 loda  0       9
 inca         11
 ldcn
 stoa
 loda  0       9
 inca         14
 lodi  0       7
 ldci          4
i12920
 sbi
 stoi
 loda  0       9
 inca         12
 ldci          4
 stoi
 loda  0       9
 inca         13
 ldci          0
 stoi
i12930
 mst           1
 loda  0       6
 cup   1   l 136
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l1705
l1706
 lda   0       6
 ldci         15
 csp         new
i12940
 loda  0       6
 stra  0       8
 loda  0       8
 lao         936
 ldci         35
 deci          1
 ixa           8
 mov           8
 loda  0       8
 inca         10
i12950
 ldcn
 stoa
 loda  0       8
 inca         11
 ldcn
 stoa
 loda  0       8
 inca         14
 ldci         13
 stoi
i12960
 loda  0       8
 inca         12
 ldci          4
 stoi
 loda  0       8
 inca         13
 ldci          0
 stoi
 mst           1
 loda  0       6
i12970
 cup   1   l 136
 ldci         17
 stri  0       7
 ldci         26
 stri  0       8
l1707
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l1708
 lda   0       6
i12980
 ldci         15
 csp         new
 loda  0       6
 stra  0       9
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
 ixa           8
 mov           8
i12990
 loda  0       9
 inca         10
 ldcn
 stoa
 loda  0       9
 inca         11
 ldcn
 stoa
 loda  0       9
 inca         14
i13000
 lodi  0       7
 ldci         16
 sbi
 stoi
 loda  0       9
 inca         12
 ldci          5
 stoi
 loda  0       9
 inca         13
i13010
 ldci          0
 stoi
 mst           1
 loda  0       6
 cup   1   l 136
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l1707
l1708
 lda   0       6
i13020
 ldci         16
 csp         new
 loda  0       6
 stra  0       8
 loda  0       8
 lca'                '
 mov           8
 loda  0       8
 inca         10
 ldoa         39
i13030
 stoa
 loda  0       8
 inca         12
 ldci          2
 stoi
 loda  0       8
 inca         13
 ldci          0
 stoi
 loda  0       8
i13040
 inca         11
 ldcn
 stoa
 loda  0       8
 inca         14
 ldci          1
 stoi
 loda  0       8
 inca         15
 ldci          0
i13050
 stoi
 ldci         27
 stri  0       7
 ldci         32
 stri  0       8
l1709
 lodi  0       7
 lodi  0       8
 leqi
 fjp       l1710
 lda   0       5
i13060
 ldci         19
 csp         new
 loda  0       5
 stra  0       9
 loda  0       9
 lao         936
 lodi  0       7
 deci          1
 ixa           8
 mov           8
i13070
 loda  0       9
 inca         10
 ldoa         39
 stoa
 loda  0       9
 inca         11
 loda  0       6
 stoa
 loda  0       9
 inca         18
i13080
 ldcb          0
 stob
 loda  0       9
 inca         17
 ldcb          1
 stob
 loda  0       9
 inca         14
 ldci          0
 stoi
i13090
 loda  0       9
 inca         15
 lodi  0       7
 ldci         12
 sbi
 stoi
 loda  0       9
 inca         12
 ldci          5
 stoi
i13100
 loda  0       9
 inca         13
 ldci          1
 stoi
 loda  0       9
 inca         16
 ldci          0
 stoi
 mst           1
 loda  0       5
i13110
 cup   1   l 136
 lodi  0       7
 inci          1
 stri  0       7
 ujp       l1709
l1710
 retp
l1697=        10
l1698=        19
l1711
 ent   1   l1712
 ent   2   l1713
 lao          48
 ldci         13
i13120
 csp         new
 ldoa         48
 stra  0       5
 loda  0       5
 lca'                '
 mov           8
 loda  0       5
 inca         10
 ldcn
 stoa
i13130
 loda  0       5
 inca         12
 ldci          0
 stoi
 lao          47
 ldci         15
 csp         new
 ldoa         47
 stra  0       5
 loda  0       5
i13140
 lca'                '
 mov           8
 loda  0       5
 inca         10
 ldcn
 stoa
 loda  0       5
 inca         11
 ldcn
 stoa
i13150
 loda  0       5
 inca         14
 ldci          0
 stoi
 loda  0       5
 inca         12
 ldci          1
 stoi
 lao          46
 ldci         16
i13160
 csp         new
 ldoa         46
 stra  0       5
 loda  0       5
 lca'                '
 mov           8
 loda  0       5
 inca         10
 ldcn
 stoa
i13170
 loda  0       5
 inca         13
 ldci          0
 stoi
 loda  0       5
 inca         11
 ldcn
 stoa
 loda  0       5
 inca         14
i13180
 ldci          0
 stoi
 loda  0       5
 inca         15
 ldci          0
 stoi
 loda  0       5
 inca         12
 ldci          2
 stoi
i13190
 lao          45
 ldci         14
 csp         new
 ldoa         45
 stra  0       5
 loda  0       5
 lca'                '
 mov           8
 loda  0       5
 inca         10
i13200
 ldcn
 stoa
 loda  0       5
 inca         11
 ldcn
 stoa
 loda  0       5
 inca         13
 ldci          0
 stoi
i13210
 loda  0       5
 inca         12
 ldci          3
 stoi
 lao          44
 ldci         19
 csp         new
 ldoa         44
 stra  0       5
 loda  0       5
i13220
 lca'                '
 mov           8
 loda  0       5
 inca         10
 ldcn
 stoa
 loda  0       5
 inca         18
 ldcb          0
 stob
i13230
 loda  0       5
 inca         11
 ldcn
 stoa
 loda  0       5
 inca         17
 ldcb          0
 stob
 loda  0       5
 inca         14
i13240
 ldci          0
 stoi
 mst           1
 loda  0       5
 inca         15
 cup   1   l 309
 loda  0       5
 inca         12
 ldci          4
 stoi
i13250
 loda  0       5
 inca         13
 ldci          1
 stoi
 loda  0       5
 inca         16
 ldci          0
 stoi
 lao          43
 ldci         19
i13260
 csp         new
 ldoa         43
 stra  0       5
 loda  0       5
 lca'                '
 mov           8
 loda  0       5
 inca         10
 ldcn
 stoa
i13270
 loda  0       5
 inca         11
 ldcn
 stoa
 loda  0       5
 inca         18
 ldcb          0
 stob
 loda  0       5
 inca         17
i13280
 ldcb          0
 stob
 loda  0       5
 inca         14
 ldci          0
 stoi
 mst           1
 loda  0       5
 inca         15
 cup   1   l 309
i13290
 loda  0       5
 inca         12
 ldci          5
 stoi
 loda  0       5
 inca         13
 ldci          1
 stoi
 loda  0       5
 inca         16
i13300
 ldci          0
 stoi
 retp
l1712=         6
l1713=         9
l1714
 ent   1   l1715
 ent   2   l1716
 ldcn
 sroa         42
 ldcb          0
 srob         29
 ldcb          1
i13310
 srob         31
 ldcb          1
 srob         30
 ldcb          1
 srob         34
 ldcb          1
 srob         33
 ldcb          1
 srob         32
 ldci          0
i13320
 sroi        159
 ldci          0
 sroi       1766
 ldci          8
 sroi         22
 ldcn
 sroa         49
 ldci          5
 ldci          4
 ldci          1
i13330
 mpi
 adi
 sroi         27
 ldci          3
 sroi         26
 ldcb          1
 srob         24
 ldci          0
 sroi         28
 ldcc ' '
i13340
 sroc         23
 ldci          0
 sroi         25
 ldcn
 sroa         50
 ldci      32767
 ldci         10
 dvi
 sroi       1765
 ldci         16
i13350
 ldci          1
 sbi
 sroi       1764
 retp
l1715=         5
l1716=         8
l1717
 ent   1   l1718
 ent   2   l1719
 ldc(  0  1  2  3  6)
 sros        192
 ldc(  8)
 ldos        192
i13360
 uni
 sros        191
 ldc( 15 25 26 27 28 29)
 ldos        191
 uni
 sros        190
 ldc( 25 27 28 29)
 sros        185
 ldc( 18 19 20 21 22 24 31)
 sros        189
i13370
 ldc( 10 14 15)
 sros        188
 ldc(  0  1  2  3  4  8 10)
 sros        187
 ldc( 31 32 33 34 35 36 37 38)
 sros        186
 retp
l1718=         5
l1719=         7
l1721
 ent   1   l1722
 ent   2   l1723
 lao         321
i13380
 ldci          1
 deci          1
 ixa           8
 lca'if              '
 mov           8
 lao         321
 ldci          2
 deci          1
 ixa           8
 lca'do              '
i13390
 mov           8
 lao         321
 ldci          3
 deci          1
 ixa           8
 lca'of              '
 mov           8
 lao         321
 ldci          4
 deci          1
i13400
 ixa           8
 lca'to              '
 mov           8
 lao         321
 ldci          5
 deci          1
 ixa           8
 lca'in              '
 mov           8
 lao         321
i13410
 ldci          6
 deci          1
 ixa           8
 lca'or              '
 mov           8
 lao         321
 ldci          7
 deci          1
 ixa           8
 lca'end             '
i13420
 mov           8
 lao         321
 ldci          8
 deci          1
 ixa           8
 lca'for             '
 mov           8
 lao         321
 ldci          9
 deci          1
i13430
 ixa           8
 lca'var             '
 mov           8
 lao         321
 ldci         10
 deci          1
 ixa           8
 lca'div             '
 mov           8
 lao         321
i13440
 ldci         11
 deci          1
 ixa           8
 lca'mod             '
 mov           8
 lao         321
 ldci         12
 deci          1
 ixa           8
 lca'set             '
i13450
 mov           8
 lao         321
 ldci         13
 deci          1
 ixa           8
 lca'and             '
 mov           8
 lao         321
 ldci         14
 deci          1
i13460
 ixa           8
 lca'not             '
 mov           8
 lao         321
 ldci         15
 deci          1
 ixa           8
 lca'then            '
 mov           8
 lao         321
i13470
 ldci         16
 deci          1
 ixa           8
 lca'else            '
 mov           8
 lao         321
 ldci         17
 deci          1
 ixa           8
 lca'with            '
i13480
 mov           8
 lao         321
 ldci         18
 deci          1
 ixa           8
 lca'goto            '
 mov           8
 lao         321
 ldci         19
 deci          1
i13490
 ixa           8
 lca'case            '
 mov           8
 lao         321
 ldci         20
 deci          1
 ixa           8
 lca'type            '
 mov           8
 lao         321
i13500
 ldci         21
 deci          1
 ixa           8
 lca'file            '
 mov           8
 lao         321
 ldci         22
 deci          1
 ixa           8
 lca'begin           '
i13510
 mov           8
 lao         321
 ldci         23
 deci          1
 ixa           8
 lca'until           '
 mov           8
 lao         321
 ldci         24
 deci          1
i13520
 ixa           8
 lca'while           '
 mov           8
 lao         321
 ldci         25
 deci          1
 ixa           8
 lca'array           '
 mov           8
 lao         321
i13530
 ldci         26
 deci          1
 ixa           8
 lca'const           '
 mov           8
 lao         321
 ldci         27
 deci          1
 ixa           8
 lca'label           '
i13540
 mov           8
 lao         321
 ldci         28
 deci          1
 ixa           8
 lca'repeat          '
 mov           8
 lao         321
 ldci         29
 deci          1
i13550
 ixa           8
 lca'record          '
 mov           8
 lao         321
 ldci         30
 deci          1
 ixa           8
 lca'downto          '
 mov           8
 lao         321
i13560
 ldci         31
 deci          1
 ixa           8
 lca'packed          '
 mov           8
 lao         321
 ldci         32
 deci          1
 ixa           8
 lca'forward         '
i13570
 mov           8
 lao         321
 ldci         33
 deci          1
 ixa           8
 lca'program         '
 mov           8
 lao         321
 ldci         34
 deci          1
i13580
 ixa           8
 lca'function        '
 mov           8
 lao         321
 ldci         35
 deci          1
 ixa           8
 lca'procedur        '
 mov           8
 lao         601
i13590
 ldci          1
 deci          1
 ixa           1
 ldci          1
 stoi
 lao         601
 ldci          2
 deci          1
 ixa           1
 ldci          1
i13600
 stoi
 lao         601
 ldci          3
 deci          1
 ixa           1
 ldci          7
 stoi
 lao         601
 ldci          4
 deci          1
i13610
 ixa           1
 ldci         15
 stoi
 lao         601
 ldci          5
 deci          1
 ixa           1
 ldci         22
 stoi
 lao         601
i13620
 ldci          6
 deci          1
 ixa           1
 ldci         28
 stoi
 lao         601
 ldci          7
 deci          1
 ixa           1
 ldci         32
i13630
 stoi
 lao         601
 ldci          8
 deci          1
 ixa           1
 ldci         34
 stoi
 lao         601
 ldci          9
 deci          1
i13640
 ixa           1
 ldci         36
 stoi
 retp
l1722=         5
l1723=         7
l1724
 ent   1   l1725
 ent   2   l1726
 lao         610
 ldci          1
 deci          1
 ixa           1
i13650
 ldci         32
 stoi
 lao         610
 ldci          2
 deci          1
 ixa           1
 ldci         43
 stoi
 lao         610
 ldci          3
i13660
 deci          1
 ixa           1
 ldci         42
 stoi
 lao         610
 ldci          4
 deci          1
 ixa           1
 ldci         44
 stoi
i13670
 lao         610
 ldci          5
 deci          1
 ixa           1
 ldci          7
 stoi
 lao         610
 ldci          6
 deci          1
 ixa           1
i13680
 ldci          6
 stoi
 lao         610
 ldci          7
 deci          1
 ixa           1
 ldci         39
 stoi
 lao         610
 ldci          8
i13690
 deci          1
 ixa           1
 ldci         36
 stoi
 lao         610
 ldci          9
 deci          1
 ixa           1
 ldci         21
 stoi
i13700
 lao         610
 ldci         10
 deci          1
 ixa           1
 ldci          5
 stoi
 lao         610
 ldci         11
 deci          1
 ixa           1
i13710
 ldci          5
 stoi
 lao         610
 ldci         12
 deci          1
 ixa           1
 ldci         25
 stoi
 lao         610
 ldci         13
i13720
 deci          1
 ixa           1
 ldci          5
 stoi
 lao         610
 ldci         14
 deci          1
 ixa           1
 ldci          4
 stoi
i13730
 lao         610
 ldci         15
 deci          1
 ixa           1
 ldci         46
 stoi
 lao         610
 ldci         16
 deci          1
 ixa           1
i13740
 ldci         40
 stoi
 lao         610
 ldci         17
 deci          1
 ixa           1
 ldci         37
 stoi
 lao         610
 ldci         18
i13750
 deci          1
 ixa           1
 ldci         38
 stoi
 lao         610
 ldci         19
 deci          1
 ixa           1
 ldci         33
 stoi
i13760
 lao         610
 ldci         20
 deci          1
 ixa           1
 ldci         20
 stoi
 lao         610
 ldci         21
 deci          1
 ixa           1
i13770
 ldci         29
 stoi
 lao         610
 ldci         22
 deci          1
 ixa           1
 ldci         31
 stoi
 lao         610
 ldci         23
i13780
 deci          1
 ixa           1
 ldci         41
 stoi
 lao         610
 ldci         24
 deci          1
 ixa           1
 ldci         35
 stoi
i13790
 lao         610
 ldci         25
 deci          1
 ixa           1
 ldci         27
 stoi
 lao         610
 ldci         26
 deci          1
 ixa           1
i13800
 ldci         19
 stoi
 lao         610
 ldci         27
 deci          1
 ixa           1
 ldci         18
 stoi
 lao         610
 ldci         28
i13810
 deci          1
 ixa           1
 ldci         34
 stoi
 lao         610
 ldci         29
 deci          1
 ixa           1
 ldci         28
 stoi
i13820
 lao         610
 ldci         30
 deci          1
 ixa           1
 ldci         45
 stoi
 lao         610
 ldci         31
 deci          1
 ixa           1
i13830
 ldci         26
 stoi
 lao         610
 ldci         32
 deci          1
 ixa           1
 ldci         30
 stoi
 lao         610
 ldci         33
i13840
 deci          1
 ixa           1
 ldci         23
 stoi
 lao         610
 ldci         34
 deci          1
 ixa           1
 ldci         22
 stoi
i13850
 lao         610
 ldci         35
 deci          1
 ixa           1
 ldci         24
 stoi
 lao         645
 ldcc '+'
 ordc
 ixa           1
i13860
 ldci          6
 stoi
 lao         645
 ldcc '-'
 ordc
 ixa           1
 ldci          6
 stoi
 lao         645
 ldcc '*'
i13870
 ordc
 ixa           1
 ldci          5
 stoi
 lao         645
 ldcc '/'
 ordc
 ixa           1
 ldci          5
 stoi
i13880
 lao         645
 ldcc '('
 ordc
 ixa           1
 ldci          8
 stoi
 lao         645
 ldcc ')'
 ordc
 ixa           1
i13890
 ldci          9
 stoi
 lao         645
 ldcc '$'
 ordc
 ixa           1
 ldci         47
 stoi
 lao         645
 ldcc '='
i13900
 ordc
 ixa           1
 ldci          7
 stoi
 lao         645
 ldcc ' '
 ordc
 ixa           1
 ldci         47
 stoi
i13910
 lao         645
 ldcc ','
 ordc
 ixa           1
 ldci         12
 stoi
 lao         645
 ldcc '.'
 ordc
 ixa           1
i13920
 ldci         14
 stoi
 lao         645
 ldcc '''
 ordc
 ixa           1
 ldci         47
 stoi
 lao         645
 ldcc '['
i13930
 ordc
 ixa           1
 ldci         10
 stoi
 lao         645
 ldcc ']'
 ordc
 ixa           1
 ldci         11
 stoi
i13940
 lao         645
 ldcc ':'
 ordc
 ixa           1
 ldci         16
 stoi
 lao         645
 ldcc '^'
 ordc
 ixa           1
i13950
 ldci         15
 stoi
 lao         645
 ldcc '<'
 ordc
 ixa           1
 ldci          7
 stoi
 lao         645
 ldcc '>'
i13960
 ordc
 ixa           1
 ldci          7
 stoi
 lao         645
 ldcc ';'
 ordc
 ixa           1
 ldci         13
 stoi
i13970
 retp
l1725=         5
l1726=         7
l1727
 ent   1   l1728
 ent   2   l1729
 ldci          1
 stri  0       5
 ldci         35
 stri  0       6
l1730
 lodi  0       5
 lodi  0       6
 leqi
i13980
 fjp       l1731
 lao         773
 lodi  0       5
 deci          1
 ixa           1
 ldci         15
 stoi
 lodi  0       5
 inci          1
 stri  0       5
i13990
 ujp       l1730
l1731
 lao         773
 ldci          5
 deci          1
 ixa           1
 ldci         14
 stoi
 lao         773
 ldci         10
 deci          1
i14000
 ixa           1
 ldci          3
 stoi
 lao         773
 ldci         11
 deci          1
 ixa           1
 ldci          4
 stoi
 lao         773
i14010
 ldci          6
 deci          1
 ixa           1
 ldci          7
 stoi
 lao         773
 ldci         13
 deci          1
 ixa           1
 ldci          2
i14020
 stoi
 ldci          0
 stri  0       5
 ldci        127
 stri  0       6
l1732
 lodi  0       5
 lodi  0       6
 leqi
 fjp       l1733
 lao         808
i14030
 lodi  0       5
 chr
 ordc
 ixa           1
 ldci         15
 stoi
 lodi  0       5
 inci          1
 stri  0       5
 ujp       l1732
l1733
i14040
 lao         808
 ldcc '+'
 ordc
 ixa           1
 ldci          5
 stoi
 lao         808
 ldcc '-'
 ordc
 ixa           1
i14050
 ldci          6
 stoi
 lao         808
 ldcc '*'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         808
 ldcc '/'
i14060
 ordc
 ixa           1
 ldci          1
 stoi
 lao         808
 ldcc '='
 ordc
 ixa           1
 ldci         13
 stoi
i14070
 lao         808
 ldcc '<'
 ordc
 ixa           1
 ldci          8
 stoi
 lao         808
 ldcc '>'
 ordc
 ixa           1
i14080
 ldci         11
 stoi
 retp
l1728=         7
l1729=         7
l1734
 ent   1   l1735
 ent   2   l1736
 lao        1460
 ldci          1
 deci          1
 ixa           4
 lca' get            '
i14090
 mov           4
 lao        1460
 ldci          2
 deci          1
 ixa           4
 lca' put            '
 mov           4
 lao        1460
 ldci          3
 deci          1
i14100
 ixa           4
 lca' rdi            '
 mov           4
 lao        1460
 ldci          4
 deci          1
 ixa           4
 lca' rdr            '
 mov           4
 lao        1460
i14110
 ldci          5
 deci          1
 ixa           4
 lca' rdc            '
 mov           4
 lao        1460
 ldci          6
 deci          1
 ixa           4
 lca' wri            '
i14120
 mov           4
 lao        1460
 ldci          7
 deci          1
 ixa           4
 lca' wro            '
 mov           4
 lao        1460
 ldci          8
 deci          1
i14130
 ixa           4
 lca' wrr            '
 mov           4
 lao        1460
 ldci          9
 deci          1
 ixa           4
 lca' wrc            '
 mov           4
 lao        1460
i14140
 ldci         10
 deci          1
 ixa           4
 lca' wrs            '
 mov           4
 lao        1460
 ldci         11
 deci          1
 ixa           4
 lca' pak            '
i14150
 mov           4
 lao        1460
 ldci         12
 deci          1
 ixa           4
 lca' new            '
 mov           4
 lao        1460
 ldci         13
 deci          1
i14160
 ixa           4
 lca' rst            '
 mov           4
 lao        1460
 ldci         14
 deci          1
 ixa           4
 lca' eln            '
 mov           4
 lao        1460
i14170
 ldci         15
 deci          1
 ixa           4
 lca' sin            '
 mov           4
 lao        1460
 ldci         16
 deci          1
 ixa           4
 lca' cos            '
i14180
 mov           4
 lao        1460
 ldci         17
 deci          1
 ixa           4
 lca' exp            '
 mov           4
 lao        1460
 ldci         18
 deci          1
i14190
 ixa           4
 lca' sqt            '
 mov           4
 lao        1460
 ldci         19
 deci          1
 ixa           4
 lca' log            '
 mov           4
 lao        1460
i14200
 ldci         20
 deci          1
 ixa           4
 lca' atn            '
 mov           4
 lao        1460
 ldci         21
 deci          1
 ixa           4
 lca' rln            '
i14210
 mov           4
 lao        1460
 ldci         22
 deci          1
 ixa           4
 lca' wln            '
 mov           4
 lao        1460
 ldci         23
 deci          1
i14220
 ixa           4
 lca' sav            '
 mov           4
 retp
l1735=         5
l1736=         7
l1737
 ent   1   l1738
 ent   2   l1739
 lao        1216
 ldci          0
 ixa           4
 lca' abi            '
i14230
 mov           4
 lao        1216
 ldci          1
 ixa           4
 lca' abr            '
 mov           4
 lao        1216
 ldci          2
 ixa           4
 lca' adi            '
i14240
 mov           4
 lao        1216
 ldci          3
 ixa           4
 lca' adr            '
 mov           4
 lao        1216
 ldci          4
 ixa           4
 lca' and            '
i14250
 mov           4
 lao        1216
 ldci          5
 ixa           4
 lca' dif            '
 mov           4
 lao        1216
 ldci          6
 ixa           4
 lca' dvi            '
i14260
 mov           4
 lao        1216
 ldci          7
 ixa           4
 lca' dvr            '
 mov           4
 lao        1216
 ldci          8
 ixa           4
 lca' eof            '
i14270
 mov           4
 lao        1216
 ldci          9
 ixa           4
 lca' flo            '
 mov           4
 lao        1216
 ldci         10
 ixa           4
 lca' flt            '
i14280
 mov           4
 lao        1216
 ldci         11
 ixa           4
 lca' inn            '
 mov           4
 lao        1216
 ldci         12
 ixa           4
 lca' int            '
i14290
 mov           4
 lao        1216
 ldci         13
 ixa           4
 lca' ior            '
 mov           4
 lao        1216
 ldci         14
 ixa           4
 lca' mod            '
i14300
 mov           4
 lao        1216
 ldci         15
 ixa           4
 lca' mpi            '
 mov           4
 lao        1216
 ldci         16
 ixa           4
 lca' mpr            '
i14310
 mov           4
 lao        1216
 ldci         17
 ixa           4
 lca' ngi            '
 mov           4
 lao        1216
 ldci         18
 ixa           4
 lca' ngr            '
i14320
 mov           4
 lao        1216
 ldci         19
 ixa           4
 lca' not            '
 mov           4
 lao        1216
 ldci         20
 ixa           4
 lca' odd            '
i14330
 mov           4
 lao        1216
 ldci         21
 ixa           4
 lca' sbi            '
 mov           4
 lao        1216
 ldci         22
 ixa           4
 lca' sbr            '
i14340
 mov           4
 lao        1216
 ldci         23
 ixa           4
 lca' sgs            '
 mov           4
 lao        1216
 ldci         24
 ixa           4
 lca' sqi            '
i14350
 mov           4
 lao        1216
 ldci         25
 ixa           4
 lca' sqr            '
 mov           4
 lao        1216
 ldci         26
 ixa           4
 lca' sto            '
i14360
 mov           4
 lao        1216
 ldci         27
 ixa           4
 lca' trc            '
 mov           4
 lao        1216
 ldci         28
 ixa           4
 lca' uni            '
i14370
 mov           4
 lao        1216
 ldci         29
 ixa           4
 lca' stp            '
 mov           4
 lao        1216
 ldci         30
 ixa           4
 lca' csp            '
i14380
 mov           4
 lao        1216
 ldci         31
 ixa           4
 lca' dec            '
 mov           4
 lao        1216
 ldci         32
 ixa           4
 lca' ent            '
i14390
 mov           4
 lao        1216
 ldci         33
 ixa           4
 lca' fjp            '
 mov           4
 lao        1216
 ldci         34
 ixa           4
 lca' inc            '
i14400
 mov           4
 lao        1216
 ldci         35
 ixa           4
 lca' ind            '
 mov           4
 lao        1216
 ldci         36
 ixa           4
 lca' ixa            '
i14410
 mov           4
 lao        1216
 ldci         37
 ixa           4
 lca' lao            '
 mov           4
 lao        1216
 ldci         38
 ixa           4
 lca' lca            '
i14420
 mov           4
 lao        1216
 ldci         39
 ixa           4
 lca' ldo            '
 mov           4
 lao        1216
 ldci         40
 ixa           4
 lca' mov            '
i14430
 mov           4
 lao        1216
 ldci         41
 ixa           4
 lca' mst            '
 mov           4
 lao        1216
 ldci         42
 ixa           4
 lca' ret            '
i14440
 mov           4
 lao        1216
 ldci         43
 ixa           4
 lca' sro            '
 mov           4
 lao        1216
 ldci         44
 ixa           4
 lca' xjp            '
i14450
 mov           4
 lao        1216
 ldci         45
 ixa           4
 lca' chk            '
 mov           4
 lao        1216
 ldci         46
 ixa           4
 lca' cup            '
i14460
 mov           4
 lao        1216
 ldci         47
 ixa           4
 lca' equ            '
 mov           4
 lao        1216
 ldci         48
 ixa           4
 lca' geq            '
i14470
 mov           4
 lao        1216
 ldci         49
 ixa           4
 lca' grt            '
 mov           4
 lao        1216
 ldci         50
 ixa           4
 lca' lda            '
i14480
 mov           4
 lao        1216
 ldci         51
 ixa           4
 lca' ldc            '
 mov           4
 lao        1216
 ldci         52
 ixa           4
 lca' leq            '
i14490
 mov           4
 lao        1216
 ldci         53
 ixa           4
 lca' les            '
 mov           4
 lao        1216
 ldci         54
 ixa           4
 lca' lod            '
i14500
 mov           4
 lao        1216
 ldci         55
 ixa           4
 lca' neq            '
 mov           4
 lao        1216
 ldci         56
 ixa           4
 lca' str            '
i14510
 mov           4
 lao        1216
 ldci         57
 ixa           4
 lca' ujp            '
 mov           4
 lao        1216
 ldci         58
 ixa           4
 lca' ord            '
i14520
 mov           4
 lao        1216
 ldci         59
 ixa           4
 lca' chr            '
 mov           4
 lao        1216
 ldci         60
 ixa           4
 lca' ujc            '
i14530
 mov           4
 retp
l1738=         5
l1739=         7
l1740
 ent   1   l1741
 ent   2   l1742
 ldci          0
 stri  0       5
 ldci        127
 stri  0       6
l1743
 lodi  0       5
 lodi  0       6
i14540
 leqi
 fjp       l1744
 lao         193
 lodi  0       5
 chr
 ordc
 ixa           1
 ldci          3
 stoi
 lodi  0       5
i14550
 inci          1
 stri  0       5
 ujp       l1743
l1744
 lao         193
 ldcc 'a'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14560
 ldcc 'b'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'c'
 ordc
 ixa           1
 ldci          0
i14570
 stoi
 lao         193
 ldcc 'd'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'e'
 ordc
i14580
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'f'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14590
 ldcc 'g'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'h'
 ordc
 ixa           1
 ldci          0
i14600
 stoi
 lao         193
 ldcc 'i'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'j'
 ordc
i14610
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'k'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14620
 ldcc 'l'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'm'
 ordc
 ixa           1
 ldci          0
i14630
 stoi
 lao         193
 ldcc 'n'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'o'
 ordc
i14640
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'p'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14650
 ldcc 'q'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'r'
 ordc
 ixa           1
 ldci          0
i14660
 stoi
 lao         193
 ldcc 's'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 't'
 ordc
i14670
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'u'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14680
 ldcc 'v'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'w'
 ordc
 ixa           1
 ldci          0
i14690
 stoi
 lao         193
 ldcc 'x'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'y'
 ordc
i14700
 ixa           1
 ldci          0
 stoi
 lao         193
 ldcc 'z'
 ordc
 ixa           1
 ldci          0
 stoi
 lao         193
i14710
 ldcc '0'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '1'
 ordc
 ixa           1
 ldci          1
i14720
 stoi
 lao         193
 ldcc '2'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '3'
 ordc
i14730
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '4'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
i14740
 ldcc '5'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '6'
 ordc
 ixa           1
 ldci          1
i14750
 stoi
 lao         193
 ldcc '7'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '8'
 ordc
i14760
 ixa           1
 ldci          1
 stoi
 lao         193
 ldcc '9'
 ordc
 ixa           1
 ldci          1
 stoi
 lao         193
i14770
 ldcc '+'
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc '-'
 ordc
 ixa           1
 ldci          2
i14780
 stoi
 lao         193
 ldcc '*'
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc '/'
 ordc
i14790
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc '('
 ordc
 ixa           1
 ldci          9
 stoi
 lao         193
i14800
 ldcc ')'
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc '$'
 ordc
 ixa           1
 ldci          2
i14810
 stoi
 lao         193
 ldcc '='
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc ' '
 ordc
i14820
 ixa           1
 ldci         10
 stoi
 lao         193
 ldcc ','
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
i14830
 ldcc '.'
 ordc
 ixa           1
 ldci          6
 stoi
 lao         193
 ldcc '''
 ordc
 ixa           1
 ldci          4
i14840
 stoi
 lao         193
 ldcc '['
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc ']'
 ordc
i14850
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc ':'
 ordc
 ixa           1
 ldci          5
 stoi
 lao         193
i14860
 ldcc '^'
 ordc
 ixa           1
 ldci          2
 stoi
 lao         193
 ldcc ';'
 ordc
 ixa           1
 ldci          2
i14870
 stoi
 lao         193
 ldcc '<'
 ordc
 ixa           1
 ldci          7
 stoi
 lao         193
 ldcc '>'
 ordc
i14880
 ixa           1
 ldci          8
 stoi
 lao        1636
 ldcc '0'
 ordc
 ixa           1
 ldci          0
 stoi
 lao        1636
i14890
 ldcc '1'
 ordc
 ixa           1
 ldci          1
 stoi
 lao        1636
 ldcc '2'
 ordc
 ixa           1
 ldci          2
i14900
 stoi
 lao        1636
 ldcc '3'
 ordc
 ixa           1
 ldci          3
 stoi
 lao        1636
 ldcc '4'
 ordc
i14910
 ixa           1
 ldci          4
 stoi
 lao        1636
 ldcc '5'
 ordc
 ixa           1
 ldci          5
 stoi
 lao        1636
i14920
 ldcc '6'
 ordc
 ixa           1
 ldci          6
 stoi
 lao        1636
 ldcc '7'
 ordc
 ixa           1
 ldci          7
i14930
 stoi
 lao        1636
 ldcc '8'
 ordc
 ixa           1
 ldci          8
 stoi
 lao        1636
 ldcc '9'
 ordc
i14940
 ixa           1
 ldci          9
 stoi
 retp
l1741=         7
l1742=         7
l1745
 ent   1   l1746
 ent   2   l1747
 lao        1552
 ldci          0
 ixa           1
 ldci          0
i14950
 stoi
 lao        1552
 ldci          1
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci          2
 ixa           1
 ldci          1
i14960
 ngi
 stoi
 lao        1552
 ldci          3
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci          4
i14970
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci          5
 ixa           1
 ldci          1
 ngi
 stoi
i14980
 lao        1552
 ldci          6
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci          7
 ixa           1
 ldci          1
i14990
 ngi
 stoi
 lao        1552
 ldci          8
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci          9
 ixa           1
i15000
 ldci          0
 stoi
 lao        1552
 ldci         10
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         11
 ixa           1
i15010
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         12
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
i15020
 ldci         13
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         14
 ixa           1
 ldci          1
 ngi
i15030
 stoi
 lao        1552
 ldci         15
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         16
 ixa           1
i15040
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         17
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         18
i15050
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         19
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         20
i15060
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         21
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
i15070
 ldci         22
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         23
 ixa           1
 ldci          0
 stoi
i15080
 lao        1552
 ldci         24
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         25
 ixa           1
 ldci          0
 stoi
i15090
 lao        1552
 ldci         26
 ixa           1
 ldci          2
 ngi
 stoi
 lao        1552
 ldci         27
 ixa           1
 ldci          0
i15100
 stoi
 lao        1552
 ldci         28
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         29
 ixa           1
i15110
 ldci          0
 stoi
 lao        1552
 ldci         30
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         31
 ixa           1
i15120
 ldci          0
 stoi
 lao        1552
 ldci         32
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         33
 ixa           1
i15130
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         34
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         35
i15140
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         36
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
i15150
 ldci         37
 ixa           1
 ldci          1
 stoi
 lao        1552
 ldci         38
 ixa           1
 ldci          1
 stoi
 lao        1552
i15160
 ldci         39
 ixa           1
 ldci          1
 stoi
 lao        1552
 ldci         40
 ixa           1
 ldci          2
 ngi
 stoi
i15170
 lao        1552
 ldci         41
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         42
 ixa           1
 ldci          0
 stoi
i15180
 lao        1552
 ldci         43
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         44
 ixa           1
 ldci          1
i15190
 ngi
 stoi
 lao        1552
 ldci         45
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         46
 ixa           1
i15200
 ldci          0
 stoi
 lao        1552
 ldci         47
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         48
i15210
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         49
 ixa           1
 ldci          1
 ngi
 stoi
i15220
 lao        1552
 ldci         50
 ixa           1
 ldci          1
 stoi
 lao        1552
 ldci         51
 ixa           1
 ldci          1
 stoi
i15230
 lao        1552
 ldci         52
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         53
 ixa           1
 ldci          1
i15240
 ngi
 stoi
 lao        1552
 ldci         54
 ixa           1
 ldci          1
 stoi
 lao        1552
 ldci         55
 ixa           1
i15250
 ldci          1
 ngi
 stoi
 lao        1552
 ldci         56
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1552
i15260
 ldci         57
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         58
 ixa           1
 ldci          0
 stoi
 lao        1552
i15270
 ldci         59
 ixa           1
 ldci          0
 stoi
 lao        1552
 ldci         60
 ixa           1
 ldci          0
 stoi
 lao        1613
i15280
 ldci          1
 deci          1
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1613
 ldci          2
 deci          1
 ixa           1
i15290
 ldci          1
 ngi
 stoi
 lao        1613
 ldci          3
 deci          1
 ixa           1
 ldci          2
 ngi
 stoi
i15300
 lao        1613
 ldci          4
 deci          1
 ixa           1
 ldci          2
 ngi
 stoi
 lao        1613
 ldci          5
 deci          1
i15310
 ixa           1
 ldci          2
 ngi
 stoi
 lao        1613
 ldci          6
 deci          1
 ixa           1
 ldci          3
 ngi
i15320
 stoi
 lao        1613
 ldci          7
 deci          1
 ixa           1
 ldci          3
 ngi
 stoi
 lao        1613
 ldci          8
i15330
 deci          1
 ixa           1
 ldci          3
 ngi
 stoi
 lao        1613
 ldci          9
 deci          1
 ixa           1
 ldci          3
i15340
 ngi
 stoi
 lao        1613
 ldci         10
 deci          1
 ixa           1
 ldci          4
 ngi
 stoi
 lao        1613
i15350
 ldci         11
 deci          1
 ixa           1
 ldci          0
 stoi
 lao        1613
 ldci         12
 deci          1
 ixa           1
 ldci          2
i15360
 ngi
 stoi
 lao        1613
 ldci         13
 deci          1
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1613
i15370
 ldci         14
 deci          1
 ixa           1
 ldci          0
 stoi
 lao        1613
 ldci         15
 deci          1
 ixa           1
 ldci          0
i15380
 stoi
 lao        1613
 ldci         16
 deci          1
 ixa           1
 ldci          0
 stoi
 lao        1613
 ldci         17
 deci          1
i15390
 ixa           1
 ldci          0
 stoi
 lao        1613
 ldci         18
 deci          1
 ixa           1
 ldci          0
 stoi
 lao        1613
i15400
 ldci         19
 deci          1
 ixa           1
 ldci          0
 stoi
 lao        1613
 ldci         20
 deci          1
 ixa           1
 ldci          0
i15410
 stoi
 lao        1613
 ldci         21
 deci          1
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1613
 ldci         22
i15420
 deci          1
 ixa           1
 ldci          1
 ngi
 stoi
 lao        1613
 ldci         23
 deci          1
 ixa           1
 ldci          1
i15430
 ngi
 stoi
 retp
l1746=         5
l1747=         7
l1720
 ent   1   l1748
 ent   2   l1749
 mst           0
 cup   0   l1721
 mst           0
 cup   0   l1724
 mst           0
i15440
 cup   0   l1727
 mst           0
 cup   0   l1737
 mst           0
 cup   0   l1734
 mst           0
 cup   0   l1740
 mst           0
 cup   0   l1745
 retp
l1748=         5
l1749=         5
l1750
i15450
 ent   1   l1751
 ent   2   l1752
 mst           0
 cup   0   l1714
 mst           0
 cup   0   l1717
 mst           0
 cup   0   l1720
 ldci          0
 sroi         51
i15460
 ldci          0
 sroi         52
 lao          54
 ldci          0
 ixa           5
 stra  0    1767
 ldoa       1767
 ldcn
 stoa
 ldoa       1767
i15470
 inca          1
 ldcn
 stoa
 ldoa       1767
 inca          2
 ldci          0
 stoi
 mst           0
 cup   0   l1693
 mst           0
i15480
 cup   0   l1690
 mst           0
 cup   0   l1696
 mst           0
 cup   0   l1711
 ldci          1
 sroi         52
 ldci          1
 sroi         51
 lao          54
i15490
 ldci          1
 ixa           5
 stra  0    1767
 ldoa       1767
 ldcn
 stoa
 ldoa       1767
 inca          1
 ldcn
 stoa
i15500
 ldoa       1767
 inca          2
 ldci          0
 stoi
 mst           0
 cup   0   l  25
 mst           0
 ldos        189
 ldos        186
 uni
i15510
 ldc( 33)
 dif
 cup   1   l1672
 retp
l1751=      1768
l1752=         7
q
i    0
 mst           0
 cup   0   l1750
 stp
q
