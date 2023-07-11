from keycloak import KeycloakOpenID, KeycloakAdmin
import os

keycloak_openid = KeycloakOpenID(server_url=os.environ.get('URL_KEYCLOAK'),
                                 client_id=os.environ.get('CLIENT_ID'),
                                 realm_name=os.environ.get('REALM'),
                                 client_secret_key=os.environ.get(
                                     'CLIENT_SECRET')
                                 )

#Crie uma instância do KeycloakAdmin
keycloak_admin = KeycloakAdmin(server_url=os.environ.get('URL_KEYCLOAK'),
                               username= 'victor',
                               password='045022',
                               realm_name=os.environ.get('REALM'),
                               verify=True)


def autenticar_token(access_token):
    result = keycloak_openid.introspect(access_token)
    return result['active']

def user(email, nome, senha):
    new_user = keycloak_admin.create_user(
        {   
            "username": nome,
            "enabled": True,
            "credentials": [{
                "type": "password",
                "value": senha,
                "temporary": False
            }]
        }
    )
    return new_user
