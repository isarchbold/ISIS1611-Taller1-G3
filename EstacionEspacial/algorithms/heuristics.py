import math
from collections import deque
from typing import Tuple

from algorithms import utils
from algorithms.problems import SystemRepairProblem

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def _manhattanDistance(a, b):
    """
    Distancia Manhattan entre dos posiciones (x, y).
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _euclideanDistance(a, b):
    """
    Distancia euclidiana entre dos posiciones (x, y).
    """
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

def _phaseDistance(state, problem, distance):
    """
    Regla base del taller: estimar la distancia directa al proximo objetivo
    OBLIGATORIO de la mision, segun la fase en la que va el robot.
    """
    # DiagnosticProblem: el estado es directamente una posicion (x, y).
    if isinstance(state[0], (int, float)):
        return distance(state, problem.goal)

    # ModuleRepairProblem: (position, hasModule).
    if len(state) == 2:
        position, hasModule = state
        if not hasModule:
            return distance(position, problem.modulePosition)
        return distance(position, problem.controlPosition)

    # SystemRepairProblem: (position, hasKit, pendingSystems).
    position, hasKit, pendingSystems = state
    if not hasKit:
        return distance(position, problem.kitPosition)
    if len(pendingSystems) > 0:
        return min(distance(position, system) for system in pendingSystems)
    return distance(position, problem.controlPosition)


def _mazeDistancesFrom(source, walls):
    """
    Devuelve un diccionario {posicion: distancia real en pasos}. 
    """
    distances = {source: 0}
    queue = deque([source])
    while queue:
        x, y = queue.popleft()
        currentDistance = distances[(x, y)]
        for dx, dy in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            nextX, nextY = x + dx, y + dy
            if nextX < 0 or nextX >= walls.width:
                continue
            if nextY < 0 or nextY >= walls.height:
                continue
            nextPosition = (nextX, nextY)
            if nextPosition in distances:
                continue
            if walls[nextX][nextY]:
                continue
            distances[nextPosition] = currentDistance + 1
            queue.append(nextPosition)
    return distances


def _mazeDistance(origin, destination, problem):
    """
    Distancia real (con muros) entre dos celdas, cacheada en problem.heuristicInfo.
    """
    cache = problem.heuristicInfo.setdefault("mazeDistances", {})
    if origin not in cache:
        cache[origin] = _mazeDistancesFrom(origin, problem.walls)
    return cache[origin].get(destination, 999999)

def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.
    """
    # TODO: Add your code here
    return _phaseDistance(state, problem, _manhattanDistance)

def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.
    """
    # TODO: Add your code here
    return _phaseDistance(state, problem, _euclideanDistance)


def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem):
    """
    Your heuristic for the SystemRepairProblem.
    """
    # TODO: Add your code here
    position, hasKit, pendingSystems = state
    controlPosition = problem.controlPosition
    if len(pendingSystems) == 0:
        return _mazeDistance(position, controlPosition, problem)
    if hasKit:
        return max(
            _mazeDistance(system, position, problem)
            + _mazeDistance(system, controlPosition, problem)
            for system in pendingSystems
        )
    kitPosition = problem.kitPosition
    if "kitToSystemToControl" not in problem.heuristicInfo:
        problem.heuristicInfo["kitToSystemToControl"] = max(
            _mazeDistance(system, kitPosition, problem)
            + _mazeDistance(system, controlPosition, problem)
            for system in problem.systemPositions)
    return (_mazeDistance(kitPosition, position, problem) + problem.heuristicInfo["kitToSystemToControl"])