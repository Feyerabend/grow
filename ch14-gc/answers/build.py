#!/usr/bin/env python3
"""
Make vm_more.c: chapter 14's vm.c with two more collectors, for exercises 14.1
and 14.5. Both are mark and sweep's marking, and differ in what follows.

  -g next      mark and sweep, allocating by next fit: each search for a free
               chunk starts where the last one ended, not at the first chunk.
  -g compact   mark, then slide every live block down to the bottom of the
               heap, in order (Lisp 2's three passes: work out where each
               block goes, change every reference, move the blocks), leaving
               one free chunk above them.

With -s, every collector also reports how many free chunks its searches
looked at, and compact how many places it moved.

    usage: python3 build.py > vm_more.c
"""

import os

s = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vm.c")).read()


def change(old, new, count=1):
    global s
    assert s.count(old) == count, old
    s = s.replace(old, new)


change("static int collector = MARK_SWEEP;",
       "static int collector = MARK_SWEEP;\n"
       "static int next_fit = 0;          /* -g next */\n"
       "static int compacting = 0;        /* -g compact */\n"
       "static long chunks_looked = 0;\n"
       "static long words_moved = 0;\n"
       "static int rover = -1;            /* next fit: where the last search ended */\n"
       "static int rover_prev = -1;       /* and the chunk before it, or -1 */")

# Next fit: the same search, begun at the rover, going round once.
change("""static int find_free(int words) {
    int prev = -1, c = free_list;

    while (c >= 0) {
        int size = heap[c].n;
        int next = heap[c + 1].n;

        if (size == words) {
            if (prev >= 0)
                heap[prev + 1].n = next;
            else
                free_list = next;
            return c;
        }
        if (size >= words + HEADER) {
            heap[c].n = size - words;
            return c + size - words;
        }
        prev = c;
        c = next;
    }
    return -1;
}""", """static int find_free(int words) {
    /* First fit starts at the first chunk; next fit at the rover, with
     * the chunk before it remembered, and goes round once. The list only
     * changes here and in a collection, which sets the rover to its start. */
    int prev = next_fit ? rover_prev : -1;
    int c = next_fit ? rover : free_list;
    int start, wrapped = 0;

    if (c < 0) {
        prev = -1;
        c = free_list;
    }
    start = c;
    while (c >= 0) {
        int size = heap[c].n;
        int next = heap[c + 1].n;

        chunks_looked++;
        if (size == words) {
            if (prev >= 0)
                heap[prev + 1].n = next;
            else
                free_list = next;
            rover = next;
            rover_prev = prev;
            return c;
        }
        if (size >= words + HEADER) {
            heap[c].n = size - words;
            rover = c;
            rover_prev = prev;
            return c + size - words;
        }
        prev = c;
        c = next;
        if (c < 0 && next_fit && !wrapped && start != free_list) {
            wrapped = 1;                /* round again from the start, */
            prev = -1;
            c = free_list;
        }
        if (wrapped && c == start)
            break;                      /* as far as where this search began */
    }
    return -1;
}""")

# Compaction, after marking.
change("static void collect(void) {", """static int forward_to[HEAP_SIZE];

static struct value moved(struct value v) {
    if (v.is_ref)
        v.n = forward_to[v.n];
    return v;
}

/* The size of whatever starts at at: a free chunk, or a block. */
static int extent(int at) {
    return heap[at].is_ref == FREE ? heap[at].n : heap[at].n + HEADER;
}

static void compact(void) {
    int at, to = 0, i, size;
    long live = 0;

    /* 1. Where each live block will go: as low as it can, in order. */
    for (at = 0; at < HEAP_SIZE; at += extent(at))
        if (heap[at].is_ref == MARKED) {
            forward_to[at] = to;
            to += extent(at);
        }
    /* 2. Every reference changed to the new place: roots, then fields. */
    for (i = 0; i < sp; i++)
        stack[i] = moved(stack[i]);
    for (i = 0; i < MEMORY_SIZE; i++)
        memory[i] = moved(memory[i]);
    for (at = 0; at < HEAP_SIZE; at += extent(at))
        if (heap[at].is_ref == MARKED)
            for (i = 0; i < heap[at].n; i++)
                heap[at + HEADER + i] = moved(heap[at + HEADER + i]);
    /* 3. The blocks moved down, unmarked. Each goes to a place no higher
     * than its own, so moving them in order never overwrites one not yet
     * moved. */
    for (at = 0; at < HEAP_SIZE; at += size) {
        size = extent(at);
        if (heap[at].is_ref == MARKED) {
            if (forward_to[at] != at) {
                memmove(&heap[forward_to[at]], &heap[at], size * sizeof (struct value));
                words_moved += size;
            }
            heap[forward_to[at]].is_ref = UNMARKED;
            live += size;
        }
    }
    /* What is left is one free chunk, if there is room for one. */
    free_list = -1;
    if (HEAP_SIZE - to >= HEADER) {
        heap[to].is_ref = FREE;
        heap[to].n = HEAP_SIZE - to;
        heap[to + 1] = integer(-1);
        free_list = to;
    } else if (to < HEAP_SIZE) {
        heap[to].is_ref = FREE;         /* one place: a chunk no search sees */
        heap[to].n = 1;
    }
    if (live > most_live)
        most_live = live;
}

static void collect(void) {""")
change("""    if (collector == MARK_SWEEP) {
        mark();
        sweep();
    } else {""", """    if (collector == MARK_SWEEP) {
        mark();
        if (compacting)
            compact();
        else
            sweep();
        rover = free_list;
        rover_prev = -1;
    } else {""")
change("""            collector == MARK_SWEEP ? "mark and sweep" : "copying",""",
       """            compacting ? "mark and compact" : next_fit ? "mark and sweep, next fit" :
            collector == MARK_SWEEP ? "mark and sweep" : "copying",""")
change("""    if (collector == MARK_SWEEP)
        fprintf(stderr, "gc: %ld places freed\\n", words_freed);""",
       """    if (compacting)
        fprintf(stderr, "gc: %ld places moved\\n", words_moved);
    else if (collector == MARK_SWEEP)
        fprintf(stderr, "gc: %ld places freed\\n", words_freed);""")
change("""    fprintf(stderr, "gc: %.3f seconds collecting\\n", (double) gc_time / CLOCKS_PER_SEC);""",
       """    if (collector == MARK_SWEEP)
        fprintf(stderr, "gc: %ld free chunks looked at\\n", chunks_looked);
    fprintf(stderr, "gc: %.3f seconds collecting\\n", (double) gc_time / CLOCKS_PER_SEC);""")
change("""            } else if (strcmp(argv[i], "copy") == 0) {
                collector = COPYING;""", """            } else if (strcmp(argv[i], "copy") == 0) {
                collector = COPYING;
            } else if (strcmp(argv[i], "next") == 0) {
                collector = MARK_SWEEP;
                next_fit = 1;
            } else if (strcmp(argv[i], "compact") == 0) {
                collector = MARK_SWEEP;
                compacting = 1;""")
change('"usage: vm [-t | -d] [-g mark | -g copy] [-S] [-s] program.vm\\n"',
       '"usage: vm [-t | -d] [-g mark | -g copy | -g next | -g compact] [-S] [-s] program.vm\\n"')
print(s, end="")
