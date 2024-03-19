from geopy.geocoders import Nominatim
import brazilcep
from shapely.geometry import Point


class Localizacao():

    
    def __init__(self, cep):
        self.cep = cep
        self.endereco = brazilcep.get_address_from_cep(cep)
        self.geolocator = Nominatim(user_agent="monigGeo")
        self.rua = f"{self.endereco['street'][0]}. {self.endereco['street'][3:]}"
        self.bairro = self.endereco['district']
        self.cidade = self.endereco['city']

    # def endereco(self):
    #     self.geolocator = Nominatim(user_agent="monigGeo")
    #     self.rua = f"{self.endereco['street'][0]}. {self.endereco['street'][3:]}"
    #     self.bairro = self.endereco['district']
    #     self.cidade = self.endereco['city']

    def location(self):
        self.localizacao = self.geolocator.geocode(f"{self.rua}, {self.bairro}-{self.cidade}")
        self.latitude = self.geolocator.geocode(f"{self.rua}, {self.bairro}-{self.cidade}").latitude
        self.longitude = self.geolocator.geocode(f"{self.rua}, {self.bairro}-{self.cidade}").longitude
        #ponto = Point(self.latitude, self.longitude)
        return f"SRID=4674;POINT({self.latitude} {self.longitude})"