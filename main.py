from __future__ import annotations
import argparse, csv, random, time
from datetime import timedelta
from typing import List, Dict

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


def is_solvable(tiles: List[int]) -> bool:
    inv = sum(
        1
        for i in range(9)
        for j in range(i + 1, 9)
        if tiles[i] and tiles[j] and tiles[i] > tiles[j]
    )
    return inv % 2 == 0


def generate_random_state() -> PuzzleState:
    tiles = list(range(9))
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):
            return PuzzleState(tiles)


def compute_path_cost(path: List[PuzzleState], cost_func) -> int:
    if not path or len(path) < 2:
        return 0
    cost = 0
    for parent, child in zip(path[:-1], path[1:]):
        cost += cost_func(parent, child.action)
    return cost


def open_writer(part_num: str) -> tuple[csv.writer, object]:
    f = open(f"results_part{part_num}.csv", "w", newline="")
    w = csv.writer(f)
    w.writerow(
        [
            "Part", "Algorithm", "CostFunction", "Heuristic",
            "InitialState", "Path", "PathLength",
            "Cost", "NodesGenerated", "NodesVisited",
        ]
    )
    return w, f


def save_results(
    part: str,
    algorithm: str,
    cost_name: str,
    heuristic_name: str | None,
    initial_state: PuzzleState,
    result: dict,
    writer: csv.writer,
):
    path = result["path"] or []
    writer.writerow(
        [
            part,
            algorithm,
            cost_name,
            heuristic_name or "None",
            initial_state,
            "|".join(str(s) for s in path) if path else "None",
            len(path),
            result["cost"],
            result["nodes_generated"],
            result["nodes_visited"],
        ]
    )


def run_single(scenario: str, tiles: List[int] | None,
               cost_funcs, heuristics, algos, writer):
    tok = scenario.split(",")
    if len(tok) not in {2, 3}:
        raise ValueError("Use: ALG,Ck[,Hj] – ex. A5,C2,H1")

    alg_key, cost_key = tok[0], tok[1]
    heur_key = tok[2] if len(tok) == 3 else None

    if alg_key not in algos:
        raise ValueError("Algoritmo inválido.")
    if cost_key not in cost_funcs:
        raise ValueError("Função de custo inválida.")
    if alg_key in {"A4", "A5"} and heur_key not in heuristics:
        raise ValueError("Heurística obrigatória para esse algoritmo.")
    if alg_key in {"A1", "A2", "A3"} and heur_key is not None:
        raise ValueError("Heurística não deve ser fornecida para esse algoritmo.")

    initial = (
        PuzzleState(tiles)
        if tiles is not None
        else generate_random_state()
    )

    if alg_key == "A1":
        res = algos[alg_key](initial)
    elif alg_key == "A2":
        res = algos[alg_key](initial)
    elif alg_key == "A3":
        res = algos[alg_key](initial, cost_funcs[cost_key])
    elif alg_key == "A4":
        res = algos[alg_key](initial, heuristics[heur_key])
    else:  # A5
        res = algos[alg_key](initial, cost_funcs[cost_key], heuristics[heur_key])

    save_results(
        "Single", alg_key, cost_key, heur_key,
        initial, res, writer
    )
    print("Resultado salvo em results_partSingle.csv")


