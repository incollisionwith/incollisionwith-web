import asyncio
from collections import OrderedDict

import aiohttp
import aiohttp.client_exceptions
import aiohttp.web
import aiohttp_jinja2

from icw.web.handlers import BaseHandler


class APIHandler(BaseHandler):
    @asyncio.coroutine
    def get_api_json(self, request, path):
        try:
            accident_url = request.app['api-url'] + path
            response = yield from request.app['api-session'].get(accident_url)
            return (yield from response.json())
        except aiohttp.client_exceptions.ClientOSError as e:
            raise aiohttp.web.HTTPServiceUnavailable
        except aiohttp.client_exceptions.ClientError as e:
            raise aiohttp.web.HTTPError(status=e.status)


class AccidentListHandler(APIHandler):
    def get(self, request):
        context, reference_data = yield from asyncio.gather(
            self.get_api_json(request, 'accident?' + request.query_string),
            self.get_api_json(request, 'reference-data'))
        context.update({
            'severity': request.GET.getall('severity', ()),
            'dateTimeLower': request.GET.get('dateTimeLower', ''),
            'dateTimeUpper': request.GET.get('dateTimeUpper', ''),
            'involvedVehicleType': request.GET.getall('involvedVehicleType', ()),
            'involvedCasualtyType': request.GET.getall('involvedCasualtyType', ()),
            'highwayAuthority': request.GET.get('highwayAuthority'),
            'policeForce': request.GET.get('policeForce'),
            'policeAttended': request.GET.get('policeAttended'),
            'news': request.GET.get('news'),
            'referenceData': reference_data,
        })
        context['referenceData']['HighwayAuthority'] = \
            OrderedDict(i for i in sorted(context['referenceData']['HighwayAuthority'].items(),
                                          key=lambda i: i[1]['label']))
        context['referenceData']['PoliceForce'] = \
            OrderedDict(i for i in sorted(context['referenceData']['PoliceForce'].items(),
                                          key=lambda i: (i[1].get('label') or '')))
        return aiohttp_jinja2.render_template('accident-list.html', request, context)


class AccidentDetailHandler(APIHandler):
    def get(self, request):
        accident_id = request.match_info['accident_id']
        context = yield from self.get_api_json(request, 'accident/' + accident_id)
        return aiohttp_jinja2.render_template('accident.html', request, context)

