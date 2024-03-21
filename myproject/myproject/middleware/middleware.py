import logging

logger = logging.getLogger(__name__)

class ContentTypeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # レスポンスのContent-Typeヘッダーをチェックし、ログに記録
        original_content_type = response.get('Content-Type', None)
        logger.debug(f"Original Content-Type: {original_content_type}")

        if original_content_type is None or 'charset' not in original_content_type:
            content_type = original_content_type.split(';')[0] if original_content_type else 'text/html'
            if content_type.startswith('text/') or content_type in ('application/javascript', 'application/json'):
                response['Content-Type'] = f'{content_type}; charset=utf-8'
                logger.debug(f"Modified Content-Type: {response['Content-Type']}")

        return response

