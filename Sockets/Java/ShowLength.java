import java.io.*;
import galatea.glider.*;
class ShowLength extends Node {
    ShowLength() {
        super("showLength", 'A');
        Glider.nodesl.add(this);
    }
    @Override
    public void fact() {
        System.out.println("\tthere are " + ModelThread.teller.getEl().ll() + " clients waiting ");
    }
}
