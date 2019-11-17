package rest;
 
import java.io.File;
import java.io.IOException;
import java.util.List;
 
/**
 * This program demonstrates a usage of the MultipartUtility class.
 * @author www.codejava.net
 *
 */
public class MultipartFileUploader {
 
    public static void main(String[] args) {
        String charset = "UTF-8";
        File uploadFile1 = new File("/home/adarsh/eclipse-workspace/flask/test/ip1");
        File uploadFile2 = new File("/home/adarsh/eclipse-workspace/flask/test/op1");
        File uploadFile3 = new File("/home/adarsh/eclipse-workspace/flask/test/description");
        
        String requestURL = "http://127.0.0.1:5000/codecouch/question/";
 
        try {
            MultipartUtility multipart = new MultipartUtility(requestURL, charset);
             
            //multipart.addHeaderField("User-Agent", "CodeJava");
            //multipart.addHeaderField("Test-Header", "Header-Value");
             
            multipart.addFormField("Usn", "f1");
            multipart.addFormField("Question_name", "Binary");
            multipart.addFormField("Tags", "DS");
            multipart.addFilePart("ip1", uploadFile1);
            multipart.addFilePart("op1", uploadFile2);
            multipart.addFilePart("description", uploadFile3);
            
            List<String> response = multipart.finish();
             
            System.out.println("SERVER REPLIED:");
             
            for (String line : response) {
                System.out.println(line);
            }
        } catch (IOException ex) {
            System.err.println(ex);
        }
    }
}