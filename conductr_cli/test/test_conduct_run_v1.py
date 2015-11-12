from conductr_cli.test.cli_test_case import strip_margin
from conductr_cli.test.conduct_run_test_base import ConductRunTestBase
from conductr_cli import conduct_run


try:
    from unittest.mock import patch, MagicMock  # 3.3 and beyond
except ImportError:
    from mock import patch, MagicMock


class TestConductRunCommand(ConductRunTestBase):

    def __init__(self, method_name):
        super().__init__(method_name)

        self.default_args = {
            'ip': '127.0.0.1',
            'port': 9005,
            'api_version': '1',
            'verbose': False,
            'long_ids': False,
            'cli_parameters': '',
            'bundle': '45e0c477d3e5ea92aa8d85c0d8f3e25c',
            'scale': 3,
            'affinity': None
        }

        self.default_url = 'http://127.0.0.1:9005/bundles/45e0c477d3e5ea92aa8d85c0d8f3e25c?scale=3'

        self.output_template = """|Bundle run request sent.
                                  |Stop bundle with: conduct stop{params} {bundle_id}
                                  |Print ConductR info with: conduct info{params}
                                  |"""

    def test_success(self):
        self.base_test_success()

    def test_success_verbose(self):
        self.base_test_success_verbose()

    def test_success_long_ids(self):
        self.base_test_success_long_ids()

    def test_success_with_configuration(self):
        self.base_test_success_with_configuration()

    def test_failure(self):
        self.base_test_failure()

    def test_failure_invalid_address(self):
        self.base_test_failure_invalid_address()

    def test_error_with_affinity_switch(self):
        args = {
            'ip': '127.0.0.1',
            'port': 9005,
            'api_version': '1.0',
            'verbose': False,
            'long_ids': False,
            'cli_parameters': '',
            'bundle': '45e0c477d3e5ea92aa8d85c0d8f3e25c',
            'scale': 3,
            'affinity': 'other-bundle'
        }

        stderr = MagicMock()
        with patch('sys.stderr', stderr):
            conduct_run.run(MagicMock(**args))

        self.assertEqual(
            strip_margin("""|ERROR: Affinity feature is only available for v1.1 onwards of ConductR
                            |"""),
            self.output(stderr))