def main():
    banner = "=" * 60
    parser = argparse.ArgumentParser(
        description="Sistema de experimentos para o 8-Puzzle"
    )
    parser.add_argument(
        "--part",
        choices=["1", "2", "3", "4", "all"],
        default="all",
        help="Qual parte executar (default: all)",
    )
    parser.add_argument(
        "--single",
        help="Executa apenas um cenário: ALG,Ck[,Hj]  ex. A5,C2,H1",
    )
    parser.add_argument(
        "--tiles",
        help="Estado inicial customizado – 9 números separados por espaço",
    )
    args = parser.parse_args()

    # dicionários de funções
    cost_funcs = {"C1": cost_function_c1, "C2": cost_function_c2,
                  "C3": cost_function_c3, "C4": cost_function_c4}
    heuristics = {"H1": heuristic_h1, "H2": heuristic_h2}
    algos = {"A1": breadth_first_search, "A2": depth_first_search,
             "A3": uniform_cost_search, "A4": greedy_search, "A5": a_star_search}

    # -------- single-run? ------------------------------------------------
    if args.single:
        writer, f = open_writer("Single")
        tiles = None
        if args.tiles:
            nums = [int(n) for n in args.tiles.split()]
            if len(nums) != 9 or set(nums) != set(range(9)):
                raise ValueError("Tiles deve conter 0-8 sem repetição.")
            if not is_solvable(nums):
                raise ValueError("Estado inicial não solucionável.")
            tiles = nums
        run_single(args.single, tiles, cost_funcs, heuristics, algos, writer)
        f.close()
        return

    # -------- execução por parte(s) -------------------------------------
    part_sel = args.part  # '1' | '2' | '3' | '4' | 'all'
    writers: Dict[str, tuple[csv.writer, object]] = {}
    for p in ("1", "2", "3", "4"):
        if part_sel in {p, "all"}:
            writers[p] = open_writer(p)

    start_time = time.time()

    # PARTE 1 ────────────────────────────────────────────────────────────
    if part_sel in {"1", "all"}:
        print(f"\n{banner}\nEXECUTANDO PARTE 1")
        w = writers["1"][0]
        for i in range(1, 31):
            print(f"Parte 1 – execução {i}/30  ({time.strftime('%H:%M:%S')})", flush=True)
            initial = generate_random_state()
            # BFS
            for ck, cf in cost_funcs.items():
                res = algos["A1"](initial)
                res["cost"] = compute_path_cost(res["path"], cf)
                save_results("Parte1", "A1", ck, None, initial, res, w)
            # DFS
            for ck, cf in cost_funcs.items():
                res = algos["A2"](initial)
                res["cost"] = compute_path_cost(res["path"], cf)
                save_results("Parte1", "A2", ck, None, initial, res, w)
            # UCS
            for ck, cf in cost_funcs.items():
                res = algos["A3"](initial, cf)
                save_results("Parte1", "A3", ck, None, initial, res, w)

    # PARTE 2 ────────────────────────────────────────────────────────────
    if part_sel in {"2", "all"}:
        print(f"\n{banner}\nEXECUTANDO PARTE 2")
        w = writers["2"][0]
        for i in range(1, 31):
            print(f"Parte 2 – execução {i}/30  ({time.strftime('%H:%M:%S')})", flush=True)
            initial = generate_random_state()
            for ck, cf in cost_funcs.items():
                # UCS
                res = algos["A3"](initial, cf)
                save_results("Parte2", "A3", ck, None, initial, res, w)
                # A*
                for hk, h in heuristics.items():
                    res = algos["A5"](initial, cf, h)
                    save_results("Parte2", "A5", ck, hk, initial, res, w)

    # PARTE 3 ────────────────────────────────────────────────────────────
    if part_sel in {"3", "all"}:
        print(f"\n{banner}\nEXECUTANDO PARTE 3")
        w = writers["3"][0]
        for i in range(1, 31):
            print(f"Parte 3 – execução {i}/30  ({time.strftime('%H:%M:%S')})", flush=True)
            initial = generate_random_state()
            # Gulosa
            for hk, h in heuristics.items():
                res = algos["A4"](initial, h)
                for ck, cf in cost_funcs.items():
                    res_c = res.copy()
                    res_c["cost"] = compute_path_cost(res["path"], cf)
                    save_results("Parte3", "A4", ck, hk, initial, res_c, w)
            # A*
            for ck, cf in cost_funcs.items():
                for hk, h in heuristics.items():
                    res = algos["A5"](initial, cf, h)
                    save_results("Parte3", "A5", ck, hk, initial, res, w)

    # PARTE 4 ────────────────────────────────────────────────────────────
    if part_sel in {"4", "all"}:
        print(f"\n{banner}\nEXECUTANDO PARTE 4")
        w = writers["4"][0]
        for i in range(1, 16):
            print(f"Parte 4 – execução {i}/15  ({time.strftime('%H:%M:%S')})", flush=True)
            initial = generate_random_state()
            # 10 BFS random
            for _ in range(10):
                res = algos["A1"](PuzzleState(initial.tiles.copy()), randomize=True)
                for ck, cf in cost_funcs.items():
                    res_c = res.copy()
                    res_c["cost"] = compute_path_cost(res["path"], cf)
                    save_results("Parte4", "A1-rand", ck, None, initial, res_c, w)
            # 10 DFS random
            for _ in range(10):
                res = algos["A2"](PuzzleState(initial.tiles.copy()), randomize=True)
                for ck, cf in cost_funcs.items():
                    res_c = res.copy()
                    res_c["cost"] = compute_path_cost(res["path"], cf)
                    save_results("Parte4", "A2-rand", ck, None, initial, res_c, w)


    for _, f in writers.values():
        f.close()

    elapsed = timedelta(seconds=int(time.time() - start_time))
    print(f"\n{banner}\nEXECUÇÃO CONCLUÍDA – {elapsed}")

    try:
        import pandas as pd
        for p in writers.keys():
            df = pd.read_csv(f"results_part{p}.csv")
            print(f"\nResumo Part {p}")
            print(df.groupby("Algorithm")['Cost'].describe())
    except ModuleNotFoundError:
        pass

if __name__ == "__main__":
    main()