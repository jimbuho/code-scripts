/*

Test Hackerrank IA Princess Rescue in Goland

*/
package main

import (
	"fmt"
	"time"
)

type Neighbour struct {
	Name string
	Location string
}

type Node struct {
	Name string
	Neighbours []Neighbour
	Color string
}

func buildNode(name string, color string, neighbours []Neighbour) *Node {
	e := new(Node)
    e.Name = name
    e.Color = color
    e.Neighbours = neighbours
    return e
}

func (n Node) GetNeighbour(name string) Neighbour {
	resp := Neighbour{}
	neighbours := n.Neighbours
    for i:=0; i<len(neighbours); i++ {
    	if neighbours[i].Name == name {
    		resp = neighbours[i]
    		break
    	}
    }
    return resp
}

type Graph struct {
	Matrix [][]string
	Nodes map[string]Node
	Size uint8
}

func buildGraph(matrix [][]string, size uint8) *Graph {
	e := new(Graph)
    e.Matrix = matrix
    e.Size = size
    e.Nodes = make(map[string]Node)
    return e
}

func (g Graph) GetNeighbours(r int, c int) []Neighbour {
	var n []Neighbour
	if r > 0 {
		nodeName := string(fmt.Sprintf("%d-%d", r-1, c))
		n = append(n, Neighbour{Name:nodeName, Location:"UP"})
	}
	if r < int(g.Size)-1 {
		nodeName := fmt.Sprintf("%d-%d", r+1, c)
		n = append(n, Neighbour{Name:nodeName, Location:"DOWN"})
	}
	if c > 0 {
		nodeName := fmt.Sprintf("%d-%d", r, c-1)
		n = append(n, Neighbour{Name:nodeName, Location:"LEFT"})
	}
	if c < int(g.Size)-1 {
		nodeName := fmt.Sprintf("%d-%d", r, c+1)
		n = append(n, Neighbour{Name:nodeName, Location:"RIGHT"})
	}

	return n
}

func (g Graph) GetNode(name string) Node {
	return g.Nodes[name]
}

func (g Graph) GetNodeByColor(color string) Node {
	resp := Node{}
	for _, element := range g.Nodes {
        if element.Color == color {
        	resp = element
        	break
        }
    }

    return resp
}

func (g Graph) Traduce(path []Node) []string {
	var response []string
	var lastV Node
	firstTime := true
	for i:=0; i<len(path); i++ {
		v := path[i]
		if !firstTime {
			node := g.Nodes[lastV.Name]
			n := node.GetNeighbour(v.Name)
			response = append(response, n.Location)
		}
		firstTime = false
		lastV = path[i]
	}

	return response
}

func (g Graph) Build() {
	N := int(g.Size)
	for i:=0; i<int(N*N); i++ {
		row := int(int(i)/N)
		col := int(i) % N
		nodeName := fmt.Sprintf("%d-%d", row, col)
		g.Nodes[nodeName] = Node{Name:nodeName, Color:g.Matrix[row][col], 
		Neighbours:g.GetNeighbours(row,col)}
	}
}

func IsInSlice(a Node, list []Node) bool {
    for _, b := range list {
        if b.Name == a.Name {
            return true
        }
    }
    return false
}

type Queue struct {
	Items [][]Node
}

func buildQueue(start Node) *Queue {
	s := Queue{}
    s.Init(start)
    return &s
}

func (q *Queue) Init(start Node) *Queue {
	q.Items = [][]Node{}
	
	var startNodes = []Node {start}
	q.Add(startNodes)
	
	return q
}

func (q *Queue) Pop() []Node {
	x := q.Items[0]
	q.Items = q.Items[1:len(q.Items)]
	return x
}

func (q *Queue) HasElements() bool {
	has := len(q.Items) > 0
	return has
}

func (q *Queue) Print(title string) {
	fmt.Print(title)
	for _, element := range q.Items {
		fmt.Print("[")
		for _, subElement := range element {
			fmt.Print(subElement.Name,",")
		}
		fmt.Print("],")
	}
	fmt.Print("\n")
}

func (q *Queue) Add(row []Node) {
	q.Items = append(q.Items, row)
}

func BFS(graph *Graph, start Node, goal Node) []Node {
	var response []Node
	var explored []Node
	queue := buildQueue(start)
	
	if start.Name == goal.Name {
		fmt.Println("Start and Goal are same")	
	}

	counter := 0
	for queue.HasElements() {
		//queue.Print("Queue BEFORE ")
		path := queue.Pop()
		node := path[len(path)-1]
		//queue.Print("Queue AFTER ")

		if !IsInSlice(node, explored) {
			neighbours := node.Neighbours
			for i:=0; i<len(neighbours); i++ {
				var newPath []Node
				newPath = append(newPath, path...)
				newPath = append(newPath, graph.GetNode(neighbours[i].Name))
				queue.Add(newPath)
				//queue.Print("Queue INSIDE ")
				if neighbours[i].Name == goal.Name {
					return newPath
				}
			}
		}

		counter += 1
	}

	fmt.Println("The path to goal was not reached")
	return response
}

func main() {
	start := time.Now().UnixNano() / int64(time.Microsecond)

	var matrix = [][]string{
        {"-","m","-"},
        {"-","-","-"},	
        {"p","-","-"},
    }

    graph := buildGraph(matrix, 3)
    graph.Build()

    bfs := BFS(graph, graph.GetNodeByColor("m"), graph.GetNodeByColor("p"))

    shortPath := graph.Traduce(bfs)

    for _, p := range shortPath {
    	fmt.Println(p)
    }

    //elapsed := time.Since(start)
    end := time.Now().UnixNano() / int64(time.Microsecond)
    elapsed := end - start
    fmt.Printf("Execution Timelapse: %d microseconds\n", elapsed)
}