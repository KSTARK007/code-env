
import java.awt.event.ActionEvent;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.net.URL;
import java.util.Iterator;
import java.util.ResourceBundle;


import com.sun.media.jfxmedia.Media;
import com.sun.media.jfxmedia.MediaPlayer;
import com.sun.prism.Image;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.image.ImageView;
import javafx.scene.media.MediaView;
import javafx.application.Application; 
import static javafx.application.Application.launch; 
import javafx.event.EventHandler;
 
import javafx.scene.Group; 
import javafx.scene.Scene; 
import javafx.scene.input.MouseEvent; 
import javafx.scene.paint.Color; 
import javafx.scene.shape.Circle; 

import javafx.scene.text.Font; 
import javafx.scene.text.FontWeight;
import javafx.scene.text.Text; 
import javafx.stage.Stage;
import rest.RestClient;
import javafx.application.Application;
import javafx.geometry.Rectangle2D;
import javafx.scene.Group;
import javafx.scene.Scene; 
import javafx.scene.layout.HBox;
import javafx.scene.paint.Color;
import javafx.stage.Stage; 
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.VBox;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.chart.BarChart;
import javafx.scene.chart.CategoryAxis;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.json.simple.JSONArray; 
import org.json.simple.JSONObject; 
import org.json.simple.parser.*;

public class MainController implements Initializable {
	@FXML
	private ImageView mv;
	@FXML
	private HBox div1;
	
	@FXML
	Button avgButton;
	
