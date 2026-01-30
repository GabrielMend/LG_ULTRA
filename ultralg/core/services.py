import requests
from collections import Counter
import random
import os
import json
import requests
import pathlib


"""Service Ultra Glass
esse serviços.py é usado para separar as funçõees de lógica da view do DJANGO. 
dentro de cada função irá ter um comentário informando o que cada função faz.
"""


# Função Main, onde precisa de uma lógica para prefixo e outro para IP sem mascara. 
def get_most_specific_route_and_as_path(resource):
    try:
        ip, mask = resource.split('/', 1)
    except ValueError:
        ip = resource
        mask = None
    # aqui é onde fazemos a requisição ao LG da Ripe que retorna em JSON#
    if mask:
        url = f"https://stat.ripe.net/data/looking-glass/data.json?resource={ip}%2F{mask}&starttime=now"
    else:
        url = f"https://stat.ripe.net/data/looking-glass/data.json?resource={ip}&starttime=now"

    try:
        resp = requests.get(url, timeout=1) # 1 sec timeout
        resp.raise_for_status()
    except requests.RequestException as e:
        return {"error": f"Erro na requisição: {e}"}, None
    # aqui onde vamos tratar os dados com as funções que estão abaixo #
    data = resp.json()
    dados = get_one_router_per_country(data)
    best_routes_only = only_as_path(dados)
    return best_routes_only, data


##### espaço para tratar JSON do RIPE #######
##### # # # # # # # # # # # # # # # # # ####
def get_one_router_per_country(response_json):
    routers = response_json.get('data', {}).get('rrcs', [])
    seen_countries = set()
    filtered_routers = []

    for router in routers:
        location = router.get('location', '')  # ex: "London, United Kingdom"
        # Pega o país após a vírgula e espaço
        parts = location.split(', ')
        country = parts[-1] if len(parts) > 1 else location.strip()

        if country not in seen_countries:
            seen_countries.add(country)
            filtered_routers.append(router)

    return filtered_routers

#Retirar da dict apenas o valor AS Path #
def only_as_path(data):
    resultado = []

    for rrc_item in data:
        pais = rrc_item.get('location', 'Unknown')
        for peer in rrc_item.get('peers', []):
            as_path = peer.get('as_path')
            prefix = peer.get('prefix')
            age = peer.get('last_updated')
            if as_path and prefix:
                resultado.append({
                    'location': pais,
                    'as_path': as_path,
                    'prefix': prefix,
                    'last_updated': age
                })

    return resultado


##### FIM DO ESPAÇO DE TRATAMENTO DO RIPE LG #######


##### TRATAMENTO DE DADOS DO ASN ######
def verify_top_asns(data):
    excluir_asns = {
        '6939': 'Hurricane Electric LLC United States',
        '6427': 'Hurricane Electric LLC United States',
        '393338': 'Hurricane Electric LLC United States',
        '20341': 'Hurricane Labs, LLC United States',
        '18850': 'Hurricane Computer Solutions Inc.',
        # Retirado a HURRICANE do LG para não gerar falso positivo #
    }

    penultimo_dir = []
    antepenultimo_dir = []

    try:
        if data.get('error') == True:
            return None
    except:
        pass

    for entry in data:
        raw_path = entry['as_path'].split()

        # Remove prepends: ASNs duplicados consecutivos (PREPEND, para não ocorrer)
        as_path = [asn for i, asn in enumerate(raw_path) if i == 0 or asn != raw_path[i-1]]

        if len(as_path) > 1 and as_path[-2] not in excluir_asns:
            penultimo_dir.append(as_path[-2])
        if len(as_path) > 2 and as_path[-3] not in excluir_asns:
            antepenultimo_dir.append(as_path[-3])

    total = len(data)

    contagem_penultimo = Counter(penultimo_dir)
    contagem_antepenultimo = Counter(antepenultimo_dir)

    top3_penultimo = contagem_penultimo.most_common(3)
    top3_antepenultimo = contagem_antepenultimo.most_common(3)

    resultado = {
        "penultimo": [],
        "antepenultimo": [],
    }

    for asn, count in top3_penultimo:
        nome = get_asn_name_multi(asn)
        resultado["penultimo"].append({
            "asn": asn,
            "nome": nome,
            "percentual": round((count / total) * 100, 2)
        })

    for asn, count in top3_antepenultimo:
        nome = get_asn_name_multi(asn)
        resultado["antepenultimo"].append({
            "asn": asn,
            "nome": nome,
            "percentual": round((count / total) * 100, 2)
        })

    return resultado




###### PEGAR NOME DO ASN #######
# === Cache persistente ===
# ALem de consultar 3 bases diferentes randomicamente, para não ocorrer two many requests #
BASE_DIR = pathlib.Path(__file__).parent  # pasta onde está services.py
ASN_CACHE_FILE = BASE_DIR / 'asn_cache.json'
TIER_ONE_CACHE = BASE_DIR / 'tier_one.json'

