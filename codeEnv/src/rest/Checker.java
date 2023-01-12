package rest;

public class Checker {
	public static void main(String[] args) {
		RestClient client = new RestClient("http://127.0.0.1:5000/codecouch/questions/", "First=-1&Number=2&Tag=&Faculty=f1", "GET");
//		Thread t = new Thread(client);
//		t.start();
		client.run();
		System.out.println(client.finalOutputString);
	}
}
