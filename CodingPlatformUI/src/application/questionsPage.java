package application;

import java.net.URL;
import java.util.ResourceBundle;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.geometry.Insets;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.Background;
import javafx.scene.layout.BackgroundFill;
import javafx.scene.layout.ColumnConstraints;
import javafx.scene.layout.CornerRadii;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.HBox;
import javafx.scene.layout.Priority;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text;

public class questionsPage implements Initializable {
	@FXML
	public ListView<GridPane> QuestionsList;

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		
		GridPane h1;
		Text q1;
		Button b1;
		String[] questions = {"Say \"Hello, World!\" with C++",
				"Input and Output",
				"Basic Data Types",
				"Conditional Statements",
				"For Loop",
				"Functions",
				"Pointer",
				"Arrays Introduction",
				"Variable Sized Arrays",
				"Attribute Parser"
				};
		for(int i=0;i<10;i++)
		{
			h1 = new GridPane();
			ColumnConstraints leftCol = new ColumnConstraints();
	        leftCol.setHgrow(Priority.ALWAYS);
	        h1.getColumnConstraints().addAll(leftCol, new ColumnConstraints(), new ColumnConstraints());
			BackgroundFill background_fill = new BackgroundFill(Color.WHITE,  CornerRadii.EMPTY, Insets.EMPTY);
			Background background = new Background(background_fill); 
			h1.setBackground(background); 
			h1.setPrefHeight(80);
			//h1.setPadding(new Insets(2));
	        //h1.setPadding(new Insets(15,50, 10,30));
	        q1 = new Text();
			
			//q1.setPrefHeight(50);  //sets height of the TextArea to 400 pixels 
			//textArea.setPrefWidth(width);    //sets width of the TextArea to 300 pixels
			
			//q1.setEditable(false);
			
			q1.setText(questions[i]);
			q1.setFont(Font.font("", FontWeight.BOLD, 25));
			
			
			b1 = new Button("Solve Problem");
			//b1.setPadding(new Insets(15,20, 10,10));
			
			h1.add(q1,0,0);
			h1.add(b1,1,0);
			//b1.setLayoutX(300);
			//b1.setLayoutY(30);
			QuestionsList.getItems().add(h1);
		}
		
		
		
		
		
		/*
		 * GridPane h2 = new GridPane(); h2.getColumnConstraints().addAll(leftCol, new
		 * ColumnConstraints(), new ColumnConstraints()); h2.setBackground(background);
		 * h2.setPrefHeight(80); Text q2 = new Text("Conditional Statements");
		 * q2.setFont(Font.font("", FontWeight.BOLD, 30));
		 * 
		 * Button b2 = new Button("Solve Problem");
		 * 
		 * b1.setStyle("-fx-text-fill: White");
		 * b1.setStyle("-fx-background-color: MediumSeaGreen");
		 * //b2.setStyle("-fx-border-color: #ff0000; -fx-border-width: 5px;");
		 * //b1.setStyle("-fx-background-color: #90FF33");
		 * b2.setStyle("-fx-background-color: MediumSeaGreen"); h2.add(q2,0,0);
		 * 
		 * h2.add(b2,1,0);
		 */
		
		//QuestionsList.getItems().add(h2);
		
	}
}
