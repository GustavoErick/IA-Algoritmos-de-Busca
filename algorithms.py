from puzzle import PuzzleState
from typing import Callable
import random
from collections import deque
import heapq
from typing import Optional


def breadth_first_search(
    initial_state: PuzzleState,
    *,
    randomize: bool = False
) -> dict:
    """Busca em Largura (A1).  randomize=True embaralha a ordem dos vizinhos."""
    queue = deque([initial_state])
    visited = {initial_state}           
    nodes_generated = nodes_visited = 0

    while queue:
        current = queue.popleft()
        nodes_visited += 1

        if current.is_goal():
            path = current.get_path()
            return {
                'path': path,
                'cost': len(path) - 1,
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }

        for succ in current.get_successors(random_order=randomize):
            if succ not in visited:
                visited.add(succ)
                queue.append(succ)
                nodes_generated += 1

    return {'path': None, 'cost': float('inf'),
            'nodes_generated': nodes_generated,
            'nodes_visited': nodes_visited}


def depth_first_search(
    initial_state: PuzzleState,
    *,
    randomize: bool = False,
    max_depth: Optional[int] = 100
) -> dict:
    """Busca em Profundidade (A2) com limite.  randomize=True → vizinhos embaralhados."""
    stack = [(initial_state, 0)]
    visited = {initial_state}           # marca já na inserção
    nodes_generated = nodes_visited = 0

    while stack:
        current, depth = stack.pop()
        nodes_visited += 1

        if current.is_goal():
            path = current.get_path()
            return {
                'path': path,
                'cost': len(path) - 1,
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }

        if max_depth is None or depth < max_depth:
            succs = current.get_successors(random_order=randomize)
            for succ in (reversed(succs) if not randomize else succs):
                if succ not in visited:
                    visited.add(succ)
                    stack.append((succ, depth + 1))
                    nodes_generated += 1

    return {'path': None, 'cost': float('inf'),
            'nodes_generated': nodes_generated,
            'nodes_visited': nodes_visited}


# Busca de Custo Uniforme  (A3)
def uniform_cost_search(initial_state: PuzzleState,
                        cost_func: Callable) -> dict:
    """Uniform Cost Search (fila de prioridade no custo acumulado g)."""
    heap = [(0, initial_state)]             # (g, nó)
    best_g = {initial_state: 0}
    visited = set()
    nodes_generated = nodes_visited = 0

    while heap:
        g, current = heapq.heappop(heap)
        if current in visited:          # nó já expandido com custo menor
            continue
        visited.add(current)
        nodes_visited += 1

        if current.is_goal():
            return {
                'path': current.get_path(),
                'cost': g,              # g já é o custo total
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }

        for succ in current.get_successors():
            step_cost = cost_func(current, succ.action)     # ← pai + ação
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                heapq.heappush(heap, (new_g, succ))
                nodes_generated += 1

    return {'path': None, 'cost': float('inf'),
            'nodes_generated': nodes_generated,
            'nodes_visited': nodes_visited}


# Busca Gulosa  (A4)  – só pequenos ajustes de duplicata / contagem
def greedy_search(initial_state: PuzzleState,
                  heuristic: Callable) -> dict:
    """Best-First Search puro (prioridade só na heurística h)."""
    h0 = heuristic(initial_state)
    heap = [(h0, initial_state)]
    visited = {initial_state}
    nodes_generated = nodes_visited = 0

    while heap:
        _, current = heapq.heappop(heap)
        nodes_visited += 1

        if current.is_goal():
            return {
                'path': current.get_path(),
                'cost': len(current.get_path()) - 1,   # custo em passos
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }

        for succ in current.get_successors():
            if succ not in visited:
                visited.add(succ)
                heapq.heappush(heap, (heuristic(succ), succ))
                nodes_generated += 1

    return {'path': None, 'cost': float('inf'),
            'nodes_generated': nodes_generated,
            'nodes_visited': nodes_visited}


# Busca A*  (A5)
def a_star_search(initial_state: PuzzleState,
                  cost_func: Callable,
                  heuristic: Callable) -> dict:
    """A* com f = g + h; desempate no menor g."""
    h0 = heuristic(initial_state)
    heap = [(h0, 0, initial_state)]      # (f, g, nó)
    best_g = {initial_state: 0}
    visited = set()
    nodes_generated = nodes_visited = 0

    while heap:
        f, g, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)
        nodes_visited += 1

        if current.is_goal():
            return {
                'path': current.get_path(),
                'cost': g,               # g é o custo ótimo encontrado
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }

        for succ in current.get_successors():
            step_cost = cost_func(current, succ.action)
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                new_f = new_g + heuristic(succ)
                heapq.heappush(heap, (new_f, new_g, succ))
                nodes_generated += 1

    return {'path': None, 'cost': float('inf'),
            'nodes_generated': nodes_generated,
            'nodes_visited': nodes_visited}