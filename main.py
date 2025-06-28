# main.py  ──────────────────────────────────────────────────────────────
from __future__ import annotations
import argparse, random, time, csv
from datetime import timedelta
from typing import List

from puzzle import PuzzleState
from costs import cost_function_c1, cost_function_c2, cost_function_c3, cost_function_c4
from heuristics import heuristic_h1, heuristic_h2
from algorithms import (
    breadth_first_search,
    depth_first_search,
    uniform_cost_search,
    greedy_search,
    a_star_search,
)

# ───────────────────────────────────────────────────────────────────────
def save_results(
    part: str,
    algorithm: str,
    cost_name: str,
    heuristic_name: str | None,
    initial_state: PuzzleState,
    result: dict,
    writer: csv.writer,
):
    """Registra uma linha no CSV."""
    path_list = result["path"] or []
    path_serialized = "|".join(str(s) for s in path_list) if path_list else "None"
    writer.writerow(
        [
            part,
            algorithm,
            cost_name,
            heuristic_name or "None",
            initial_state,
            path_serialized,
            len(path_list),
            result["cost"],
            result["nodes_generated"],
            result["nodes_visited"],
        ]
    )


# ───────────────────────────────────────────────────────────────────────
def is_solvable(tiles: List[int]) -> bool:
    """8-Puzzle 3 × 3 é solucionável se #inversões for par."""
    inversions = sum(
        1
        for i in range(len(tiles))
        for j in range(i + 1, len(tiles))
        if tiles[i] and tiles[j] and tiles[i] > tiles[j]
    )
    return inversions % 2 == 0


def generate_random_state() -> PuzzleState:
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):
            return PuzzleState(tiles)


# ───────────────────────────────────────────────────────────────────────
def run_single(args, cost_funcs, heuristics, algos, writer):
    """Permite executar apenas um cenário via --single A5,C2,H1"""
    token = args.single.split(",")
    if len(token) not in {2, 3}:
        raise ValueError("Use: ALG,Ck[,Hj] (ex.: A5,C3,H2)")
    alg_key, cost_key = token[0], token[1]
    heur_key = token[2] if len(token) == 3 else None

    initial = generate_random_state()
    if alg_key == "A1":
        res = algos[alg_key](initial)
    elif alg_key == "A2":
        res = algos[alg_key](initial)
    elif alg_key == "A3":
        res = algos[alg_key](initial, cost_funcs[cost_key])
    elif alg_key == "A4":
        if heur_key is None:
            raise ValueError("Gulosa (A4) precisa de heurística")
        res = algos[alg_key](initial, heuristics[heur_key])
    elif alg_key == "A5":
        if heur_key is None:
            raise ValueError("A* (A5) precisa de heurística")
        res = algos[alg_key](initial, cost_funcs[cost_key], heuristics[heur_key])
    else:
        raise ValueError("Algoritmo desconhecido")

    save_results("Single", alg_key, cost_key, heur_key, initial, res, writer)
    print("Resultado salvo. Arquivo: results.csv")


