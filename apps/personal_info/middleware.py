import logging

from apps.personal_info.models import WebRequest

LOGGER = logging.getLogger('personal_info')


class RequestLogMiddleware:
    """ The middleware that stores all http requests to database """
    def process_request(self, request):
        """
        The middleware overridden method, which is called before
        calling view function
        :param request: the request that comes in
        :return: None
        """
        pass