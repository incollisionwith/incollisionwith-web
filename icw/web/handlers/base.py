import asyncio

from aiohttp.web_exceptions import HTTPMethodNotAllowed

__all__ = ['BaseHandler']


class BaseHandler(object):
    http_methods = {'get', 'post', 'put', 'delete', 'patch', 'options', 'head'}

    @asyncio.coroutine
    def __call__(self, request):
        method = request.method.lower()
        if method not in self.http_methods:
            raise HTTPMethodNotAllowed(method=request.method,
                                       allowed_methods=[m for m in self.http_methods if getattr(self, m, None)])
        try:
            handler = getattr(self, method)
        except AttributeError:
            raise HTTPMethodNotAllowed(method=request.method,
                                       allowed_methods=[m for m in self.http_methods if getattr(self, m, None)])
        return (yield from handler(request))