def load_asn_cache():
    if os.path.exists(ASN_CACHE_FILE):
        with open(ASN_CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_asn_cache(cache):
    with open(ASN_CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

asn_cache = load_asn_cache()

# === Resolução ASN com múltiplas fontes ===

def get_asn_name_multi(asn):
    if asn in asn_cache:
        return asn_cache[asn]

    sources = [
        f"https://api.bgpview.io/asn/{asn}", #bgp view API
        f"https://stat.ripe.net/data/as-overview/data.json?resource=AS{asn}", #stat ripe ASN
        f"https://api.iptoasn.com/v1/as/ip/AS{asn}" #iptoasn
    ]
    random.shuffle(sources)

    for url in sources:
        try:
            response = requests.get(url, headers={"User-Agent": "Mozilla"}, timeout=1)
            if response.status_code != 200:
                continue
            data = response.json()

            if "bgpview.io" in url:
                name = data.get("data", {}).get("name")
            elif "ripe" in url:
                name = data.get("data", {}).get("holder")
            elif "iptoasn" in url:
                name = data.get("as_description")

            if name:
                full_name = f"AS{asn} - {name}"
                asn_cache[asn] = full_name
                save_asn_cache(asn_cache)
                return full_name
        except:
            continue

    fallback = f"AS{asn}"
    asn_cache[asn] = fallback
    save_asn_cache(asn_cache)
    return fallback


###### PARTE DO CÓDIGO QUE VERIFICA  A PRESENÇA DE TIER 1 NO AS PATH, CASO NÃO TENHA É PROVAVEL QUE DEVIDO A ESPECIFICIDADE SÓ ESTEJA ENVIANDO PARA IX/PNI #####
### CARREGANDO O JSON COM OS TIER ONE ###
TIER_ONE_CACHE = 'tier_one.json'
def load_tier_asn():
    if os.path.exists(TIER_ONE_CACHE):
        with open(TIER_ONE_CACHE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def verifica_tier1(dados):
    tier1_found = False
    tier1_asns =  load_tier_asn()
    tier1_present = set()  # para guardar os ASNs que apareceram
    for entry in dados:
        as_path_list = entry['as_path'].split()
        for asn in as_path_list:
            if asn in tier1_asns:
                tier1_found = True
                tier1_present.add(asn)
    if tier1_found:
        return 0
    else:
        return "NO TIER-1 FOUND IN AS PATH, LIKELY ANNOUNCEMENT ONLY TO IX AND PNI"


###### Essa parte do código é destinada para verificar o RPKI e ROA #######

###### Essa parte do código é destinada para verificar o RPKI e ROA #######

def extract_origin_asn(lg_data):
    """
    Extrai o ASN de origem a partir dos dados do Looking Glass.
    Retorna o ASN (str) ou None se não encontrar.
    """
    try:
        # Tenta pegar a lista de RRCs
        rrcs = lg_data.get('data', {}).get('rrcs', [])
        if not rrcs:
            return None
        
        # Pega o primeiro peer do primeiro RRC (Geralmente consistente para Origin ASN)
        first_rrc = rrcs[0]
        peers = first_rrc.get('peers', [])
        
        if not peers:
            return None
            
        return str(peers[0].get('asn_origin'))
        
    except (AttributeError, IndexError, TypeError):
        return None

def extract_prefix(lg_data):
    """
    Extrai o Prefixo a partir dos dados do Looking Glass.
    Retorna o Prefixo (str) ou None se não encontrar.
    """
    try:
        # Tenta pegar a lista de RRCs dentro de 'data'
        rrcs = lg_data.get('data', {}).get('rrcs', [])
        
        # Se a lista de RRCs estiver vazia, retorna None
        if not rrcs:
            return None
        
        # Pega o primeiro RRC da lista
        first_rrc = rrcs[0]
        
        # Pega a lista de peers dentro desse RRC
        peers = first_rrc.get('peers', [])
        
        # Se a lista de peers estiver vazia, retorna None
        if not peers:
            return None
            
        # Retorna o prefixo do primeiro peer encontrado
        return str(peers[0].get('prefix'))
        
    except (AttributeError, IndexError, TypeError):
        return None

def fetch_rpki_validation(asn, prefix):
    """
    Consulta a API de validação RPKI do RIPE e retorna um dicionário limpo.
    """
    url = f"https://stat.ripe.net/data/rpki-validation/data.json?resource=AS{asn}&prefix={prefix}"
    
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=3)
        response.raise_for_status()
        data = response.json()
        
        # Acessa os dados reais dentro da resposta do RIPE
        rpki_data = data.get('data', {})
        
        # Normaliza o status para facilitar no front-end
        status = rpki_data.get('status', 'unknown')
        validating_roas = rpki_data.get('validating_roas', [])
        
        # Tenta pegar o max_length da primeira ROA válida, se houver
        max_len = None
        if validating_roas:
            max_len = validating_roas[0].get('max_length')

        message = f"RPKI status is {status} for AS{asn}."
        if max_len:
            message += f" (Max Length: {max_len})"

        return {
            "status": status.upper(),  # 'VALID', 'INVALID_ASN', 'INVALID_LENGTH', 'UNKNOWN'
            "origin_asn": asn,
            "prefix": prefix,
            "max_length": max_len,
            "max_length_str": str(max_len) if max_len else "",
            "roas_found": validating_roas,
            "raw_message": message
        }

    except requests.RequestException:
        return {
            "status": "ERROR",
            "origin_asn": asn,
            "prefix": prefix,
            "roas_found": [],
            "raw_message": "Erro ao conectar com a API RPKI."
        }

def take_asn_and_verify_rpki_roa(lg_data):
    """
    Função Principal (Orquestradora):
    1. Recebe o prefixo e os dados do Looking Glass já consultados anteriormente.
    2. Extrai o ASN de origem do Looking Glass.
    3. Valida esse ASN + Prefixo na base RPKI.
    """
    
    # 1. Tenta descobrir quem está anunciando o IP (Origin ASN)
    origin_asn = extract_origin_asn(lg_data)
    prefix = extract_prefix(lg_data)
    
    if not origin_asn:
        return {
            "status": "ERROR_NO_ASN",
            "raw_message": "Não foi possível identificar o ASN de origem nos dados do Looking Glass para validar o RPKI."
        }

    # 2. Com o ASN em mãos, faz a validação RPKI
    resultado_rpki = fetch_rpki_validation(origin_asn, prefix)
    
    return resultado_rpki