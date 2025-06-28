from puzzle import PuzzleState
from costs import cost_function_c1, cost_function_c2, cost_function_c3, cost_function_c4
from heuristics import heuristic_h1, heuristic_h2
from algorithms import breadth_first_search, depth_first_search, greedy_search, a_star_search, uniform_cost_search
import random
from typing import List

def save_results(part: str, algorithm: str, cost_func: str, heuristic: str, 
                 initial_state: PuzzleState, result: dict):
    """Salva os resultados em um arquivo"""
    with open('results.csv', 'a') as f:
        f.write(f"{part},{algorithm},{cost_func},{heuristic if heuristic else 'None'},")
        f.write(f"{initial_state},{result['path'][-1] if result['path'] else 'None'},")
        f.write(f"{len(result['path']) if result['path'] else 0},{result['cost']},")
        f.write(f"{result['nodes_generated']},{result['nodes_visited']}\n")


def is_solvable(tiles: List[int]) -> bool:
    # Conta o número de inversões
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            # Ignora o espaço vazio (0)
            if tiles[i] != 0 and tiles[j] != 0 and tiles[i] > tiles[j]:
                inversions += 1
    
    # Encontra a linha do espaço vazio (contando a partir do fundo)
    blank_row = 3 - (tiles.index(0) // 3)  # 1, 2 ou 3 (de baixo para cima)
    
    # Regra para solvabilidade:
    # - Se o número de inversões for par, o espaço vazio deve estar em linha ímpar
    # - Se o número de inversões for ímpar, o espaço vazio deve estar em linha par
    return (inversions % 2 == 0 and blank_row % 2 == 1) or \
           (inversions % 2 == 1 and blank_row % 2 == 0)


def generate_random_state() -> PuzzleState:
    """Gera um estado inicial aleatório válido"""
    tiles = list(range(9))  # 0-8 (0 é o espaço vazio)
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):
            return PuzzleState(tiles)


def main():
    """Função principal que executa todos os experimentos do trabalho"""
    import time
    from datetime import timedelta
    
    print("\n" + "="*50)
    print("SISTEMA DE EXPERIMENTOS PARA O 8-PUZZLE")
    print("="*50)
    print("Este programa executará todos os experimentos do trabalho:")
    print("- Parte 1: Largura vs. Profundidade vs. Custo Uniforme")
    print("- Parte 2: Custo Uniforme vs. A*")
    print("- Parte 3: Busca Gulosa vs. A*")
    print("- Parte 4: Buscas com Randomização de Vizinhança")
    print("\nOs resultados serão salvos em 'results.csv'")
    print("="*50 + "\n")
    
    # Verifica se o usuário quer continuar
    start = input("Pressione Enter para iniciar ou 'q' para sair: ")
    if start.lower() == 'q':
        return
    
    # Cria arquivo de resultados com cabeçalho
    with open('results.csv', 'w') as f:
        f.write("Part,Algorithm,CostFunction,Heuristic,InitialState,GoalState,PathLength,Cost,NodesGenerated,NodesVisited\n")
    
    # Registra tempo inicial
    start_time = time.time()
    
    try:
        # Dicionários com as funções disponíveis
        cost_funcs = {
            'C1': cost_function_c1,
            'C2': cost_function_c2,
            'C3': cost_function_c3,
            'C4': cost_function_c4
        }
        
        heuristics = {
            'H1': heuristic_h1,
            'H2': heuristic_h2
        }
        
        algorithms = {
            'A1': breadth_first_search,
            'A2': depth_first_search,
            'A3': uniform_cost_search,
            'A4': greedy_search,
            'A5': a_star_search
        }
        
        # Parte 2: Custo Uniforme vs. A* (30 execuções)
        print("\n" + "="*50)
        print("EXECUTANDO PARTE 2: Custo Uniforme vs. A*")
        print("="*50)
        for i in range(1, 31):
            print(f"\nExecução {i}/30 - {time.strftime('%H:%M:%S')}")
            initial = generate_random_state()
            
            # i. Busca de Custo Uniforme
            for cost_name, cost_func in cost_funcs.items():
                print(f"  UCS com {cost_name}...", end=' ', flush=True)
                result = algorithms['A3'](initial, cost_func)
                save_results('Parte2', 'A3', cost_name, None, initial, result)
                print("OK")
            
            # ii. Busca A* com todas combinações
            for cost_name, cost_func in cost_funcs.items():
                for heuristic_name, heuristic in heuristics.items():
                    print(f"  A* com {cost_name}+{heuristic_name}...", end=' ', flush=True)
                    result = algorithms['A5'](initial, cost_func, heuristic)
                    save_results('Parte2', 'A5', cost_name, heuristic_name, initial, result)
                    print("OK")
        
    except KeyboardInterrupt:
        print("\nExecução interrompida pelo usuário!")
    except Exception as e:
        print(f"\nERRO: {str(e)}")
    finally:
        # Calcula tempo total de execução
        total_time = timedelta(seconds=int(time.time() - start_time))
        print("\n" + "="*50)
        print("EXECUÇÃO CONCLUÍDA")
        print("="*50)
        print(f"Tempo total: {total_time}")
        print(f"Resultados salvos em: results.csv")
        
        # Mostra estatísticas básicas se pandas estiver instalado
        try:
            import pandas as pd
            df = pd.read_csv('results.csv')
            print("\nRESUMO ESTATÍSTICO:")
            print(df.groupby(['Part', 'Algorithm'])['Cost'].describe())
        except:
            print("\nInstale pandas para análise estatística completa (pip install pandas)")

if __name__ == "__main__":
    main()