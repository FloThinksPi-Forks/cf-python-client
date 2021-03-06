import re
import unittest
from functools import reduce
from http import HTTPStatus

from abstract_test_case import AbstractTestCase
from cloudfoundry_client.doppler.client import DopplerClient


class TestLoggregator(unittest.TestCase, AbstractTestCase):
    @classmethod
    def setUpClass(cls):
        cls.mock_client_class()

    def setUp(self):
        self.build_client()
        self.doppler = DopplerClient(
            re.sub("^http", "ws", self.TARGET_ENDPOINT), proxy="", verify_ssl=False, credentials_manager=self.client
        )

    def test_recents(self):
        boundary = "d661b2c1426a3abcf1c0524d7fdbc774c42a767bdd6702141702d16047bc"
        app_guid = "app_id"
        self.client.get.return_value = self.mock_response(
            "/apps/%s/recentlogs" % app_guid,
            HTTPStatus.OK,
            {"content-type": "multipart/x-protobuf; boundary=%s" % boundary},
            "recents",
            "GET_response.bin",
        )
        cpt = reduce(lambda increment, _: increment + 1, self.doppler.recent_logs(app_guid), 0)
        self.client.get.assert_called_with(self.client.get.return_value.url, stream=True)
        self.assertEqual(cpt, 200)
