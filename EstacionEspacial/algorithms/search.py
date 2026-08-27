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
    nodos_cola= utils.PriorityQueue()
    nodos_cola.push((problem.getStartState(), [], 0), 0)
    visitados = set()
    
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
    frontera = utils.PriorityQueue()
    estadoInicial = problem.getStartState()
    frontera.push((estadoInicial, [], 0), heuristic(estadoInicial, problem))

    visitados = set()

    while not frontera.isEmpty():
        estadoActual, acciones, costoAcumulado = frontera.pop()

        if problem.isGoalState(estadoActual):
            return acciones
        if estadoActual not in visitados:
            visitados.add(estadoActual)
            for sucesor, accion, costo in problem.getSuccessors(estadoActual):
                if sucesor not in visitados:
                    nuevoCosto = costoAcumulado + costo
                    prioridad = nuevoCosto + heuristic(sucesor, problem)
                    frontera.push((sucesor, acciones + [accion], nuevoCosto), prioridad)
    return []
# Abbreviations 
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch