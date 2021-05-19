from dbHandler import dbHandler

class crudOperator:
    
    def __init__(self):
        self.db_handler = dbHandler()
        self.new_db = self.db_handler.new_db
        
    def check_user_and_password(self,user,password):
        table = "clientes"
        query = "SELECT id FROM " + table + " where nombre_usuario='"+user+"' and contrasenia='"+password+"';"
        id = self.db_handler.sql_execute_query(query)
        
        if(len(id[1])>0):
            response = id[1]
            response= response[0][0]
            return response
        else:
            return "error"

    def get_devices(self,client_id):
        table = "dispositivos"
        query = "SELECT id, modelo_poste, serial, ubicacion, ciudad, fecha_instalacion FROM " + table + " where cliente_id='"+client_id+"';"
        devices = self.db_handler.sql_execute_query(query)
 
        if(len(devices[1])>0):
            response = devices[1]    
            return response
        else:
            return "error"

    def get_device(self,device_id):
       
        table = "dispositivos"
        query = "SELECT id, modelo_poste, serial, ubicacion,ciudad, fecha_instalacion FROM " + table + " where id="+device_id+";"
        devices = self.db_handler.sql_execute_query(query)         
        if(len(devices[1])>0):
            response = devices[1]    
            return response
        else:
            return "error"

    def get_nombre_cliente(self, client_id):
        table = "clientes"
        query = "SELECT nombre FROM " + table + " where id="+client_id+";"
        id = self.db_handler.sql_execute_query(query)        
        if(len(id[1])>0):
            response = id[1]
            response= response[0][0]
            return response
        else:
            return "error"

    def get_estado_poste(self,poste_id):
        table = "eventos"
        query = "SELECT creado_en, evento FROM " + table + " where id_dispositivo='"+poste_id+"' ORDER BY creado_en desc Limit 1;"
        devices = self.db_handler.sql_execute_query(query)
        if(len(devices[1])>0):
            response = devices[1]    
            return response
        else:
            return "error"


    # User table operations
    def insert_mensaje(self, id_dispositivo,mensaje,color,duracion,tipo,estado):
        '''
        according to 
        params={id_dispositivo:XXXX,
                mensaje:XXXX,
                color:XXXX}            
        '''
        table = "mensajes" 
        try:
            query = "INSERT INTO " + table + "(id_dispositivo, mensaje,color,duracion,tipo, activado) " +\
                "VALUES(" + str(id_dispositivo) +",\'" + mensaje + "\'"+",\'" + color + "\'"+"," + duracion +",\'" +tipo +"'," + estado +");"
            mensaje = self.db_handler.sql_execute_query(query)
            return mensaje[0]
        except:
            print("error inserting new message")        
            return "error"
    def actualizar_ubicacion(self,ubicacion,ciudad,serial):
        table = "dispositivos"
        query = "UPDATE " +table+" SET ubicacion='"+ubicacion+"', ciudad='"+ciudad+"' where serial='"+serial+"';"
        print(self.db_handler.sql_execute_query(query))

    def actualizar_ciudad(self,ciudad,serial):
        table = "dispositivos"
        query = "UPDATE " +table+" SET ciudad='"+ciudad+"' where serial='"+serial+"';"
        self.db_handler.sql_execute_query(query)

    # User table operations
    def insert_evento(self, id_dispositivo,evento):
        '''       
        '''
        table = "eventos" 
        try:
            query = "INSERT INTO " + table + "(id_dispositivo, evento) " +\
                "VALUES(" + str(id_dispositivo) +",\'" + evento + "\');"
            mensaje = self.db_handler.sql_execute_query(query)
            return mensaje[0]
        except:
            print("error inserting new event")        
            return "error"
    
    def insert_cliente(self,nombre):
        '''       
        '''
        table = "clientes" 
        try:
            query = "INSERT INTO " + table + "(nombre) " +\
                "VALUES("+str(nombre) + "\');"
            mensaje = self.db_handler.sql_execute_query(query)
            return mensaje[0]
        except:
            print("error inserting new event")        
            return "error"
    def get_mensaje(self,id):
        '''
        '''
        table = "mensajes"
        query = "SELECT id,mensaje,color,tipo,duracion,activado,modificado_en FROM " + table + " where id_dispositivo="+str(id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]
    def get_mensaje_con_id(self,mensaje_id):
        table = "mensajes"
        query = "SELECT id,mensaje,color,tipo,duracion,activado,modificado_en,id_dispositivo FROM " + table + " where id="+str(mensaje_id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1][0]
    def get_all_mensaje(self):
        table = "mensajes"
        query = "SELECT * FROM " + table +";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]

    def activar_mensaje(self,id):
        table = "mensajes"
        query = "UPDATE " +table+" SET activado=1, modificado_en=datetime('now') where id="+str(id)+";"
        self.db_handler.sql_execute_query(query)     

    def desactivar_mensaje(self,id):
        table = "mensajes"
        query = "UPDATE " +table+" SET activado=0, modificado_en=datetime('now') where id="+str(id)+";"
        self.db_handler.sql_execute_query(query)
    
    def borrar_mensaje(self,id):
        table = "mensajes"
        query =  "DELETE FROM " + table +" where id="+str(id)+";"
        self.db_handler.sql_execute_query(query)

    def get_all_eventos(self):
        table = "eventos"
        query = "SELECT * FROM " + table +";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]
 
    def modify_mensaje_sin_duracion(self,mensaje,color,tipo,id,estado):
        table = "mensajes"
        if(estado=="Activado"):
            estado="1"
        if(estado=="Desactivado"):
            estado="0"
        query = "UPDATE "+table+" set mensaje ='"+mensaje+"',color ='"+color+"',tipo ='"+tipo+ "', activado ="+estado+", modificado_en=datetime('now') where id="+str(id)+";"
 
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[0]
    
    def modify_mensaje(self,mensaje,color,tipo,duracion,id,estado):
        table = "mensajes"
        if(estado=="Activado"):
            estado="1"
        if(estado=="Desactivado"):
            estado="0"
        if(mensaje=="" and duracion ==""):
            query = "UPDATE "+table+" set color ='"+color+"', tipo ='"+tipo+"',activado ="+estado+", modificado_en=datetime('now') where id="+str(id)+";"
        elif(mensaje==""):
            query = "UPDATE "+table+" set color ='"+color+"', tipo ='"+tipo+"', duracion ="+duracion+ ", activado ="+estado+", modificado_en=datetime('now') where id="+str(id)+";"            
        elif(duracion==""):
            query = "UPDATE "+table+" set mensaje ='"+mensaje+"', color ='"+color+"', tipo ='"+tipo+"',activado ="+estado+", modificado_en=datetime('now') where id="+str(id)+";"
        else:
            query = "UPDATE "+table+" set mensaje ='"+mensaje+"', color ='"+color+"', tipo ='"+tipo+"', duracion ="+duracion+ ", activado ="+estado+", modificado_en=datetime('now') where id="+str(id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[0]

    def modify_color(self,color,id):
        table = "mensajes"
        query = "UPDATE "+table+" set color ='"+color+"', modificado_en=datetime('now') where id="+str(id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[0]    

    def get_users(self):
        table = "clientes"
        query = "SELECT id,nombre,telefono,nombre_usuario,contrasenia,creado_en,modificado_en FROM " + table +";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]

    def remove_user(self,id):
        table = "clientes"
        query = "DELETE FROM " + table +" where id="+str(id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]

    def create_user(self, nombre,telefono,nombre_usuario,contrasenia):
        table = "clientes"
        query = "INSERT INTO " + table +" ('nombre', 'telefono', 'nombre_usuario', 'contrasenia')" +\
        " VALUES ( '"+nombre +"','" + telefono +"','" + nombre_usuario+ "','"+ contrasenia +"');"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]
    
    def create_device(self, ubicacion,client_id,ciudad,modelo_poste,serial):
        table = "dispositivos"
        query = "INSERT INTO " + table +" ('ubicacion', 'cliente_id', 'ciudad', 'modelo_poste', serial)" +\
        " VALUES ( '"+ubicacion +"','" + client_id +"','" + ciudad+ "','"+ modelo_poste+ "','"+ serial +"');"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]


    def remove_device(self,id):
        table = "dispositivos"
        query = "DELETE FROM " + table +" where id="+str(id)+";"
        mensaje = self.db_handler.sql_execute_query(query)
        return mensaje[1]



    