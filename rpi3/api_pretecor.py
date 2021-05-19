import requests
from datetime import datetime
import json
class API:
    def __init__(self):
        #abriendo config file
        with open('/home/pi/config.json') as f:
            config = json.load(f)   
        self.server_ip = config["SERVER_IP"]
        self.end_point_passwd = config["END_POINT_PASSWD"]
        self.get_data_end_point = config["GET_DATA_END_POINT"]
        self.insert_event_end_point = config["INSERT_EVENT_END_POINT"]

    def make_request(self,method, url, payload, headers):
        status_code = 0
        content = None
        try:
            if(method == "GET"):                                 
                r = requests.get(url = url,params=payload,timeout=1)                 
            else:
                #print("haciendo post")                 
                r = requests.post(url = url, data=payload, headers=headers,timeout=3)                 
            content = r.json()
            status_code = r.status_code
            if(status_code != 200):
                status = 'pending'
            else:
                status = 'sent'
        except:
            status = 'pending'
        return status, content

    def get_data(self,poste_id):
        url = self.server_ip + self.get_data_end_point 
        params={
            "id":poste_id,
            "passwd":self.end_point_passwd, 
        }
        
        status,response = self.make_request(method="GET",url=url,payload=params,headers="" )
        return status,response

    def insert_event(self,poste_id,event):
 
        url = self.server_ip + self.insert_event_end_point 
        #print(url)
        params={
            "id_dispositivo":poste_id,
            "evento": event,
            "passwd":self.end_point_passwd, 
        }
        
        status,response = self.make_request(method="POST",url=url,payload=params,headers="" )
        return status,response
"""
example of use


if __name__ == "__main__":
    device_id = 1
    api = API()
    status,response = api.get_data(device_id)
  
    if(status=="sent"):
        for datos in response["respuesta"]:        
            print(datos["mensaje"])
    
    status,response = api.insert_event(device_id,"poste_encendido")
    print(status, response)

"""
