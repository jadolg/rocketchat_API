from unittest.mock import Mock, patch

import pytest
import requests

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketApiException,
    RocketBadStatusCodeException,
    RocketConnectionException,
)
from rocketchat_API.rocketchat import RocketChat


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


def test_bad_status_code_exception_str():
    """Test the __str__ method of RocketBadStatusCodeException"""
    exception = RocketBadStatusCodeException(502, "<html>Bad Gateway</html>")
    str_repr = str(exception)
    assert "502" in str_repr
    assert "Bad Gateway" in str_repr


def test_bad_status_code_exception_json_response():
    """Test RocketBadStatusCodeException when response is valid JSON"""
    exception = RocketBadStatusCodeException(400, '{"error": "Bad request"}')
    assert exception.response_json == {"error": "Bad request"}


def test_api_exception_raised_on_error_response(logged_rocket):
    """Test that RocketApiException is raised when API returns success=False"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = (
        '{"success": false, "error": "Invalid room", "errorType": "error-invalid-room"}'
    )
    mock_response.json.return_value = {
        "success": False,
        "error": "Invalid room",
        "errorType": "error-invalid-room",
    }

    with patch.object(logged_rocket.session, "get", return_value=mock_response):
        with pytest.raises(RocketApiException) as exc_info:
            logged_rocket.channels_info(room_id="INVALID_ROOM_ID")

        assert exc_info.value.status_code == 400
        assert exc_info.value.error == "Invalid room"
        assert exc_info.value.error_type == "error-invalid-room"


def test_api_exception_without_error_type(logged_rocket):
    """Test RocketApiException when errorType is not provided"""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.text = '{"success": false, "error": "Something went wrong"}'
    mock_response.json.return_value = {
        "success": False,
        "error": "Something went wrong",
    }

    with patch.object(logged_rocket.session, "get", return_value=mock_response):
        with pytest.raises(RocketApiException) as exc_info:
            logged_rocket.channels_info(room_id="INVALID_ROOM_ID")

        assert exc_info.value.error_type is None
        assert "Something went wrong" in str(exc_info.value)


def test_bad_status_code_with_json_but_no_success_false(logged_rocket):
    """Test error response with valid JSON but without success=False field"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = '{"message": "Internal server error"}'
    mock_response.json.return_value = {"message": "Internal server error"}

    with patch.object(logged_rocket.session, "get", return_value=mock_response):
        with pytest.raises(RocketBadStatusCodeException) as exc_info:
            logged_rocket.channels_info(room_id="GENERAL")

        assert exc_info.value.status_code == 500


def test_bad_status_code_with_non_dict_json_response(logged_rocket):
    """Test error response with valid JSON that is not a dict (e.g., array or string)"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = '["error1", "error2"]'
    mock_response.json.return_value = ["error1", "error2"]

    with patch.object(logged_rocket.session, "get", return_value=mock_response):
        with pytest.raises(RocketBadStatusCodeException) as exc_info:
            logged_rocket.channels_info(room_id="GENERAL")

        assert exc_info.value.status_code == 500


def test_connection_exception_on_unexpected_login_response():
    """Test that RocketConnectionException is raised when login gets unexpected response"""
    mock_session = Mock()
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": "unexpected"}
    mock_session.post.return_value = mock_response

    with pytest.raises(RocketConnectionException):
        RocketChat(user="test", password="test", session=mock_session)


def test_call_api_put_with_files(logged_rocket):
    """Test call_api_put when files parameter is passed (use_json=False branch)"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}

    with patch.object(
        logged_rocket.session, "put", return_value=mock_response
    ) as mock_put:
        logged_rocket.call_api_put(
            "test.endpoint", files={"file": ("test.txt", b"content")}, key="value"
        )
        # Verify that data parameter is used instead of json when files are passed
        mock_put.assert_called_once()
        call_kwargs = mock_put.call_args[1]
        assert "data" in call_kwargs
        assert "json" not in call_kwargs or call_kwargs["json"] is None
        assert call_kwargs["files"] == {"file": ("test.txt", b"content")}


def test_call_api_put_with_use_json_false(logged_rocket):
    """Test call_api_put when use_json is explicitly set to False"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True}

    with patch.object(
        logged_rocket.session, "put", return_value=mock_response
    ) as mock_put:
        logged_rocket.call_api_put("test.endpoint", use_json=False, key="value")
        # Verify that data parameter is used instead of json
        mock_put.assert_called_once()
        call_kwargs = mock_put.call_args[1]
        assert "data" in call_kwargs
        assert "json" not in call_kwargs or call_kwargs["json"] is None
