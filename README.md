Maria Celeste Enciso Virto - 23200125
----

# Simulador de Cache em Python

Este código implementa um simulador de cache que analisa o comportamento de acessos a memória em diferentes configurações. Ele calcula estatísticas como taxa de hits, misses e classificando seus tipos.

## Funcionalidades

Leitura do Arquivo de Entrada

- O arquivo de entrada lido em blocos de 4 bytes (endereços de 32 bits).
- Para cada endereços lido, o código extrai:
  - Tag: Identifica o bloco na memória principal.
  - Índice: Determina em qual conjunto do cache o bloco deve ser armazenado.
  - Offset: Define a posição dentro do bloco (não utilizado diretamente neste simulador).

Exemplo de entrada: 

```python
python cache_simulator.py <nsets> <bsize> <assoc> <subst> <flag_saida> <arquivo>
```

## Mapeamento e Substituição

- Mapeamento Direto (quando "assoc = 1"): cada bloco da memória é mapeado para exatamente uma linha no cache.
- Mapeamento Associativo (quando "assoc > 1"): um bloco pode ser colocado em qualquer linha do conjunto correspondente.
  - Politicas de substituição suportadas:
    - Aleatória (R): Escolhe um bloco aleatório para substituição.
    - FIFO (F): Substitui o bloco que está no cache há mais tempo.
    - LRU (L): Substitui o bloco menos recentemente usado.

## Classificação de Misses

- Compulsório (Compulsory): Ocorre quando um bloco é acessado pela primeira vez.
- Capacidade (Capacity): Ocorre quando o cache está cheio (em mapeamento totalmente associativo).
- Conflito (Conflict): Ocorre em mapeamento associativo por conjunto devido a colisão em um conjunto específico.

## Saída de Dados

- Modo Detalhado ("flag_saida = 0"):
  - Exibe estatísticas completas, incluindo contagem e taxa de hits e misses, além da classificação dos misses.

### Exemplo

Entrada:
```shell
python cache_simulator.py 2 1 8 L 0 bin_100.bin
```

Saída:
```shell
=== Estatísticas Detalhadas ===
Total de acessos: 100
Hits: 46 (0.4600)
Misses: 54 (0.5400)

Tipos de Misses:
Compulsórios: 16 (0.2963)
Capacidade: 36 (0.6667)
Conflito: 2 (0.0370)
```

- Modo Compacto ("flag_saida = 1"):
 - Imprime os resultados em uma única linha no formato:  
    
“total_acessos taxa_hit taxa_miss taxa_compulsorio taxa_capacidade taxa_conflito”

### Exemplo 

Entrada:
```bash
python cache_simulator.py 2 1 8 L 1 bin_100.bin`
````

Saída:
```shell
100 0.4600 0.5400 0.2963 0.6667 0.0370
```

## Bibliotecas Utilizadas

- "sys": Para ler argumentos da linha de comando.
- "math": Para cálculos de logaritmo (determinar bits de tag, índice e offset).
- "random": Para implementar a polotica de substituição aleatória.
- "collections.deque": Para implementar a polotica FIFO eficientemente.
