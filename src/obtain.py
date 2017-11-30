import requests
import re

def get_all_values():
    r = requests.get('http://www.numeroalazar.com.ar/')
    content = r.content


    res = re.search(r'<div[\s]+(?=class="[^"]+"[\s]+id="numeros_generados"|id="numeros_generados"[\s]+class="[^"]+")[^>]*>.+?<h2>[^\<]+<\/h2>(.+?)<\/div>', content, flags=re.MULTILINE|re.DOTALL).group(1).strip()

    raw_values = res.split('<br>')
    values = []
    for value in raw_values:
        try:
            aux = float(value)
            values.append(aux)
        except:
            pass

    return values


def get_a_value():
    r = requests.get('http://www.numeroalazar.com.ar/')
    content = r.content

    res = re.search(r'<div[\s]+(?=class="[^"]+"[\s]+id="numeros_generados"|id="numeros_generados"[\s]+class="[^"]+")[^>]*>.+?<h2>[^\<]+<\/h2>(.+?)<br>', content, flags=re.MULTILINE|re.DOTALL).group(1).strip()

    return float(res)

print(get_a_value())
