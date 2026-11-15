#!/bin/sh
# Run every answer and compare what it prints with its .out file.
#     ./check.sh          check
#     ./check.sh expect   write the .out files afresh (read them before keeping)
# The answers that change the machine or the compiler are patches, applied
# here to copies:
#   infer.patch   verification by type inference, for class files below 50 (1)
#   emit.patch    emit as a byte, as chapter 10's machine writes it (3)
#   pc.patch      the call's pc stored only where something can throw (5)
# With $JAVA set, Java runs the same class files, and must agree; what it
# says is not in the .out files, which are the same with Java and without.
set -e
cd "$(dirname "$0")"
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
CC=${CC:-cc}
PYTHON=${PYTHON:-python3}
F="-std=c11 -O2 -w"
J="-XX:-ShowCodeDetailsInExceptionMessages"
mode=$1
ENKEL=../../ch10-enkel

answer() {
    name=$1
    shift
    if [ "$mode" = expect ]; then
        "$@" > "$name.out" 2>&1 || true
    else
        "$@" 2>&1 | diff -u "$name.out" - || exit 1
    fi
}

java_says() {   # java_says folder class: what Java prints, and its status
    { env -u JAVA_TOOL_OPTIONS $JAVA $J -cp "$1" "$2" 2>&1; echo "status $?"; }
}

machine() {     # machine name patch...: the machine, changed by the patches
    d="$work/$1"
    mkdir -p "$d"
    shift
    cp ../jvm.h ../class.c ../verify.c ../run.c ../main.c "$d"
    for p in "$@"; do (cd "$d" && patch -s < "$OLDPWD/$p"); done
    (cd "$d" && $CC $F -o jvm class.c verify.c run.c main.c)
}

