from rest_framework.authentication import TokenAuthentication as TokenAuthentication_


class TokenAuthentication(TokenAuthentication_):
    keyword = 'Bearer'
