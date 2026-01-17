import json


class RocketConnectionException(Exception):
    """Exception raised when a connection to the Rocket.Chat server fails.

    This exception is raised during login when the server returns an unexpected
    response that is neither a successful authentication nor an authentication error.
    """

    pass


class RocketAuthenticationException(Exception):
    """Exception raised when authentication to the Rocket.Chat server fails.

    This exception is raised when login credentials are invalid and the server
    returns a 401 Unauthorized response.
    """

    pass


class RocketMissingParamException(Exception):
    """Exception raised when a required parameter is missing from an API call.

    This exception is raised client-side when a method requires certain parameters
    (e.g., room_id or room_name) but none of the acceptable parameters were provided.
    """

    pass


class RocketUnsuportedIntegrationType(Exception):
    """Exception raised when an unsupported integration type is specified.

    This exception is raised when attempting to create or manage an integration
    with a type that is not supported by the API wrapper.
    """

    pass


class RocketApiException(Exception):
    """Exception raised when the Rocket.Chat API returns an error response (success=false).

    This exception is raised for proper API failures where the server returns
    a valid JSON response indicating the operation failed.

    Attributes:
        status_code: HTTP status code from the response
        response: Raw response text
        response_json: Parsed JSON response (dict)
        error: Error message from the API response
        error_type: Error type from the API response (if available)
    """

    def __init__(self, status_code, response, response_json):
        self.status_code = status_code
        self.response = response
        self.response_json = response_json
        self.error = response_json.get("error", "Unknown error")
        self.error_type = response_json.get("errorType")
        message = f"API error: {self.error}"
        if self.error_type:
            message = f"API error ({self.error_type}): {self.error}"
        super().__init__(message)


class RocketBadStatusCodeException(Exception):
    """Exception raised for HTTP errors that are not proper API error responses.

    This exception is raised for communication failures, such as when a reverse
    proxy returns an error, or when the server returns non-JSON content.

    Attributes:
        status_code: HTTP status code from the response
        response: Raw response text
        response_json: Parsed JSON response if available, None otherwise
    """

    def __init__(self, status_code, response):
        self.status_code = status_code
        self.response = response
        self.response_json = None
        try:
            self.response_json = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            pass
        self.message = (
            f"Wrong status code received: {status_code}. Response: {response}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.status_code} -> {self.message}"
