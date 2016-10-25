//UDPClient.java

import java.net.*;
import java.io.*;

class UDPClient
{
   public static void main(String args[]) throws Exception
   {

   	  byte[] send_data = new byte[1024];

      BufferedReader infromuser =
                        new BufferedReader(new InputStreamReader(System.in));

      DatagramSocket client_socket = new DatagramSocket();

      InetAddress IPAddress =  InetAddress.getByName("127.0.0.1");

      while (true)
      {

      	System.out.println("Type Something (q or Q to quit): ");

      	String data = infromuser.readLine();

      	if (data.equals("q") || data.equals("Q"))
      	break;

      	else

      	{

      	send_data = data.getBytes();

        DatagramPacket send_packet = new DatagramPacket(send_data, send_data.length, IPAddress, 5000);

        client_socket.send(send_packet);

        }

      }

      client_socket.close();
   }
}
