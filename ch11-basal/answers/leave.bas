# Exercise 11.6: a GOTO that leaves a subroutine
GOSUB twice
PRINT "back"
END
!twice
PRINT "in"
GOTO out
RETURN
!out
PRINT "out"
END
