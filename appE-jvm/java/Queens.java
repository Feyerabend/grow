public class Queens {

    static final int N = 8;
    static int[] column = new int[N];
    static int solutions;

    static boolean safe(int row, int col) {
        for (int r = 0; r < row; r++) {
            int c = column[r];
            if (c == col || c - col == r - row || c - col == row - r) {
                return false;
            }
        }
        return true;
    }

    static void place(int row) {
        if (row == N) {
            solutions++;
            return;
        }
        for (int col = 0; col < N; col++) {
            if (safe(row, col)) {
                column[row] = col;
                place(row + 1);
            }
        }
    }

    public static void main(String[] args) {
        place(0);
        System.out.print("solutions for ");
        System.out.print(N);
        System.out.print(" queens: ");
        System.out.println(solutions);
    }
}
