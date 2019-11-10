package application;
	
import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.layout.*; 
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.Group; 
import javafx.scene.control.*; 
//import javafx.scene.layout.BorderPane;


public class Main extends Application {
	@FXML
	private ComboBox<String> languages;
	
	@Override
	public void start(Stage primaryStage) {
		try {
			
			//Load external fxml file 
			Parent root = FXMLLoader.load(getClass().getClassLoader().getResource("SolveCode.fxml"));			
			//Parent root = FXMLLoader.load(getClass().getClassLoader().getResource("DisplayQuestions.fxml"));
			
			
			
			
			
			Scene scene = new Scene(root);
			scene.getStylesheets().add(getClass().getResource("application.css").toExternalForm());
			primaryStage.setTitle("Coding Platform");
			//primaryStage.setFullScreen(true);
			primaryStage.setMaximized(true);
			primaryStage.setScene(scene);
			primaryStage.show();
		} catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		launch(args);
	}
}
