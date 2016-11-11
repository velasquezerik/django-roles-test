import java.io.*;
import galatea.glider.*;
class Exit extends Node {
    Exit() {
        super("exit", 'E');
        Glider.nodesl.add(this);
    }
    @Override
    public void fscan() {
        System.out.print("EXIT:\t" + Glider.getTime());
        Glider.act(0, ModelThread.showLength);
    }
}
