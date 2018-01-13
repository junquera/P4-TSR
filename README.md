# PEC

## Especificación de la aplicación

Nuestra aplicación consistirá en un servidorque, mediante peticiones REST, ofrecerá al usuario la posibilidad de obtener números aleatorios (extraídos de otra página) especificando algunas condiciones. Para ello, desarrollaremos el código en python utilizando el framework Flask. Para el despliegue del sistema utilizaremos Docker y una arquitectura destinada a la alta disponibilidad y al balanceo de carga de las peticiones (no servirá para nada en un sistema que finalmente sólo utilizaremos nosotros, pero me parecía interesante para estudiarlo). A continuación pasaremos a detallarlo todo.

Para el control de versiones del software hemos utilizado GIT, utilizando como repositorio remoto [GitHub](https://github.com): [https://github.com/junquera/P4-TSR](https://github.com/junquera/P4-TSR)

### Obtención y filtrado de datos

Para la obtención de los datos, codificada en el archivo `src/app/obtain.py`, hemos utilizado la librería `requests`. Descargamos la página `http://www.numeroalazar.com.ar/` y mediante una expresión regular, obtenemos el primer valor de la lista.

``` python
# Extracción de datos
re.search(r'<div[\s]+(?=class="[^"]+"[\s]+id="numeros_generados"|id="numeros_generados"[\s]+class="[^"]+")[^>]*>.+?<h2>[^\<]+<\/h2>(.+?)<\/div>', content, flags=re.MULTILINE|re.DOTALL)
```

En la primera implementación utilicé la librería `xml`:

``` python
import xml.etree.ElementTree as ET
root = ET.fromstring(content)
v = root.find(//div[@id='numeros_generados']//h2)
```

Posteriormente probé con la librería `BeautifulSoup`, destinada al parsing de documentos XML, pero para ajustarme a los requisitos del enunciado, terminé implementando la expresión regular.

> TODO CRON DE OBTENCIÓN DE DATOS

### Almacenamiento

La lógica para el manejo del almacenamiento de los datos está codificada en el archivo `almacenamiento.py`. He creado una clase para la base de datos local, otra para la base de datos online y, por último, una clase que actúa de interfaz para que al leer los datos se acceda sólo a la local y al insertarlos se haga en las dos. He decidido utilizar la base de datos local como base de datos principal (porque así trabajaremos con ella más rápido) y la de la nube como backup. Al instanciarse la clase `Almacenamiento`, se borran los datos de la base de datos local y se descargan los de la nube.

#### Almacenamiento local

Para el almacenamiento de los datos en local he utilizado una base de datos MongoDB. Es una base de datos NoSQL simple y rápida, con la que se interactúa a través de mensajes en formato JSON. Nos es muy útil por la facilidad de generar estos mensajes en python.

En ambos casos, la estructura del *documento* almacenado es la siguiente:

``` python
{
"value": valor_aleatorio,
"date": fecha_en_formato_ISO
}
```

#### Almacenamiento en la nube

Para la nube, he utilizado la plataforma [Xively](https://www.xively.com/). Es más compleja que otras propuestas, pero quería probar a utilizar el protocolo MQTT, muy utilizado últimamente para IoT (de hecho, Xively está pensado como plataforma en la nube para dispositivos del Internet de las Cosas).

Para la subida de datos utilizamos el protocolo MQTT. En este protocolo los clientes se conectan (en MQTT diremos que se suscriben) a una lista manejada por un *broker* (en este caso, Xively). Dicho broker se encarga de entregar los mensajes que produzca un publicador a los clientes suscritos. Nuestra conexión se hará de forma cifrada, y está codificada en el archivo `xively.py`, y la subida corresponde con el método `publish_random_value_mqtt`.

Para la descarga de los datos (codificada en `retrieve_random_values_http`)  utilizaremos la API REST de Xively. La autenticación se realiza mediante un token JWT (JSON Web Tokens) obtenido al iniciar sesión, y que iremos renovando cada 25 minutos:

``` python
payload = {
          "emailAddress" : xiv_data['login_username'],
          "password" : xiv_data['login_password'],
          "accountId": xiv_data['account_id'],
          "renewalType": "short"
      }

  response = requests.request("POST", login_url, data=payload)

  if response.status_code == 200:
      self.jwt = json.loads(response.text)['jwt']
```

Todos los valores de autenticación se encuentran en el archivo `config.py`, aunque por seguridad no están incluidos en nuestro repositorio GIT, y simplemente hemos subido la plantilla (`config_template.py`).

El uso de Xively, como comentaba anteriormente, ha hecho todo mucho más complicado de lo que habría podido ser: requería de aprender un protocolo nuevo, estudiar toda su documentación para la autenticación, el manejo de librerías poco comunes... Pero nos ha permitido ver distintas formas de comunicación entre servicios web y mostrar claramente cómo, a través de nuestra API REST, realmente estamos abstrayendo un servicio muy complejo.

### Presentación de la web

### Umbral histórico - Petición del usuario (dato 1)

### Umbral histórico - Respuesta de la aplicación al usuario (dato 1)

### Valor medio - Petición del usuario y respuesta de la aplicación (dato 2)

### Interfaz gráfica de usuario de las plataformas externas (dato 3)

## Especificación avanzada

### Desarrollo de umbral actual (respondiendo por SSE o *web pusher*)

- SSE: http://flask.pocoo.org/snippets/116/

- Web Pusher: https://sendpulse.com/

### Docker



## Nginx



## GIT



## Bibliografía

- https://statusq.org/archives/2014/10/25/6161/

- https://www.coria.com/blog/xively/xivelyonpython-step2
- https://junquera.app.xively.com/devices/84740985-263b-4777-a44a-53710e34de82
- https://developer.xively.com/docs/device-authentication-methods
- https://developer.xively.com/

- https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
- https://www.digitalocean.com/community/tutorials/how-to-set-up-nginx-server-blocks-virtual-hosts-on-ubuntu-16-04
- http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/
