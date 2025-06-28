def run_experiments():
    """Executa todos os experimentos conforme especificado no trabalho"""
    # Dicionários com as funções disponíveis
    cost_functions = {
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
    
    # Cabeçalho do arquivo de resultados
    with open('results.csv', 'w') as f:
        f.write("Part,Algorithm,CostFunction,Heuristic,InitialState,GoalState,PathLength,Cost,NodesGenerated,NodesVisited\n")
    
    # Parte 1: Largura vs. Profundidade vs. Custo Uniforme (30 execuções)
    print("Executando Parte 1: Largura vs. Profundidade vs. Custo Uniforme")
    for i in range(1, 31):
        print(f"Execução {i}/30")
        initial_state = generate_random_state()
        
        # i. Busca em Largura com todas as funções de custo
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            result = algorithms['A1'](initial_state)
            # Para BFS, calculamos o custo após a busca (já que a ordem não é afetada)
            if result['path']:
                total_cost = sum(cost_functions[cost_name](step, step.action) for step in result['path'][1:])
                result['cost'] = total_cost
            save_results('Parte1', 'A1', cost_name, None, initial_state, result)
        
        # ii. Busca em Profundidade com todas as funções de custo
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            result = algorithms['A2'](initial_state)
            if result['path']:
                total_cost = sum(cost_functions[cost_name](step, step.action) for step in result['path'][1:])
                result['cost'] = total_cost
            save_results('Parte1', 'A2', cost_name, None, initial_state, result)
        
        # iii. Busca de Custo Uniforme com todas as funções de custo
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            result = algorithms['A3'](initial_state, cost_functions[cost_name])
            save_results('Parte1', 'A3', cost_name, None, initial_state, result)
    
    # Parte 2: Custo Uniforme vs. A* (30 execuções)
    print("\nExecutando Parte 2: Custo Uniforme vs. A*")
    for i in range(1, 31):
        print(f"Execução {i}/30")
        initial_state = generate_random_state()
        
        # i. Busca de Custo Uniforme com todas as funções de custo
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            result = algorithms['A3'](initial_state, cost_functions[cost_name])
            save_results('Parte2', 'A3', cost_name, None, initial_state, result)
        
        # ii. Busca A* com todas combinações de funções de custo e heurísticas
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            for heuristic_name in ['H1', 'H2']:
                result = algorithms['A5'](initial_state, cost_functions[cost_name], heuristics[heuristic_name])
                save_results('Parte2', 'A5', cost_name, heuristic_name, initial_state, result)
    
    # Parte 3: Busca Gulosa vs. A* (30 execuções)
    print("\nExecutando Parte 3: Busca Gulosa vs. A*")
    for i in range(1, 31):
        print(f"Execução {i}/30")
        initial_state = generate_random_state()
        
        # i. Busca Gulosa com ambas heurísticas
        for heuristic_name in ['H1', 'H2']:
            result = algorithms['A4'](initial_state, heuristics[heuristic_name])
            # Para busca gulosa, calculamos o custo com todas funções após a busca
            for cost_name in ['C1', 'C2', 'C3', 'C4']:
                if result['path']:
                    total_cost = sum(cost_functions[cost_name](step, step.action) for step in result['path'][1:])
                    result['cost'] = total_cost
                save_results('Parte3', 'A4', cost_name, heuristic_name, initial_state, result)
        
        # ii. Busca A* com todas combinações (igual à Parte 2)
        for cost_name in ['C1', 'C2', 'C3', 'C4']:
            for heuristic_name in ['H1', 'H2']:
                result = algorithms['A5'](initial_state, cost_functions[cost_name], heuristics[heuristic_name])
                save_results('Parte3', 'A5', cost_name, heuristic_name, initial_state, result)
    
    # Parte 4: Largura vs. Profundidade com randomização (15 execuções, 10 repetições cada)
    print("\nExecutando Parte 4: Buscas com randomização de vizinhança")
    for i in range(1, 16):
        print(f"Execução {i}/15")
        initial_state = generate_random_state()
        
        # i. Busca em Largura com randomização (10 repetições)
        for _ in range(10):
            result = algorithms['A1'](PuzzleState(initial_state.tiles.copy()))  # Nova instância
            # Calcula custo para todas funções
            for cost_name in ['C1', 'C2', 'C3', 'C4']:
                if result['path']:
                    total_cost = sum(cost_functions[cost_name](step, step.action) for step in result['path'][1:])
                    result['cost'] = total_cost
                save_results('Parte4', 'A1-random', cost_name, None, initial_state, result)
        
        # ii. Busca em Profundidade com randomização (10 repetições)
        for _ in range(10):
            result = algorithms['A2'](PuzzleState(initial_state.tiles.copy()))  # Nova instância
            for cost_name in ['C1', 'C2', 'C3', 'C4']:
                if result['path']:
                    total_cost = sum(cost_functions[cost_name](step, step.action) for step in result['path'][1:])
                    result['cost'] = total_cost
                save_results('Parte4', 'A2-random', cost_name, None, initial_state, result)
    
    print("\nTodos os experimentos foram concluídos! Resultados salvos em results.csv")


def main():
    """Função principal que executa o programa"""
    print("Iniciando experimentos do 8-Puzzle")
    print("=================================")
    
    try:
        run_experiments()
    except Exception as e:
        print(f"Erro durante a execução dos experimentos: {str(e)}")
        return
    
    print("\nAnálise dos resultados:")
    print("1. Os resultados detalhados de cada execução foram salvos em 'results.csv'")
    print("2. Você pode usar este arquivo para gerar estatísticas e gráficos")
    print("3. Para análises adicionais, considere usar pandas ou outras ferramentas")
    
    # Exemplo de como carregar e mostrar um resumo dos resultados
    try:
        import pandas as pd
        df = pd.read_csv('results.csv')
        print("\nResumo estatístico dos custos encontrados:")
        print(df.groupby(['Part', 'Algorithm'])['Cost'].describe())
    except:
        print("\nInstale pandas (pip install pandas) para análise estatística avançada")

if __name__ == "__main__":
    main()