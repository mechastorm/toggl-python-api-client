import logging
import requests

class TogglClientApi:

    defaultCredentials = {
        'token': '',
        'username': '',
        'workspace_name': '',
        'base_url': 'https://www.toggl.com/api',
        'ver': 8
    }
    credentials = {}
    api_token = ''
    api_username = ''
    api_base_url = None
    workspace_name = None
    requests = None

    def __init__(self, credentials, requests):
        self.credentials = dict(self.defaultCredentials.items() + credentials.items())
        self.api_base_url = self.credentials['base_url'] + '/v' + str(self.credentials['ver'])
        self.api_token = self.credentials['token']
        self.api_username = self.credentials['username']
        self.requests = requests
        return

    def get_workspace_by_name(self, name):
        workspace_found = None
        list_response = self.get_workspaces();

        if list_response.status_code != requests.codes.ok:
            list_response.raise_for_status()

        workspace_list = list_response.json()
        for workspace in workspace_list:
            if workspace['name'] == name:
                workspace_found = workspace

        return workspace_found

    def get_workspaces(self):
        return self.query('/workspaces');

    def get_workspace_members(self, workspace_id):
        response = self.query('/workspaces/'+str(workspace_id)+'/workspace_users');
        return response

    def query(self, url, params={}, method='GET'):
        response = None
        api_endpoint = self.api_base_url + url
        toggl_auth = (self.api_token, 'api_token')
        toggl_headers = {'content-type': 'application/json'}

        if method == "POST":
            return False
        elif method == "GET":
            response = self._do_get_query(api_endpoint, headers=toggl_headers, auth=toggl_auth, params=params)
        else:
            response = self._do_get_query(api_endpoint, headers=toggl_headers, auth=toggl_auth, params=params)

        logging.debug(response)

        return response

    @staticmethod
    def _do_get_query(url, headers, auth, params):
        response = requests.get(url, headers=headers, auth=auth, params=params)

        return response