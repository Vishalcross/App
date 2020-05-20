import java.util.*;
import java.math.*;
public class hello{
    static void print(boolean a[][]){
        System.out.println("Numbers");
        for(int i=0;i<a.length;i++){
            for(int j=0;j<a[0].length;j++){
                System.out.print( (a[i][j]?1:0) + " ");
            }
            System.out.println();
        }
    }
    
    static void print(String a[][]) {
        System.out.println("String");
        for (int i = 0; i < a.length; i++) {
            for (int j = 0; j < a[0].length; j++) {
                System.out.print(a[i][j]+" ");
            }
            System.out.println();
        }
    }
    public static void main(String[] args){
        Scanner scan = new Scanner(System.in);
        int t = scan.nextInt();
        while(t-- >0){
            int h = scan.nextInt();
            int leaves = (int)Math.pow(2, h-1);
            // System.out.println(h+" height & leaves "+leaves);
            // boolean num_cascade[] = new boolean[leaves];
            Queue<Boolean> q = new LinkedList<>();
            // Queue<Boolean> p = new LinkedList<>();
            for(int i=0;i<leaves;i++){
                q.add(scan.nextInt()==0?false:true);
            }
            for(int i=0;i<h-1;i++){
                int x = (int)Math.pow(2,i+1);
                for(int j=0;j<leaves/x;j++){
                    // System.out.print(scan.next());
                    String op = scan.next();
                    if(op.compareTo("or") == 0){
                        boolean result = q.remove() | q.remove();
                        q.add(result);
                    }
                    else if(op.compareTo("and") == 0){
                        boolean result = q.remove() & q.remove();
                        q.add(result);
                    }
                    else if(op.compareTo("nand") == 0){
                        boolean result = !(q.remove() & q.remove());
                        q.add(result);
                    }
                    else if(op.compareTo("nor") == 0){
                        boolean result = !(q.remove() | q.remove());
                        q.add(result);
                    }
                    else if(op.compareTo("xor") == 0){
                        boolean result = q.remove() ^ q.remove();
                        q.add(result);
                    }
                    else if(op.compareTo("xnor") == 0){
                        boolean result = !(q.remove() ^ q.remove());
                        q.add(result);
                    }
                }
                
            }
            System.out.println(q.peek());
            // break;
        }
        scan.close();
    }
}
