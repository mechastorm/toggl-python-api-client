import sys, argparse
import unittest
from pymock import Controller, Any
from ..api_client import TogglClientApi
import requests

class ToogleClientApiTests(unittest.TestCase):

    api = None

    # Runs before *every* tests
    def setUp(self):
        self.credentials = {
            'workspace_name': 'Invoke Labs',
            'token': 'b5528eb340da077d442f0e7e9f70ffea',
            'username': ''  # Username is not required in Toggl's API
        }
        self.api = TogglClientApi(self.credentials, requests)

    # Runs after *every* tests
    def tearDown(self):
        del self.api

    def test_api_client_instance_created(self):
        self.assertNotEqual(self.api, None)

    def test_overriding_default_base_url_and_version_on_instance_creation(self):
        my_base_url = 'http://myownapi.com'
        my_ver_no = 12
        credentials = {
            'base_url': my_base_url,
            'ver': my_ver_no
        }
        self.api = TogglClientApi(credentials, requests)
        self.assertEqual(self.api.api_base_url, my_base_url + '/v' + str(my_ver_no))

    def test_api_token_set(self):
        self.assertNotEqual(self.api.api_token, '')

    # def test_api_username_set(self):
    #     self.assertNotEqual(self.api.api_username, '')

    def test_valid_toggl_base_url(self):
        self.assertEqual(self.api.api_base_url, 'https://www.toggl.com/api/v8')

    def test_api_toggl_auth_check_response_ok(self):
        response = self.api.query('/me')
        self.assertEqual(response.status_code, requests.codes.ok)

    def test_api_toggl_get_list_of_workspaces_response_ok(self):
        response = self.api.get_workspaces()
        self.assertEqual(response.status_code, requests.codes.ok)

    def test_api_toggl_get_workspace_by_name_found(self):
        workspace = self.api.get_workspace_by_name(self.credentials['workspace_name'])
        self.assertNotEqual(workspace['id'], '')

    def test_api_toggl_get_workspace_members_response_ok(self):
        workspace = self.api.get_workspace_by_name(self.credentials['workspace_name'])
        response = self.api.get_workspace_members(workspace['id'])
        self.assertEqual(response.status_code, requests.codes.ok)

    def _api_toggl_get_member_total_hours_range_response_ok(self):
        response = self.api.get_user_hours_range(workspace_user_id, start_date, end_date)
        self.assertEqual(response.status_code, requests.codes.ok)