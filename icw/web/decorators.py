import asyncio
import urllib


def wraps_api(meth, pattern):
    @asyncio.coroutine
    def f(request):
        url = urllib.urljoin(request.app['api-url'],
                             pattern.format(**request.match_info))
