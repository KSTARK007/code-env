import java.io.IOException;
import java.util.Iterator;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;

import com.sun.org.apache.xerces.internal.impl.xpath.regex.ParseException;

import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.geometry.HPos;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.stage.Window;
import rest.RestClient;

public class LoginFormApplication extends Application {

    private Stage stage;
    public String usn;

	@Override
    public void start(Stage primaryStage) throws Exception {
    	
    	this.stage = primaryStage;
        primaryStage.setTitle("Login Form JavaFX Application");

        // Create the registration form grid pane
        GridPane gridPane = createRegistrationFormPane();
        // Add UI controls to the registration form grid pane
        addUIControls(gridPane);
        // Create a scene with registration form grid pane as the root node
        Scene scene = new Scene(gridPane, 800, 500);
        // Set the scene in primary stage	
        primaryStage.setScene(scene);
        
        primaryStage.show();
    }


    private GridPane createRegistrationFormPane() {
        // Instantiate a new Grid Pane
        GridPane gridPane = new GridPane();

        // Position the pane at the center of the screen, both vertically and horizontally
        gridPane.setAlignment(Pos.CENTER);

        // Set a padding of 20px on each side
        gridPane.setPadding(new Insets(40, 40, 40, 40));

        // Set the horizontal gap between columns
        gridPane.setHgap(10);

        // Set the vertical gap between rows
        gridPane.setVgap(10);

        // Add Column Constraints

        // columnOneConstraints will be applied to all the nodes placed in column one.
        ColumnConstraints columnOneConstraints = new ColumnConstraints(100, 100, Double.MAX_VALUE);
        columnOneConstraints.setHalignment(HPos.RIGHT);

        // columnTwoConstraints will be applied to all the nodes placed in column two.
        ColumnConstraints columnTwoConstrains = new ColumnConstraints(200,200, Double.MAX_VALUE);
        columnTwoConstrains.setHgrow(Priority.ALWAYS);

        gridPane.getColumnConstraints().addAll(columnOneConstraints, columnTwoConstrains);

        return gridPane;
    }

    private void addUIControls(GridPane gridPane) {
        // Add Header
        Label headerLabel = new Label("Login Form");
        headerLabel.setFont(Font.font("Arial", FontWeight.BOLD, 24));
        gridPane.add(headerLabel, 0,0,2,1);
        GridPane.setHalignment(headerLabel, HPos.CENTER);
        GridPane.setMargin(headerLabel, new Insets(20, 0,20,0));
        
        // Add SRN Label
        Label srnLabel = new Label("SRN : ");
        gridPane.add(srnLabel, 0,3);

        // Add SRN Text Field
        TextField srnField = new TextField();
        srnField.setPrefHeight(40);
        gridPane.add(srnField, 1,3);


        // Add Password Label
        Label passwordLabel = new Label("Password : ");
        gridPane.add(passwordLabel, 0, 4);

        // Add Password Field
        PasswordField passwordField = new PasswordField();
        passwordField.setPrefHeight(40);
        gridPane.add(passwordField, 1, 4);
     
        // Add Submit Button
        Button submitButton = new Button("Submit");
        submitButton.setPrefHeight(40);
        submitButton.setDefaultButton(true);
        submitButton.setPrefWidth(100);
        gridPane.add(submitButton, 0, 6, 2, 1);
        GridPane.setHalignment(submitButton, HPos.CENTER);
        GridPane.setMargin(submitButton, new Insets(20, 0,20,0));

        submitButton.setOnAction(new EventHandler<ActionEvent>() {
            @Override
            public void handle(ActionEvent event) {
          
                if(passwordField.getText().isEmpty()) {
                    showAlert(Alert.AlertType.ERROR, gridPane.getScene().getWindow(), "Form Error!", "Please enter a password");
                    return;
                }
                if(srnField.getText().isEmpty()) {
                    showAlert(Alert.AlertType.ERROR, gridPane.getScene().getWindow(), "Form Error!", "Please enter your SRN");
                    return;
                }
                
                int val = login(srnField.getText(), passwordField.getText());
                
//                if(val==0)
//                showAlert(Alert.AlertType.CONFIRMATION, gridPane.getScene().getWindow(), "Login Successful!", "Welcome Student");
//                
//                else if(val==1)
//                	showAlert(Alert.AlertType.CONFIRMATION, gridPane.getScene().getWindow(), "Login Successful!", "Welcome Faculty");
//                
                if(val<0)
                	showAlert(Alert.AlertType.CONFIRMATION, gridPane.getScene().getWindow(), "Login Unsuccessful!", "Try Again");
                
                
                if(val>=0) {
                	try {
                		System.out.println("HEREE");
                		stage.close();
  	            		FXMLLoader loader = new FXMLLoader(getClass().getResource("DisplayQuestions.fxml"));
  	            		Parent root = loader.load();
  	            		questionsPage questionsPageController = loader.getController();
  	            		questionsPageController.setUsn(usn);
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
            }
        });
    }

    private void showAlert(Alert.AlertType alertType, Window owner, String title, String message) {
        Alert alert = new Alert(alertType);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.initOwner(owner);
        alert.show();
    }
    
    public int login(String srn,String pwd) {
		String serviceUrl =  "http://127.0.0.1:5000/codecouch/login/";
		String parameters = "Usn="+srn+"&Password="+pwd;
		String GET = "GET";
		String POST = "POST";
		
		JSONParser parser = new JSONParser(); 
		RestClient client = new RestClient(serviceUrl, parameters, GET);
		client.run();
		

		this.usn = srn;
		
		Object obj = null;
		
		try {
			obj = parser.parse(client.finalOutputString);
		} catch (org.json.simple.parser.ParseException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		System.out.println(client.finalOutputString);
		
		
		JSONArray responseArray =  (JSONArray) obj;
		
		int val = Integer.parseInt((String) responseArray.get(0));
				
		return val;
	}

    public static void main(String[] args) {
        launch(args);
    }
    
}
