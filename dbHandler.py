import sqlite3
import os
from sqlite3 import Error

class dbHandler:

    def __init__(self):
        """
        Crea la base de datos en caso de no existir
        """
      
        self.db_filename = "database.db"
        db_exists = not os.path.exists(self.db_filename)
        connection = sqlite3.connect(self.db_filename)
        self.new_db = False
        if db_exists:
            self.new_db = True
            print("CREATING DB")
            self.sql_create_tables(connection)
            self.sql_init_data()
        else:
            self.new_db = False
            self.sql_create_tables(connection)
        connection.close()
    
    def sql_create_tables(self, connection):
        """
        Crea la tabla para la base de datos 
        toma el objeto connection como entrada para
        manejar la db
        """
        connection.execute("PRAGMA foreign_keys = ON;")
        cursorObj = connection.cursor()
      
        clientes = "CREATE TABLE IF NOT EXISTS clientes(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
                        nombre VARCHAR(50) NOT NULL,\
                        telefono VARCHAR(50) ,\
                        nombre_usuario VARCHAR(50) NOT NULL,\
                        contrasenia VARCHAR(50) NOT NULL,\
                        creado_en TEXT DEFAULT CURRENT_TIMESTAMP,\
                        modificado_en TEXT DEFAULT CURRENT_TIMESTAMP);"       

        dispositivos = "CREATE TABLE IF NOT EXISTS dispositivos(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
                            ubicacion VARCHAR(50) ,\
                            cliente_id INTEGER NOT NULL, \
                            ciudad VARCHAR(50) NOT NULL, \
                            modelo_poste VARCHAR(50) NOT NULL,\
                            serial VARCHAR(50) NOT NULL,\
                            fecha_instalacion DATETIME DEFAULT CURRENT_TIMESTAMP,\
                            creado_en TEXT DEFAULT CURRENT_TIMESTAMP,\
                            modificado_en TEXT DEFAULT CURRENT_TIMESTAMP);"
                                                                                  
        mensajes = "CREATE TABLE IF NOT EXISTS mensajes(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
                        id_dispositivo INTEGER NOT NULL,\
                        mensaje VARCHAR(50) NOT NULL,\
                        color VARCHAR(20) NOT NULL,\
                        tipo VARCHAR(20) NOT NULL,\
                        duracion INTEGER NOT NULL,\
                        activado INTEGER NOT NULL,\
                        creado_en TEXT DEFAULT CURRENT_TIMESTAMP,\
                        modificado_en TEXT DEFAULT CURRENT_TIMESTAMP);" 

        eventos = "CREATE TABLE IF NOT EXISTS eventos(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
                        id_dispositivo INTEGER NOT NULL,\
                        evento VARCHAR(50) NOT NULL,\
                        creado_en TEXT DEFAULT CURRENT_TIMESTAMP);"     
        
        

        cursorObj.execute(clientes)
        cursorObj.execute(dispositivos)
        cursorObj.execute(mensajes)
        cursorObj.execute(eventos)
        # Upload changes to the DB
        connection.commit()
        

    def sql_init_data(self):
        '''
        Insert all the init data (Security params)
        '''
        test_data = ["INSERT INTO clientes ('id', 'nombre', 'telefono', 'nombre_usuario', 'contrasenia') VALUES ('1', 'alcaldia_bga', '3012512011', 'alcaldia_bga', 'alcaldia1234');",
                    "INSERT INTO clientes ('id', 'nombre', 'telefono', 'nombre_usuario', 'contrasenia') VALUES ('2', 'gerente_cc', '3012512011', 'gerente_cc', 'gerente1234');",
                    "INSERT INTO dispositivos ('id', 'ubicacion', 'cliente_id', 'ciudad', 'modelo_poste', 'serial') VALUES ('1', 'parque san pio', '1','Bucaramanga', 'abcd', 'ad58we1');",
                    "INSERT INTO dispositivos ('id', 'ubicacion', 'cliente_id', 'ciudad','modelo_poste', 'serial') VALUES ('2', 'parque Giron', '1','Giron', 'abcd', 'ad58we2');",
                    "INSERT INTO dispositivos ('id', 'ubicacion', 'cliente_id','ciudad', 'modelo_poste', 'serial') VALUES ('3', 'c.c cañaveral', '2','Floridablanca', 'efgh', 'qwdaf4');",
                    "INSERT INTO dispositivos ('id', 'ubicacion', 'cliente_id', 'ciudad','modelo_poste', 'serial') VALUES ('4', 'c.c de la cuesta', '2','Piedecuesta', 'efgh', 'qwdaf5');",                     
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(1,' ', 'Negro','Fecha',10,1);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(1,'prueba 2', 'Blanco','Texto',30,0);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(2,'prueba 3', 'Verde', 'Texto_especial',40,1);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(2,' ', 'Azul','Trm',20,0);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(3,' ', 'Morado','Bandera',30,1);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(3,'prueba 6', 'Gris','Texto',20,0);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(4,'prueba 7', 'Naranja','Texto_especial',40,1);",
                    "INSERT INTO mensajes('id_dispositivo', 'mensaje','color','tipo','duracion','activado') VALUES(4,' ', 'Rojo','Hora',30,0);",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (1, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (2, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (3, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (4, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (1, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (2, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (3, 'ON');",
                    "INSERT INTO eventos('id_dispositivo', 'evento') VALUES (4, 'ON');"]
        
        for test_data in test_data:
            query = test_data
            self.sql_execute_query(query)
        print("INIT DATA INSERTED")
        
    def sql_execute_query(self, query):        
        ok = False
        data = None
        try:
            with sqlite3.connect(self.db_filename) as connection:
                connection.execute("PRAGMA foreign_keys = ON;")
                cur = connection.cursor()
                cur.execute(query)
                data = cur.fetchall()
                ok = True
                #time.sleep(1)
        except Error as e:            
            print("Error in the DB:",e)
            print("Using Query:",query)
        return [ok, data]
    
 