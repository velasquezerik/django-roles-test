//ModelThread.java

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


class ModelThread extends Thread
{
  private List _listeners = new ArrayList();
  public void run()
  {
    try
    {
      System.out.println ("Start Running Thread");
      this._fireModelEvent(1,"Start Running Thread");
      for(int i = 0; i < 1000; ++i)
      {
        System.out.println ("Running Thread ---> Time " + i);
        this._fireModelEvent(2,"Running Thread ---> Time " + i);
        Thread.sleep(100);
      }
      System.out.println ("Finish Running Thread");
      this._fireModelEvent(1,"Finish Running Thread");
    }
    catch(InterruptedException ex)
    {
      Thread.currentThread().interrupt();
    }
  }

  public synchronized void addModelListener( ModelListener l )
  {
        _listeners.add( l );
  }

  public synchronized void removeModelListener( ModelListener l )
  {
        _listeners.remove( l );
  }

  private synchronized void _fireModelEvent(  int type, String description )
  {
    ModelEvent mood = new ModelEvent( this, type, description );
    Iterator listeners = _listeners.iterator();
    while( listeners.hasNext() )
    {
      ( (ModelListener) listeners.next() ).modelReceived( mood );
    }
  }

  public static void main(String args[]){
     ModelThread obj = new ModelThread();
     obj.start();
  }

}
