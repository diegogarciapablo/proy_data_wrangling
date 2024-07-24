from flask import Flask, jsonify, request, render_template, redirect
from pymongo import MongoClient
import pandas as pd
import requests
#nombrando la aplicacion
app = Flask(__name__, static_url_path='', static_folder='')

#pagina de inicio para mostrar la bienvenida
@app.route('/')
def root():
    return render_template('main.html')

#esta ruta muestra todos los personajes
@app.route('/muestra_pjs')
def all_pjs():
    client = MongoClient('mongodb+srv://devan246:devan789@devan246.w7hadve.mongodb.net/')
    db = client['RyM']
    coll= db['personajes']
    resultado_pet = coll.find({},{'_id':False})
    lista_pjs = []
    for result in resultado_pet:
        lista_pjs.append(result)    
    response = jsonify({'status':200,'message':'para volver atras use el boton del navegador','data':lista_pjs})
    return response

#esta ruta es intermedia para concatenar el hipervinculo con un texto para su filtrado
@app.route('/generar_enlace', methods=['GET'])
def generar_enlace():
    # Obtén el texto desde la pagina
    texto = request.args.get('textoInput', '')  
    url_base = "/muestra_pj?var_name="
    # Concatena el texto a la URL base
    enlace_completo = url_base + texto  
    return redirect(enlace_completo)

#esta ruta es para el filtrado de los resultados por medio de un nombre
@app.route('/muestra_pj')
def one_pj():
    value1= request.args.get('var_name', type=str)
    client = MongoClient('mongodb+srv://devan246:devan789@devan246.w7hadve.mongodb.net/')
    db = client['RyM']
    coll= db['personajes']
    resultado_pet = coll.find({'nombre':value1},{'_id':False})
    lista_pjs = []
    for result in resultado_pet:
        lista_pjs.append(result)    
    if len(lista_pjs)==0:
        response = jsonify({'status':200,'message':'no escribio el nombre correctamente','data':lista_pjs})
    else:
        response = jsonify({'status':200,'message':'para volver atras use el boton del navegador','data':lista_pjs})
    return response
app.run(debug=True, host='localhost', port= 5000)