public class Bounds {

    static int sum(int[] a, int n) {
        int s = 0;
        for (int i = 0; i <= n; i++) {
            s += a[i];
        }
        return s;
    }

    public static void main(String[] args) {
        int[] a = new int[10];
        for (int i = 0; i < a.length; i++) {
            a[i] = i * i;
        }
        System.out.println(sum(a, 9));
        System.out.println(sum(a, 10));
    }
}
