import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.PriorityQueue;

public class Huff {
    public static HuffmanNode buildHuffmanTree(Map<Character, Integer> frequencyMap) {

        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>();

        for (Map.Entry<Character, Integer> entry : frequencyMap.entrySet()) {
            pq.add(new HuffmanNode(entry.getKey(), entry.getValue()));
        }

        while (pq.size() > 1) {
            HuffmanNode left = pq.poll();
            HuffmanNode right = pq.poll();
            HuffmanNode merged = new HuffmanNode('\0', left.frequency + right.frequency);
            merged.left = left;
            merged.right = right;
            pq.add(merged);
        }

        return pq.poll(); 
    }

    public static void generateHuffmanCodes(HuffmanNode root, String code, Map<Character, String> huffmanCodes) {
        if (root == null) return;

        if (root.left == null && root.right == null) {
            huffmanCodes.put(root.character, code);
        }

        generateHuffmanCodes(root.left, code + "0", huffmanCodes);
        generateHuffmanCodes(root.right, code + "1", huffmanCodes);
    }

    public static Map<Character, Integer> countCharacterFrequency(String input) {
        Map<Character, Integer> frequencyMap = new HashMap<>();

        for (char c : input.toCharArray()) {
            if (Character.isLetter(c)) {
                char lowerCase = Character.toLowerCase(c);
                frequencyMap.put(lowerCase, frequencyMap.getOrDefault(lowerCase, 0) + 1);
            } 
            else if (c == ' ') {
                frequencyMap.put(c, frequencyMap.getOrDefault(c, 0) + 1);
            }
        }

        return frequencyMap;
    }

    public static String encoder(Map<Character, String> mots, String texte) {
        StringBuilder textecoder = new StringBuilder();
        for (int i = 0; i < texte.length(); i++) {
            Character characterdutexte = Character.toLowerCase(texte.charAt(i));
            if (mots.containsKey(characterdutexte)) {
                textecoder.append(mots.get(characterdutexte));
            } else {
                throw new IllegalArgumentException("Le caractère "+ characterdutexte +" n'est pas dans la bibliothèque");
            }
        }
        return textecoder.toString();
    }

    public static String decode(HuffmanNode root, String encodedText) {
        StringBuilder decodedText = new StringBuilder();
        HuffmanNode current = root;

        for (int i = 0; i < encodedText.length(); i++) {
            
            char bit = encodedText.charAt(i);
            if (bit == '0') {
                current = current.left;
            } else if (bit == '1') {
                current = current.right;
            }

            if (current.left == null && current.right == null) {
                decodedText.append(current.character);
                current = root;  
            }
        }
        return decodedText.toString();
    }

    public static void compressFile(String inputPath, String outputPath,String dictonary) {
        try {

            String content = new String(Files.readAllBytes(Paths.get(inputPath)));
            
            // Construire l'arbre de Huffman
            Map<Character, Integer> freqMap = countCharacterFrequency(content);
            HuffmanNode root = buildHuffmanTree(freqMap);
            
            Map<Character, String> huffmanCodes = new HashMap<>();
            generateHuffmanCodes(root, "", huffmanCodes);
            
            String encodedText = encoder(huffmanCodes, content);
            

            writeCompressedFile(outputPath, huffmanCodes, encodedText,dictonary);
            
            System.out.println("Fichier compressé avec succès: " + outputPath);
        } catch (IOException e) {
            System.err.println("Erreur lors de la compression: " + e.getMessage());
        }
    }

    public static void decompressFile(String inputPath, String outputPath,String dictionary) {
        try {

            ObjectInputStream ois = new ObjectInputStream(new FileInputStream(inputPath));
            ObjectInputStream dico = new ObjectInputStream(new FileInputStream(dictionary));
            
            // Lire les métadonnées
            @SuppressWarnings("unchecked")
            Map<Character, String> huffmanCodes = (Map<Character, String>) dico.readObject();
            String encodedText = (String) ois.readObject();
            ois.close();
            
            HuffmanNode root = rebuildHuffmanTree(huffmanCodes);
            
            String decodedText = decode(root, encodedText);
            
            // Écrire le fichier décompressé
            Files.write(Paths.get(outputPath), decodedText.getBytes());
            
            System.out.println("Fichier décompressé avec succès: " + outputPath);
        } catch (IOException | ClassNotFoundException e) {
            System.err.println("Erreur lors de la décompression: " + e.getMessage());
        }
    }

