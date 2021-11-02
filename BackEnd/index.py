from flask import Flask,request,jsonify
from flask_cors import CORS
from entrada import Entrada
import json,re
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import re

app=Flask(__name__)
app.config["DEBUG"]=True

CORS(app)

entrada=[]

#Registro Entrada
def crearEntrada(fecha,total):
    entrada.append(Entrada(fecha,total))

#mostrar datos
def obtener_entrada():
    return json.dumps([ob.__dict__ for ob in entrada])

#elilminar entrada
def eliminar_entrada(user):
    for x in entrada:
        if x.user==user:
            entrada.remove(x)
            return True
    return False 

#carga masiva
def cargamasiva(data):

    file = open("entradaASD.xml", "w")
    file.write(data)
    file.close()

    objetoTree=xml.parse("entradaASD.xml")
    root=objetoTree.getroot()

    tiempoA=[]
    referenciaA=[]
    nit_emisor=[]
    nit_receptor=[]
    total=[]

    facturas_recibidas=0
    cantidad_emisores=0
    cantidad_receptores=0

    for dte in root.findall("DTE"):
        for tiempo in dte.findall("TIEMPO"):
            a=re.findall(r'[0-9]+[/]+[0-9]+[/]+[0-9]+[0-9]+[0-9]+[0-9]',str(tiempo.text))
            fec="".join(a)
            tiempoA.append(fec)
    
    for dte in root.findall("DTE"):
        for referencia in dte.findall("REFERENCIA"):
            referenciaA.append(referencia.text)
    
    print(tiempoA)
    print(referenciaA)

    a=[0,1,2]
    b=[0,1,2]
    c=[0,1,2]

    for x,y,z in zip(a,b,c):
        print(x,y,z)

    


    

#carga masiva
@app.route('/cargar',methods=['POST'])
def carga():
    dato = request.json
    cargamasiva(dato['data'])
    return '{"data":"Cargados"}'

#INICIAR EL SERVIDOR
if __name__== "__main__": 
    app.run(debug=True)