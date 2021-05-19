from flask import Flask, request,make_response,redirect, render_template, abort
from crudOperator import crudOperator
from dataTransform import data_tranform
import json
import time
app = Flask(__name__)
crud_operator = crudOperator()
dataTransform=data_tranform()
clave = "pretec2020"
diff_time_zone=0
################### Templates ########################################
@app.route('/')
def index():
    response=make_response(redirect('/index'))     
    return response

@app.route('/index')
def _index():      
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def _login():      
    error=None
    global diff_time_zone
 
    if(request.method == 'GET'):   
        diff_time_zone=request.args.get('timeZone')  
        dataTransform.diff_time_zone=diff_time_zone           
        return render_template('login.html',error=error)
    if(request.method == 'POST'):
        user=request.form.get('username')
        password=request.form.get('password')
        #check if user and password exists
        id=crud_operator.check_user_and_password(user,password)
        if(id!="error"):
            response=make_response(redirect('/dispositivos')) 
            response.set_cookie('client_id',str(id) )    
            return response
        else:
            return render_template('login.html',error="Usuario o contraseña incorrecto")

@app.route('/dispositivos',methods=['GET','POST'])
def _dispositivos():
    if(request.method == 'GET'):

        client_id=request.cookies.get('client_id')
        dispositivos=crud_operator.get_devices(client_id)        
        dispositivos=dataTransform.get_devices_report(dispositivos) 
        #enviar nombre usuario             
        nombre_cliente=crud_operator.get_nombre_cliente(client_id) 
        return render_template('dispositivos.html',dispositivos=dispositivos,nombre_cliente=nombre_cliente)
    if(request.method == 'POST'):
        if "estado_poste_id" in request.form:
            client_id=request.cookies.get('client_id')
            #enviar nombre usuario             
            nombre_cliente=crud_operator.get_nombre_cliente(client_id) 
            id = request.form.get("estado_poste_id")
            estado_poste=crud_operator.get_estado_poste(id)     
            dispositivo=crud_operator.get_device(id)        
            dispositivo=dataTransform.get_device_report(dispositivo[0])
            serial = dispositivo["serial"]
            ubicacion = dispositivo["ubicacion"]
            ciudad = dispositivo["ciudad"]
            estado_poste=dataTransform.get_status_report(estado_poste)                
            return render_template('estado_poste.html',estado_poste=estado_poste,nombre_cliente=nombre_cliente,ubicacion=ubicacion,serial=serial,ciudad=ciudad)
        
        elif "administrar_id" in request.form:                 
            id = request.form.get("administrar_id")
            response=make_response(redirect('/admin_mensajes')) 
            response.set_cookie('poste_id',str(id) )    
            return response
        
        elif  "guardar_ubicacion" in request.form:
            serial = request.form.get("guardar_ubicacion")
            ubicacion = request.form.get("ubicacion")
            ciudad = request.form.get("ciudad")
            print(ubicacion)
            response=make_response(redirect('/dispositivos')) 
            if(ubicacion==None or ubicacion == ""):
                crud_operator.actualizar_ciudad(ciudad,serial)                
            else:
                crud_operator.actualizar_ubicacion(ubicacion,ciudad,serial)
            return response
        else:             
            abort(404)

@app.route('/admin_mensajes',methods=['GET','POST'])
def _admin_mensajes():
    if(request.method == 'GET'):
        client_id=request.cookies.get('client_id')
        #enviar nombre usuario             
        nombre_cliente=crud_operator.get_nombre_cliente(client_id)   
        poste_id = request.cookies.get('poste_id')             
        dispositivo=crud_operator.get_device(poste_id)        
        dispositivo=dataTransform.get_device_report(dispositivo[0])
        serial = dispositivo["serial"]
        ubicacion = dispositivo["ubicacion"]
        mensajes = crud_operator.get_mensaje(poste_id)
        mensajes = dataTransform.get_mensajes_report(mensajes) 
        return render_template('admin_mensajes.html',mensajes=mensajes,nombre_cliente=nombre_cliente,ubicacion=ubicacion,serial=serial)
    if(request.method == 'POST'):    
        if "id_desactiva" in request.form:              
            id = request.form.get("id_desactiva")
            crud_operator.desactivar_mensaje(id)
            response=make_response(redirect('/admin_mensajes')) 
            return response
        elif "id_activa" in request.form:
            id = request.form.get("id_activa")
            crud_operator.activar_mensaje(id)
            response=make_response(redirect('/admin_mensajes')) 
            return response
        elif "id_borrar" in request.form:
            id = request.form.get("id_borrar")
            crud_operator.borrar_mensaje(id)
            response=make_response(redirect('/admin_mensajes')) 
            return response
        else:
            abort(404)

