from puzzle import PuzzleState

def cost_function_c1(state: PuzzleState, action: str) -> int:
    """Todas as ações custam 2"""
    return 2

def cost_function_c2(state: PuzzleState, action: str) -> int:
    """Vertical=2, Horizontal=3"""
    return 2 if action in ['up', 'down'] else 3

def cost_function_c3(state: PuzzleState, action: str) -> int:
    """Vertical=3, Horizontal=2"""
    return 3 if action in ['up', 'down'] else 2

def cost_function_c4(state: PuzzleState, action: str) -> int:
    """Como C2, mas ação para centro custa 5"""
    base_cost = cost_function_c2(state, action)
    new_blank_pos = state.blank_pos + {'up': -3, 'right': 1, 'down': 3, 'left': -1}[action]
    return 5 if new_blank_pos == 4 else base_cost  # Posição 4 é o centro
