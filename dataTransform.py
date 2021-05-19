import json
import time
from datetime import datetime,timedelta
class data_tranform():
    def __init__(self):
        self.diff_time_zone = 0

    def get_date(self,time_str):
        format = '%Y-%m-%d %H:%M:%S' 
        date = datetime.strptime(time_str, format)
        date = date - timedelta(hours=int(self.diff_time_zone), minutes=0)
        return str(date)
    def estado_poste(self,ultima_conexion):
        now = datetime.utcnow()
        format = '%Y-%m-%d %H:%M:%S' 
        ultima = datetime.strptime(ultima_conexion, format)        
        time_difference = now-ultima
        time_difference_in_minutes = time_difference / timedelta(minutes=1)
        if time_difference_in_minutes>2:
            return "OFFLINE"
        else:
            return "ONLINE"
    def get_json_report(self,mensaje):
        Respuesta={'respuesta':[]}        
        for mensaje in mensaje:
            Respuesta['respuesta'].append({"id":str(mensaje[0]),"mensaje":mensaje[1],"color":mensaje[2],"tipo":mensaje[3],"duracion":mensaje[4],"activo":mensaje[5],"creado_a":mensaje[6]})
        json_string = json.dumps(Respuesta)     
        return json_string
    
    def get_clients_report(self,mensaje):
        Respuesta={'respuesta':[]}        
        for mensaje in mensaje:
            Respuesta['respuesta'].append({"id":str(mensaje[0]),"nombre":mensaje[1],"telefono":mensaje[2],"user_name":mensaje[3],"password":mensaje[4],"creado_en":mensaje[5],"actualizado_en":mensaje[6]})
        json_string = json.dumps(Respuesta)     
        return json_string

    def get_vector_report(self,mensaje):
        mensajes= []
        for mensaje in mensaje:
            mensajes.append(mensaje)
        return mensajes

    def get_devices_report(self,dispositivos):
        Respuesta={'respuesta':[]}        
        for dispositivo in dispositivos:
            fecha_instalacion =  dispositivo[5]     
            fecha_instalacion=self.get_date(fecha_instalacion)
            Respuesta['respuesta'].append({"id":dispositivo[0],"modelo_poste":dispositivo[1],"serial":dispositivo[2],"ubicacion":dispositivo[3],"ciudad":dispositivo[4],"fecha_instalacion":fecha_instalacion})
        return Respuesta

    def get_device_report(self,dispositivo):      
        fecha_instalacion =  dispositivo[5]     
        fecha_instalacion=self.get_date(fecha_instalacion)
        Respuesta = {"id":dispositivo[0],"modelo_poste":dispositivo[1],"serial":dispositivo[2],"ubicacion":dispositivo[3],"ciudad":dispositivo[4],"fecha_instalacion":fecha_instalacion}
        return Respuesta

    def get_status_report(self,estado_poste):
        Respuesta={}
        try:
            ultima_conexion = estado_poste[0][0]     
            estado = self.estado_poste(ultima_conexion)    
            Respuesta["estado"] =estado
            ultima_conexion = self.get_date(ultima_conexion)      
            Respuesta["last_connection"] =ultima_conexion

        except:
            Respuesta["last_connection"] =0
            Respuesta["estado"] = "OFFLINE"
        return Respuesta

    def  get_mensajes_report(self,mensajes):
        Respuesta={'respuesta':[]}
        for mensaje in mensajes:
            modificado =  mensaje[6]     
            modificado=self.get_date(modificado)
            Respuesta['respuesta'].append({"id":mensaje[0],"mensaje":mensaje[1],"color":mensaje[2],"tipo":mensaje[3],"duracion":mensaje[4],"activado":mensaje[5],"modificado":modificado})
        return Respuesta

    def get_mensaje_report(self,mensaje):   
        if(mensaje[5]==1):
            estado="Activado"
        else:
            estado="Desactivado"
        modificado=mensaje[6]
        modificado=self.get_date(modificado)
        Respuesta={"id":mensaje[0],"mensaje":mensaje[1],"color":mensaje[2],"tipo":mensaje[3],"duracion":mensaje[4],"activado":estado,"modificado":modificado,"id_dispositivo":mensaje[7]}  
        return Respuesta

