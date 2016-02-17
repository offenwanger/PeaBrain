import sqlite3
import json
import numpy as np

class DatabaseConnector:
    def __init__(self):
        self.connection = sqlite3.connect('../assets/peaBrain.db')
        self.c = self.connection.cursor()

    def getTrainingCases(self, tableName):
        cases = []
        for row in self.c.execute('SELECT training_cases.intensities FROM training_sets CROSS JOIN training_cases '
                       'WHERE training_sets.name = ? AND training_sets.id = training_cases.setId', (tableName,)):
            cases.append(json.loads(row[0])[0])
        return cases

    def getTrainingSetId(self, setName):
        row = self.c.execute("SELECT id FROM training_sets WHERE name = ?", (setName,)).fetchone()
        if row is None:
            return False;

        return row[0]


    def dispose(self):
        self.connection.close()

    def getNetwork(self, networkName):
        row = self.c.execute('SELECT * FROM networks WHERE name = ?', (networkName,)).fetchone()
        if row is None:
            return False;

        class NetworkRow:
            pass

        returnable = NetworkRow()
        returnable.id = row[0]
        returnable.name = row[1]

        returnable.weights = []
        ws = json.loads(row[2])
        for index in range(len(ws)):
            returnable.weights.append(np.zeros((len(ws[index]), len(ws[index][0]))))
            for i, weightRow in enumerate(ws[index]):
                for j, elem in enumerate(weightRow):
                    returnable.weights[index][i,j] = elem

        returnable.model = json.loads(row[3])
        returnable.imageHeight = row[4]
        returnable.imageWidth = row[5]
        returnable.trainingSets = json.loads(row[6])

        return returnable;

    def deleteNetwork(self, networkName):
        self.c.execute('DELETE FROM networks WHERE name = ?', (networkName,))
        self.connection.commit()

    def storeNetwork(self, name, weights, model, imageHeight, imageWidth, trainingSets):
        self.deleteNetwork(name)
        ws = []
        for index in range(len(weights)):
            ws.append(np.around(weights[index], 4).tolist())
        self.c.execute("INSERT INTO networks(name, weights, model, image_height, image_width, training_sets) "
                       "VALUES (?,?,?,?,?,?)",
                       (name, json.dumps(ws), json.dumps(model), imageHeight, imageWidth, json.dumps(trainingSets),))
        self.connection.commit()