    private static void writeCompressedFile(String path, Map<Character, String> huffmanCodes, String encodedText,String dictionary) 
            throws IOException {
        ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(path));
        ObjectOutputStream dico = new ObjectOutputStream(new FileOutputStream(dictionary));
        
        dico.writeObject(huffmanCodes);
        oos.writeObject(encodedText);
        oos.close();
        dico.close();
    }

    public static HuffmanNode rebuildHuffmanTree(Map<Character, String> huffmanCodes) {
        HuffmanNode root = new HuffmanNode('\0', 0);
        
        for (Map.Entry<Character, String> entry : huffmanCodes.entrySet()) {
            HuffmanNode current = root;
            String code = entry.getValue();
            
            for (int i = 0; i < code.length(); i++) {
                char bit = code.charAt(i);
                
                if (bit == '0') {
                    if (current.left == null) {
                        current.left = new HuffmanNode('\0', 0);
                    }
                    current = current.left;
                } else {
                    if (current.right == null) {
                        current.right = new HuffmanNode('\0', 0);
                    }
                    current = current.right;
                }
            }
            
            current.character = entry.getKey();
        }
        
        return root;
    }

    public static boolean compareFiles(String file1, String file2) throws IOException {
        byte[] f1 = Files.readAllBytes(Paths.get(file1));
        byte[] f2 = Files.readAllBytes(Paths.get(file2));
        return Arrays.equals(f1, f2);
    }

    public static Map<Character, String> loadDictionary(String dictPath) throws IOException, ClassNotFoundException {
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream(dictPath))) {
            return (Map<Character, String>) ois.readObject();
        }
    }

    public static boolean isIntexte(String inputFile, String boutDetexte, String outputFile) {
        try {

            // Lire tout le contenu du fichier d'entrée
            String content = new String(Files.readAllBytes(Paths.get(inputFile)));;
            ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream(outputFile));
            
            // Vérifier si le texte recherché est présent
            int index = content.indexOf(boutDetexte);
            if (index == -1) {
                return false; // Texte non trouvé
            }
            
            // Mettre en valeur toutes les occurrences
            String highlightedContent = content.replace(boutDetexte, "**" + boutDetexte + "**");
            
            // Écrire dans le fichier de sortie
            oos.writeObject(highlightedContent);

            oos.close();
            
            return true;
            
        } catch (IOException e) {
            System.err.println("Erreur de traitement des fichiers: " + e.getMessage());
            return false;
        }
    }
    // public static void main(String[] args) {
        
    //     String text = "ABRACADABRA dho";
    //     Map<Character, Integer> result = countCharacterFrequency(text);
    //     HuffmanNode root = buildHuffmanTree(result);
    //     Map<Character, String> huffmanCode = new HashMap<>();
    //     generateHuffmanCodes(root, "", huffmanCode); 
        

    //     System.out.println("Codes Huffman générés :");
    //     for (Map.Entry<Character, String> entry : huffmanCode.entrySet()) {
    //         // if (huffmanCode.containsKey('A')) {
    //         //     System.out.println("yes contains A  valeur : "+huffmanCode.get('A'));
    //         // }
    //         System.out.println(entry.getKey() + " : " + entry.getValue());
    //     }
    //     // System.out.println('A' == 'a');
    //     String textecoder = encoder(huffmanCode, "BABA B");
    //     String retourTexteInitial = decode(root, textecoder);
    //     System.out.println(text+" : "+textecoder);
    //     System.out.println("texte "+textecoder+" decoder :"+ retourTexteInitial);
    //     // for (Map.Entry<Character, Integer> entry : result.entrySet()) {
    //     //     System.out.println(entry.getKey() + " : " + entry.getValue());
    //     // }
    // }
}
