from unittest.mock import Mock, patch

import pytest
import requests

from rocketchat_API.APIExceptions.RocketExceptions import RocketBadStatusCodeException


def test_bad_status_code_exception(logged_rocket):
    """Test that RocketBadStatusCodeException is raised for non-JSON error responses"""
    mock_response = Mock()
    mock_response.status_code = 502
    mock_response.text = "<html>Bad Gateway</html>"
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("", "", 0)

    with patch.object(logged_rocket.session, "get", return_value=mock_response):
        with pytest.raises(RocketBadStatusCodeException) as exc_info:
            logged_rocket.channels_info(room_id="GENERAL")

        assert exc_info.value.status_code == 502
        assert "<html>Bad Gateway</html>" in exc_info.value.response
