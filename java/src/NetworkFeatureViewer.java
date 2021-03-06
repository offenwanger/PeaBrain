import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.image.BufferedImage;
import java.sql.SQLException;
import java.util.*;
import java.util.List;

/**
 * Created by Pixie on 22/01/2016.
 */
public class NetworkFeatureViewer extends JApplet {
    public static void main(String s[]) {
        String networkName = "testNetwork";

        try{
            NetworkFeatureViewer viewer = new NetworkFeatureViewer(networkName);

            JFrame f = new JFrame("ImageDrawing");
            f.addWindowListener(new WindowAdapter() {
                public void windowClosing(WindowEvent e) {
                    //    System.exit(0);
                }
            });

            viewer.buildUI();
            f.add("Center", viewer);
            f.pack();
            f.setVisible(true);
        } catch(SQLException e){
            System.out.println(e.getMessage());
            return;
        }

    }

    static Network network;
    static int curIndex = 0;
    DatabaseAdaptor adaptor;
    NetworkFeatureImageHolder holder;

    public NetworkFeatureViewer (String networkName) throws SQLException{
        adaptor = new DatabaseAdaptor();
        network = adaptor.getNetwork(networkName);
        System.out.println(network.weights.get(0)[0][0]);
        System.out.println(network.weights.size());
        System.out.println(network.weights.get(0).length);
        System.out.println(network.weights.get(0)[0].length);

        System.out.println(network.weights.get(1).length);
        System.out.println(network.weights.get(1)[0].length);

    }

    public void init() {
        buildUI();
    }

    public void buildUI() {/*
        final JApplet frame = this;
        holder = new NetworkFeatureImageHolder(cases.get(curIndex));
        add("Center", holder);

        final NetworkFeatureViewControlBar bar = new NetworkFeatureViewControlBar();

        bar.setActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if(e.getSource() == bar.next){
                    //%cases.length will make it 0 if it = cases.length
                    curIndex = (curIndex+1)%cases.size();
                    System.out.println("Next: "+curIndex);
                    remove(holder);
                    holder = new NetworkFeatureImageHolder(cases.get(curIndex));
                    add("Center", holder);
                    frame.getContentPane().validate();
                    frame.getContentPane().repaint();

                }
                if(e.getSource() == bar.prev){
                    curIndex--;
                    if(curIndex == -1) curIndex = cases.size()-1;
                    remove(holder);
                    holder = new NetworkFeatureImageHolder(cases.get(curIndex));
                    add("Center", holder);
                    frame.getContentPane().validate();
                    frame.getContentPane().repaint();
                }
                if(e.getSource() == bar.delete){
                    adaptor.deleteTrainingCase(cases.get(curIndex).id);
                    cases.remove(curIndex);
                    if(cases.size() == 0){
                        JOptionPane.showMessageDialog(holder,"Set Empty, deleting");
                        System.exit(0);

                    }
                    if(curIndex == cases.size()){
                        curIndex = 0;
                    }
                    frame.getContentPane().validate();
                    frame.getContentPane().repaint();
                }
            }
        });

        add("North", bar);


        Button clearDups = new Button("Cleaer Duplicates");
        this.add("South", clearDups);
        clearDups.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                Set<String> caseSet = new HashSet<>();
                List<TrainingCase> dups = new ArrayList<TrainingCase>();
                for(TrainingCase c: cases){
                    if (caseSet.contains(Arrays.toString(c.intensities))) {
                        adaptor.deleteTrainingCase(c.id);
                        dups.add(c);

                        curIndex = 0;
                        remove(holder);
                        holder = new NetworkFeatureImageHolder(cases.get(curIndex));
                        add("Center", holder);
                        frame.getContentPane().validate();
                        frame.getContentPane().repaint();
                    } else {
                        caseSet.add(Arrays.toString(c.intensities));
                    }
                }
                for(TrainingCase c: dups){
                    cases.remove(c);
                }
            }
        });*/
    }

}

class NetworkFeatureViewControlBar extends JPanel {
    Button next;
    Button delete;
    Button prev;
    ActionListener listener;

    public NetworkFeatureViewControlBar(){
        this.setLayout(new FlowLayout());
        prev = new Button("Prev");
        this.add(prev);
        delete = new Button("Delete");
        this.add(delete);
        next = new Button("Next");
        this.add(next);
    }

    public void setActionListener(ActionListener actionListener){
        next.removeActionListener(listener);
        next.addActionListener(actionListener);
        delete.removeActionListener(listener);
        delete.addActionListener(actionListener);
        prev.removeActionListener(listener);
        prev.addActionListener(actionListener);
        listener = actionListener;
    }

}

class NetworkFeatureImageHolder extends Component {
    private BufferedImage bi;
    int w, h;

    public NetworkFeatureImageHolder(TrainingCase tCase) {
        bi = new BufferedImage(tCase.width, tCase.height, BufferedImage.TYPE_INT_RGB);
        w = bi.getWidth(null);
        h = bi.getHeight(null);
        for(int i=0;i<tCase.intensities.length;i++) {
            int x = i / w;
            int y = i % w;
            if (tCase.intensities[i] == 1) {
                bi.setRGB(x, y, Color.white.getRGB());
            } else {
                bi.setRGB(x, y, new Color((float)tCase.intensities[i], (float)tCase.intensities[i], (float)tCase.intensities[i]).getRGB());
            }
        }

    }

    public Dimension getPreferredSize() {
        return new Dimension(w, h);
    }


    /* In this example the image is recalculated on the fly every time
     * This makes sense where repaints are infrequent or will use a
     * different filter/op from the last.
     * In other cases it may make sense to "cache" the results of the
     * operation so that unless 'opIndex' changes, drawing is always a
     * simple copy.
     * In such a case create the cached image and directly apply the filter
     * to it and retain the resulting image to be repainted.
     * The resulting image if untouched and unchanged Java 2D may potentially
     * use hardware features to accelerate the blit.
     */

    public void paint(Graphics g) {

        Graphics2D g2 = (Graphics2D) g;

        g.drawImage(bi, 0, 0, null);

    }
}