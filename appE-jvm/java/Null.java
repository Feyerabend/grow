public class Null {

    static int[] table;

    public static void main(String[] args) {
        System.out.println("before");
        if (args.length > 0) {
            table = new int[1];
        }
        System.out.println(table[0]);
    }
}
