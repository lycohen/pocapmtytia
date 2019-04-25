import os

from flask import Flask
import random   
import time
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)
os.environ['http_proxy']=''
os.environ['https_proxy']=''
os.environ['no_proxy']='.bancogalicia.com.ar,.cluster.local,.svc,10.0.68.0/24,10.0.68.1,10.0.68.2,10.0.68.3,10.254.128.0/18,10.254.128.1,10.254.192.0/18,127.0.0.1,169.254.169.254,api-ocp-lab-internal.bancogalicia.com.ar,localhost,lookubglus01.bancogalicia.com.ar,lookubglus02.bancogalicia.com.ar,lookubglus03.bancogalicia.com.ar,lookubinf01.bancogalicia.com.ar,lookubinf02.bancogalicia.com.ar,lookubinf03.bancogalicia.com.ar,lookubmas01.bancogalicia.com.ar,lookubmas02.bancogalicia.com.ar,lookubmas03.bancogalicia.com.ar,lookubnod02.bancogalicia.com.ar,lookubnod03.bancogalicia.com.ar,registry.redhat.io,*.bancogalicia.com.ar'


app.config['ELASTIC_APM'] = {
    # allowed app_name chars: a-z, A-Z, 0-9, -, _, and space from elasticapm.contrib.flask
    'DEBUG': True,
    'SERVER_URL': 'http://elastic01.bancogalicia.com.ar:8200',
    'SERVICE_NAME': 'pythonpoc',
    'TRACES_SEND_FREQ': 5,
    'FLUSH_INTERVAL': 1, # 2.x
    'MAX_QUEUE_SIZE': 1, # 2.x
}

apm = ElasticAPM(app)

@app.route('/')
def hello_world():
    #target = os.environ.get('TARGET', 'World')
    #return 'Hello {}!\n'.format(target)
    return 'TYT-IA POC Observability'
#def show_import():
#	im = Image.Open('images/logo.jpg')
#	im.show()
@app.route('/health')
def getSaludRND():
    i=random.randint(0,100)
    espera=random.randint(0,2)
    time.sleep(espera)
    apm.capture_message('INFO - Resultado:' + str(i) + ' Espera:'+str(espera) )
    if (i>67):
        return 'DOWN\n'
    else:
        return 'UP\n'    
#def show_import():
#	im = Image.Open('images/logo.jpg')
#	im.show()
@app.route('/error')       
def forceError():
    try:
        a=1/0
    except Exception as err:
        #este da error
        #apm.capture_error('ERROR'+  str(err))
        #este ok
        apm.capture_exception()
        return str(err)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
