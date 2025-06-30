# Algoritmos de Busca - 8-Puzzle

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Implementação de diversos algoritmos de busca para resolver o problema do 8-puzzle, comparando seu desempenho e eficiência.

## 🧩 Sobre o 8-Puzzle

O 8-puzzle é um quebra-cabeça deslizante que consiste em uma grade 3×3 com 8 peças numeradas e um espaço vazio. O objetivo é reorganizar as peças de um estado inicial para alcançar um estado objetivo deslizando as peças para o espaço vazio.

## 🔬 Algoritmos Implementados

O projeto implementa cinco algoritmos de busca diferentes:

1. **A1 - Busca em Largura (BFS)**
   - Completo e ótimo para grafos não ponderados
   - Explora todos os nós no nível atual antes de passar para o próximo nível

2. **A2 - Busca em Profundidade (DFS)**
   - Eficiente em memória
   - Não garante encontrar a solução ótima
   - Pode ficar preso em caminhos infinitos sem restrições adequadas

3. **A3 - Busca de Custo Uniforme (UCS)**
   - Ótimo quando todos os custos são não-negativos
   - Explora nós em ordem de custo do caminho
   - Garante o caminho de menor custo

4. **A4 - Busca Gulosa**
   - Usa heurísticas para estimar distância até o objetivo
   - Muito eficiente quando a heurística é boa
   - Não garante solução ótima

5. **A5 - Busca A***
   - Combina UCS e Busca Gulosa
   - Ótimo quando usa heurísticas admissíveis
   - Geralmente o mais eficiente entre os algoritmos admissíveis

## 📊 Funções de Custo e Heurísticas

### Funções de Custo
- **C1**: Custo básico de movimento
- **C2**: Custo baseado no valor da peça
- **C3**: Custo baseado na direção do movimento
- **C4**: Métrica de custo combinada

### Heurísticas
- **H1**: Número de peças fora do lugar
- **H2**: Distância Manhattan até a posição objetivo

## 🚀 Começando

### Pré-requisitos
- Python 3.x
- pip (instalador de pacotes Python)

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GustavoErick/IA-Algoritmos-de-Busca.git
cd IA-Algoritmos-de-Busca
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executando partes 
```bash
python main.py --part 1  # Executa experimentos da parte 1
python main.py --part 2  # Executa experimentos da parte 2
python main.py --part 3  # Executa experimentos da parte 3
python main.py --part 4  # Executa experimentos da parte 4
```

Cada parte executa:
- 30 iterações com estados iniciais aleatórios (exceto parte 4)
- Salva resultados em `results_part{N}.csv`
- Mostra progresso e tempo de execução
- Exibe resumo estatístico (se pandas estiver instalado)

#### Executando Cenários Específicos
```bash
python main.py --single ALG,Ck[,Hj]
```

Onde:
- ALG: Algoritmo (A1, A2, A3, A4, A5)
- Ck: Função de Custo (C1, C2, C3, C4)
- Hj: Heurística (H1, H2) - obrigatória para A4 e A5

Exemplos:
```bash
python main.py --single A1,C1    # Busca em Largura com custo C1
python main.py --single A2,C2    # Busca em Profundidade com custo C2
python main.py --single A3,C3    # Busca de Custo Uniforme com custo C3
python main.py --single A4,C1,H1 # Busca Gulosa com custo C1 e heurística H1
python main.py --single A5,C2,H2 # A* com custo C2 e heurística H2
```

#### Estado Inicial Personalizado
```bash
python main.py --tiles "1 2 3 4 0 5 6 7 8" --single A1,C1
```

O parâmetro `--tiles` permite especificar um estado inicial personalizado:
- Use números de 0 a 8
- 0 representa o espaço vazio
- Os números devem ser separados por vírgula
- A ordem representa a configuração do tabuleiro da esquerda para a direita, de cima para baixo


## 📈 Estrutura dos Experimentos

O programa executa quatro conjuntos de experimentos:

1. **Parte 1**: BFS vs DFS vs UCS
   - 30 execuções
   - Compara estratégias básicas de busca
   - Testa todas as funções de custo

2. **Parte 2**: UCS vs A*
   - 30 execuções
   - Compara busca informada e não-informada ótima
   - Testa todas as funções de custo e heurísticas

3. **Parte 3**: Gulosa vs A*
   - 30 execuções
   - Compara abordagens baseadas em heurística
   - Testa todas as combinações de funções de custo e heurísticas

4. **Parte 4**: Randomização de Vizinhança
   - 15 execuções com 10 repetições cada
   - Testa BFS e DFS com seleção randomizada de vizinhos
   - Analisa impacto da randomização na qualidade da solução

## 📋 Resultados

Os resultados são salvos em `results.csv` com as seguintes métricas:
- Algoritmo utilizado
- Função de custo
- Heurística (quando aplicável)
- Estado inicial
- Caminho da solução
- Comprimento do caminho
- Custo total
- Número de nós gerados
- Número de nós visitados


## 🧪 Estrutura do Projeto

```
IA-Algoritmos-de-Busca/
├── main.py              # Arquivo principal de execução
├── puzzle.py            # Implementação do estado do 8-puzzle
├── algorithms.py        # Implementação dos algoritmos de busca
├── costs.py            # Funções de custo
├── heuristics.py       # Funções heurísticas
├── requirements.txt     # Dependências do projeto
└── README.md           # Documentação do projeto
```

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ✨ Autores

[Gustavo Erick  - 536884](https://github.com/GustavoErick)
[Victor Gabriel - 512076](https://github.com/Picxs)
[Lucas Anthony - 539300](https://github.com/LukasAnthony)
