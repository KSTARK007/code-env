
/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package finalseproj;

import java.io.IOException;
import rest.RestClient;
import java.net.URL;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.ResourceBundle;
import java.util.logging.Level;
import java.util.logging.Logger;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.event.EventType;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import org.json.simple.JSONArray; 
import org.json.simple.JSONObject; 
import org.json.simple.parser.*;
/**
 * FXML Controller class
 *
 * @author hemu
 */
public class ArticlesPageController implements Initializable {

    /**
     * Initializes the controller class.
     * @param url
     * @param rb
     */
    
//    
    @FXML
    VBox buttonBox;
    
//    @FXML
//    Label articleContentLabel;
    
    @FXML
    TextField searchArticleName; //contains the text of the article to be searched
    
    @FXML
    Button postArticleButton ,searchArticleButton; //button to search article
    
    @FXML
    ScrollPane masterScrollPane;
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        //make a get request with a default search key initially (search word data)
    
        makeGetRequest("Array");
    
        masterScrollPane.setHbarPolicy(ScrollPane.ScrollBarPolicy.NEVER);
       
        //start of post an article Event
        EventHandler<ActionEvent> postArticleEvent = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) { //articlePost
                //System.out.println("Article is boing posted");
                //make a post request
                try {
                    FXMLLoader loader1 = new FXMLLoader(getClass().getResource("postArticlePage.fxml"));
                    Parent root1 = loader1.load();  	            		
                    Stage stage1 = new Stage();
                    stage1.setScene(new Scene(root1));
                    stage1.setMaximized(true);
                    stage1.setTitle("Post article");
                    stage1.show();
                    //Stage st = (Stage) solveButton.getScene().getWindow();
                    //st.close();
                } catch (IOException e1) {
                    // TODO Auto-generated catch block
                    e1.printStackTrace();
                }
                //Label conf = new Label("Article has been posted successfully");
                //masterScrollPane.setContent(conf);
            }
        };
        postArticleButton.setOnAction(postArticleEvent);
        //end of post a handler event
        
        
        //start of search an article Event
        EventHandler<ActionEvent> searchArticleEvent = new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) { //articlePost
                //System.out.println("Article is boing posted");
                String schStr = searchArticleName.getText();
                
                System.out.println("schStr is "+schStr);
                
                //make a get request
                Label emptyLabel = new  Label("");
         
                masterScrollPane.setContent(emptyLabel);
                makeGetRequest(schStr);
                
                //Label conf = new Label("Article has been posted successfully");
                //masterScrollPane.setContent(conf);
            }
        };
        searchArticleButton.setOnAction(searchArticleEvent);
        //end of search a handler event
        
        
        //System.out.println("Controller init called");
        Integer numberOfArticles = 5;
        
        
        
    }    
    
    String getNameOfArticle() { //add any parameters if required here
        return "Article";
    }
    
    
    //*******************************************************************
    //*******************************************************************
    //*******************************************************************
    //*******************************************************************
    //Make the get request for the article search
    public void makeGetRequest(String p) {
        //System.out.print(p);
        String getUrl = "http://localhost:5001/getfile/";
        getUrl+=p; //initially show data ablout a linked list (just to simulate a non empty articles page)
        String parameters = ""; //search for data initially
        
        JSONParser parser = new JSONParser(); 
	RestClient client = new RestClient(getUrl, parameters, "GET");
        client.run();
        Object obj = null;
        String es = client.finalOutputString;
        if(es.charAt(2)== 'e' && es.charAt(3)== 'r' && es.charAt(4)== 'r' && es.charAt(5)== 'o' && es.charAt(6)== 'r')
            return;
         
          try {
            //auto removal of previous existing catch block by eclipse
            obj = parser.parse(client.finalOutputString); // TODO Auto-generated catch block
        } catch (ParseException ex) {
            //System.out.println("In the catch, data has not been fetched!!");
            Logger.getLogger(ArticlesPageController.class.getName()).log(Level.SEVERE, null, ex);
        }
        //System.out.println("Did not go to catch");
        //articleContentLabel.setText(client.finalOutputString);
        //System.out.println(client.finalOutputString);
        
        
        JSONObject jsonObject = (JSONObject) obj;
        
        Iterator<String> keys;
        // Iterator<String> keys = (Iterator<String>) jsonObject.keySet();
        keys = (Iterator<String>) jsonObject.keySet().iterator();
       
        String completeArticleContent = ""; //this is the article that is displayed
        
        //create a Vbox that is appended to the scroll pane
        VBox vbox = new VBox();
        
       
        while(keys.hasNext()) {
            String key = (String) keys.next();
            Map article = (Map)jsonObject.get(key);
            Iterator<String> articleKeys;
            articleKeys = (Iterator<String>) article.keySet().iterator();
            while(articleKeys.hasNext()) {
                String articleKey = (String)articleKeys.next();
                String articleValue = (String)article.get(articleKey);
                
                completeArticleContent += articleKey;
                completeArticleContent += ":\n";
                completeArticleContent += articleValue;
                completeArticleContent += "\n\n";
                //System.out.println(completeArticleContent);
                Label contentLabel = new Label(completeArticleContent); 
                contentLabel.setPrefWidth(950);
                contentLabel.setWrapText(true);
                vbox.getChildren().add(contentLabel);
                completeArticleContent = "";
                
                
            }
            Label paddingLabel = new  Label("          ");
            paddingLabel.setPrefSize(1000, 80);
            vbox.getChildren().add(paddingLabel);
            
        }
        masterScrollPane.setContent(vbox);
    }
    
}