@app.route('/edit_mensaje',methods=['GET','POST'])
def _edit_mensajes():  
    if(request.method == 'POST'):
        client_id=request.cookies.get('client_id')
        #enviar nombre usuario             
        nombre_cliente=crud_operator.get_nombre_cliente(client_id)  
        mensaje_id=request.form.get('mensaje_id')                               
        mensaje = crud_operator.get_mensaje_con_id(mensaje_id)
        mensaje = dataTransform.get_mensaje_report(mensaje)  
       
        id_dispositivo = mensaje["id_dispositivo"]           
        dispositivo=crud_operator.get_device(str(id_dispositivo))        
        dispositivo=dataTransform.get_device_report(dispositivo[0])
        serial = dispositivo["serial"]
        ubicacion = dispositivo["ubicacion"]
        return render_template('edit_mensaje.html',mensaje=mensaje,nombre_cliente=nombre_cliente,ubicacion=ubicacion,serial=serial)

@app.route('/check_edited',methods=['GET','POST'])
def _check_edited():  
    if(request.method == 'POST'):
        tipo_mensaje = request.form.get('tipo_mensaje')     
        id=request.form.get('mensaje_id')
        texto=request.form.get('texto')
        color=request.form.get('color')
        duracion= request.form.get('duracion')     
        estado =  request.form.get('estado') 
        print(texto, tipo_mensaje, id, color, duracion,estado)        
        if(texto==None):
            texto=""
        if(tipo_mensaje!="Texto" and tipo_mensaje!="Texto Especial"):
            texto="    "        
        crud_operator.modify_mensaje(texto,color,tipo_mensaje,duracion,id,estado)
        response=make_response(redirect('/admin_mensajes')) 
        return response
    

@app.route('/nuevo_mensaje',methods=['GET','POST'])
def _nuevo_mensaje():  
        client_id=request.cookies.get('client_id')
        #enviar nombre usuario             
        nombre_cliente=crud_operator.get_nombre_cliente(client_id)  
        id_dispositivo = request.cookies.get('poste_id')
        dispositivo=crud_operator.get_device(str(id_dispositivo))        
        dispositivo=dataTransform.get_device_report(dispositivo[0])
        serial = dispositivo["serial"]
        ubicacion = dispositivo["ubicacion"]
        return render_template('nuevo_mensaje.html',nombre_cliente=nombre_cliente,ubicacion=ubicacion,serial=serial)
 
@app.route('/guardar_mensaje_creado',methods=['GET','POST'])
def _guardar_mensaje_creado():  
    id_dispositivo = request.cookies.get('poste_id')
    if(request.method == 'POST'):
        tipo_mensaje = request.form.get('tipo_mensaje')
        if(tipo_mensaje == "Texto" or tipo_mensaje=="Texto Especial"):             
            texto=request.form.get('texto')
            color=request.form.get('color')          
            duracion= request.form.get('duracion')   
            estado= request.form.get('estado')    
            if len(duracion) == 0:
                duracion="0"
            crud_operator.insert_mensaje(id_dispositivo,texto,color,duracion,tipo_mensaje,estado)
        else:             
            texto=""
            color=request.form.get('color')
            duracion= request.form.get('duracion')  
            estado= request.form.get('estado')      
            if len(duracion) == 0:
                duracion="0"     
            crud_operator.insert_mensaje(id_dispositivo,texto,color,duracion,tipo_mensaje,estado)

        response=make_response(redirect('/admin_mensajes')) 
        return response
      
################## API #################################

@app.route('/api/get_data',methods=['GET'])
def get(): 
    global clave
    if(request.method == 'GET'):
        """
        los campos del request son id y clave        
        """
        passwd = request.args.get('passwd')
        id = request.args.get('id') 
        if(passwd==clave):
            mensaje = crud_operator.get_mensaje(id)    
            mensaje = dataTransform.get_json_report(mensaje)     
            return(str(mensaje))
        else:
            abort(404)
    else:
        abort(404)

