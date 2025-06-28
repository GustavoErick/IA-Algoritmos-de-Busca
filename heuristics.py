from puzzle import PuzzleState


def heuristic_h1(state: PuzzleState) -> int:
    """Número de peças fora do lugar ×2"""
    sorted_tiles = [i for i in range(1, 9)] + [0]
    wrong = sum(1 for i in range(9) if state.tiles[i] != 0 and state.tiles[i] != sorted_tiles[i])
    return wrong * 2

def heuristic_h2(state: PuzzleState) -> int:
    """Distância Manhattan × 2 considerando os 9 estados-meta cíclicos."""
    total = 0
    for i in range(9):
        tile = state.tiles[i]
        if tile == 0:
            continue

        # posição atual da peça
        cur_row, cur_col = divmod(i, 3)

        # duas posições corretas no ciclo 1‥8
        correct_pos1 = tile - 1           # onde ela fica no objetivo “clássico”
        correct_pos2 = tile % 8           # posição seguinte no ciclo (ou 0 → 8)

        row1, col1 = divmod(correct_pos1, 3)
        row2, col2 = divmod(correct_pos2, 3)

        dist1 = abs(cur_row - row1) + abs(cur_col - col1)
        dist2 = abs(cur_row - row2) + abs(cur_col - col2)

        total += min(dist1, dist2)

    return total * 2