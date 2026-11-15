# Appendix H: Lua's virtual machine

The appendix describes Lua 5.0's register machine from the paper by
Ierusalimschy, de Figueiredo and Celes (2005), and sets beside it what
`luac -l -l` of Lua 5.5.1 shows. It builds no machine, so this folder
holds only the worked answers to its exercises, in `answers/`.

    make check

needs `lua` and `luac` 5.5 on the PATH, and runs `three.asm` and
`loop.asm` on chapter 19's stack and register machines, in
`../ch19-registers`.
