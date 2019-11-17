import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.ResourceBundle;

import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import rest.MultipartUtility;

public class postQuestionsController implements Initializable{

	@FXML
	public TextField QuestionName,tags;
	@FXML
	public Button desFileInput,inputfile1,outputfile1,addfiles,submit;
	@FXML 
	public AnchorPane root;
	@FXML 
	public TextArea response;
	public String usn; 
	public File descriptionFile;
	List<File> testCaseInputs = new ArrayList<>();
	List<File> testCaseOutputs = new ArrayList<>();
	public int currentButtons = 1;
	public double LayoutIpX,LayoutIpY;
	public double LayoutOpX,LayoutOpY;
	public double currentPad = 30.0;
	
	
	@Override
	public void initialize(URL location, ResourceBundle resources) {
		LayoutIpX = inputfile1.getLayoutX();
		LayoutIpY = inputfile1.getLayoutY();
		LayoutOpX = outputfile1.getLayoutX();
		LayoutOpY = outputfile1.getLayoutY();
		FileChooser fileChooser = new FileChooser();
		
		
			//Stage s =  desFileInput.getScene();
            //File selectedFile = fileChooser.showOpenDialog(desFileInput.getScene().getWindow());
        
		EventHandler<ActionEvent> fileButtonEvent = new EventHandler<ActionEvent>() { 
            public void handle(ActionEvent e) 
            {                                     		
            	Stage stage = (Stage)((Node) e.getSource()).getScene().getWindow();
            	descriptionFile = fileChooser.showOpenDialog(stage);                 
            }                  
        };
        EventHandler<ActionEvent> AddtestCasesip = new EventHandler<ActionEvent>() { 
            public void handle(ActionEvent e) 
            {                                     		
            	File file;
            	Stage stage = (Stage)((Node) e.getSource()).getScene().getWindow();
            	file = fileChooser.showOpenDialog(stage);
            	String name = ((Button)e.getSource()).getText();
            	int idx = Character.getNumericValue(name.charAt(name.length()-1));
            	
            	testCaseInputs.add(idx-1, file);
	            	
            }                  
        };
        
        EventHandler<ActionEvent> AddtestCasesop = new EventHandler<ActionEvent>() { 
            public void handle(ActionEvent e) 
            {                                     		
            	File file;
            	Stage stage = (Stage)((Node) e.getSource()).getScene().getWindow();
            	file = fileChooser.showOpenDialog(stage);
            	String name = ((Button)e.getSource()).getText();
            	int idx = Character.getNumericValue(name.charAt(name.length()-1));
            	System.out.println("idx is op "+idx);
            	testCaseOutputs.add(idx-1, file);
	            	
            }                  
        };
        inputfile1.setOnAction(AddtestCasesip);
        outputfile1.setOnAction(AddtestCasesop);
        EventHandler<ActionEvent> addFilesEvent = new EventHandler<ActionEvent>() { 
            public void handle(ActionEvent e) 
            {             
            	currentButtons++;
            	Button ip = new Button("input file "+currentButtons);
            	Button op = new Button("output file "+currentButtons);
            	ip.setLayoutX(LayoutIpX);
            	ip.setLayoutY(LayoutIpY+currentPad+10);
            	
            	op.setLayoutX(LayoutOpX);
            	op.setLayoutY(LayoutOpY+currentPad+10);
            	submit.setLayoutY(LayoutIpY+50+currentPad);
            	currentPad+=40;
	            root.getChildren().add(ip);
	            root.getChildren().add(op);
	            ip.setOnAction(AddtestCasesip);
	            op.setOnAction(AddtestCasesop);
            }                  
        };
        addfiles.setOnAction(addFilesEvent);                      
        desFileInput.setOnAction(fileButtonEvent);
        submit.setOnAction(e->postData());
       
        
	}
	public void setUsn(String usn) {
		this.usn = usn;
	}
	
	public void postData()
	{
		 String charset = "UTF-8";
	     String requestURL = "http://127.0.0.1:5000/codecouch/question/";
		
        try {
            MultipartUtility multipart = new MultipartUtility(requestURL, charset);
             
            //multipart.addHeaderField("User-Agent", "CodeJava");
            //multipart.addHeaderField("Test-Header", "Header-Value");
             
            multipart.addFormField("Usn",usn);
            multipart.addFormField("Question_name", QuestionName.getText());
            multipart.addFormField("Tags", tags.getText());            
            multipart.addFilePart("description", descriptionFile);
            for(int i=0;i<currentButtons;i++)
            {
            	System.out.println("Button "+i);
            	multipart.addFilePart("ip"+(i+1),testCaseInputs.get(i));
            	multipart.addFilePart("op"+(i+1),testCaseOutputs.get(i));
            }
            
            List<String> response = multipart.finish();
             
            System.out.println("SERVER REPLIED:");
            
            String res="";
            for (String line : response) {
                System.out.println(line);
                res+=line;
            }
            this.response.setText(res); 
            this.response.setOpacity(1.0);
        } catch (IOException ex) {
            System.err.println(ex);
        }
		
	}

}
