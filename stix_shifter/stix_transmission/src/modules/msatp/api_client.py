"""Apiclient for MSATP"""
import json
from ..utils.RestApiClient import RestApiClient

DEFAULT_LIMIT = 10000
DEFAULT_OFFSET = 0


class APIClient:
    """API Client to handle all calls."""
    def __init__(self, connection, configuration):
        """Initialization.
        :param connection: dict, connection dict
        :param configuration: dict,config dict"""

        headers = dict()
        url_modifier_function = None
        auth = configuration.get('auth')
        self.endpoint = 'api/advancedqueries/run'
        self.host = connection.get('host')

        if auth:
            if 'access_token' in auth:
                headers['Authorization'] = "Bearer " + auth['access_token']

        self.client = RestApiClient(connection.get('host'),
                                    connection.get('port', None),
                                    connection.get('cert', None),
                                    headers,
                                    url_modifier_function=url_modifier_function,
                                    cert_verify=connection.get('selfSignedCert', True),
                                    mutual_auth=connection.get('use_securegateway', False),
                                    sni=connection.get('sni', None)
                                    )

    def ping_box(self):
        """Ping the endpoint."""
        endpoint = '/api'
        return self.client.call_api(endpoint, 'GET')

    def run_search(self, query_expression, offset=DEFAULT_OFFSET, length=DEFAULT_LIMIT):
        """get the response from MSatp endpoints
        :param query_expression: str, search_id
        :param offset: int,offset value
        :param length: int,length value
        :return: response, json object"""
        serialize = '| serialize rn = row_number() | where rn >= {offset} | limit {length}'
        headers = dict()
        headers['Content-Type'] = 'application/json'
        headers['Accept'] = 'application/json'
        endpoint = self.endpoint
        query_expression = query_expression + serialize.format(offset=offset, length=length)
        query_expression = json.dumps({'Query': query_expression}).encode("utf-8")
        return self.client.call_api(endpoint, 'POST', headers=headers, data=query_expression)
