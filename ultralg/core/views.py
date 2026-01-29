from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .services import get_most_specific_route_and_as_path, verify_top_asns, verifica_tier1, take_asn_and_verify_rpki_roa

@csrf_protect
def home(request):
    result = None
    top_ans = None
    tier1 = None
    rpki = None
    hide_navbar = request.GET.get("hide_navbar") == "1"

    if request.method == 'POST':
        command = request.POST.get('command')
        target = request.POST.get('target')

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
                    rpki = take_asn_and_verify_rpki_roa(target, lg_data)
                    print(f"DEBUG RPKI DATA: {rpki}")

    return render(request, 'core/index.html', {
        'result': result,
        'top_ans': top_ans,
        'tier1': tier1,
        'rpki': rpki,
        'hide_navbar': hide_navbar
    })