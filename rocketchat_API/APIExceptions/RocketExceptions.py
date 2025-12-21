class RocketConnectionException(Exception):
    pass


class RocketAuthenticationException(Exception):
    pass


class RocketMissingParamException(Exception):
    pass


class RocketUnsuportedIntegrationType(Exception):
    pass


class RocketBadStatusCodeException(Exception):
    def __init__(self, status_code, response):
        self.status_code = status_code
        self.message = (
            f"Wrong status code received: {status_code}. Response: {response}"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.status_code} -> {self.message}"
