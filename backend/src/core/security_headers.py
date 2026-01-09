from fastapi import FastAPI
from typing import Dict, Any

def add_security_headers(app: FastAPI):
    """
    Add security headers to the FastAPI application
    """
    # Add security headers via middleware
    @app.middleware("http")
    async def add_security_headers_middleware(request, call_next):
        response = await call_next(request)

        # Strict Transport Security
        response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'

        # X-Content-Type-Options
        response.headers['X-Content-Type-Options'] = 'nosniff'

        # X-Frame-Options
        response.headers['X-Frame-Options'] = 'DENY'

        # X-XSS-Protection
        response.headers['X-XSS-Protection'] = '1; mode=block'

        # Referrer Policy
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

        # Permissions Policy
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

        return response

# Alternative implementation using a SecurityHeadersMiddleware class
class SecurityHeadersMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        async def send_wrapper(message):
            if message['type'] == 'http.response.start':
                # Add security headers to the response
                headers = []
                for key, value in message.get('headers', []):
                    headers.append((key, value))

                # Add security headers
                headers.extend([
                    (b'strict-transport-security', b'max-age=63072000; includeSubDomains; preload'),
                    (b'x-content-type-options', b'nosniff'),
                    (b'x-frame-options', b'DENY'),
                    (b'x-xss-protection', b'1; mode=block'),
                    (b'referrer-policy', b'strict-origin-when-cross-origin'),
                    (b'permissions-policy', b'geolocation=(), microphone=(), camera=()'),
                ])

                message['headers'] = headers

            await send(message)

        await self.app(scope, receive, send_wrapper)