	@Override
	public void initialize(URL location, ResourceBundle resources) {
		// TODO Auto-generated method stub
		
//		EventHandler<MouseEvent> event1 = new EventHandler<MouseEvent>() {
//            @Override
//            public void handle(MouseEvent event) {
//            	Object obj = null;
//                System.out.println("Button clicked");

//				try {
//					obj = new JSONParser().parse(new FileReader("C:\\Users\\Iruvanti Aishwarya\\Desktop\\JSONExample.json"));
//				} catch (IOException | ParseException e) {
//					// TODO Auto-generated catch block
//					e.printStackTrace();
//				} 
				
				//Kavya
				String serviceUrl =  "http://127.0.0.1:5000/codecouch/student/analysis/s1";
				String parameters = "";
				JSONParser parser = new JSONParser(); 
				RestClient client = new RestClient(serviceUrl, parameters, "GET");
				client.run();
				
				Object obj = null;
				
				try {
					obj = parser.parse(client.finalOutputString);
				} catch (ParseException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				System.out.println(client.finalOutputString);
				
				//Kavya
				
				
                System.out.println("Button clicked");

                
                JSONObject jsonObject = (JSONObject) obj;
                Iterator<String> keys = (Iterator<String>) jsonObject.keySet().iterator();
                
            

               // Iterator<String> keys = (Iterator<String>) jsonObject.keySet();
                int i =1;
                while(keys.hasNext()) {
                    String key = (String) keys.next();
                    if (jsonObject.get(key) instanceof JSONObject) {
                          // do something with jsonObject here
                    	JSONObject abc = (JSONObject) jsonObject.get(key);
                        int avg = (int) (Float.parseFloat((String) abc.get("avg"))); 
                        int classavg = (int) (Float.parseFloat((String) abc.get("class_avg"))); 
//                        int score = ((Long)abc.get("score")).intValue();
                        String name = (String) abc.get("name"); 
                        VBox vb1 = new VBox();
                		
                		Label lb1 = new Label("Program: "+(String) abc.get("name"));
                		lb1.setId("lbtest"+i);
                		
                		Label lbscore = new Label("Score: "+(String)abc.get("score"));
                		lbscore.setId("lbscore"+i);
                		
                		Label lbavg = new Label("Avg: "+(String)abc.get("avg"));
                		lbavg.setId("lbscore"+i);
                		
                		Button buttonimage = new Button("PERFORMANCE COMPARISON");
                		buttonimage.setId("a3");
                		
                		CategoryAxis xAxis    = new CategoryAxis();
                        xAxis.setLabel("Devices");

                        NumberAxis yAxis = new NumberAxis();
                        yAxis.setLabel("Visits");

                        BarChart     barChart = new BarChart(xAxis, yAxis);

                        XYChart.Series dataSeries1 = new XYChart.Series();
                        dataSeries1.setName("2014");

                        dataSeries1.getData().add(new XYChart.Data("0-5", 567));
                        dataSeries1.getData().add(new XYChart.Data("5-10"  , 65));
                        dataSeries1.getData().add(new XYChart.Data("10-15"  , 123));
                        dataSeries1.getData().add(new XYChart.Data("15-20"  , 23));
                        dataSeries1.getData().add(new XYChart.Data("20-25"  , 223));
                        dataSeries1.getData().add(new XYChart.Data("25-30"  , 23));

                        barChart.getData().add(dataSeries1);

                		//Button button2 = new Button("Average");
                        vb1.getChildren().addAll(lb1,lbscore,lbavg,barChart);
                        div1.getChildren().add(vb1);



                        i = i+1;
                      
                        

                    }
                }

              //throw new UnsupportedOperationException("Not supported yet."); //To change body of generated methods, choose Tools | Templates.
                System.out.println("Button clicked");
              //  int n = 5; //get from server
                /*
        		for(int i=0;i<n;i++) {
        		VBox vb1 = new VBox();
        		
        		Label lb1 = new Label("test"+i);
        		lb1.setId("lbtest"+i);
        		
        		Label lbscore = new Label("score:"+50);
        		lbscore.setId("lbscore"+i);
        		
        		Label lbavg = new Label("Avg"+50);
        		lbavg.setId("lbscore"+i);
        		
        		Button buttonimage = new Button("PERFORMANCE COMPARISON");
        		buttonimage.setId("a3");
        		
        		CategoryAxis xAxis    = new CategoryAxis();
                xAxis.setLabel("Devices");

                NumberAxis yAxis = new NumberAxis();
                yAxis.setLabel("Visits");

                BarChart     barChart = new BarChart(xAxis, yAxis);

                XYChart.Series dataSeries1 = new XYChart.Series();
                dataSeries1.setName("2014");

                dataSeries1.getData().add(new XYChart.Data("0-5", 567));
                dataSeries1.getData().add(new XYChart.Data("5-10"  , 65));
                dataSeries1.getData().add(new XYChart.Data("10-15"  , 123));
                dataSeries1.getData().add(new XYChart.Data("15-20"  , 23));
                dataSeries1.getData().add(new XYChart.Data("20-25"  , 223));
                dataSeries1.getData().add(new XYChart.Data("25-30"  , 23));

                barChart.getData().add(dataSeries1);

        		//Button button2 = new Button("Average");
                vb1.getChildren().addAll(lb1,lbscore,lbavg,barChart);
                div1.getChildren().add(vb1);

        		}*/
            
//            }
//        };
        //avgButton.setOnAction(event1);
//       avgButton.addEventFilter(MouseEvent.MOUSE_CLICKED, event1);

	}
	@FXML
	public void Tests(ActionEvent event) {
		javafx.scene.image.Image image = new javafx.scene.image.Image("src/media/s55.jpg");
        mv.setImage(image);

	}
	@FXML
	public void onclick(ActionEvent event) {
		int n = 5; //get from server
		for(int i=0;i<n;i++) {
		VBox vb1 = new VBox();
		
		Label lb1 = new Label("test"+i);
		lb1.setId("lbtest"+i);
		
		Label lbscore = new Label("score:"+50);
		lbscore.setId("lbscore"+i);
		
		Label lbavg = new Label("Avg"+50);
		lbavg.setId("lbscore"+i);
		
		Button buttonimage = new Button("PERFORMANCE COMPARISON");
		buttonimage.setId("a3");
		
		CategoryAxis xAxis    = new CategoryAxis();
        xAxis.setLabel("Devices");

        NumberAxis yAxis = new NumberAxis();
        yAxis.setLabel("Visits");

        BarChart     barChart = new BarChart(xAxis, yAxis);

        XYChart.Series dataSeries1 = new XYChart.Series();
        dataSeries1.setName("2014");

        dataSeries1.getData().add(new XYChart.Data("Desktop", 567));
        dataSeries1.getData().add(new XYChart.Data("Phone"  , 65));
        dataSeries1.getData().add(new XYChart.Data("Tablet"  , 23));

        barChart.getData().add(dataSeries1);

		//Button button2 = new Button("Average");
        vb1.getChildren().addAll(lb1,lbscore,lbavg,barChart);
        div1.getChildren().add(vb1);

		}

	}
	


}
