import pydot

def ParseGraph(graph):
	graph_nodes = graph.get_node_list()
	graph_edges = graph.get_edge_list()
	nodes = []
	final = {}
	start = {}
	edges = []
	for i in graph_nodes:
		node = i
		name = node.get_name()
		nodes.append(name)
		if node.get_shape() == "\"doublecircle\"":
			label = node.get_label()
			if label[0] == '"':
				l = len(label) - 1
				label = label[1:l]
			final[name] = label
		if node.get_color() == "\"green\"":
			label = node.get_label()
			if label[0] == '"':
				l = len(label) - 1
				label = label[1:l]
			start[name] = label
	for i in graph_edges:
		edge = i
		begin = edge.get_source()
		end = edge.get_destination()
		label = edge.get_label()
		if label[0] == '"':
			l = len(label) - 1
			label = label[1:l]
		edges.append((begin, label, end))
	return (nodes, edges, start, final)

def ParseGrammar(grammar):
	terminal = {}
	nonterminal = {}
	for i in grammar:
		[first, second] = i.split(':')
		first = first.strip()
		second = second.strip()
		if ' ' in second:
			[fst, snd] = second.split()
			fst = fst.strip()
			snd = snd.strip()
			if (fst, snd) in nonterminal:
				(nonterminal[(fst, snd)]).append(first)
			else:
				nonterminal[(fst, snd)] = [first]
		else:
			if second in terminal:
				(terminal[second]).append(first)
			else:
				terminal[second] = [first]
	return(terminal, nonterminal)

def TransitiveClosure(matrix, length, nonterminal, ways, nodes):
	repeat = False
	for i in range(length):
		for j in range(length):
			for k in range(length):
				for x in matrix[i][j]:
					for y in matrix[j][k]:
						for l in nonterminal.get((x, y), []):
							if not (l in matrix[i][k]):
								(matrix[i][k]).append(l)
								ways.add((nodes[i], l, nodes[k]))
								repeat = True
	return repeat

def MatrixAnalysis(name, nodes, edges):
	grammar = open(name, 'r').read().split('\n')
	(terminal, nonterminal) = ParseGrammar(grammar)
	length = len(nodes)
	matrix = [[[] for x in range(length)] for y in range(length)]
	ways = set()
	for i in edges:
		(begin, label, end) = i
		B = nodes.index(begin)
		E = nodes.index(end)
		route = matrix[B][E]
		for j in terminal.get(label, []):
			route.append(j)
			ways.add((begin, j, end))
	for i in terminal.get("eps", []):
		for j in range(length):
			(matrix[j][j]).append(i)
			ways.add((j, i, j))
	repeat = True
	while(repeat):
		repeat = TransitiveClosure(matrix, length, nonterminal, ways, nodes)
	return ways

def GraphProduct(GraphEdges, AutEdges, AutStartNodes, AutFinalNodes):
	nodes = set()
	edges = []
	startNodes = {}
	finalNodes = {}
	for i in GraphEdges:
		(i_start, i_label, i_final) = i
		for j in AutEdges:
			(j_start, j_label, j_final) = j
			if j_label == i_label:
				nodes.add((i_start, j_start))
				nodes.add((i_final, j_final))
				if j_start in AutStartNodes:
					startNodes[(i_start, j_start)] = AutStartNodes[j_start]
				if j_final in AutFinalNodes:
					finalNodes[(i_final, j_final)] = AutFinalNodes[j_final]
				edges.append(((i_start, j_start), i_label, (i_final, j_final)))
	return (edges, list(nodes), startNodes, finalNodes)

def GetWays(node, edges):
	res = []
	for i in edges:
		(begin, label, end) = i
		if begin == node:
			res.append((label, end))
	return res

def FindWays(Edges, StartNodes, FinalNodes, Nodes, ways):
	repeat = False
	Begins = {}
	Burned = {}
	res = []
	for i in Nodes:
		Burned[i] = False
		Begins[i] = set()
		Begins[i].add(i)
	WorkList = set()
	for i in StartNodes.keys():
		WorkList.add(i)
	while WorkList != set():
		Node = WorkList.pop()
		if Burned[Node]:
			continue
		Burned[Node] = True
		for i in GetWays(Node, Edges):
			(label, end) = i
			WorkList.add(end)
			Begins[end] = Begins[end].union(Begins[Node])
	for j in FinalNodes.keys():
		WorkList = Begins[j]
		history = set()
		while WorkList != set():
			Node = WorkList.pop()
			if Node in history:
				continue
			history.add(Node)
			for i in Begins[Node]:
				WorkList.add(i)
			if Node in StartNodes:
				if StartNodes[Node] == FinalNodes[j]:
					(GraphBegin, AutBegin) = Node
					(GraphEnd, AutEnd) = j
					if not ((GraphBegin, StartNodes[i], GraphEnd) in ways):
						res.append((GraphBegin, StartNodes[i], GraphEnd))
						repeat = True
	return (res, repeat)

