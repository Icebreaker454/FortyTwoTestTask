import logging
import json

from apps.personal_info.models import WebRequest

LOGGER = logging.getLogger('personal_info.info')


class RequestLogMiddleware(object):
    """ The middleware that stores all http requests to database  """
    @classmethod
    def process_request(cls, request):
        """
        The middleware overridden method, which is called before
        calling view function
        :param cls: the class instance
        :param request: the request that comes in
        :return: None
        """
        if not request.path.endswith('favicon.ico'):
            # I definitely don't want to spam the db with AJAX update
            # requests, though i can store some of them as normal
            if request.path == '/requests/' and request.is_ajax():
                LOGGER.info("Request object ignored by middleware")
                return None
            else:
                WebRequest(
                    path=request.path,
                    remote_address=request.META.get('REMOTE_ADDR', ''),
                    get=json.dumps(request.GET),
                    post=json.dumps(request.POST),
                    method=request.method
                ).save()
                LOGGER.info("Request object stored by middleware")
