import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.SQLException;
import java.util.Arrays;
import java.util.List;

import javax.imageio.ImageIO;

import org.json.*;
import support.thumbnailator.*;

public class Main {

    public static void main(String[] args) {
        int imagesWidth = 40;
        int imagesHeight = 40;
        boolean crop = false;

        int type = BufferedImage.TYPE_BYTE_GRAY;
        //should keep this like it is or stull won't work.

        String query = "cup";
        String startIndex = "1"; //to get more than 10 results have to make this call multiple times incrementing this by 10

        String googleUrl = "https://www.googleapis.com/customsearch/v1";
        String apikey = "AIzaSyDT7BAVflA3acD1XGrzqvnG5uyXATtW6F0";
        String cxcode = "012863778237739576778%3Akci5_jubz7g";
        String colourType = "gray"; //Returns black and white, grayscale, or color images: mono, gray, and color. (string)
        String searchString = googleUrl + "?q=" + query + "&cx=" + cxcode + "&imgColorType=" + colourType + "&safe=high&searchType=image&start=" + startIndex + "&key=" + apikey;

        String jsonResultString = "";

        boolean isCashed = false;
        Path p = Paths.get(System.getProperty("user.dir") + "/../assets/previousSearches.txt");
        System.out.print(p.toString());
        System.out.println("Loading:" + p.toAbsolutePath());
        try {
            List<String> cash = Files.readAllLines(p);

            for (int i = 0; i < cash.size(); i++) {
                String line = cash.get(i);
                if (line.contains(searchString)) {
                    System.out.println("Found Search in Cache");
                    jsonResultString = cash.get(i + 1);
                    isCashed = true;
                    break;
                }
            }
        } catch (IOException e) {
            print("Cannot open cache!");
            e.printStackTrace();
            //at this point I don't want to continue if there is an issue with the cache.
            return;
        }

        if (!isCashed) {
            System.out.print("Performing search");
            try {
                URL url = new URL(searchString);

                URLConnection connection = url.openConnection();

                String line;
                StringBuilder builder = new StringBuilder();

                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                while ((line = reader.readLine()) != null) {
                    builder.append(line);
                }

                jsonResultString = builder.toString();

                try (PrintWriter out = new PrintWriter(new BufferedWriter(new FileWriter(System.getProperty("user.dir") + "/../assets/previousSearches.txt", true)))) {
                    out.println(searchString);
                    out.println(jsonResultString);
                } catch (IOException e) {
                    System.out.println("Error with cache file!");
                    e.printStackTrace();
                    //we do not return at this point because at this point we've already used the unit query quota
                }
            } catch (MalformedURLException e) {
                print("Something is wrong with the URL for the search: "+searchString);
                e.printStackTrace();
                return;
            } catch (IOException e) {
                print("Something went wrong with the return connection.");
                e.printStackTrace();
                return;
            }

        }

        if (!jsonResultString.equals("")) {
            JSONObject json = new JSONObject(jsonResultString);
            print("Json object:" + json);
            print(Arrays.toString(json.keySet().toArray()));
            print(json.getJSONArray("items").getJSONObject(0).getString("link"));
            print(Arrays.toString(json.getJSONArray("items").getJSONObject(0).keySet().toArray()));

            String setName = colourType + "-" + imagesWidth + "x" + imagesHeight + "-" + query;

            DatabaseAdaptor adaptor = null;
            try {
                adaptor = new DatabaseAdaptor();
                adaptor.createTrainingSet(setName, imagesHeight,imagesWidth);
            } catch (SQLException e) {
                if(e.getMessage().contains("Cannot have duplicate set names")){
                    print("Set in DB, adding to set");
                } else {
                    print("Error with database!");
                    e.printStackTrace();
                }
            }

            for (int i = 0; i < json.getJSONArray("items").length(); i++) {
                String imageUrl = json.getJSONArray("items").getJSONObject(i).getString("link");
                try {
                    BufferedImage image = ImageIO.read(new URL(imageUrl));

                    if (image.getHeight() == 0 || image.getWidth() == 0) {
                        continue;
                    }

                    BufferedImage convertedImg = new BufferedImage(image.getWidth(), image.getHeight(), type);
                    convertedImg.getGraphics().drawImage(image, 0, 0, null);

                    int colour = convertedImg.getRGB(0,0)& 0xFF;
                    for (int j = 0; j < convertedImg.getWidth(); j++) {
                        if(colour != (convertedImg.getRGB(0,0)& 0xFF)) {
                            break;
                        }
                        for (int k = 0; k < convertedImg.getHeight(); k++) {
                            if(colour != (convertedImg.getRGB(j,k)& 0xFF)){
                                colour = convertedImg.getRGB(j,k)& 0xFF;
                                break;
                            }
                        }
                    }
                    if (colour != (convertedImg.getRGB(0,0)& 0xFF)) {
                        //there is content in this image
                        BufferedImage resizedImage = getResizedImage(convertedImg, imagesWidth, imagesHeight, crop);

                        float[] data = new float[resizedImage.getWidth()*resizedImage.getHeight()];
                        int index=0;
                        for (int j = 0; j < resizedImage.getWidth(); j++) {
                            for (int k = 0; k < resizedImage.getHeight(); k++) {
                                data[index] = new Float(resizedImage.getRGB(j,k)& 0xFF)/255;
                                index++;
                            }
                        }

                        try {
                            if(adaptor!=null)  adaptor.storeTrainingCase(setName, data);
                        } catch (SQLException e){
                            print("SQL exception while trying to store case: "+e.getMessage());

                            e.printStackTrace();
                        }
                        int offset = 0;
                        try {
                            offset = Integer.parseInt(startIndex);
                        } catch(NumberFormatException e){
                            print("Error in start index, not an int: "+startIndex);
                        }
                        File outputfile = new File(System.getProperty("user.dir") + "/../assets/images/" + colourType +"-"+resizedImage.getWidth()+"x"+resizedImage.getHeight()+"-"+query + (i+offset)+".png");
                        ImageIO.write(resizedImage, "png", outputfile);


                    }
                } catch(MalformedURLException e) {
                    print("Bad URL for search: "+imageUrl);
                    e.printStackTrace();
                } catch (IOException e) {
                    print("Error in writing image! "+imageUrl);
                    e.printStackTrace();
                } catch(Exception e){
                    print("Error! "+e.getMessage() );
                    e.printStackTrace();
                }
            }


        } else {
            System.out.println("Could not get JSON string");
        }


    }



