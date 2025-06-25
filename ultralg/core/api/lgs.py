import requests

def lg_alt(prefix):
    lg_alt = "http://lg.as53062.net.br/lg/?command=bgp&protocol=ipv4&query={prefix}}&router=as53062"
    alt = requests.get(lg_alt)
    return alt.text