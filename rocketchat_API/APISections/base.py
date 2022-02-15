import re

import requests

from rocketchat_API.APIExceptions.RocketExceptions import (
    RocketAuthenticationException,
    RocketConnectionException,
)


class RocketChatBase:
    API_path = "/api/v1/"

    def __init__(
        self,
        user=None,
        password=None,
        auth_token=None,
        user_id=None,
        server_url="http://127.0.0.1:3000",
        ssl_verify=True,
        proxies=None,
        timeout=30,
        session=None,
        client_certs=None,
    ):
        """Creates a RocketChat object and does login on the specified server"""
        self.headers = {}
        self.server_url = server_url
        self.proxies = proxies
        self.ssl_verify = ssl_verify
        self.cert = client_certs
        self.timeout = timeout
        self.req = session or requests
        if user and password:
            self.login(user, password)  # skipcq: PTC-W1006
        if auth_token and user_id:
            self.headers["X-Auth-Token"] = auth_token
            self.headers["X-User-Id"] = user_id

    @staticmethod
    def __reduce_kwargs(kwargs):
        if "kwargs" in kwargs:
            for arg in kwargs["kwargs"].keys():
                kwargs[arg] = kwargs["kwargs"][arg]

            del kwargs["kwargs"]
        return kwargs

    def call_api_delete(self, method):
        url = self.server_url + self.API_path + method

        return self.req.delete(
            url,
            headers=self.headers,
            verify=self.ssl_verify,
            cert=self.cert,
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def call_api_get(self, method, api_path=None, **kwargs):
        args = self.__reduce_kwargs(kwargs)
        if not api_path:
            api_path = self.API_path
        url = self.server_url + api_path + method
        # convert to key[]=val1&key[]=val2 for args like key=[val1, val2], else key=val
        params = "&".join(
            "&".join(i + "[]=" + j for j in args[i])
            if isinstance(args[i], list)
            else i + "=" + str(args[i])
            for i in args
        )
        return self.req.get(
            "%s?%s" % (url, params),
            headers=self.headers,
            verify=self.ssl_verify,
            cert=self.cert,
            proxies=self.proxies,
            timeout=self.timeout,
        )

    def call_api_post(self, method, files=None, use_json=None, **kwargs):
        reduced_args = self.__reduce_kwargs(kwargs)
        # Since pass is a reserved word in Python it has to be injected on the request dict
        # Some methods use pass (users.register) and others password (users.create)
        if "password" in reduced_args and method != "users.create":
            reduced_args["pass"] = reduced_args["password"]
        if use_json is None:
            # see https://requests.readthedocs.io/en/master/user/quickstart/#more-complicated-post-requests
            # > The json parameter is ignored if either data or files is passed.
            # If files are sent, json should not be used
            use_json = files is None
        if use_json:
            return self.req.post(
                self.server_url + self.API_path + method,
                json=reduced_args,
                files=files,
                headers=self.headers,
                verify=self.ssl_verify,
                cert=self.cert,
                proxies=self.proxies,
                timeout=self.timeout,
            )
        return self.req.post(
            self.server_url + self.API_path + method,
            data=reduced_args,
            files=files,
            headers=self.headers,
            verify=self.ssl_verify,
            cert=self.cert,
            proxies=self.proxies,
            timeout=self.timeout,
        )

    # Authentication

    def login(self, user, password):
        request_data = {"password": password}
        if re.match(
            r"^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
            user,
        ):
            request_data["user"] = user
        else:
            request_data["username"] = user
        login_request = requests.post(
            self.server_url + self.API_path + "login",
            data=request_data,
            verify=self.ssl_verify,
            proxies=self.proxies,
            cert=self.cert,
            timeout=self.timeout,
        )
        if login_request.status_code == 401:
            raise RocketAuthenticationException()

        if (
            login_request.status_code == 200
            and login_request.json().get("status") == "success"
        ):
            self.headers["X-Auth-Token"] = (
                login_request.json().get("data").get("authToken")
            )
            self.headers["X-User-Id"] = login_request.json().get("data").get("userId")
            return login_request

        raise RocketConnectionException()

    def logout(self, **kwargs):
        """Invalidate your REST rocketchat_API authentication token."""
        return self.call_api_post("logout", kwargs=kwargs)
