import java.util.Map;

public class Main {
    public static void main(String[] args) {
        String inputFile = "input.txt";
        String compressedFile = "compressed.huff";
        String dicoFile = "dico.huff";
        String misenvaleur = "misvaleur.txt";
        String decompressedFile = "decompressed.txt";

        try {
            Huff.compressFile(inputFile, compressedFile,dicoFile);


            // Huff.decompressFile(compressedFile, decompressedFile,dicoFile);
    
            Map<Character, String> huffmanCodes = Huff.loadDictionary(dicoFile);
            HuffmanNode root = Huff.rebuildHuffmanTree(huffmanCodes);

            for (Map.Entry<Character, String> entry : huffmanCodes.entrySet()) {
                        // if (huffmanCode.containsKey('A')) {
                        //     System.out.println("yes contains A  valeur : "+huffmanCode.get('A'));
                        // }
                        System.out.println(entry.getKey() + " : " + entry.getValue());
            }

            String encoder = Huff.encoder(huffmanCodes, "raha makany ela");
            System.out.println("binary : "+encoder);
            String decoder = Huff.decode(root, "011000001110001111101000100001100101011110000111100");
            System.out.println(decoder);
            // if (Huff.compareFiles(inputFile, decompressedFile)) {
            //     System.out.println("Compression/décompression réussie !");
            //     System.out.println(decoder);
            //     System.out.println(encoder);

            // boolean found = Huff.isIntexte(inputFile, decoder, misenvaleur);

            // if (found) {
            //     System.out.println("Texte trouvé et mis en valeur dans le fichier de sortie");
            // } else {
            //     System.out.println("Texte non trouvé, fichier de sortie inchangé");
            // }
            // } else {
                // System.out.println("Erreur lors de la compression/décompression");
            // }            
        } catch (Exception e) {
            System.out.println(e);
        }

    }
}
