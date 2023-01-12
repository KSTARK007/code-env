/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package finalseproj;

import java.net.URL;
import java.util.ResourceBundle;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import org.json.simple.parser.JSONParser;
import rest.RestClient;

/**
 * FXML Controller class
 *
 * @author hemu
 */
public class PostArticlePageController implements Initializable {

    /**
     * Initializes the controller class.
     */
    
    @FXML
    Button submitArticleBtn; //submit button
    @FXML
    TextField articleTitleTextArea; //article title
    @FXML
    TextArea articleTextArea; //article contents (data)
    @FXML
    TextArea articleCodeTextArea; //article code
    @FXML
    TextArea articleDataTextArea; //article 
    @FXML
    TextArea articleLinkTextArea; //links
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        // TODO
        System.out.print("Init function called\n");
        EventHandler<ActionEvent> submitArticle = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
                //add the post API call here
                //check if the data in the text area == NULL then add a default name (just to make things easy)
              
               
                System.out.println("Article is being posted");
                //articleTextArea.setText("Posting article");
                //remove  the below 2 lines of code
                
                String title = articleTitleTextArea.getText();
                String code = articleCodeTextArea.getText();
                String link = articleLinkTextArea.getText();
                String artCont = articleTextArea.getText();
//                System.out.println(title);
//                System.out.println(code);
//                System.out.println(link);
//                System.out.println(artCont);
                
                String getUrl = "http://localhost:5001/postfile/";
                getUrl = getUrl + title+";"+ artCont+";"+code+";"+link; 
                String parameters = ""; //search for data initially

                JSONParser parser = new JSONParser(); 
                RestClient client = new RestClient(getUrl, parameters, "GET");
                client.run();
                //add post request here
            }
        };
        submitArticleBtn.setOnAction(submitArticle);
    }    
    
}
//refer below for code snippets

//start of post an article Event
        
        //end of post a handler event
        
//        System.out.println("Controller init called");
//        Integer numberOfArticles = 5;
//        
//        
//        Button btnPostArticle = new Button();
//        btnPostArticle.setText("Post an article");
//        btnPostArticle.setOnAction(postArticleEvent);
//        buttonBox.getChildren().add(btnPostArticle);
//        
//        for(int i=0; i<numberOfArticles; ++i) {
//    
//            Button btn1 = new Button();
//            btn1.setText(getNameOfArticle());
//            btn1.setOnAction(event1);
//            buttonBox.getChildren().add(btn1);
//        }