def BottomUpAnalysis(name, nodes, edges):
	automaton = (pydot.graph_from_dot_file(name))[0]
	(AutNodes, AutEdges, AutStartNodes, AutFinalNodes) = ParseGraph(automaton)
	Edges = edges.copy()
	ways = set()
	flag = True
	while flag:
		(ProductEdges, ProductNodes, ProductStarts, ProductFinals) = GraphProduct(Edges, AutEdges, AutStartNodes, AutFinalNodes)
		(newWays, flag) = FindWays(ProductEdges, ProductStarts, ProductFinals, ProductNodes, ways)
		if flag:
			Edges = set(Edges)
			for i in newWays:
				Edges.add(i)
				ways.add(i)
			Edges = list(Edges)
	return ways

def TopDownAnalysis(name, nodes, edges):
	automaton = (pydot.graph_from_dot_file(name))[0]
	(AutNodes, AutEdges, AutStartNodes, AutFinalNodes) = ParseGraph(automaton)
	nonterminals = set()
	WorkList = set()
	Stack = []
	StackLength = -1
	StackEdges = set()
	ways = set()
	history = set()
	poppedNodes = {}
	for i in AutStartNodes.keys():
		node = i
		nonterminals.add(AutStartNodes[i])
		for j in nodes:
			StackNode = None
			if (node, j) in Stack:
				StackNode = Stack.index((node, j))
			else:
				StackLength = StackLength + 1
				StackNode = StackLength
			Stack.append((AutStartNodes[i], j))
			WorkList.add((node, j, StackNode))
	while WorkList != set():
		(AutomatonPointer, GraphPointer, StackPointer) = WorkList.pop()
		if (AutomatonPointer, GraphPointer, StackPointer) in history:
			continue
		history.add((AutomatonPointer, GraphPointer, StackPointer))
		AutomatonWays = GetWays(AutomatonPointer, AutEdges)
		GraphWays = GetWays(GraphPointer, edges)
		for i in AutomatonWays:
			(AutomatonLabel, AutomatonEnd) = i
			for j in GraphWays:
				(GraphLabel, GraphEnd) = j
				if AutomatonLabel == GraphLabel:
					WorkList.add((AutomatonEnd, GraphEnd, StackPointer))
				else:
					if AutomatonLabel in nonterminals:
						StackEndNode = None
						if (AutomatonLabel, GraphPointer) in Stack:
							StackEndNode = Stack.index((AutomatonLabel, GraphPointer))
						else:
							Stack.append((AutomatonLabel, GraphPointer))
							StackLength = StackLength + 1
							StackEndNode = StackLength
						StackEdges.add((StackEndNode, AutomatonEnd, StackPointer))
						Nodes = []
						for k in AutStartNodes.keys():
							if AutomatonLabel == AutStartNodes[k]:
								Nodes.append(k)
						for k in Nodes:
							WorkList.add((k, GraphPointer, StackEndNode))
						if StackEndNode in poppedNodes:
							PoppedGraphPointers = poppedNodes[StackEndNode]
							for k in PoppedGraphPointers:
								WorkList.add((AutomatonEnd, k, StackPointer))
		if AutomatonPointer in AutFinalNodes:
			NewWays = GetWays(StackPointer, list(StackEdges))
			for i in NewWays:
				(NewAutomatonPointer, NewStackPointer) = i
				WorkList.add((NewAutomatonPointer, GraphPointer, NewStackPointer))
			(lbl, beg) = Stack[StackPointer]
			ways.add((beg, lbl, GraphPointer))
			if StackPointer in poppedNodes:
				(poppedNodes[StackPointer]).append(GraphPointer)
			else:
				poppedNodes[StackPointer] = [GraphPointer]
	return ways

if __name__ == "__main__":
	Type = None
	print("Please, choose an analysis type (1-3 or Matrix, Top-Down, Bottom-Up): ")
	while True:
		analysis = str(input())
		if (analysis == "Matrix") | (analysis == "1"):
			Type = 1
			break
		elif (analysis == "Top-Down") | (analysis == "2"):
			Type = 2
			break
		elif (analysis == "Bottom-Up") | (analysis == "3"):
			Type = 3
			break
		print("Wrong type. Please, try again: ")
	print("Enter the path to the graph file: ")
	Graph = str(input())
	if Type == 1:
		print("Enter the path to the grammar file: ")
	else:
		print("Enter the path to the recursive automaton file: ")
	Grammar = str(input())
	print("Enter the path to the output file (leave empty to display on screen): ")
	Out = str(input())
	graph = (pydot.graph_from_dot_file(Graph))[0]
	(Nodes, Edges, StartNodes, FinalNodes) = ParseGraph(graph)
	result = None
	if Type == 1:
		result = MatrixAnalysis(Grammar, Nodes, Edges)
	elif Type == 2:
		result = TopDownAnalysis(Grammar, Nodes, Edges)
	else:
		result = BottomUpAnalysis(Grammar, Nodes, Edges)
	if Out == "":
		print("Displaying results:")
		for i in result:
			(begin, label, end) = i
			print(str(begin) + ", " + str(label) + ", " + str(end))
	else:
		file = open(Out, 'w')
		for i in result:
			(begin, label, end) = i
			file.write(str(begin) + ", " + str(label) + ", " + str(end) + "\n")
		file.close()
		print("Results written to " + Out)