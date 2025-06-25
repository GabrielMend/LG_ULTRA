from collections import Counter



def verify_last_asn(data):
    excluir_asns = {'6939', '6427', '393338', '20341', '18850'}

    penultimo_dir = []
    antepenultimo_dir = []

    for entry in data:
        as_path = entry['as_path'].split()
        if len(as_path) > 1 and as_path[-2] not in excluir_asns:
            penultimo_dir.append(as_path[-2])
        if len(as_path) > 2 and as_path[-3] not in excluir_asns:
            antepenultimo_dir.append(as_path[-3])

    total = len(data)

    contagem_penultimo = Counter(penultimo_dir)
    contagem_antepenultimo = Counter(antepenultimo_dir)

    top3_penultimo = contagem_penultimo.most_common(3)
    top3_antepenultimo = contagem_antepenultimo.most_common(3)

    print("Top 3 AS na posição 3 da direita (penúltimo AS) excluindo ASNs listados:")
    for asn, count in top3_penultimo:
        perc = (count / total) * 100
        print(f"{asn}: {perc:.2f}%")

    print("\nTop 3 AS na posição 4 da direita (antepenúltimo AS) excluindo ASNs listados:")
    for asn, count in top3_antepenultimo:
        perc = (count / total) * 100
        print(f"{asn}: {perc:.2f}%")