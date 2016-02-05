import asyncio

import aiohttp_jinja2

from icw.web.handlers import BaseHandler


class IndexHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        context = {}
        return aiohttp_jinja2.render_template('index.html', request, context)


class AboutDataHandler(BaseHandler):
    @asyncio.coroutine
    def get(self, request):
        context = {}
        return aiohttp_jinja2.render_template('about-data.html', request, context)
