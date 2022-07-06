from cmath import inf
from flask import Flask, jsonify, request
from LCSApi import lcsAlgo
from JobSchedulingApi import jobScheduling
from BacktrackingKnapsackApi import resultHandler
from BranchAndBoundKnapsackApi import bresultHandler
from StrassenMatrixMulApi import getMatrices
from BellmanFordApi import Graph
from DFSApi import GraphDFS


app = Flask(__name__)
@app.route("/")
def home():
    return '''
            <h2> endpoints : <h2/>
            <p> /strassen method=>POST  input value should be in JSON format eg \"{"A":[matrixA] , "B":[matrixB]}\" <p/>
            <p> /LCS?seq1=value&seq2=value method=>GET <p/>
            <p> /jobScheduling/count of jobs(user input)?jobs  method=>GET eg /2?job1=12&job2=22  <p/>
            <p> /backtrackKnapsack method=>POST input value should be in JSON format eg \"{"capacity":20 , "weights":[10,5,20] ,"values":[5,7,3] }\" <p/>
            <p> /branchAndBoundKnapsack method=>POST input value should be in JSON format eg \"{"capacity":20 , "weights":[10,5,20] ,"values":[5,7,3] }\" <p/>
            <p> /DFS method=>POST input value should be in JSON format eg \"{"matrix":[] , "startVertex":2 }\" <p/>
            <p> /bellmanFord method=>POST input value should be in JSON format eg \"{"matrix":[] , "vertices":4 , "stratVertex":2 }\" <p/>
           '''
@app.route("/strassen",methods=['POST'])
def strassen():
    a = request.json['A']
    b = request.json['B']
    return jsonify({"result":str(getMatrices(a,b))})

@app.route('/LCS', methods=['GET'])
def LCS():
    seq1 = request.args['seq1']
    seq2 = request.args['seq2']

    return jsonify(lcsAlgo(seq1,seq2))

@app.route('/jobScheduling/<count>', methods=['GET'])
def jobScheduling(count):
    jobs =[ ("job"+str(x) , int(request.args[f"job{x}"])) for x in range(1,int(count)+1) ]
     
    return jsonify(jobScheduling(jobs))

@app.route('/backtrackKnapsack', methods=['POST'])
def backtrackKnapsack():
    capacity = request.json['capacity']
    weights = request.json['weights']
    values = request.json['weights']
     
    return jsonify(resultHandler(int(len(weights)),capacity,weights,values))

@app.route('/branchAndBoundKnapsack', methods=['POST'])
def branchAndBoundKnapsack():
    capacity = request.json['capacity']
    weights = request.json['weights']
    values = request.json['weights']
     
    return jsonify(bresultHandler(int(len(weights)),capacity,weights,values))

@app.route("/DFS",methods=['POST'])
def DFS():
    g = GraphDFS()
    g.edgeHandler(request.json["matrix"])
    result = g.DFS(request.json["startVertex"])
    return jsonify({"result":result})

@app.route("/bellmanFord",methods=['POST'])
def bellmanFord():
    g = Graph(request.json["vertices"])
    g.edgeHandler(request.json["matrix"])
    result = g.bellmanFord(request.json["startVertex"])
    for key in result:
        if result[key] == inf:
            result[key] = "Infinity" 
    return jsonify({"result":result})



if __name__ == '__main__':
    app.run()