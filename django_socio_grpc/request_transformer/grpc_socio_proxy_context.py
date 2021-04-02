import json


class SocioProxyHttpRequest:
    HEADERS_KEY = "HEADERS"
    MAP_HEADERS = {"AUTHORIZATION": "HTTP_AUTHORIZATION"}

    def __init__(self, grpc_context):
        grpc_request_metadata = dict(grpc_context.invocation_metadata())
        self.headers = json.loads(grpc_request_metadata.get(self.HEADERS_KEY.lower(), "{}"))
        self.META = {
            self.MAP_HEADERS.get(key.upper()): value for key, value in self.headers.items()
        }
        # INFO - A.D.B - 04/01/2021 - Not implemented for now
        self.GET = {}
        self.POST = {}
        self.COOKIES = {}
        self.FILES = {}


class GRPCSocioProxyContext:
    """Proxy context, provide http1 proxy request object
    and grpc context object"""

    def __init__(self, grpc_context):
        self.grpc_context = grpc_context
        self.proxy_http_request = SocioProxyHttpRequest(self)

    def __getattr__(self, attr):
        try:
            if hasattr(self.grpc_context, attr):
                return getattr(self.grpc_context, attr)
            if hasattr(self.proxy_http_request, attr):
                return getattr(self.proxy_http_request, attr)
        except AttributeError:
            return self.__getattribute__(attr)
