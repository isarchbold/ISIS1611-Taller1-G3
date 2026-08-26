from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    # TODO: Add your code here
    frontier = utils.Stack()
    startState = problem.getStartState()
    frontier.push((startState, []))

    visited = set()

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        if state not in visited:
            visited.add(state)

            for successor, action, stepCost in problem.getSuccessors(state):
                if successor not in visited:
                    frontier.push((successor, actions + [action]))

    return []
    #utils.raiseNotDefined()


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    frontier = utils.Queue()
    startState = problem.getStartState()
    frontier.push((startState, []))

    visited = set()

    visited.add(startState)

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        for successor, action, stepCost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)

                newActions = actions + [action]
                frontier.push((successor, newActions))
    return []

def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    #Se reusa codigo de data structures de EDA de dijkstra 
    # TODO: Add your code here
    nodos_cola= utils.PriorityQueue()
    nodos_cola.push((problem.getStartState(), [], 0), 0)
    
    visitados = set() #por complejidad 
    
    while not nodos_cola.isEmpty():
        estadoActual, acciones, costoAcumulado = nodos_cola.pop()
        
        if problem.isGoalState(estadoActual):
            return acciones
        if estadoActual not in visitados:
            visitados.add(estadoActual)
            for sucesor, accion, costo in problem.getSuccessors(estadoActual):
                if sucesor not in visitados:
                    nuevoCosto = costoAcumulado + costo
                    nodos_cola.push((sucesor, acciones + [accion], nuevoCosto), nuevoCosto)
        
        
        
    
    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    utils.raiseNotDefined()


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
