public class Switch {

    static int days(int month) {
        switch (month) {
        case 2:
            return 28;
        case 4: case 6: case 9: case 11:
            return 30;
        default:
            return 31;
        }
    }

    static char roman(int digit) {
        switch (digit) {
        case 1: return 'I';
        case 5: return 'V';
        case 10: return 'X';
        case 50: return 'L';
        case 100: return 'C';
        case 500: return 'D';
        case 1000: return 'M';
        default: return '?';
        }
    }

    public static void main(String[] args) {
        int total = 0;
        for (int m = 1; m <= 12; m++) {
            total += days(m);
        }
        System.out.println(total);
        int[] values = { 1000, 500, 100, 50, 10, 5, 1, 7 };
        for (int i = 0; i < values.length; i++) {
            System.out.print(roman(values[i]));
        }
        System.out.println();
    }
}
