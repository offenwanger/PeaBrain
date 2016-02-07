/**
 * Created by Pixie on 19/01/2016.
 */
import java.sql.*;
import java.util.ArrayList;
import java.util.Arrays;

import org.json.*;

public class DatabaseAdaptor {
    Connection conn;
    public DatabaseAdaptor() throws SQLException {
        conn = DriverManager.getConnection("jdbc:sqlite:../assets/peaBrain.db");
        System.out.println("Opened database successfully");
    }

    public void createTrainingSet(String name, int height, int width) throws SQLException{
        int id=getTrainingSetId(name);
        if(id != -1){
            throw new SQLException("Cannot have duplicate set names");
        }

        String sql = "INSERT INTO training_sets (name,height,width) " +
                "VALUES ('"+name+"', "+height+", "+width+");";
        Statement stmt = conn.createStatement();
        stmt.executeUpdate(sql);

        stmt.close();
    }

    public void storeTrainingCase(String setName, float[] intensities) throws SQLException{
        int id = getTrainingSetId(setName);
        if(id==-1){
            throw new SQLException("Set does not exist");
        }

        JSONArray inten = new JSONArray(Arrays.asList(intensities));

        System.out.println("Storing Array: "+inten);

        String sql = "INSERT INTO training_cases (setId,intensities) " +
                "VALUES ('"+id+"', '"+inten+"');";
        Statement stmt = conn.createStatement();
        stmt.executeUpdate(sql);

        stmt.close();
    }

    private int getTrainingSetId(String setName) throws SQLException{
        Statement stmt;
        stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery( "SELECT id FROM training_sets WHERE name = '"+setName+"'");
        if ( rs.next() ) {
            int id = rs.getInt("id");
            rs.close();
            stmt.close();
            return id;
        } else {
            rs.close();
            stmt.close();
            return -1;
        }


    }

    /**
     * Gets the dimentions for the given set, returned as int[]{width, height}
     * @param setName
     * @return
     * @throws SQLException
     */
    private int[] getTrainingSetDimentions(String setName) throws SQLException{
        Statement stmt;
        stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery( "SELECT width, height FROM training_sets WHERE name = '"+setName+"'");
        if ( rs.next() ) {
            int[] dims = new int[]{ rs.getInt("width"),rs.getInt("height")};
            rs.close();
            stmt.close();
            return dims;
        } else {
            rs.close();
            stmt.close();
            return null;
        }
    }



    public static void main(String[] args){
        Connection c = null;
        Statement stmt = null;
        try {
            Class.forName("org.sqlite.JDBC");
            c = DriverManager.getConnection("jdbc:sqlite:assets/peaBrain.db");

            stmt = c.createStatement();
            String sql = "CREATE TABLE IF NOT EXISTS training_sets (" +
                    " id INTEGER PRIMARY KEY AUTOINCREMENT," +
                    " name VARCHAR(255)," +
                    " height INTEGER," +
                    " width INTEGER " +
                    ")";
            stmt.executeUpdate(sql);

            sql = "CREATE TABLE IF NOT EXISTS training_cases (" +
                    " id INTEGER PRIMARY KEY AUTOINCREMENT," +
                    " setId INTEGER," +
                    " intensities TEXT " +
                    ")";
            stmt.executeUpdate(sql);



            stmt.close();
        } catch ( Exception e ) {
            System.err.println( e.getClass().getName() + ": " + e.getMessage() );
            System.exit(0);
        }
        System.out.println("Opened database successfully");
    }

    public TrainingCase[] getCasesByTrainingSetName(String setName) throws SQLException {
        Statement stmt;
        stmt = conn.createStatement();

        if(getTrainingSetId(setName) == -1){
            throw new SQLException("Set does not exist!");
        }

        int[] dims = getTrainingSetDimentions(setName);
        int width = dims[0];
        int height = dims[1];

        ResultSet rs = stmt.executeQuery(
                "SELECT training_cases.* FROM training_sets CROSS JOIN training_cases " +
                "WHERE training_sets.name = '"+setName+"' AND training_sets.id = training_cases.setId");
        ArrayList<TrainingCase> list = list = new ArrayList<TrainingCase>();
        while ( rs.next() ) {
            TrainingCase t = new TrainingCase();
            t.id = rs.getInt("id");
            t.setName = setName;
            JSONArray arr = new JSONArray(rs.getString("intensities")).getJSONArray(0);
            t.intensities = new double[arr.length()];
            for(int i =0;i<arr.length();i++){
                t.intensities[i] = arr.getDouble(i);
            }
            t.width = width;
            t.height = height;
            list.add(t);
        }
        rs.close();
        stmt.close();
        return list.toArray(new TrainingCase[list.size()]);
    }

    public boolean deleteTrainingCase(int id){
        try {
            PreparedStatement st = conn.prepareStatement("DELETE FROM training_cases WHERE id = ?");
            st.setString(1, ""+id);
            st.executeUpdate();
            return true;
        }catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
    }

}
