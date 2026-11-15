public class Bits {

    static int a, b;

    static int abs(int x) {
        return x < 0 ? -x : x;
    }

    // Each operation on values not known when compiling, so that javac
    // cannot work it out itself and the machine must.
    static void show(int x, int y) {
        System.out.print(x / y);
        System.out.print(' ');
        System.out.print(x % y);
        System.out.print(' ');
        System.out.print(x >>> y);
        System.out.print(' ');
        System.out.print(x >> y);
        System.out.print(' ');
        System.out.print(x << y);
        System.out.print(' ');
        System.out.print(x ^ y | x & y);
        System.out.print(' ');
        System.out.print((byte) x);
        System.out.print(' ');
        System.out.print((short) x);
        System.out.print(' ');
        System.out.print((int) (char) x);
        System.out.print(' ');
        System.out.println(x * y + -x);
    }

    public static void main(String[] args) {
        int min = 0x80000000, max = 0x7fffffff;
        System.out.println(max + 1);
        show(min, -1);
        show(-7, 2);
        show(7, -2);
        show(-1, 28);
        show(1, 33);
        show(70000, 200);
        show(max, max);
        System.out.println(abs(-12345) + abs(678));
        int s = 0;
        for (int i = 0; i < 100000; i += 300) {
            s += i;
        }
        System.out.println(s);
        a = b = 1000000;
        System.out.println(a * b);
        int[] counts = new int[4];
        for (int i = 0; i < 1000; i++) {
            counts[i & 3] += i;
            counts[(i >> 2) & 3]++;
        }
        int[] same = counts;
        if (same == counts && same != null) {
            System.out.println(counts[0] + counts[1] + counts[2] + counts[3]);
        }
        System.out.println(counts.length);
    }
}