@app.route('/api/insert_event',methods=['POST'])
def insert_event(): 
    global clave
    if(request.method == 'POST'):
        """
        los campos del request son id y clave        
        """
        evento = request.form.get('evento')
        id_dispositivo = request.form.get('id_dispositivo')
        passwd = request.form.get('passwd')         
        if(evento!=None and id_dispositivo!=None and passwd !=None):
            if(passwd==clave):
                mensaje = crud_operator.insert_evento(id_dispositivo,evento)   
                if(mensaje == True):
                    return( json.dumps({'response':'event inserted'}))
                else:
                    return(json.dumps({'response':'error inserting event'}))
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)

@app.route('/api/get_users',methods=['GET'])
def get_users():    
    global clave
    if(request.method == 'GET'):
        """
        los campos del request son  clave        
        """
        passwd = request.args.get('passwd')
      
        if(passwd !=None):
            if(passwd==clave):
                mensaje = crud_operator.get_users()
                mensaje = dataTransform.get_clients_report(mensaje)  
                return(str(mensaje))     
          
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)

@app.route('/api/remove_user',methods=['POST'])
def remove_user():    
    global clave
    if(request.method == 'POST'):
        """
        los campos del request son  clave        
        """
        
        passwd = request.form.get('passwd')
        client_id = request.form.get('client_id') 
  
        if(passwd !=None and client_id!=None):
            if(passwd==clave):
                mensaje = crud_operator.remove_user(client_id)                
                return(json.dumps({'response':'user removed'}))     
          
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)

@app.route('/api/create_user',methods=['POST'])
def create_user():    
    global clave
    if(request.method == 'POST'):
        """
        los campos del request son  clave        
        """
        
        passwd = request.form.get('passwd')
        nombre = request.form.get('nombre') 
        telefono = request.form.get('telefono') 
        nombre_usuario = request.form.get('nombre_usuario') 
        contrasenia = request.form.get('contrasenia') 
     
        if(passwd !=None and nombre_usuario!=None and contrasenia!=None ):
            if(passwd==clave):
                mensaje = crud_operator.create_user(nombre,telefono,nombre_usuario,contrasenia)                
                return(json.dumps({'response':'user created'}))     
          
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)


@app.route('/api/get_devices',methods=['GET'])
def get_devices():    
    global clave
    if(request.method == 'GET'):
        """
        los campos del request son  clave        
        """
        passwd = request.args.get('passwd')
        client_id = request.args.get('client_id')
        if(passwd !=None and id !=None ):
            if(passwd==clave):
                mensaje = crud_operator.get_devices(client_id)
                mensaje = dataTransform.get_devices_report(mensaje)  
                return(str(mensaje))   
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)
 
@app.route('/api/remove_device',methods=['POST'])
def remove_device():    
    global clave
    if(request.method == 'POST'):
        """
        los campos del request son  clave        
        """
        
        passwd = request.form.get('passwd')
        device_id = request.form.get('device_id') 
  
        if(passwd !=None and device_id!=None):
            if(passwd==clave):
                mensaje = crud_operator.remove_device(device_id)                
                return(json.dumps({'response':'device removed'}))     
          
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)

@app.route('/api/create_device',methods=['POST'])
def create_device():    
    global clave
    if(request.method == 'POST'):
        """
        los campos del request son  clave        
        """
        
        passwd = request.form.get('passwd')
        ubicacion = request.form.get('ubicacion') 
        client_id = request.form.get('client_id') 
        ciudad = request.form.get('ciudad') 
        modelo_poste = request.form.get('modelo_poste') 
        serial = request.form.get('serial') 
     
        if(passwd !=None and client_id!=None and ciudad!=None and modelo_poste!=None and serial!=None ):
            if(passwd==clave):
                mensaje = crud_operator.create_device(ubicacion,client_id,ciudad,modelo_poste,serial )                
                return(json.dumps({'response':' device created'}))     
          
                 
            else:
                return(json.dumps({'response':'bad passwd'}))
        else:
           
            return(json.dumps({'response':'error in post data'}))
    else:
        abort(404)
 
if __name__ == "__main__":    
 
    app.run(debug=True,port=int("80"),host='0.0.0.0')
