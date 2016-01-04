import asyncio

import aiohttp
import aiohttp.web
import aiohttp_jinja2

from icw.web.handlers import BaseHandler


class APIHandler(BaseHandler):
    @asyncio.coroutine
    def get_api_json(self, request, path):
        try:
            accident_url = request.app['api-url'] + path
            response = yield from request.app['api-session'].get(accident_url + '?' + request.query_string)
            return (yield from response.json())
        except aiohttp.errors.ClientError as e:
            raise aiohttp.web.HTTPError(status=e.status)


class AccidentListHandler(APIHandler):
    def get(self, request):
        context = yield from self.get_api_json(request, 'accident')
        return aiohttp_jinja2.render_template('accident-list.html', request, context)


class AccidentDetailHandler(APIHandler):
    def get(self, request):
        accident_id = request.match_info['accident_id']
        context = yield from self.get_api_json(request, 'accident/' + accident_id)
        return aiohttp_jinja2.render_template('accident.html', request, context)

