from keycloak import KeycloakOpenID
import os

keycloak_openid = KeycloakOpenID(server_url=os.environ.get('URL_KEYCLOAK'),
                                 client_id=os.environ.get('CLIENT_ID'),
                                 realm_name=os.environ.get('REALM'),
                                 client_secret_key=os.environ.get('CLIENT_SECRET')
                                 )


def autenticar_token(access_token):
    result = keycloak_openid.introspect(access_token)
    return result['active']
