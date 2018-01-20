import Analyzer, time, pydot

if __name__ == "__main__":
	graphs = ["(abb)^n.dot", "a^nb.dot", "ab.dot", "Cycle.dot", "EightForm.dot", "Sequence.dot"]
	grammars = ["a^nb.txt", "a^nb^m.txt", "a^nb^n.txt", "S^2n.txt", "SSS.txt"]
	automatons = ["a^nb.dot", "a^nb^m.dot", "a^nb^n.dot", "S^2n.dot", "SSS.dot"]
	Expected = [[3, 1, 2, 0, 20, 0], [1, 1, 1, 0, 110, 0], [4, 3, 4, 6, 129, 6], [3, 2, 3, 15, 60, 12], [1, 1, 1, 25, 100, 15]]
	Passed = True
	I = 0
	print("Matrix Analysis:")
	for i in grammars:
		print(i)
		J = 0
		for j in graphs:
			graph = (pydot.graph_from_dot_file("UnitTests/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.MatrixAnalysis("UnitTests/grammars/" + i, Nodes, Edges)
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
			graph = (pydot.graph_from_dot_file("UnitTests/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.TopDownAnalysis("UnitTests/automatons/" + i, Nodes, Edges)
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
			graph = (pydot.graph_from_dot_file("UnitTests/graphs/" + j))[0]
			(Nodes, Edges, StartNodes, FinalNodes) = Analyzer.ParseGraph(graph)
			timeStart = time.time()
			results = Analyzer.BottomUpAnalysis("UnitTests/automatons/" + i, Nodes, Edges)
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