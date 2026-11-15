l   3
 ent   1   l   4
 ent   2   l   5
 lao          12
 lda   0       5
 csp         rdi
 ldci          0
 sroi          9
i   10
 ldci          1
 sroi         11
 ldoi         12
 stri  0      13
l   6
 ldoi         11
 lodi  0      13
 leqi
 fjp       l   7
 lao          10
 lda   0       5
i   20
 csp         rdi
 ldoi          9
 ldoi         10
 adi
 sroi          9
 ldoi         11
 inci          1
 sroi         11
 ujp       l   6
l   7
 lca'the sum of      '
i   30
 ldci         11
 ldci         11
 lda   0       6
 csp         wrs
 ldoi         12
 ldci          1
 lda   0       6
 csp         wri
 lca' numbers is     '
 ldci         12
i   40
 ldci         12
 lda   0       6
 csp         wrs
 ldoi          9
 ldci          1
 lda   0       6
 csp         wri
 lda   0       6
 csp         wln
 retp
l   4=        14
l   5=         9
q
i    0
 mst           0
 cup   0   l   3
 stp
q
