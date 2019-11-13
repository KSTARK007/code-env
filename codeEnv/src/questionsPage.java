

import java.io.IOException;
import java.net.URL;
import java.util.HashMap;
import java.util.Iterator;
import java.util.ResourceBundle;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

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

public class questionsPage implements Initializable {
	@FXML
	public ListView<AnchorPane> QuestionsList;

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		loadDefaultDisp();
		
	}
	
	public void loadDefaultDisp() {
		String serviceUrl =  "http://127.0.0.1:5000/codecouch/questions/";
		int start = -1;
		int last = 3;
		String faculty = "f1";
		String parameters = "Last="+start+"&Number="+last+"&Tag=&Faculty="+faculty;
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
		while(itr.hasNext()){         
		    obj = itr.next();
		    JSONObject question = (JSONObject) obj;
		    addProblem(question.get("name").toString(),question.get("tags").toString(),question.get("tags").toString());		    
		}	
	}
	
	public void addProblem(String name,String tags,String id) {
		
	
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
	            		solveCodeController.setQuestionId(id);
	            		
	            		Stage stage = new Stage();
	                    stage.setScene(new Scene(root));
	                    stage.setMaximized(true);
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
