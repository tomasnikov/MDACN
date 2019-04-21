import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Main {

    public static void main(String[] args) {
        fixList();
    }

    public static void fixNames() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader("LanguageNamesOld.csv"));
            ArrayList<String> names = new ArrayList<>();

            String line;
            while ((line = reader.readLine()) != null) {
                names.add(line);
            }

            FileWriter writer = new FileWriter("LanguageNames.csv");

            for (String s : names) {
                String newstring = s.substring(s.indexOf(">")+1, s.indexOf("</"));
                writer.append(newstring);
                writer.append("\n");
            }

            writer.flush();
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static double getSimilarity(String lang1, String lang2) {
        String urlName = "http://www.elinguistics.net/Compare_Languages.aspx?Language1=" + lang1 + "&Language2=" + lang2 + "&Order=Calc";

        try {
            URL nosSite = new URL(urlName);
            BufferedReader in = new BufferedReader(
                    new InputStreamReader(nosSite.openStream())
            );
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                if (inputLine.contains("The genetic proximity between")) {
                    break;
                }
            }
            in.close();

            String resultString = inputLine.substring(inputLine.indexOf("</font><font size=4><b>")+23, inputLine.indexOf("</b></font></td></tr><tr>"));
            resultString = resultString.replace(",", ".");

            return Double.parseDouble(resultString);
        } catch (Exception e) {
            e.printStackTrace();
        }

        return -1;
    }

    public static void createAllComparisons() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader("LanguageNames.csv"));
            ArrayList<String> names = new ArrayList<>();

            String line;
            while ((line = reader.readLine()) != null) {
                names.add(line);
            }

            double[][] similarities = new double[names.size()][names.size()];

            for (int i = 0; i < names.size(); i++) {
                for (int j = 0; j < i; j++) {
                    similarities[i][j] = similarities[j][i];
                }

                similarities[i][i] = 1;

                for (int j = i+1; j < names.size(); j++) {
                    similarities[i][j] = getSimilarity(names.get(i), names.get(j));

                    System.out.println("i: " + i + " j: " + j + " value: " + similarities[i][j]);
                }
            }

            FileWriter writer = new FileWriter("LanguageSimilarities.csv");

            for (int i = 0; i < names.size(); i++) {
                for (int j = 0; j < names.size(); j++) {
                    writer.append(Double.toString(similarities[i][j]));
                    if (j < names.size() - 1) {
                        writer.append(",");
                    }
                }

                writer.append("\n");
            }

            writer.flush();
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static void fixList() {
        try {
            BufferedReader reader = new BufferedReader(new FileReader("LanguageNames.csv"));
            ArrayList<String> names = new ArrayList<>();

            String line;
            while ((line = reader.readLine()) != null) {
                names.add(line);
            }

            double[][] similarities = new double[names.size()][names.size()];
            BufferedReader reader2 = new BufferedReader(new FileReader("LanguageSimilarities.csv"));

            int it = 0;
            while ((line = reader2.readLine()) != null) {
                similarities[it] = Arrays.stream(line.split(",")).mapToDouble(Double::parseDouble).toArray();
                it++;
            }

            for (int i = 0; i < names.size(); i++) {
                for (int j = 0; j < names.size(); j++) {
                    if (similarities[i][j] == 1) {
                        similarities[i][j] = 0;
                    }

                    similarities[i][j] = (100-similarities[i][j])/100;
                }
            }

            FileWriter writer = new FileWriter("LanguageSimilarities2.csv");

            for (int i = 0; i < names.size(); i++) {
                for (int j = 0; j < names.size(); j++) {
                    writer.append(Double.toString(similarities[i][j]));
                    if (j < names.size() - 1) {
                        writer.append(",");
                    }
                }

                writer.append("\n");
            }

            writer.flush();
            writer.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
