from unittest import TestCase
from unittest.mock import MagicMock, ANY

from rabbitpy.rpc.client import RpcClient


class TestClient(TestCase):

    """Test the rpc client."""

    def test_payload_legacy_rpc(self):
        """Test command for legacy RPC implementation

        """
        c = RpcClient()
        c._send_command = MagicMock()

        call_payload = {"test": 1}
        c.rpc('do_that', call_payload)

        # Note: this command should be called with the payload, server routing
        # key, and possibly a dict containing the reply_to and correlation id.
        c._send_command.assert_called_with(
            {
                "data": {
                    "command": "do_that",
                    "options": call_payload,
                }
            },
            'do_that',  # generated routing key
            ANY
        )

    def test_payload_standard_rpc(self):
        """Test command for standard RPC
        :returns: TODO

        """
        c = RpcClient(legacy=False)
        c._send_command = MagicMock()
        call_payload = {"test": 2}
        c.rpc('do_that', call_payload)
        c._send_command.assert_called_with(call_payload,
                                           'do_that',  # routing key
                                           ANY)  # properties

    def test_rpc_properties(self):
        """Test setup rpc properties.  """
        c = RpcClient()
        c._send_command = MagicMock()
        c.rpc('whatever', {"data": "x"})
        c._send_command.assert_called_with(
            ANY,
            'whatever',
            {
                "reply_to": "whatever.client",
                "correlation_id": ANY
            }
        )
        # This part shouldn't matter if legacy or not.
        c = RpcClient(legacy=False, client_queue='test.my.queue')
        c._send_command = MagicMock()
        c.rpc('whatever', {"data": "x"})
        c._send_command.assert_called_with(
            ANY,
            'whatever',
            {
                "reply_to": "test.my.queue",
                "correlation_id": ANY
            }
        )

    def test_task_properties(self):
        """Setup task properties

        """
        c = RpcClient()
        c._send_command = MagicMock()
        c.task('whatever', {"data": "x"})
        c._send_command.assert_called_with(
            ANY,
            'whatever'
        )
        # This part shouldn't matter if legacy or not.
        c = RpcClient(legacy=False, client_queue='test.my.queue')
        c._send_command = MagicMock()
        c.task('whatever', {"data": "x"})
        c._send_command.assert_called_with(
            ANY,
            'whatever'
        )
