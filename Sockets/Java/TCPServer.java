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
import java.util.*;
import java.lang.reflect.Field;

class TCPServer
{

  public static void main(String[] args) throws IOException {

    if (args.length < 1)
    {
      System.err.println("Usage: java TCPServer <port number>");
      System.exit(1);
    }
    //Get the port number
    int portNumber = Integer.parseInt(args[0]);

    String fromclient;
    String toclient;
    try
    {

      //init de the server on port number
      ServerSocket Server = new ServerSocket (portNumber);
      System.out.println ("TCPServer Waiting for client on port " + portNumber);

      //wait for client connected
      Socket connected = Server.accept();
      System.out.println( " THE CLIENT " + " " + connected.getInetAddress() +" : "+connected.getPort()+" IS CONNECTED ");

      //Buffer get info to send
      BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

      //Buffer in for client data
      BufferedReader inFromClient = new BufferedReader(new InputStreamReader (connected.getInputStream()));

      //Buffer out for client data
      PrintWriter outToClient = new PrintWriter( connected.getOutputStream(),true);

      //create thread
      ModelThread obj = new ModelThread();

      //send args to sim 
      String [] args2 = new String[args.length-1];
      for(int i = 1; i < args.length ; ++i)
      {
        args2[i-1] = args[i];
      }
      obj.setArg(args2);

      //create ModelListener
      ModelListener modListener = new ModelEventListener(connected);

      //ModelThread assing listeners
      obj.addModelListener(modListener);


      while(true)
      {

        //read from client
        System.out.println ("TCPServer Waiting for client");
        //fromclient = inFromClient.readLine();
        char[] inputChars = new char[512];
        int charsRead = 0;
        charsRead =  inFromClient.read(inputChars); //<< THIS LINE IS PAUSING THE THREAD!>
        //System.out.println( "RECIEVEDAAAAAA:" + inputChars );
        fromclient = String.valueOf(inputChars);
        String[] parts = fromclient.split(" ");
        String code = parts[0];
        int result = Integer.parseInt(code);
        //print data
        System.out.println( "RECIEVED: " + fromclient );

        //create thread

        int caseNumber = result;
        switch(caseNumber)
        {
          //close connection
          case 0:
          {
            System.out.println("Caso 0 Exit");
            if(obj.isAlive())
            {
              Thread.State state = obj.getState();
              System.out.println("Thread state = " + state);
              System.out.println("Exit: Thread alive stop");
              obj.stop();
            }
            connected.close();
            System.exit(1);
            break;
          }
          //start the thread
          case 1:
          {
            System.out.println("Caso 1 Start");
            Thread.State state = obj.getState();
            System.out.println("Thread state = " + state);
            if(state == Thread.State.TIMED_WAITING)
            {
              obj.resume();
            }
            else
            {
              if(state != Thread.State.TERMINATED)
              {
                obj.start();
              }
            }
            break;
          }
          //sleep the thread
          case 2:
          {
            String value_sleep = parts[2];
            result = Integer.valueOf(value_sleep.trim());
            int time = result;
            System.out.println("Caso 2 Sleep");
            if(obj.isAlive())
            {
              try
              {
                Thread.State state = obj.getState();
                System.out.println("Thread state = " + state);
                System.out.println("Sleep: Thread alive sleep");
                obj.sleep(time);
              }
              catch(InterruptedException ex)
              {
                Thread.currentThread().interrupt();
              }
            }
            break;
          }
          //stop the thread
          case 3:
          {
            System.out.println("Caso 3 Stop");
            if(obj.isAlive())
            {
              Thread.State state = obj.getState();
              System.out.println("Thread state = " + state);
              System.out.println("Stop: Thread alive stop");
              obj.stop();
            }
            connected.close();
            System.exit(1);
            break;
          }
          //yield the thread
          case 4:
          {
            System.out.println("Caso 4 Yield");
            if(obj.isAlive())
            {
              Thread.State state = obj.getState();
              System.out.println("Thread state = " + state);
              System.out.println("Yield: Thread alive yield");
              obj.yield();
            }
            break;
          }
          //pause the thread
          case 5:
          {
            System.out.println("Caso 5 Pause");
            if(obj.isAlive())
            {
              Thread.State state = obj.getState();
              System.out.println("Thread state = " + state);
              System.out.println("Pause: Thread alive suspend");
              obj.suspend();
            }
            break;
          }
          //set variable thread
          case 6:
          {
            try
            {
              try
              {
                String value_name = parts[2];
                System.out.println("Caso 6 Set");
                Class  aClass = obj.getClass();
                Field field = aClass.getField(value_name.trim());
                int str1 = (int) field.get(obj);

                String value_sleep = parts[3];
                result = Integer.valueOf(value_sleep.trim());
                int time = result;

                field.set(obj, time);

                int value_return = str1;
                Thread.State state = obj.getState();
                System.out.println("Thread state = " + state);
                System.out.println("Set: Thread alive set " + time);
                break;
              }
              catch (IllegalAccessException e) {
                  System.out.println(e);
                  System.exit(1);
              }

            }
            catch (NoSuchFieldException e) {
                System.out.println(e);
                System.exit(1);
            }
            break;
          }
          //get variable thread
          case 7:
          {
            try
            {
              try
              {
                String value_name = parts[2];

                System.out.println("Caso 7 Get");
                Class  aClass = obj.getClass();
                Field field = aClass.getField(value_name.trim());
                int str1 = (int) field.get(obj);

                int value_return = str1;
                Thread.State state = obj.getState();
                System.out.println("Thread state = " + state);
                System.out.println("Get: Thread alive get " + value_return);
                break;
              }
              catch (IllegalAccessException e) {
                  System.out.println(e);
                  System.exit(1);
              }

            }
            catch (NoSuchFieldException e) {
                System.out.println(e);
                System.exit(1);
            }
            break;

          }
          case 8:
          {
            System.out.println("Caso 8 Other");
            break;
          }
          case 9:
          {
            System.out.println("Caso 9 Other");
            break;
          }
        }
      }
    }
    catch (IOException e) {
        System.out.println(e);
        System.exit(1);
    }
  }
}
