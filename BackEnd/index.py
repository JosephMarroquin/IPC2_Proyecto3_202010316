from flask import Flask,request,jsonify
from flask_cors import CORS
from entrada import Entrada
import json,re
import xml.etree.ElementTree as xml
import xml.etree.ElementTree as ET
import re
from matplotlib import pyplot as plt

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

    emisores_malos=0
    receptores_malos=0

    referenciaDuplicada=0

    #Datos para la base
    for dte in root.findall("DTE"):
        for tiempo in dte.findall("TIEMPO"):
            for totalPago in dte.findall("TOTAL"):
                a=re.findall(r'[0-9]+[/]+[0-9]+[/]+[0-9]+[0-9]+[0-9]+[0-9]',str(tiempo.text))
                fec="".join(a)
                crearEntrada(fec,totalPago.text)
            

    #Lectura XML
    for dte in root.findall("DTE"):
        for tiempo in dte.findall("TIEMPO"):
            a=re.findall(r'[0-9]+[/]+[0-9]+[/]+[0-9]+[0-9]+[0-9]+[0-9]',str(tiempo.text))
            fec="".join(a)
            tiempoA.append(fec)
            facturas_recibidas+=1
    
    for dte in root.findall("DTE"):
        for referencia in dte.findall("REFERENCIA"):
            referenciaA.append(referencia.text)
    
    for dte in root.findall("DTE"):
        for nitEmisor in dte.findall("NIT_EMISOR"):
            nit_emisor.append(nitEmisor.text)
    
    for dte in root.findall("DTE"):
        for nitReceptor in dte.findall("NIT_RECEPTOR"):
            nit_receptor.append(nitReceptor.text)
    
    for dte in root.findall("DTE"):
        for totalPago in dte.findall("TOTAL"):
            total.append(totalPago.text)
    
    #Emisores
    for i in range(len(nit_emisor)):
        nit_emisor[i] = nit_emisor[i].strip()
    
    emisoresSINREPETIR=[]

    for item in nit_emisor:
        if item not in emisoresSINREPETIR and not re.search(r'[a-zA-Z]',item) and len(item)<=20:
            emisoresSINREPETIR.append(item)
    
    for item in nit_emisor:
        if re.search(r'[a-zA-Z]',item) or len(item)>20:
            emisores_malos+=1
    
    cantidad_emisores=int(len(emisoresSINREPETIR))

    #Receptores
    for i in range(len(nit_receptor)):
        nit_receptor[i] = nit_receptor[i].strip()
    
    receptoresSINREPETIR=[]

    for item in nit_receptor:
        if item not in receptoresSINREPETIR and not re.search(r'[a-zA-Z]',item) and len(item)<=20:
            receptoresSINREPETIR.append(item)
    
    for item in nit_receptor:
        if re.search(r'[a-zA-Z]',item) or len(item)>20:
            receptores_malos+=1
    
    cantidad_receptores=int(len(receptoresSINREPETIR))

    #Referencia duplicada
    for i in range(len(referenciaA)):
        referenciaA[i] = referenciaA[i].strip()
    
    referenciaSINREPETIR=[]

    for item in referenciaA:
        if item not in referenciaSINREPETIR and len(item)<=40:
            referenciaSINREPETIR.append(item)
    
    referenciaDuplicada=int(len(referenciaA))-int(len(referenciaSINREPETIR))

    facturas_correctas=0

    facturas_correctas=int(facturas_recibidas)-int(emisores_malos)-int(receptores_malos)-int(referenciaDuplicada)
    
    #print(tiempoA)
    #print(referenciaA)
    #print(nit_emisor)
    #print(nit_receptor)
    #print(total)
    #print(facturas_recibidas)
    #print(cantidad_emisores)
    #print(emisores_malos)
    #print(cantidad_receptores)
    #print(receptores_malos)
    #print(referenciaDuplicada)
    #print(facturas_correctas)

    #XML SALIDA
    reporte = ET.Element('LISTAAUTORIZACIONES')
    reporte.text="\n"
    autorizacion = ET.SubElement(reporte, 'AUTORIZACION')
    autorizacion.text="\n"
    facturaRecibidaXML = ET.SubElement(autorizacion, 'FACTURAS_RECIBIDAS')
    facturaRecibidaXML.text=str(facturas_recibidas)
    erroresXML = ET.SubElement(autorizacion, 'ERRORES')
    erroresXML.text="\n"
    emisormaloXML = ET.SubElement(erroresXML, 'NIT_EMISOR')
    emisormaloXML.text="\n"+str(emisores_malos)+"\n"
    receptormaloXML = ET.SubElement(erroresXML, 'NIT_RECEPTOR')
    receptormaloXML.text="\n"+str(receptores_malos)+"\n"
    referenciaduplicadaXML = ET.SubElement(erroresXML, 'REFERENCIA_DUPLICADA')
    referenciaduplicadaXML.text="\n"+str(referenciaDuplicada)+"\n"
    facturacorrectaXML = ET.SubElement(autorizacion, 'FACTURAS_CORRECTAS')
    facturacorrectaXML.text="\n"+str(facturas_correctas)+"\n"
    cantidademisoresXML = ET.SubElement(autorizacion, 'CANTIDAD_EMISORES')
    cantidademisoresXML.text="\n"+str(cantidad_emisores)+"\n"
    cantidadreceptoresXML = ET.SubElement(autorizacion, 'CANTIDAD_RECEPTORES')
    cantidadreceptoresXML.text="\n"+str(cantidad_receptores)+"\n"

    conteo=0
    for tiempoX,referencia,nemisor,nreceptor,total in zip(tiempoA,referenciaA,nit_emisor,nit_receptor,total):
        fechaXML = ET.SubElement(autorizacion, 'FECHA')
        fechaXML.text="\n"+str(tiempoX)+"\n"
        listadoAutorizacionXML = ET.SubElement(autorizacion, 'LISTADO_AUTORIZACIONES')
        listadoAutorizacionXML.text="\n"
        aprobacionXML = ET.SubElement(listadoAutorizacionXML, 'APROBACION')
        aprobacionXML.text="\n"
        nitemisorXML = ET.SubElement(aprobacionXML, 'NIT_EMISOR', ref=str(referencia))
        nitemisorXML.text="\n"+str(nemisor)+"\n"
        nitreceptorXML = ET.SubElement(aprobacionXML, 'NIT_RECEPTOR')
        nitreceptorXML.text="\n"+str(nreceptor)+"\n"
        codaprobacionXML = ET.SubElement(aprobacionXML, 'CODIGO_APROBACION')
        conteo+=1
        characters = "/"
        for x in range(len(characters)):
            string=tiempoX
            string = string.replace(characters[x],"")
        codaprobacionXML.text="\n"+str(string)+"0000000"+str(conteo)+"\n"
        totalXML = ET.SubElement(aprobacionXML, 'TOTAL')
        totalXML.text="\n"+str(total)+"\n"
    
    totalaprobacionesXML = ET.SubElement(listadoAutorizacionXML, 'TOTAL_APROBACIONES')
    totalaprobacionesXML.text="\n"+str(facturas_correctas)+"\n"
    
        

    datosXML = ET.tostring(reporte)
    with open("autorizaciones.xml",'w') as f:
        f.write(datosXML.decode('utf-8'))

    #a=[0,1,2]
    #b=[0,1,2]
    #c=[0,1,2]

    #for x,y,z in zip(a,b,c):
        #print(x,y,z)

