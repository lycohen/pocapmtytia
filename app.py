import os

#from PIL import Image
from flask import Flask,Response,send_from_directory
import random   
import time
from elasticapm.contrib.flask import ElasticAPM

app = Flask(__name__)


app.config['ELASTIC_APM'] = {
    # allowed app_name chars: a-z, A-Z, 0-9, -, _, and space from elasticapm.contrib.flask
    'DEBUG': True,
    'SERVER_URL': 'http://delasticsearch01.bancogalicia.com.ar:8200',
    'SERVICE_NAME': 'pythonpoc',
    'TRACES_SEND_FREQ': 5,
    'FLUSH_INTERVAL': 1, # 2.x
    'MAX_QUEUE_SIZE': 1, # 2.x
}

apm = ElasticAPM(app)

@app.route('/hello_world')
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
    
@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    print (root_dir)
    return send_from_directory(os.path.join(root_dir), filename)
    #return app.send_static_file('home.html')    


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
