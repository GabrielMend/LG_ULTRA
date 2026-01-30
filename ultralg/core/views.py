from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.core.cache import cache
from django.conf import settings
import requests
from .services import get_most_specific_route_and_as_path, verify_top_asns, verifica_tier1, take_asn_and_verify_rpki_roa

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_protect
def home(request):
    # --- Rate Limiting / Anti-Flood Core ---
    ip = get_client_ip(request)
    cache_key = f"lg_ratelimit_{ip}"
    
    # Janela de 60 segundos
    if not cache.add(cache_key, 1, 60):
        try:
            request_count = cache.incr(cache_key)
        except ValueError:
            cache.set(cache_key, 1, 60)
            request_count = 1
    else:
        request_count = 1

    # Se passar de 15 req/min, ativa o modo Captcha
    require_captcha = request_count > 15
    captcha_error = False
    # ---------------------------------------

    result = None
    top_ans = None
    tier1 = None
    rpki = None
    lg_data = None
    hide_navbar = request.GET.get("hide_navbar") == "1"
    
    # Shareable URL support: pre-fill form from query params
    command_param = request.GET.get("type", "")
    target_param = request.GET.get("address", "")
    
    # Auto-execute if valid params are present
    auto_execute = bool(command_param and target_param)

    if request.method == 'POST' or auto_execute:
        # --- Verificação do Captcha (se necessário) ---
        if require_captcha:
            turnstile_token = request.POST.get('cf-turnstile-response')
            if not turnstile_token:
                captcha_error = True
            else:
                try:
                    verify_r = requests.post(
                        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
                        data={
                            'secret': settings.TURNSTILE_SECRET_KEY,
                            'response': turnstile_token,
                            'remoteip': ip
                        },
                        timeout=5
                    )
                    verify_resp = verify_r.json()
                    if not verify_resp.get('success'):
                        captcha_error = True
                except:
                    captcha_error = True
        # ---------------------------------------------

        if captcha_error:
            result = None
        else:
            # Support both POST form and GET query params
            if request.method == 'POST':
                command = request.POST.get('command')
                target = request.POST.get('target')
            else:  # auto_execute from query params
                command = command_param
                target = target_param

            if not command or not target:
                result = "Erro: comando e destino são obrigatórios."
            else:
                # Agora retorna uma tupla (routes_list, raw_json)
                ripe, lg_data = get_most_specific_route_and_as_path(target)
                
                # Verifica se ripe é um dict de erro ou a lista de resultados
                if isinstance(ripe, dict) and "error" in ripe:
                    result = ripe["error"]
                else:
                    result = ripe
                    top_ans = verify_top_asns(result)
                    tier1 = verifica_tier1(result)
                    
                    if lg_data:
                        rpki = take_asn_and_verify_rpki_roa(lg_data)
                        

    return render(request, 'core/index.html', {
        'result': result,
        'top_ans': top_ans,
        'tier1': tier1,
        'rpki': rpki,
        'hide_navbar': hide_navbar,
        'show_captcha': require_captcha,
        'turnstile_site_key': settings.TURNSTILE_SITE_KEY,
        'captcha_error': captcha_error,
        'command_value': command_param or request.POST.get('command', ''),
        'target_value': target_param or request.POST.get('target', ''),
        'raw_bgp_data': lg_data,
    })