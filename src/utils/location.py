from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable
import brazilcep
from shapely.geometry import Point
import time


class Localizacao():

    
    def __init__(self, cep):
        self.cep = cep
        self.endereco = brazilcep.get_address_from_cep(cep)
        self.geolocator = Nominatim(user_agent="monigGeo")
        if len(self.endereco['street']) >= 4:
            self.rua = f"{self.endereco['street'][0]}. {self.endereco['street'][3:]}"
        else:
            self.rua = self.endereco['street'] 
        # self.rua = f"{self.endereco['street'][0]}. {self.endereco['street'][3:]}"
        self.bairro = self.endereco['district']
        self.cidade = self.endereco['city']
        print(self.geolocator.__dict__)
       

    # def endereco(self):
    #     self.geolocator = Nominatim(user_agent="monigGeo")
    #     self.rua = f"{self.endereco['street'][0]}. {self.endereco['street'][3:]}"
    #     self.bairro = self.endereco['district']
    #     self.cidade = self.endereco['city']

     
    def location(self):
        point = Point(0, 0) 
        try:
            result = self.geolocator.geocode(f"{self.rua}, {self.bairro}-{self.cidade}")

            if result:  
                self.latitude = result.latitude
                self.longitude = result.longitude
                return f"SRID=4674;POINT({self.latitude} {self.longitude})"
            else:
                print(f"Localização não encontrada para {self.rua}, {self.bairro}-{self.cidade}")
                return "SRID=4674;{}".format(point) # Valor default

        except GeocoderUnavailable as e:
            print(f"Erro de geocodificação: {e}")
            
            return "SRID=4674;{}".format(point)  # Valor default 
            
        
# cep = "18260-000"
# retorno = Localizacao(cep).location()
# print(retorno)
#python src/utils/location.py