# ───────────────────────────────────────────────────────────────────────
def main():
    banner = "=" * 60
    print(f"\n{banner}\nSISTEMA DE EXPERIMENTOS PARA O 8-PUZZLE\n{banner}")
    print("Partes executadas: 1, 2, 3 e 4 (conforme enunciado).\n")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--single",
        help="Executa apenas um cenário: ALG,Ck[,Hj]  (ex.: A5,C2,H1)",
        default="",
    )
    args = parser.parse_args()

    # dicionários
    cost_funcs = {"C1": cost_function_c1, "C2": cost_function_c2,
                  "C3": cost_function_c3, "C4": cost_function_c4}
    heuristics = {"H1": heuristic_h1, "H2": heuristic_h2}
    algos = {"A1": breadth_first_search, "A2": depth_first_search,
             "A3": uniform_cost_search, "A4": greedy_search, "A5": a_star_search}

    # arquivo CSV
    csvfile = open("results.csv", "w", newline="")
    writer = csv.writer(csvfile)
    writer.writerow(
        [
            "Part",
            "Algorithm",
            "CostFunction",
            "Heuristic",
            "InitialState",
            "Path",
            "PathLength",
            "Cost",
            "NodesGenerated",
            "NodesVisited",
        ]
    )

    # single-run rápido?
    if args.single:
        run_single(args, cost_funcs, heuristics, algos, writer)
        csvfile.close()
        return

    start_time = time.time()

    # ── PARTE 1 ── Largura × Profundidade × UCS
    print("\n" + banner + "\nEXECUTANDO PARTE 1")
    for i in range(1, 31):
        print(f"Parte 1 – execução {i}/30")
        initial = generate_random_state()

        # BFS
        for ck, cf in cost_funcs.items():
            res = algos["A1"](initial)
            if res["path"]:
                res["cost"] = sum(cf(p, p.action) for p in res["path"][1:])
            save_results("Parte1", "A1", ck, None, initial, res, writer)

        # DFS
        for ck, cf in cost_funcs.items():
            res = algos["A2"](initial)
            if res["path"]:
                res["cost"] = sum(cf(p, p.action) for p in res["path"][1:])
            save_results("Parte1", "A2", ck, None, initial, res, writer)

        # UCS
        for ck, cf in cost_funcs.items():
            res = algos["A3"](initial, cf)
            save_results("Parte1", "A3", ck, None, initial, res, writer)

    # ── PARTE 2 ── UCS × A*
    print("\n" + banner + "\nEXECUTANDO PARTE 2")
    for i in range(1, 31):
        print(f"Parte 2 – execução {i}/30")
        initial = generate_random_state()
        for ck, cf in cost_funcs.items():
            # UCS
            res = algos["A3"](initial, cf)
            save_results("Parte2", "A3", ck, None, initial, res, writer)
            # A* (todas as heurísticas)
            for hk, h in heuristics.items():
                res = algos["A5"](initial, cf, h)
                save_results("Parte2", "A5", ck, hk, initial, res, writer)

    # ── PARTE 3 ── Gulosa × A*
    print("\n" + banner + "\nEXECUTANDO PARTE 3")
    for i in range(1, 31):
        print(f"Parte 3 – execução {i}/30")
        initial = generate_random_state()

        # Gulosa
        for hk, h in heuristics.items():
            res = algos["A4"](initial, h)
            for ck, cf in cost_funcs.items():
                if res["path"]:
                    res["cost"] = sum(cf(p, p.action) for p in res["path"][1:])
                save_results("Parte3", "A4", ck, hk, initial, res, writer)

        # A*
        for ck, cf in cost_funcs.items():
            for hk, h in heuristics.items():
                res = algos["A5"](initial, cf, h)
                save_results("Parte3", "A5", ck, hk, initial, res, writer)

    # ── PARTE 4 ── Randomização de vizinhança
    print("\n" + banner + "\nEXECUTANDO PARTE 4")
    for i in range(1, 16):
        print(f"Parte 4 – execução {i}/15")
        initial = generate_random_state()

        # 10 BFS randomizadas
        for rep in range(10):
            res = algos["A1"](PuzzleState(initial.tiles.copy()), randomize=True)
            for ck, cf in cost_funcs.items():
                if res["path"]:
                    res["cost"] = sum(cf(p, p.action) for p in res["path"][1:])
                save_results("Parte4", "A1-rand", ck, None, initial, res, writer)

        # 10 DFS randomizadas
        for rep in range(10):
            res = algos["A2"](PuzzleState(initial.tiles.copy()), randomize=True)
            for ck, cf in cost_funcs.items():
                if res["path"]:
                    res["cost"] = sum(cf(p, p.action) for p in res["path"][1:])
                save_results("Parte4", "A2-rand", ck, None, initial, res, writer)

    # ────────────────────────────────────────────────────────────────────
    csvfile.close()
    elapsed = timedelta(seconds=int(time.time() - start_time))
    print(f"\n{banner}\nEXECUÇÃO TERMINADA. Tempo total: {elapsed}\n"
          f"Resultados salvos em results.csv")

    # Resuminho (se pandas instalado)
    try:
        import pandas as pd

        df = pd.read_csv("results.csv")
        print("\nRESUMO DOS CUSTOS POR ALGORITMO:")
        print(df.groupby(["Part", "Algorithm"])["Cost"].describe())
    except ModuleNotFoundError:
        print("Instale pandas se quiser ver estatísticas resumidas.")


if __name__ == "__main__":
    main()
