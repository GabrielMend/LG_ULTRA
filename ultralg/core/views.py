from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .services import get_most_specific_route_and_as_path, verify_top_asns, verifica_tier1

@csrf_protect
def home(request):
    result = None
    top_ans = None
    tier1 = None
    hide_navbar = request.GET.get("hide_navbar") == "1"

    if request.method == 'POST':
        command = request.POST.get('command')
        target = request.POST.get('target')

        if not command or not target:
            result = "Erro: comando e destino são obrigatórios."
        else:
            ripe = get_most_specific_route_and_as_path(target)
            result = ripe
            top_ans = verify_top_asns(result)
            tier1 = verifica_tier1(result)

    return render(request, 'core/index.html', {
        'result': result,
        'top_ans': top_ans,
        'tier1': tier1,
        'hide_navbar': hide_navbar  # agora é dinâmico
    })