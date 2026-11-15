"""
Copies of chapter 3's and chapter 4's machines that read their program from a
file of numbers instead of having it written into the C source. Used by the
measurements of chapter 4; the machines themselves are unchanged.
"""

import os
import subprocess

READ = """
static int loaded[65536];

static int load(const char *path) {
    FILE *f = fopen(path, "r");
    int n = 0;
    if (f == NULL)
        return -1;
    while (n < 65536 && fscanf(f, "%d", &loaded[n]) == 1)
        n++;
    fclose(f);
    return n;
}
"""


def unchecked(path_ch03):
    """Chapter 3's machine, reading its program from argv[1]."""
    source = open(path_ch03).read()
    source = source.replace("int main(void) {\n    run(program);",
                            READ + "int main(int argc, char *argv[]) {\n"
                            "    if (argc < 2 || load(argv[1]) < 0)\n        return 2;\n"
                            "    run(loaded);", 1)
    return source


def checked(path_ch04):
    """Chapter 4's machine, reading its program from argv[1]."""
    source = open(path_ch04).read()
    start = source.index("int main(int argc, char *argv[]) {")
    source = source[:start] + READ + """int main(int argc, char *argv[]) {
    if (argc < 2)
        return 2;
    code_len = load(argv[1]);
    if (code_len < 0)
        return 2;
    code = loaded;
    run();
    return 0;
}
"""
    return source


def build(source, exe, flags):
    c = exe + ".c"
    with open(c, "w") as f:
        f.write(source)
    subprocess.run(["cc", "-std=c99", "-w"] + flags + ["-o", exe, c], check=True)
    return exe
