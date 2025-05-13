import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SardinasPatterson {

    public static boolean isUniquelyDecodable(Set<String> code) {
        System.out.println("=== Début de l'algorithme de Sardinas-Patterson ===");
        System.out.println("Code initial: " + code);
        
        List<Set<String>> sets = new ArrayList<>();
        Set<String> c1 = computeC1(code);
        sets.add(c1);
        
        System.out.println("\nÉtape 1 - Calcul de C1:");
        System.out.println("C1 = " + c1);
        
        if (c1.contains("")) {
            System.out.println("→ C1 contient le mot vide → Code NON UD");
            return false;
        }
        
        int step = 2;
        while (true) {
            System.out.println("\nÉtape " + step + ":");
            Set<String> previousSet = sets.get(sets.size() - 1);
            Set<String> nextSet = computeNextSet(code, previousSet);
            
            System.out.println("Calcul de C" + step + " à partir de C" + (step-1) + " = " + previousSet);
            System.out.println("C" + step + " = " + nextSet);
            
            if (nextSet.isEmpty()) {
                System.out.println("→ C" + step + " est vide → Code UD");
                return true;
            }
            
            if (nextSet.contains("")) {
                System.out.println("→ C" + step + " contient le mot vide → Code NON UD");
                return false;
            }
            
            for (int i = 0; i < sets.size(); i++) {
                if (sets.get(i).equals(nextSet)) {
                    System.out.println("→ C" + step + " est égal à C" + (i+1) + " → Code UD (pas de mot vide trouvé)");
                    return true;
                }
            }
            
            sets.add(nextSet);
            step++;
        }
    }

    private static Set<String> computeC1(Set<String> code) {
        Set<String> c1 = new HashSet<>();
        
        for (String u : code) {
            for (String v : code) {
                if (!u.equals(v) && u.startsWith(v)) {
                    String suffix = u.substring(v.length());
                    c1.add(suffix);
                    System.out.println("  " + u + " commence par " + v + " → ajoute '" + suffix + "' à C1");
                }
            }
        }
        
        return c1;
    }

    private static Set<String> computeNextSet(Set<String> code, Set<String> previousSet) {
        Set<String> nextSet = new HashSet<>();
        
        for (String u : code) {
            for (String s : previousSet) {
                if (s.startsWith(u)) {
                    String suffix = s.substring(u.length());
                    nextSet.add(suffix);
                    System.out.println("  " + s + " commence par " + u + " → ajoute '" + suffix + "'");
                }
            }
        }
        
        for (String s : previousSet) {
            for (String u : code) {
                if (u.startsWith(s)) {
                    String suffix = u.substring(s.length());
                    nextSet.add(suffix);
                    System.out.println("  " + u + " commence par " + s + " → ajoute '" + suffix + "'");
                }
            }
        }
        
        return nextSet;
    }


    public static void main(String[] args) {
        testCode(new HashSet<>(Arrays.asList("1", "00", "01", "10")), false);
        
        testCode(new HashSet<>(Arrays.asList("0", "10", "11")), true);
        
        testCode(new HashSet<>(Arrays.asList("0", "01", "0110")), false);
        
        testCode(new HashSet<>(Arrays.asList("000", "010", "011", "01001")), true);
    }

    private static void testCode(Set<String> code, boolean expected) {
        System.out.println("\n\nTest: " + code);
        System.out.println("Résultat attendu: " + (expected ? "UD" : "NON UD"));
        boolean result = isUniquelyDecodable(code);
        System.out.println("Résultat obtenu: " + (result ? "UD" : "NON UD"));
        System.out.println("is code : "+result);
        System.out.println(result == expected ? "✓ CORRECT" : "✗ ERREUR");
    }
}