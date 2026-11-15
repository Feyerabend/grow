/* Bits: CRC-32, as zip computes it, with its table. */
#include "io.h"

static unsigned table[256];

static unsigned crc32(const char *s)
{
    unsigned c = 0xFFFFFFFFu;
    while (*s)
        c = table[(c ^ (unsigned char)*s++) & 0xFF] ^ (c >> 8);
    return c ^ 0xFFFFFFFFu;
}

static void hex(unsigned x)
{
    for (int i = 28; i >= 0; i -= 4)
        put("0123456789abcdef"[(x >> i) & 15]);
}

int main(void)
{
    for (unsigned n = 0; n < 256; n++) {
        unsigned c = n;
        for (int k = 0; k < 8; k++)
            c = c & 1 ? 0xEDB88320u ^ (c >> 1) : c >> 1;
        table[n] = c;
    }
    static const char *texts[] = {"", "a", "abc", "123456789",
        "The quick brown fox jumps over the lazy dog"};
    for (int i = 0; i < 5; i++) {
        hex(crc32(texts[i]));
        newline();
    }
    return 0;
}