# 1. Type inference. Every class of javac's, made old, version 49 and no
#    stack maps, prints what it printed; and so does Revisit, whose loop
#    must be gone round again. The broken classes, made old, are refused
#    as type checking refused them, but for those whose fault was in the
#    frames, which inference does not read.
infer() {
    machine infer infer.patch
    mkdir -p "$work/old" "$work/oldbroken"
    k=0
    for c in ../classes/*.class Revisit.class; do
        k=$((k + 1))
        n=$(basename "$c" .class)
        $PYTHON old.py "$c" "$work/old/$n.class"
        { "$work/infer/jvm" "$work/old/$n.class" 2>&1; echo "status $?"; } > "$work/$n.got"
        want=../tests/$n.out
        [ "$n" = Revisit ] && want=$work/Revisit.want && echo 45 > $want && echo "status 0" >> $want
        cmp -s "$want" "$work/$n.got" || { echo "$n differs"; cat "$work/$n.got"; return 1; }
        if [ -n "$JAVA" ]; then
            java_says "$work/old" "$n" | cmp -s "$want" - || { echo "Java: $n differs"; return 1; }
        fi
    done
    echo "$k classes made old print as they did"
    "$work/infer/jvm" -f "$work/old/Sieve.class" | grep -v ^verified
    "$work/infer/jvm" -f "$work/old/Revisit.class" | grep -v ^verified
    # the cases on which the two machines already differ are left out
    for b in $(awk -F'\t' '$4 == "" { print $1 }' ../build/broken/cases.txt); do
        c=$(cd ../build/broken/$b && ls *.class)
        mkdir -p "$work/oldbroken/$b"
        $PYTHON old.py "../build/broken/$b/$c" "$work/oldbroken/$b/$c" > /dev/null 2>&1 || {
            echo "$b: cannot be made old"; continue; }
        if "$work/infer/jvm" -v "$work/oldbroken/$b/$c" > /dev/null 2>&1; then v=accepted; else v=refused; fi
        echo "$b: $v"
        if [ -n "$JAVA" ]; then
            if java_says "$work/oldbroken/$b" "${c%.class}" | grep "VerifyError\|ClassFormatError" > /dev/null; then
                w=refused; else w=accepted; fi
            [ "$v" = "$w" ] || { echo "Java: $b $w"; return 1; }
        fi
    done
}

# 2. An index past the end: chapter 10's machine reads the next array;
#    the JVM throws.
past() {
    $PYTHON $ENKEL/enkel.py past.p > "$work/past.asm"
    $PYTHON $ENKEL/asm.py "$work/past.asm" "$work/past.vm"
    echo "chapter 10's machine:"
    $ENKEL/vm "$work/past.vm"
    $PYTHON ../enkelj.py past.p "$work"
    echo "this JVM:"
    "$work/jvm-plain" "$work/Past.class" || echo "status $?"
    if [ -n "$JAVA" ]; then
        { "$work/jvm-plain" "$work/Past.class" 2>&1; echo "status $?"; } > "$work/past.ours"
        java_says "$work" Past | cmp -s "$work/past.ours" - || { echo "Java differs"; return 1; }
    fi
}

# 3. emit of 233: the bytes each writes, as numbers, before and after the
#    patch to enkelj.py.
bytes() {
    $PYTHON $ENKEL/enkel.py bytes.p > "$work/bytes.asm"
    $PYTHON $ENKEL/asm.py "$work/bytes.asm" "$work/bytes.vm"
    echo "chapter 10's machine: $($ENKEL/vm "$work/bytes.vm" | od -An -tu1)"
    $PYTHON ../enkelj.py bytes.p "$work"
    echo "this JVM, print(char): $("$work/jvm-plain" "$work/Bytes.class" | od -An -tu1)"
    [ -z "$JAVA" ] || [ "$(env -u JAVA_TOOL_OPTIONS $JAVA -cp "$work" Bytes | od -An -tu1)" = \
        "$("$work/jvm-plain" "$work/Bytes.class" | od -An -tu1)" ] || { echo "Java differs"; return 1; }
    mkdir -p "$work/emit/appE-jvm"
    ln -s "$(cd $ENKEL && pwd)" "$work/emit/ch10-enkel"
    cp ../enkelj.py ../classfile.py "$work/emit/appE-jvm"
    (cd "$work/emit/appE-jvm" && patch -s < "$OLDPWD/emit.patch")
    $PYTHON "$work/emit/appE-jvm/enkelj.py" bytes.p "$work/emit"
    echo "this JVM, write(int): $("$work/jvm-plain" "$work/emit/Bytes.class" | od -An -tu1)"
    [ -z "$JAVA" ] || [ "$(env -u JAVA_TOOL_OPTIONS $JAVA -cp "$work/emit" Bytes | od -An -tu1)" = \
        "$("$work/jvm-plain" "$work/emit/Bytes.class" | od -An -tu1)" ] || { echo "Java differs"; return 1; }
    for s in $ENKEL/samples/*.p; do
        $PYTHON "$work/emit/appE-jvm/enkelj.py" "$s" "$work/emit"
        n=$($PYTHON ../enkelj.py -name "$(basename "$s" .p)")
        "$work/jvm-plain" "$work/emit/$n.class" | cmp -s "${s%.p}.out" - || { echo "$s differs"; return 1; }
    done
    echo "and the samples print as before"
}

# 4. The stack maps' share of the class files: javac's, and enkelj's for
#    chapter 10's samples.
sizes() {
    mkdir -p "$work/enkelj"
    for s in $ENKEL/samples/*.p; do $PYTHON ../enkelj.py "$s" "$work/enkelj"; done
    $PYTHON sizes.py ../classes "$work/enkelj"
}

# 5. The pc stored only where something can throw: everything prints, and
#    traps, as before. How much faster, hint.sh measures, by hand.
pc() {
    machine pc pc.patch
    for c in ../classes/*.class; do
        n=$(basename "$c" .class)
        { "$work/pc/jvm" "$c" 2>&1; echo "status $?"; } | cmp -s ../tests/$n.out - || {
            echo "$n differs"; return 1; }
    done
    $PYTHON ../enkelj.py ../tests/share.p "$work"
    { "$work/pc/jvm" "$work/Share.class" 2>&1; echo "status $?"; } | diff -u ../tests/share.out - || return 1
    echo "$(ls ../classes/*.class | wc -l | tr -d ' ') classes and share.p print and trap as before"
}

(cd .. && $CC $F -o "$work/jvm-plain" class.c verify.c run.c main.c)
answer infer infer
answer past past
answer bytes bytes
answer sizes sizes
answer pc pc
echo "answers: ok"
