public class Target1HelloFuzzing {

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            cov_info[0] = '1';
            System.out.print("\n" + new String(cov_info));
            System.out.println("[TARGET] Require 1 arg!!!");
            System.exit(0);
        }
        // Start to process
        char[] charArr = args[0].toCharArray();
        if (charArr[0] == 'h') {
            cov_info[5] = '1';
            System.out.print("\n" + new String(cov_info));
            System.out.println("[TARGET] Catch h!");
            if (charArr[1] == 'e') {
                cov_info[4] = '1';
                System.out.print("\n" + new String(cov_info));
                System.out.println("[TARGET] Catch he!");
                if (charArr[2] == 'l') {
                    cov_info[3] = '1';
                    System.out.print("\n" + new String(cov_info));
                    System.out.println("[TARGET] Catch hel!");
                    if (charArr[3] == 'l') {
                        cov_info[2] = '1';
                        System.out.print("\n" + new String(cov_info));
                        System.out.println("[TARGET] Catch hell!");
                        if (charArr[4] == 'o') {
                            cov_info[1] = '1';
                            System.out.print("\n" + new String(cov_info));
                            throw new Exception("[TARGET] Hello! Find a bug!");
                        } else {
                            cov_info[6] = '1';
                            System.out.print("\n" + new String(cov_info));
                            System.out.println("[TARGET] Failed at (4, o)!");
                        }
                    } else {
                        cov_info[7] = '1';
                        System.out.print("\n" + new String(cov_info));
                        System.out.println("[TARGET] Failed at (3, l)!");
                    }
                } else {
                    cov_info[8] = '1';
                    System.out.print("\n" + new String(cov_info));
                    System.out.println("[TARGET] Failed at (2, l)!");
                }
            } else {
                cov_info[9] = '1';
                System.out.print("\n" + new String(cov_info));
                System.out.println("[TARGET] Failed at (1, e)!");
            }
        } else {
            cov_info[10] = '1';
            System.out.print("\n" + new String(cov_info));
            System.out.println("[TARGET] Failed at (0, h)!");
        }
        System.out.print("\n" + new String(cov_info));
    }

    public static char[] cov_info = { '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0' };
}
