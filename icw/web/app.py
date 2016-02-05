import asyncio
import os

import aiohttp
import aiohttp.web
import aiohttp_jinja2
from aiohttp_utils import negotiation
import jinja2

from . import handlers


def get_app():
    app = aiohttp.web.Application()

    app['api-url'] = os.environ['ICW_API']
    app['google-analytics-tracking-id'] = os.environ.get('GOOGLE_ANALYTICS_TRACKING_ID')
    app['api-session'] = aiohttp.ClientSession()
    app['static-url'] = '/static/'

    app.router.add_route('*', '/',
                         handlers.IndexHandler())
    app.router.add_route('*', '/incident',
                         handlers.AccidentListHandler())
    app.router.add_route('*', '/incident/{accident_id}',
                         handlers.AccidentDetailHandler())
    app.router.add_route('*', '/about-data',
                         handlers.AboutDataHandler())

    app.router.add_static(app['static-url'],
                          os.path.join(os.path.dirname(__file__), 'static'))

    negotiation.setup(app)
    aiohttp_jinja2.setup(app,
                         loader=jinja2.PackageLoader('icw.web', 'templates'),
                         context_processors=[asyncio.coroutine(lambda request: {
                             'static_url': app['static-url'],
                             'api_url': app['api-url'],
                             'google_analytics_tracking_id': app['google-analytics-tracking-id']
                         })])

    return app
