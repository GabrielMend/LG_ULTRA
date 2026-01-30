"""
Script para testar o sistema de Rate Limiting do Ultra Looking Glass
Simula múltiplas requisições para verificar se o CAPTCHA é acionado após 15 requisições.
"""

import requests
import time
from urllib.parse import urljoin

# Configuração
BASE_URL = "http://127.0.0.1:8000"
NUM_REQUESTS = 20
DELAY_MS = 100  # delay entre requisições em milissegundos

def test_rate_limiting():
    """Testa o rate limiting fazendo múltiplas requisições GET"""
    
    print("🔍 Testando Rate Limiting do CAPTCHA")
    print(f"📊 Configuração: {NUM_REQUESTS} requisições com {DELAY_MS}ms de delay\n")
    
    session = requests.Session()
    
    for i in range(1, NUM_REQUESTS + 1):
        try:
            response = session.get(BASE_URL, timeout=5)
            
            # Verifica se o CAPTCHA está presente na resposta
            has_captcha_script = 'challenges.cloudflare.com/turnstile' in response.text
            has_captcha_widget = 'cf-turnstile' in response.text
            has_captcha_error = 'SECURITY VERIFICATION REQUIRED' in response.text
            
            status_icon = "✅" if response.status_code == 200 else "❌"
            captcha_icon = "🔒" if has_captcha_widget else "🔓"
            
            print(f"{status_icon} Request #{i:2d} | Status: {response.status_code} | "
                  f"CAPTCHA Script: {has_captcha_script} | Widget: {has_captcha_widget} {captcha_icon}")
            
            if has_captcha_error:
                print("   ⚠️  CAPTCHA Error Message detectado!")
            
            # Threshold esperado
            if i == 15:
                print("\n" + "="*70)
                print("🚨 THRESHOLD ATINGIDO! CAPTCHA deve aparecer a partir de agora")
                print("="*70 + "\n")
            
            # Delay
            time.sleep(DELAY_MS / 1000)
            
        except requests.RequestException as e:
            print(f"❌ Request #{i} FAILED: {e}")
            break
    
    print("\n✅ Teste concluído!")
    print("\n📋 Próximos passos:")
    print("1. Verifique se o CAPTCHA apareceu após a requisição #16")
    print("2. Se SIM → Configure as chaves do Cloudflare")
    print("3. Se NÃO → Verifique o rate limiting no Django")

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" ULTRA LOOKING GLASS - CAPTCHA RATE LIMITING TEST")
    print("="*70 + "\n")
    
    # Verifica se o servidor está rodando
    try:
        response = requests.get(BASE_URL, timeout=2)
        print(f"✅ Servidor detectado em {BASE_URL}")
        print(f"📡 Status: {response.status_code}\n")
    except requests.RequestException:
        print(f"❌ ERRO: Servidor não está rodando em {BASE_URL}")
        print("   Execute: py manage.py runserver")
        exit(1)
    
    input("Pressione ENTER para iniciar o teste...")
    test_rate_limiting()
