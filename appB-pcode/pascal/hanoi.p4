l   3
 ent   1   l   4
 ent   2   l   5
 lodi  0       5
 ldci          0
 grti
 fjp       l   6
 mst           1
i   10
 lodi  0       5
 ldci          1
 sbi
 lodc  0       6
 chkc  0     127
 lodc  0       8
 chkc  0     127
 lodc  0       7
 chkc  0     127
 cup   4   l   3
i   20
 lca'disc            '
 ldci          5
 ldci          5
 lda   1       6
 csp         wrs
 lodi  0       5
 ldci          1
 lda   1       6
 csp         wri
 lca' from           '
i   30
 ldci          6
 ldci          6
 lda   1       6
 csp         wrs
 lodc  0       6
 ldci          1
 lda   1       6
 csp         wrc
 lca' to             '
 ldci          4
i   40
 ldci          4
 lda   1       6
 csp         wrs
 lodc  0       7
 ldci          1
 lda   1       6
 csp         wrc
 lda   1       6
 csp         wln
 mst           1
i   50
 lodi  0       5
 ldci          1
 sbi
 lodc  0       8
 chkc  0     127
 lodc  0       7
 chkc  0     127
 lodc  0       6
 chkc  0     127
 cup   4   l   3
l   6
i   60
 retp
l   4=         9
l   5=        13
l   7
 ent   1   l   8
 ent   2   l   9
 mst           0
 ldci          3
 ldcc 'A'
 chkc  0     127
 ldcc 'C'
 chkc  0     127
 ldcc 'B'
i   70
 chkc  0     127
 cup   4   l   3
 retp
l   8=         9
l   9=         9
q
i    0
 mst           0
 cup   0   l   7
 stp
q
