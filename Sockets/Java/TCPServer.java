//TCPServer.java

/*
    <GALATEA WEB: Web system simulations>
    Copyright (C) 2016  Erik Velasquez erikvelasquez.25@gmail.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

import java.io.*;
import java.net.*;

/*public class KKMultiServer {
    public static void main(String[] args) throws IOException {

    if (args.length != 1) {
        System.err.println("Usage: java KKMultiServer <port number>");
        System.exit(1);
    }

        int portNumber = Integer.parseInt(args[0]);
        boolean listening = true;

        try (ServerSocket serverSocket = new ServerSocket(portNumber)) {
            while (listening) {
	            new KKMultiServerThread(serverSocket.accept()).start();
	        }
	    } catch (IOException e) {
            System.err.println("Could not listen on port " + portNumber);
            System.exit(-1);
        }
    }
}*/

class TCPServer
{
  /*public static void main(String[] args) throws IOException {

    if (args.length != 1)
    {
      System.err.println("Usage: java TCPServer <port number>");
      System.exit(1);
    }
    //Get the port number
    int portNumber = Integer.parseInt(args[0]);

    String fromclient;
    String toclient;
    try{

      //init de the server on port number
      ServerSocket Server = new ServerSocket (portNumber);
      System.out.println ("TCPServer Waiting for client on port " + portNumber);
    }
    catch (IOException e) {
        System.out.println(e);
    }

  }*/
   public static void main(String argv[]) throws IOException
      {
         String fromclient;
         String toclient;

         ServerSocket Server = new ServerSocket (5000);

         System.out.println ("TCPServer Waiting for client on port 5000");

         while(true)
         {
         	Socket connected = Server.accept();
            System.out.println( " THE CLIENT"+" "+
            connected.getInetAddress() +":"+connected.getPort()+" IS CONNECTED ");

            BufferedReader inFromUser =
            new BufferedReader(new InputStreamReader(System.in));

            BufferedReader inFromClient =
               new BufferedReader(new InputStreamReader (connected.getInputStream()));

            PrintWriter outToClient =
               new PrintWriter(
                  connected.getOutputStream(),true);

            while ( true )
            {

            	System.out.println("SEND(Type Q or q to Quit):");
            	toclient = inFromUser.readLine();

            	if ( toclient.equals ("q") || toclient.equals("Q") )
            	{
            		outToClient.println(toclient);
            		connected.close();
            		break;
            	}
            	else
            	{
            	outToClient.println(toclient);
                }

            	fromclient = inFromClient.readLine();

                if ( fromclient.equals("q") || fromclient.equals("Q") )
                {
                	connected.close();
                	break;
                }

		        else
		        {
		         System.out.println( "RECIEVED:" + fromclient );
		        }

			}

          }
      }
}
