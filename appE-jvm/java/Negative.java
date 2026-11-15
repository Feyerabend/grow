public class Negative {

    static int[] make(int n) {
        return new int[n];
    }

    public static void main(String[] args) {
        System.out.println(make(3).length);
        System.out.println(make(-1).length);
    }
}
