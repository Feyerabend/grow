l   3
 ent   1   l   4
 ent   2   l   5
 ldci          3
 ldci          2
 flt
 flo
 dvr
i   10
 sror         11
 ldci          1
 ldci          3
 flt
 flo
 dvr
 sror         10
 ldcr  0.1            
 sror          9
 ldor         11
i   20
 ldci         12
 lda   0       6
 csp         wrr
 ldor         11
 ldci          1
 lda   0       6
 csp         wrr
 ldor         11
 ngr
 ldci         20
i   30
 lda   0       6
 csp         wrr
 ldor         11
 ldci          9
 lda   0       6
 csp         wrr
 ldor         11
 ldci         10
 lda   0       6
 csp         wrr
i   40
 ldor         11
 ldci         30
 lda   0       6
 csp         wrr
 lda   0       6
 csp         wln
 ldor         10
 ldci         24
 lda   0       6
 csp         wrr
i   50
 ldor         10
 ldcr  1e30           
 mpr
 ldci         15
 lda   0       6
 csp         wrr
 ldci          2
 flt
 csp         sqt
 ldci          9
i   60
 lda   0       6
 csp         wrr
 lda   0       6
 csp         wln
 ldor          9
 ldci          2
 ldor          9
 flo
 mpr
 adr
i   70
 ldci         25
 lda   0       6
 csp         wrr
 ldor         11
 ldor         10
 mpr
 ldci         12
 lda   0       6
 csp         wrr
 ldor         11
i   80
 ldor         10
 sbr
 ldci         12
 lda   0       6
 csp         wrr
 ldor         10
 ngr
 ldci         12
 lda   0       6
 csp         wrr
i   90
 lda   0       6
 csp         wln
 ldor         11
 ngr
 trc
 sroi         12
 ldoi         12
 ldci          3
 lda   0       6
 csp         wri
i  100
 ldor         11
 trc
 ldci          3
 lda   0       6
 csp         wri
 ldor         10
 ldci       1000
 flt
 mpr
 trc
i  110
 ldci          5
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
 ldci          1
 flt
 csp         sin
 ldci         24
 lda   0       6
i  120
 csp         wrr
 ldci          1
 flt
 csp         cos
 ldci         24
 lda   0       6
 csp         wrr
 lda   0       6
 csp         wln
 ldci          1
i  130
 flt
 csp         exp
 ldci         24
 lda   0       6
 csp         wrr
 ldci          2
 flt
 csp         log
 ldci         24
 lda   0       6
i  140
 csp         wrr
 ldci          1
 flt
 csp         atn
 ldci         24
 lda   0       6
 csp         wrr
 lda   0       6
 csp         wln
 ldor         11
i  150
 ngr
 abr
 ldci          8
 lda   0       6
 csp         wrr
 ldor         11
 sqr
 ldci          8
 lda   0       6
 csp         wrr
i  160
 ldci          7
 ldci          2
 flt
 flo
 dvr
 ldci          8
 lda   0       6
 csp         wrr
 ldcr  2.5e-3         
 ldci         12
i  170
 lda   0       6
 csp         wrr
 lda   0       6
 csp         wln
 ldor         11
 ldor         10
 grtr
 fjp       l   6
 lca'x > y           '
 ldci          5
i  180
 ldci          5
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   6
 ldor         11
 ldci          2
 flt
 mpr
 ldci          3
i  190
 flt
 equr
 fjp       l   7
 lca'x * 2 = 3       '
 ldci          9
 ldci          9
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   7
i  200
 ldor         10
 ldor         10
 adr
 ldor         10
 adr
 ldci          3
 ldci          3
 flt
 flo
 dvr
i  210
 neqr
 fjp       l   8
 lca'thirds: not 1   '
 ldci         13
 ldci         13
 lda   0       6
 csp         wrs
 lda   0       6
 csp         wln
l   8
 retp
l   4=        13
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
