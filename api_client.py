import requests
import json


class TogglClientApi:

    defaultCredentials = {
        'token': '',
        'username': '',
        'workspace_name': '',
        'base_url': 'https://www.toggl.com/api',
        'ver_api': 8,
        'base_url_report': 'https://toggl.com/reports/api',
        'ver_report': 2
    }
    credentials = {}
    api_token = ''
    api_username = ''
    api_base_url = None
    api_report_base_url = None
    workspace_name = None
    requests = None

    def __init__(self, credentials):
        self.credentials = dict(self.defaultCredentials.items() + credentials.items())
        self.api_base_url = self.build_api_url(self.credentials['base_url'], self.credentials['ver_api'])
        self.api_report_base_url = self.build_api_url(self.credentials['base_url_report'], self.credentials['ver_report'])
        self.api_token = self.credentials['token']
        self.api_username = self.credentials['username']
        return

    @staticmethod
    def build_api_url(base_url, version):
        return base_url + '/v' + str(version)

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

    """
    @param start_date YYYY-MM-DD
    @param end_date YYYY-MM-DD
    """""
    def get_user_hours_range(self, user_agent, workspace_id, user_id, start_date, end_date):
        params = {
            'workspace_id': workspace_id,
            'since': start_date,
            'until': end_date,
            'user_agent': user_agent,
            'user_ids': user_id,
            'grouping': 'users',
            'subgrouping': 'projects'
        }
        projects_worked_response = self.query_report('/summary', params)

        json_response = projects_worked_response.json()

        if len(json_response['data']) > 0:
            time_total = json_response['data'][0]['time']
        else:
            time_total = 0

        return time_total

    def query_report(self, url, params={}, method='GET'):
        return self._query(self.api_report_base_url, url, params, method)

    def query(self, url, params={}, method='GET'):
        return self._query(self.api_base_url, url, params, method)

    def _query(self, base_url, url, params, method):
        api_endpoint = base_url + url
        toggl_auth = (self.api_token, 'api_token')
        toggl_headers = {'content-type': 'application/json'}

        if method == "POST":
            response = self._do_post_query(api_endpoint, headers=toggl_headers, auth=toggl_auth, params=params)
        elif method == "GET":
            response = self._do_get_query(api_endpoint, headers=toggl_headers, auth=toggl_auth, params=params)
        else:
            response = self._do_get_query(api_endpoint, headers=toggl_headers, auth=toggl_auth, params=params)

        return response

    @staticmethod
    def _do_get_query(url, headers, auth, params):
        response = requests.get(url, headers=headers, auth=auth, params=params)

        return response

    @staticmethod
    def _do_post_query(url, headers, auth, params):
        response = requests.post(url, headers=headers, auth=auth,
                                 data=json.dumps(params))
        return response
