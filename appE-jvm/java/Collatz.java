public class Collatz {

    static int[] steps = new int[1000];
    static int longest = 1;

    static int length(int n) {
        int k = 0;
        do {
            if ((n & 1) == 0) {
                n = n / 2;
            } else {
                n = 3 * n + 1;
            }
            k++;
        } while (n != 1);
        return k;
    }

    public static void main(String[] args) {
        for (int n = 2; n < steps.length; n++) {
            steps[n] = length(n);
            if (steps[n] > steps[longest]) {
                longest = n;
            }
        }
        System.out.print("longest below 1000: ");
        System.out.print(longest);
        System.out.print(", in ");
        System.out.print(steps[longest]);
        System.out.println(" steps");
    }
}