#grafica
def graficaR(data):

    fecha=[]
    total=[]
    
    for ent in entrada:

        if data==ent.getFecha():
            fecha.append(ent.getFecha())
            total.append(ent.getTotal())

    fig, ax = plt.subplots()
    ax.scatter(fecha, total)
    plt.savefig('FrontEnd/static/img/graficaResumen.png')

def graficaRango(dataI,dataF):

    fechaR=[]
    totalR=[]
    
    for ent in entrada:

        if dataI==ent.getFecha():
            if ent.getFecha()<=dataF:
                fechaR.append(ent.getFecha())
                totalR.append(ent.getTotal())
        elif ent.getFecha()<=dataF:
            fechaR.append(ent.getFecha())
            totalR.append(ent.getTotal())

    fig, ax = plt.subplots()
    ax.scatter(fechaR, totalR)
    plt.savefig('FrontEnd/static/img/graficaRango.png')

#carga masiva
@app.route('/cargar',methods=['POST'])
def carga():
    dato = request.json
    cargamasiva(dato['data'])
    return '{"data":"Cargados"}'

#grafica Resumen
@app.route('/graficaR',methods=['POST'])
def graficaresumen():
    dato=request.json
    graficaR(dato['fecha'])
    return '{"data":"Creado"}'


#grafica Rango
@app.route('/graficaRango',methods=['POST'])
def graficarangoo():
    dato=request.json
    graficaRango(dato['fechaI'],dato['fechaF'])
    return '{"data":"Creado"}'

#INICIAR EL SERVIDOR
if __name__== "__main__": 
    app.run(debug=True)