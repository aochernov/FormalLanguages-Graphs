import Analyzer, time, pydot

if __name__ == "__main__":
	graphs = ["skos.dot", "generations.dot", "travel.dot", "univ-bench.dot", "atom-primitive.dot", "biomedical-measure-primitive.dot", "foaf.dot", "people-pets.dot", "funding.dot", "wine.dot", "pizza.dot"]
	grammars = ["Q1.txt", "Q2.txt", "Q3.txt"]
	automatons = ["Q1.dot", "Q2.dot", "Q3.dot"]
	print("Matrix Analysis:")
	for i in grammars:
		print(i)
		for j in graphs:
			graph = (pydot.graph_from_dot_file("Test/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.MatrixAnalysis("Test/grammars/" + i, Nodes, Edges)
			timeFinal = time.time()
			Snumber = 0
			for k in results:
				(begin, label, end) = k
				if label == "S":
					Snumber = Snumber + 1
			print(str(j) + ": " + str(Snumber) + ", " + str(timeFinal - timeStart))
	print("\nTop-Down Analysis:")
	for i in automatons:
		print(i)
		for j in graphs:
			graph = (pydot.graph_from_dot_file("Test/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.TopDownAnalysis("Test/automatons/" + i, Nodes, Edges)
			timeFinal = time.time()
			Snumber = 0
			for k in results:
				(begin, label, end) = k
				if label == "S":
					Snumber = Snumber + 1
			print(str(j) + ": " + str(Snumber) + ", " + str(timeFinal - timeStart))
	print("\nBottom-Up Analysis:")
	for i in automatons:
		print(i)
		for j in graphs:
			graph = (pydot.graph_from_dot_file("Test/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.BottomUpAnalysis("Test/automatons/" + i, Nodes, Edges)
			timeFinal = time.time()
			Snumber = 0
			for k in results:
				(begin, label, end) = k
				if label == "S":
					Snumber = Snumber + 1
			print(str(j) + ": " + str(Snumber) + ", " + str(timeFinal - timeStart))