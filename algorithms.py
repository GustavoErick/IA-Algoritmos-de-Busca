from __future__ import annotations

"""Algoritmos de busca para o projeto 8-Puzzle.
Cada rotina devolve um dicionário com as chaves:
    path             – lista[PuzzleState] do início até o objetivo (incluso) ou None
    cost             – custo do caminho solução (de acordo com a função de custo da busca)
    nodes_generated  – total de nós inseridos na fronteira
    nodes_visited    – total de nós efetivamente expandidos (retirados da fronteira)

As implementações seguem as convenções exigidas no trabalho:
  • A1 – Busca em Largura (BFS)
  • A2 – Busca em Profundidade (DFS) com limite opcional de profundidade
  • A3 – Busca de Custo Uniforme (UCS)
  • A4 – Busca Gulosa (Greedy Best-First)
  • A5 – Busca A* (A estrela)

Todos os algoritmos compartilham dois comportamentos opcionais:
  • randomize (bool)       – se True, os sucessores são gerados em ordem aleatória
  • max_depth (int|None)   – limite de profundidade da DFS (None = ilimitado)
"""

from collections import deque
from typing import Callable, Optional
import heapq
from puzzle import PuzzleState


def _expand_successors(state: PuzzleState, *, randomize: bool):
    """Yield successors optionally shuffled."""
    succs = state.get_successors(random_order=randomize)
    # For DFS without randomization we push in reverse to keep classic LIFO order
    return succs if randomize else list(reversed(succs))

# ──────────────────────────────────────────────
# A1 – Breadth‑First Search
# ──────────────────────────────────────────────

def breadth_first_search(initial_state: PuzzleState, *, randomize: bool = False) -> dict:
    queue = deque([initial_state])
    visited = {initial_state}
    nodes_generated = nodes_visited = 0

    while queue:
        current = queue.popleft()
        nodes_visited += 1

        if current.is_goal():
            path = current.get_path()
            return {
                "path": path,
                "cost": len(path) - 1,
                "nodes_generated": nodes_generated,
                "nodes_visited": nodes_visited,
            }

        for succ in current.get_successors(random_order=randomize):
            if succ not in visited:
                visited.add(succ)
                queue.append(succ)
                nodes_generated += 1

    return {
        "path": None,
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_visited": nodes_visited,
    }

# ──────────────────────────────────────────────
# A2 – Depth‑First Search (with optional limit)
# ──────────────────────────────────────────────

def depth_first_search(
    initial_state: PuzzleState,
    *,
    randomize: bool = False,
    max_depth: Optional[int] = 100,
) -> dict:
    stack: list[tuple[PuzzleState, int]] = [(initial_state, 0)]
    visited = {initial_state}
    nodes_generated = nodes_visited = 0

    while stack:
        current, depth = stack.pop()
        nodes_visited += 1

        if current.is_goal():
            path = current.get_path()
            return {
                "path": path,
                "cost": len(path) - 1,
                "nodes_generated": nodes_generated,
                "nodes_visited": nodes_visited,
            }

        if max_depth is None or depth < max_depth:
            for succ in _expand_successors(current, randomize=randomize):
                if succ not in visited:
                    visited.add(succ)
                    stack.append((succ, depth + 1))
                    nodes_generated += 1

    return {
        "path": None,
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_visited": nodes_visited,
    }

# ──────────────────────────────────────────────
# A3 – Uniform‑Cost Search
# ──────────────────────────────────────────────

def uniform_cost_search(initial_state: PuzzleState, cost_func: Callable) -> dict:
    heap: list[tuple[int, PuzzleState]] = [(0, initial_state)]  # (g, state)
    best_g = {initial_state: 0}
    visited = set()
    nodes_generated = nodes_visited = 0

    while heap:
        g, current = heapq.heappop(heap)
        if current in visited:
            continue  # stale entry
        visited.add(current)
        nodes_visited += 1

        if current.is_goal():
            return {
                "path": current.get_path(),
                "cost": g,
                "nodes_generated": nodes_generated,
                "nodes_visited": nodes_visited,
            }

        for succ in current.get_successors():
            step_cost = cost_func(current, succ.action)
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                heapq.heappush(heap, (new_g, succ))
                nodes_generated += 1

    return {
        "path": None,
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_visited": nodes_visited,
    }

# ──────────────────────────────────────────────
# A4 – Greedy Best‑First Search
# ──────────────────────────────────────────────

def greedy_search(initial_state: PuzzleState, heuristic: Callable) -> dict:
    h0 = heuristic(initial_state)
    heap: list[tuple[int, PuzzleState]] = [(h0, initial_state)]  # (h, state)
    visited = {initial_state}
    nodes_generated = nodes_visited = 0

    while heap:
        _, current = heapq.heappop(heap)
        nodes_visited += 1

        if current.is_goal():
            path = current.get_path()
            return {
                "path": path,
                "cost": len(path) - 1,
                "nodes_generated": nodes_generated,
                "nodes_visited": nodes_visited,
            }

        for succ in current.get_successors():
            if succ not in visited:
                visited.add(succ)
                heapq.heappush(heap, (heuristic(succ), succ))
                nodes_generated += 1

    return {
        "path": None,
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_visited": nodes_visited,
    }

# ──────────────────────────────────────────────
# A5 – A* Search
# ──────────────────────────────────────────────

def a_star_search(initial_state: PuzzleState, cost_func: Callable, heuristic: Callable) -> dict:
    h0 = heuristic(initial_state)
    heap: list[tuple[int, int, PuzzleState]] = [(h0, 0, initial_state)]  # (f, g, state)
    best_g = {initial_state: 0}
    visited = set()
    nodes_generated = nodes_visited = 0

    while heap:
        f, g, current = heapq.heappop(heap)
        if current in visited:
            continue  # stale entry
        visited.add(current)
        nodes_visited += 1

        if current.is_goal():
            return {
                "path": current.get_path(),
                "cost": g,
                "nodes_generated": nodes_generated,
                "nodes_visited": nodes_visited,
            }

        for succ in current.get_successors():
            step_cost = cost_func(current, succ.action)
            new_g = g + step_cost
            if succ not in best_g or new_g < best_g[succ]:
                best_g[succ] = new_g
                new_f = new_g + heuristic(succ)
                heapq.heappush(heap, (new_f, new_g, succ))
                nodes_generated += 1

    return {
        "path": None,
        "cost": float("inf"),
        "nodes_generated": nodes_generated,
        "nodes_visited": nodes_visited,
    }
