import Analyzer, time, pydot

if __name__ == "__main__":
	graphs = ["skos.dot", "generations.dot", "travel.dot", "univ-bench.dot", "atom-primitive.dot", "biomedical-measure-primitive.dot", "foaf.dot", "people-pets.dot", "funding.dot", "wine.dot", "pizza.dot"]
	grammars = ["Q1.txt", "Q2.txt", "Q3.txt"]
	automatons = ["Q1.dot", "Q2.dot", "Q3.dot"]
	Expected = [[810, 2164, 2499, 2540, 15454, 15156, 4118, 9472, 17634, 66572, 56195], [1, 0, 63, 81, 122, 2871, 10, 37, 1158, 133, 1262], [32, 19, 31, 12, 3, 0, 46, 36, 18, 1215, 9520]]
	Passed = True
	I = 0
	print("Matrix Analysis:")
	for i in grammars:
		J = 0
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
			if (Snumber == Expected[I][J]):
				print("Passed")
			else:
				print("Not Passed")
				Passed = False
			J = J + 1
		I = I + 1
	I = 0
	print("\nTop-Down Analysis:")
	for i in automatons:
		J = 0
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
			if (Snumber == Expected[I][J]):
				print("Passed")
			else:
				print("Not Passed")
				Passed = False
			J = J + 1
		I = I + 1
	I = 0
	print("\nBottom-Up Analysis:")
	for i in automatons:
		J = 0
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
			if (Snumber == Expected[I][J]):
				print("Passed")
			else:
				print("Not Passed")
				Passed = False
			J = J + 1
		I = I + 1
	if Passed:
		print("\n\nAll Tests Passed")