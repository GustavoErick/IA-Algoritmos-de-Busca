def breadth_first_search(initial_state: PuzzleState) -> dict:
    """Implementação da Busca em Largura"""
    queue = deque([initial_state])
    visited = set()
    nodes_generated = 0
    nodes_visited = 0
    
    while queue:
        current = queue.popleft()
        nodes_visited += 1
        
        if current.is_goal():
            path = current.get_path()
            return {
                'path': path,
                'cost': len(path) - 1,  # Número de ações
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }
        
        if current not in visited:
            visited.add(current)
            successors = current.get_successors()
            nodes_generated += len(successors)
            queue.extend(successors)
    
    return {
        'path': None,
        'cost': float('inf'),
        'nodes_generated': nodes_generated,
        'nodes_visited': nodes_visited
    }


def depth_first_search(initial_state: PuzzleState, max_depth=50) -> dict:
    """Implementação da Busca em Profundidade com limite"""
    stack = [(initial_state, 0)]
    visited = set()
    nodes_generated = 0
    nodes_visited = 0
    
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
        
        if current not in visited and depth < max_depth:
            visited.add(current)
            successors = current.get_successors()
            nodes_generated += len(successors)
            for successor in reversed(successors):
                stack.append((successor, depth + 1))
    
    return {
        'path': None,
        'cost': float('inf'),
        'nodes_generated': nodes_generated,
        'nodes_visited': nodes_visited
    }


def uniform_cost_search(initial_state: PuzzleState, cost_func: Callable) -> dict:
    """Implementação da Busca de Custo Uniforme"""
    heap = []
    heapq.heappush(heap, (0, initial_state))
    visited = set()
    nodes_generated = 0
    nodes_visited = 0
    
    while heap:
        current_cost, current = heapq.heappop(heap)
        nodes_visited += 1
        
        if current.is_goal():
            path = current.get_path()
            total_cost = sum(cost_func(step, step.action) for step in path[1:])
            return {
                'path': path,
                'cost': total_cost,
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }
        
        if current not in visited:
            visited.add(current)
            successors = current.get_successors()
            nodes_generated += len(successors)
            for successor in successors:
                action_cost = cost_func(successor, successor.action)
                heapq.heappush(heap, (current_cost + action_cost, successor))
    
    return {
        'path': None,
        'cost': float('inf'),
        'nodes_generated': nodes_generated,
        'nodes_visited': nodes_visited
    }


def greedy_search(initial_state: PuzzleState, heuristic: Callable) -> dict:
    """Implementação da Busca Gulosa"""
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), initial_state))
    visited = set()
    nodes_generated = 0
    nodes_visited = 0
    
    while heap:
        _, current = heapq.heappop(heap)
        nodes_visited += 1
        
        if current.is_goal():
            path = current.get_path()
            return {
                'path': path,
                'cost': len(path) - 1,  # Não usa função de custo durante a busca
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }
        
        if current not in visited:
            visited.add(current)
            successors = current.get_successors()
            nodes_generated += len(successors)
            for successor in successors:
                heapq.heappush(heap, (heuristic(successor), successor))
    
    return {
        'path': None,
        'cost': float('inf'),
        'nodes_generated': nodes_generated,
        'nodes_visited': nodes_visited
    }


def a_star_search(initial_state: PuzzleState, cost_func: Callable, heuristic: Callable) -> dict:
    """Implementação da Busca A*"""
    heap = []
    heapq.heappush(heap, (heuristic(initial_state), 0, initial_state))
    visited = set()
    nodes_generated = 0
    nodes_visited = 0
    
    while heap:
        _, current_cost, current = heapq.heappop(heap)
        nodes_visited += 1
        
        if current.is_goal():
            path = current.get_path()
            total_cost = sum(cost_func(step, step.action) for step in path[1:])
            return {
                'path': path,
                'cost': total_cost,
                'nodes_generated': nodes_generated,
                'nodes_visited': nodes_visited
            }
        
        if current not in visited:
            visited.add(current)
            successors = current.get_successors()
            nodes_generated += len(successors)
            for successor in successors:
                action_cost = cost_func(successor, successor.action)
                g = current_cost + action_cost
                f = g + heuristic(successor)
                heapq.heappush(heap, (f, g, successor))
    
    return {
        'path': None,
        'cost': float('inf'),
        'nodes_generated': nodes_generated,
        'nodes_visited': nodes_visited
    }

