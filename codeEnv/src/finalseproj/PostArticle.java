///*
// * To change this license header, choose License Headers in Project Properties.
// * To change this template file, choose Tools | Templates
// * and open the template in the editor.
// */
//package postarticle;
//
//import java.io.IOException;
//import javafx.application.Application;
//import javafx.event.ActionEvent;
//import javafx.event.EventHandler;
//import javafx.fxml.FXML;
//import javafx.fxml.FXMLLoader;
//import javafx.scene.Parent;
//import javafx.scene.Scene;
//import javafx.scene.control.Button;
//import javafx.scene.control.ComboBox;
//import javafx.scene.layout.StackPane;
//import javafx.stage.Stage;
//
///**
// *
// * @author hemu
// */
//public class PostArticle extends Application {
//    @FXML
//    private ComboBox<String> languages;
//    @Override
//    public void start(Stage primaryStage) throws IOException { 
//       /* try {
//		//Load external fxml file 
//		Parent root = FXMLLoader.load(getClass().getClassLoader().getResource("postArticlePage.fxml"));
//		Scene scene = new Scene(root);
//		//scene.getStylesheets().add(getClass().getResource("postarticlepage.css").toExternalForm());
//		primaryStage.setTitle("Upload Articles");
//		primaryStage.setMaximized(true);
//		primaryStage.setScene(scene);
//		primaryStage.show();
//		
//        } catch(Exception e) {
//                System.out.print("ikkada dobindi");
//                
//                
//		e.printStackTrace();
//	}*/
//        
//        FXMLLoader loader = new FXMLLoader(getClass().getResource("postArticlePage.fxml"));
//        Parent root = loader.load();
//        PostArticlePageController postArticlePageController = loader.getController();
//        System.out.println("Here2");   
//        Scene scene = new Scene(root);
//        scene.getStylesheets().add(getClass().getResource("postarticlepages.css").toExternalForm());
//        primaryStage.setTitle("Post articles");
//        primaryStage.setMaximized(true);
//        primaryStage.setScene(scene);
//        primaryStage.show();
//     };
//    
//
//    /**
//     * @param args the command line arguments
//     */
//    public static void main(String[] args) {
//        launch(args);
//    }
//    
//}


/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

package finalseproj;

import finalseproj.PostArticlePageController;
import java.io.IOException;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.layout.StackPane;
import javafx.stage.Stage;

/**
 *
 * @author hemu
 */
public class PostArticle extends Application {
    
    @Override
    public void start(Stage primaryStage) throws IOException {

        
        FXMLLoader loader = new FXMLLoader(getClass().getResource("postArticlePage.fxml"));
        Parent root = loader.load();
        PostArticlePageController postArticlePageController = loader.getController();
        System.out.println("Here2");   
        Scene scene = new Scene(root);
        scene.getStylesheets().add(getClass().getResource("postarticlepage.css").toExternalForm());
        primaryStage.setTitle("Post articles");
        primaryStage.setMaximized(true);
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        launch(args);
    }
    
}