    public static void print(Object s) {
        System.out.println(s);
    }

    private static BufferedImage getResizedImage(BufferedImage srcImg, int w, int h, boolean crop) throws IOException {
        try {
            float scale = new Float(h) / srcImg.getHeight();

            if (crop) {
                if (new Float(w) / srcImg.getWidth() > scale) {
                    scale = new Float(w) / srcImg.getWidth();
                }
            } else {
                if (new Float(w) / srcImg.getWidth() < scale) {
                    scale = new Float(w) / srcImg.getWidth();
                }
            }

            int width = Math.round(srcImg.getWidth() * scale);
            int height = Math.round(srcImg.getHeight() * scale);

            BufferedImage resizedImg = Thumbnails.of(srcImg)
                    .size(width, height)
                    .asBufferedImage();

            if (crop) {
                resizedImg = resizedImg.getSubimage(width / 2 - w / 2, height / 2 - h / 2, w, h);
                return resizedImg;
            } else {

                BufferedImage newImage = new BufferedImage(w, h, resizedImg.getType());

                Graphics g = newImage.getGraphics();

                g.setColor(Color.white);
                g.fillRect(0, 0, w, h);
                g.drawImage(resizedImg, w / 2 - resizedImg.getWidth() / 2, h / 2 - resizedImg.getHeight() / 2, null);
                g.dispose();

                return newImage;
            }

        } catch (IOException e) {
            throw e;
        }
    }

}