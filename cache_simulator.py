import sys
import math
import random
from collections import deque

def main():
    
    if len(sys.argv) != 7:
        print("Uso: python cache_simulator.py <nsets> <bsize> <assoc> <subst> <flag_saida> <arquivo>")
        sys.exit(1)

    try:
        nsets = int(sys.argv[1])
        bsize = int(sys.argv[2])
        assoc = int(sys.argv[3])
        subst = sys.argv[4].upper()
        flag_out = int(sys.argv[5])
        arquivo = sys.argv[6]

        if nsets <= 0 or bsize <= 0 or assoc <= 0:
            raise ValueError("nsets, bsize e assoc devem ser positivos")
        
        if not math.log2(nsets).is_integer() or not math.log2(bsize).is_integer():
            raise ValueError("nsets e bsize devem ser potências de 2")
        
        if subst not in ['R', 'F', 'L']:
            raise ValueError("Política de substituição deve ser R, F ou L")
        
        if flag_out not in [0, 1]:
            raise ValueError("flag_saida deve ser 0 ou 1")

        bits_offset = int(math.log2(bsize))
        bits_indice = int(math.log2(nsets))
        bits_tag = 32 - bits_offset - bits_indice

        cache = []
        fifo_queues = []
        lru_lists = []
        
        for _ in range(nsets):
            conjunto = []
            for i in range(assoc):
                conjunto.append({'valid': False, 'tag': None})
            cache.append(conjunto)
            fifo_queues.append(deque(range(assoc)))
            lru_lists.append(list(range(assoc)))

        hits = misses = 0
        compulsorio = capacidade = conflito = 0
        contador_ordem = 0

        with open(arquivo, 'rb') as f:
            while True:
                bytes_lidos = f.read(4)
                if not bytes_lidos or len(bytes_lidos) < 4:
                    break
                
                endereco = int.from_bytes(bytes_lidos, 'big')
                tag = endereco >> (bits_offset + bits_indice)
                indice = (endereco >> bits_offset) & (nsets - 1)
                
                hit = False
                for i, bloco in enumerate(cache[indice]):
                    if bloco['valid'] and bloco['tag'] == tag:
                        hit = True
                        hits += 1
                        if subst == 'L':
                            lru_lists[indice].remove(i)
                            lru_lists[indice].append(i)
                        break
                
                if not hit:
                    misses += 1
                    conjunto = cache[indice]
                    bloco_subst = None
                    bloco_idx = None
                    
                    for i, bloco in enumerate(conjunto):
                        if not bloco['valid']:
                            bloco_subst = bloco
                            bloco_idx = i
                            compulsorio += 1
                            break
                    
                    if bloco_subst is None:
                        if all(all(b['valid'] for b in c) for c in cache):
                            capacidade += 1
                        else:
                            conflito += 1
                        
                        if subst == 'R':
                            random.seed(indice + contador_ordem)
                            bloco_idx = random.randint(0, assoc-1)
                            bloco_subst = conjunto[bloco_idx]
                            random.seed(0)
                        elif subst == 'F':
                            bloco_idx = fifo_queues[indice].popleft()
                            bloco_subst = conjunto[bloco_idx]
                            fifo_queues[indice].append(bloco_idx)
                        else:
                            bloco_idx = lru_lists[indice].pop(0)
                            bloco_subst = conjunto[bloco_idx]
                            lru_lists[indice].append(bloco_idx)
                    
                    bloco_subst['valid'] = True
                    bloco_subst['tag'] = tag
                    
                    if bloco_idx is not None:
                        if subst == 'L' and bloco_idx in lru_lists[indice]:
                            lru_lists[indice].remove(bloco_idx)
                        if subst == 'L':
                            lru_lists[indice].append(bloco_idx)

                    contador_ordem += 1

        total = hits + misses
        taxa_hit = round(hits / total, 4) if total > 0 else 0
        taxa_miss = round(misses / total, 4) if total > 0 else 0
        taxa_comp = round(compulsorio / misses, 4) if misses > 0 else 0
        taxa_cap = round(capacidade / misses, 4) if misses > 0 else 0
        taxa_conf = round(conflito / misses, 4) if misses > 0 else 0

        if flag_out == 0:
            print("\n=== Estatísticas Detalhadas ===")
            print(f"Total de acessos: {total}")
            print(f"Hits: {hits} ({taxa_hit:.4f})")
            print(f"Misses: {misses} ({taxa_miss:.4f})")
            print("\nTipos de Misses:")
            print(f"Compulsórios: {compulsorio} ({taxa_comp:.4f})")
            print(f"Capacidade: {capacidade} ({taxa_cap:.4f})")
            print(f"Conflito: {conflito} ({taxa_conf:.4f})")
        else:
            print(f"{total} {taxa_hit:.4f} {taxa_miss:.4f} {taxa_comp:.4f} {taxa_cap:.4f} {taxa_conf:.4f}")

    except Exception as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
