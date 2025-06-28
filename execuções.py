# Parte 1: Largura vs. Profundidade vs. Custo Uniforme (30 execuções)
        print("\n" + "="*50)
        print("EXECUTANDO PARTE 1: Largura vs. Profundidade vs. Custo Uniforme")
        print("="*50)
        for i in range(1, 31):
            print(f"\nExecução {i}/30 - {time.strftime('%H:%M:%S')}")
            initial = generate_random_state()
            
            # i. Busca em Largura com todas funções de custo
            for cost_name, cost_func in cost_funcs.items():
                print(f"  BFS com {cost_name}...", end=' ', flush=True)
                result = algorithms['A1'](initial)
                if result['path']:
                    result['cost'] = sum(cost_func(step, step.action) for step in result['path'][1:])
                save_results('Parte1', 'A1', cost_name, None, initial, result)
                print("OK")
            
            # ii. Busca em Profundidade com todas funções de custo
            for cost_name, cost_func in cost_funcs.items():
                print(f"  DFS com {cost_name}...", end=' ', flush=True)
                result = algorithms['A2'](initial)
                if result['path']:
                    result['cost'] = sum(cost_func(step, step.action) for step in result['path'][1:])
                save_results('Parte1', 'A2', cost_name, None, initial, result)
                print("OK")
            
            # iii. Busca de Custo Uniforme com todas funções de custo
            for cost_name, cost_func in cost_funcs.items():
                print(f"  UCS com {cost_name}...", end=' ', flush=True)
                result = algorithms['A3'](initial, cost_func)
                save_results('Parte1', 'A3', cost_name, None, initial, result)
                print("OK")
        

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
        
        # Parte 3: Busca Gulosa vs. A* (30 execuções)
        print("\n" + "="*50)
        print("EXECUTANDO PARTE 3: Busca Gulosa vs. A*")
        print("="*50)
        for i in range(1, 31):
            print(f"\nExecução {i}/30 - {time.strftime('%H:%M:%S')}")
            initial = generate_random_state()
            
            # i. Busca Gulosa
            for heuristic_name, heuristic in heuristics.items():
                print(f"  Gulosa com {heuristic_name}...", end=' ', flush=True)
                result = algorithms['A4'](initial, heuristic)
                for cost_name, cost_func in cost_funcs.items():
                    if result['path']:
                        result['cost'] = sum(cost_func(step, step.action) for step in result['path'][1:])
                    save_results('Parte3', 'A4', cost_name, heuristic_name, initial, result)
                print("OK")
            
            # ii. Busca A* (igual Parte 2)
            for cost_name, cost_func in cost_funcs.items():
                for heuristic_name, heuristic in heuristics.items():
                    print(f"  A* com {cost_name}+{heuristic_name}...", end=' ', flush=True)
                    result = algorithms['A5'](initial, cost_func, heuristic)
                    save_results('Parte3', 'A5', cost_name, heuristic_name, initial, result)
                    print("OK")

    # Parte 4: Randomização de vizinhança (15 execuções, 10 repetições)
    for i in range(1, 16):
        print(f"\nExecução {i}/15 - {time.strftime('%H:%M:%S')}")
        initial = generate_random_state()

        # i. BFS randomizada
        for run in range(10):
            print(f"  BFS randomizada {run + 1}/10...", end=' ', flush=True)
            result = algorithms['A1'](PuzzleState(initial.tiles.copy()), randomize=True)
            for cost_name, cost_func in cost_funcs.items():
                if result['path']:
                    result['cost'] = sum(cost_func(step, step.action)
                                         for step in result['path'][1:])
                save_results('Parte4', 'A1-random', cost_name, None, initial, result)
            print("OK")

        # ii. DFS randomizada
        for run in range(10):
            print(f"  DFS randomizada {run + 1}/10...", end=' ', flush=True)
            result = algorithms['A2'](PuzzleState(initial.tiles.copy()), randomize=True)
            for cost_name, cost_func in cost_funcs.items():
                if result['path']:
                    result['cost'] = sum(cost_func(step, step.action)
                                         for step in result['path'][1:])
                save_results('Parte4', 'A2-random', cost_name, None, initial, result)
            print("OK")

