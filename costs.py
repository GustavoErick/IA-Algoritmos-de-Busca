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


def cost_function_c4(parent: PuzzleState, action: str) -> int:
    # deslocamento que a ação aplica sobre o índice do zero
    delta = {'up': -3, 'right': 1, 'down': 3, 'left': -1}[action]
    new_blank = parent.blank_pos + delta          # posição do zero depois do movimento
    return 5 if new_blank == 4 else cost_function_c2(parent, action)