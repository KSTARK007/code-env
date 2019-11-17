

import java.io.IOException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.ResourceBundle;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

import com.sun.glass.events.MouseEvent;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.ColumnConstraints;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontPosture;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;
import javafx.stage.Stage;
import rest.RestClient;
import finalseproj.*;
public class questionsPage implements Initializable {
	@FXML
	public ListView<AnchorPane> QuestionsList;
	
	@FXML
	public Button previous;
	@FXML
	public Button next;
	@FXML
	public Button profile,articles;
	
	int firstId = 0,lastId = 10,perPageQuestions=10;
	
	public String usn;
	
	public void setUsn(String usn) {
		this.usn = usn;
		System.out.println(this.usn);
	}
	
	@Override
	public void initialize(URL location, ResourceBundle resources) {
		loadQuestions(firstId,lastId,0);
		
		//Event handler for previous button
		EventHandler<ActionEvent> previousButtonEvent = new EventHandler<ActionEvent>() { 
            public void handle(ActionEvent e) 
            { 
            	if(firstId>0)
            	{	
            		QuestionsList.getItems().clear();
            		firstId-=perPageQuestions;	            	
	            	lastId-=perPageQuestions;
	            	loadQuestions(firstId,lastId,0);
	            	
            	}
            } 
        };
       
        previous.setOnAction(previousButtonEvent);
        
      //Event handler for next button
      		EventHandler<ActionEvent> nextButtonEvent = new EventHandler<ActionEvent>() { 
                  public void handle(ActionEvent e) 
                  {                                     		
                  		firstId+=perPageQuestions;	            	
      	            	lastId+=perPageQuestions;
      	            	int res = loadQuestions(firstId,lastId,1);
      	            	
      	            	/*
      	            	 * If  page was not updated then undo updation*/
      	            	if(res==0)
      	            	{
      	            		firstId-=perPageQuestions;	            	
          	            	lastId-=perPageQuestions;
          	            	System.out.println("Debug: Page didn't update\n");
      	            	}
      	           	
                  	}                  
              };
              next.setOnAction(nextButtonEvent);
              
            
              EventHandler<ActionEvent> profileButtonEvent = new EventHandler<ActionEvent>() {
            	  @Override
                  public void handle(ActionEvent e) 
                  {                                     		
            		  try {
  	            		FXMLLoader loader = new FXMLLoader(getClass().getResource("Main.fxml"));
  	            		Parent root = loader.load();  	            		
  	            		Stage stage = new Stage();
  	                    stage.setScene(new Scene(root));
  	                    stage.setMaximized(true);
  	                    stage.setTitle("Profile");
  	                    stage.show();
  	                    //Stage st = (Stage) solveButton.getScene().getWindow();
  	                    //st.close();
  					} catch (IOException e1) {
  						// TODO Auto-generated catch block
  						e1.printStackTrace();
  					}
                      	
                  	}                  
              };
              
              
              profile.setOnAction(profileButtonEvent);
              
              EventHandler<ActionEvent> articleButtonEvent = new EventHandler<ActionEvent>() {
            	  @Override
            	  
                  public void handle(ActionEvent e) 
                  {                                     		
            		  try {
            			  FXMLLoader loader = new FXMLLoader(getClass().getResource("finalseproj/articlesPage.fxml"));
            		        Parent root = loader.load();
            		        ArticlesPageController articlesPageController = loader.getController();
            		        System.out.println("Here2");   
            		        Scene scene = new Scene(root);
            		        scene.getStylesheets().add(getClass().getResource("finalseproj/articlespage.css").toExternalForm());
            		        Stage primaryStage = new Stage();
            		        primaryStage.setTitle("Articles");
            		        primaryStage.setScene(scene);
            		        primaryStage.show();
  					} catch (IOException e1) {
  						// TODO Auto-generated catch block
  						e1.printStackTrace();
  					}
                      	
                  	}                  
              };
              
              articles.setOnAction(articleButtonEvent);
            
	}
	/*
	 * 
	 * */
  

	
	public int loadQuestions(int first,int last,int testForClear) {
		String serviceUrl =  "http://127.0.0.1:5000/codecouch/questions/";
		String faculty = "f1";
		String parameters = "First="+first+"&Number="+last+"&Tag=&Faculty=";
		String GET = "GET";
		String POST = "POST";
		
		JSONParser parser = new JSONParser(); 
		RestClient client = new RestClient(serviceUrl, parameters, GET);
		client.run();
		
		Object obj = null;
		
		try {
			obj = parser.parse(client.finalOutputString);
		} catch (ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	
		
		JSONArray responseArray =  (JSONArray) obj;
		Iterator<String> itr = responseArray.iterator();
		if(testForClear==1)
		{
			if(responseArray.size()==0)
				return 0;
			else
			{
				QuestionsList.getItems().clear();
			}
		}
		
		while(itr.hasNext()){         
		    obj = itr.next();
		    JSONObject question = (JSONObject) obj;
		    addProblem(question.get("name").toString(),question.get("tags").toString(),question.get("id").toString());		    
		}	
		return 1;
	}

	public void addProblem(String name,String tags,String id) {
		System.out.println("id is "+id);
	
		AnchorPane anchorpane = new AnchorPane();
		
		//ColumnConstraints leftCol = new ColumnConstraints();
        //leftCol.setHgrow(Priority.ALWAYS);
        
        //gridpane.getColumnConstraints().addAll(leftCol, new ColumnConstraints(), new ColumnConstraints());
		
        BackgroundFill background_fill = new BackgroundFill(Color.WHITE,  CornerRadii.EMPTY, Insets.EMPTY);
		Background background = new Background(background_fill); 
		
		anchorpane.setBackground(background); 
		anchorpane.setPrefHeight(80);
		
		//gridpane.setPadding(new Insets(2));
        //gridpane.setPadding(new Insets(15,50, 10,30));
		
		Text questionName = new Text();
		
		//q1.setPrefHeight(50);  //sets height of the TextArea to 400 pixels 
		//textArea.setPrefWidth(width);    //sets width of the TextArea to 300 pixels		
		//q1.setEditable(false);	
		questionName.setText(name);
		questionName.setFont(Font.font("", FontWeight.BOLD, 25));
		Text Tags = new Text();
		
		Tags.setText(addHashTag(tags));
		Tags.setFont(Font.font("", FontPosture.ITALIC, 20));
		
		Button solveButton = new Button("Solve Problem");
		//b1.setPadding(new Insets(15,20, 10,10));
		EventHandler<ActionEvent> event = new EventHandler<ActionEvent>() { 
	            public void handle(ActionEvent e) 
	            { 
	            	try {
	            		FXMLLoader loader = new FXMLLoader(getClass().getResource("SolveCode.fxml"));
	            		Parent root = loader.load();
	            		SolveCodeController solveCodeController =  loader.getController();
	            		solveCodeController.setUsn(usn);
	            		solveCodeController.setQuestionId(id);
	            		
	            		Stage stage = new Stage();
	                    stage.setScene(new Scene(root));
	                    //stage.setMaximized(true);
	                    stage.setTitle("Solve code");
	                    stage.show();
	                    //Stage st = (Stage) solveButton.getScene().getWindow();
	                    //st.close();
					} catch (IOException e1) {
						// TODO Auto-generated catch block
						e1.printStackTrace();
					}
	            	
	            } 
	        };
	      //When button clicked, load window and pass data
	        solveButton.setOnAction(event);
		//gridpane.add(questionName,0,0);
		//gridpane.add(solveButton,1,0);
		//gridpane.add(Tags,0,10);
		//b1.setLayoutX(300);
		//b1.setLayoutY(30);
		//QuestionsList.getItems().add(gridpane);
	       AnchorPane.setTopAnchor(questionName, 5.0);
	       AnchorPane.setLeftAnchor(questionName, 10.0);
	       
	       AnchorPane.setRightAnchor(solveButton, 10.0);
	       AnchorPane.setTopAnchor(solveButton, 10.0);
	       
	       AnchorPane.setBottomAnchor(Tags, 10.0);
	       AnchorPane.setLeftAnchor(Tags, 10.0);
	       
	       anchorpane.getChildren().add(questionName);
	       anchorpane.getChildren().add(solveButton);
	       anchorpane.getChildren().add(Tags);
	       
	       QuestionsList.getItems().add(anchorpane);
	       
	}
	
	public String addHashTag(String tags) {
		if(tags.length()==0)
			return tags;
		else {
			String[] strArray = tags.split(" ");
			tags = "";
			for(String ele:strArray) {
				tags += ("#"+ele+" ");
			}
			return tags;
		}
	}
}
