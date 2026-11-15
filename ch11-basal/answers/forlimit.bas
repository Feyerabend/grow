# Exercise 11.2: the limit is evaluated once, so changing N inside the loop
# does not change how many rounds there are
LET N = 3
FOR I = 1 TO N
  PRINT I
  LET N = N - 1
NEXT I
PRINT N
