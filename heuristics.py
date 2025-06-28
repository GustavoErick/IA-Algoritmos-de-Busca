
def heuristic_h1(state: PuzzleState) -> int:
    """Número de peças fora do lugar ×2"""
    sorted_tiles = [i for i in range(1, 9)] + [0]
    wrong = sum(1 for i in range(9) if state.tiles[i] != 0 and state.tiles[i] != sorted_tiles[i])
    return wrong * 2

def heuristic_h2(state: PuzzleState) -> int:
    """Distância Manhattan ×2 (considerando múltiplos objetivos)"""
    total = 0
    for i in range(9):
        tile = state.tiles[i]
        if tile == 0:
            continue
            
        # Posição atual
        current_row, current_col = i // 3, i % 3
        
        # Posições corretas possíveis (considerando múltiplos objetivos)
        correct_pos1 = tile - 1
        correct_pos2 = tile if tile < 8 else 8
        
        # Calcula distância Manhattan para ambas posições corretas
        row1, col1 = correct_pos1 // 3, correct_pos1 % 3
        dist1 = abs(current_row - row1) + abs(current_col - col1)
        
        row2, col2 = correct_pos2 // 3, correct_pos2 % 3
        dist2 = abs(current_row - row2) + abs(current_col - col2)
        
        # Usa a menor distância
        total += min(dist1, dist2)
    
    return total * 2