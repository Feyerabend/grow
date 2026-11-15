public class Revisit {

    // At the loop's head, a is first null, then an int[]: inference must
    // go round the loop again with the merged type.
    public static void main(String[] args) {
        int[] a = null;
        int s = 0;
        for (int i = 0; i < 10; i++) {
            if (a == null) {
                a = new int[10];
            }
            a[i] = i;
            s += a[i];
        }
        System.out.println(s);
    }
}
