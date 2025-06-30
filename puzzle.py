import heapq
import random
from collections import deque
from typing import List, Tuple, Dict, Optional, Callable

_goal_base = [1, 2, 3, 4, 5, 6, 7, 8]
GOALS = {
    tuple(_goal_base[:i] + [0] + _goal_base[i:])
    for i in range(9)
}

class PuzzleState:
    """Representa um estado do 8-Puzzle"""
    def __init__(self, tiles: List[int], parent=None, action=None, cost=0):
        self.tiles = tiles          # Lista de 9 elementos (0 representa o espaço vazio)
        self.parent = parent        # Estado pai na árvore de busca
        self.action = action        # Ação que levou a este estado
        self.cost = cost            # Custo acumulado
        self.blank_pos = tiles.index(0)  # Posição do espaço vazio
        
    def __eq__(self, other):
        return self.tiles == other.tiles
    
    def __hash__(self):
        return hash(tuple(self.tiles))
    
    def __lt__(self, other):
        return self.cost < other.cost
    
    def is_goal(self) -> bool:
        """Retorna True se o tabuleiro é uma das 9 metas permitidas."""
        return tuple(self.tiles) in GOALS
    
    def get_successors(self, random_order=False) -> List['PuzzleState']:
        """Gera estados sucessores válidos"""
        moves = []
        row, col = self.blank_pos // 3, self.blank_pos % 3
        
        # Define possíveis movimentos (cima, direita, baixo, esquerda)
        actions = []
        if row > 0: actions.append(('up', -3))
        if col < 2: actions.append(('right', 1))
        if row < 2: actions.append(('down', 3))
        if col > 0: actions.append(('left', -1))
        
        if random_order:
            random.shuffle(actions)
            
        for action, delta in actions:
            new_tiles = self.tiles.copy()
            new_pos = self.blank_pos + delta
            new_tiles[self.blank_pos], new_tiles[new_pos] = new_tiles[new_pos], new_tiles[self.blank_pos]
            moves.append(PuzzleState(new_tiles, self, action, self.cost + 1))
            
        return moves
    
    def get_path(self) -> List['PuzzleState']:
        """Recupera o caminho desde o estado inicial"""
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return list(reversed(path))
    
    def __str__(self):
        return str(self.tiles)