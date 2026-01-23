#!/usr/bin/env python3
"""
Local OAuth callback server for Life Hub
Handles the OAuth redirect and captures the authorization code
"""

import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import webbrowser
import threading

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback from Google"""

    auth_code = None

    def do_GET(self):
        """Handle the OAuth callback request"""
        # Parse the authorization code from the callback URL
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)

        if 'code' in params:
            # Store the authorization code
            OAuthCallbackHandler.auth_code = params['code'][0]

            # Send success response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            success_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Life Hub - Connected!</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }
                    .container {
                        text-align: center;
                        background: rgba(255,255,255,0.1);
                        padding: 3rem;
                        border-radius: 20px;
                        backdrop-filter: blur(10px);
                    }
                    h1 { font-size: 3rem; margin: 0 0 1rem 0; }
                    p { font-size: 1.2rem; opacity: 0.9; }
                    .checkmark {
                        font-size: 4rem;
                        animation: scaleIn 0.5s ease-out;
                    }
                    @keyframes scaleIn {
                        0% { transform: scale(0); }
                        50% { transform: scale(1.2); }
                        100% { transform: scale(1); }
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="checkmark">✅</div>
                    <h1>Connected!</h1>
                    <p>Your account has been successfully connected to Life Hub.</p>
                    <p>You can close this window and return to your terminal.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(success_html.encode())
        elif 'error' in params:
            # Handle error
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            error_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Life Hub - Error</title>
                <style>
                    body {{
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: #f44336;
                        color: white;
                    }}
                    .container {{
                        text-align: center;
                        background: rgba(0,0,0,0.2);
                        padding: 3rem;
                        border-radius: 20px;
                    }}
                    h1 {{ font-size: 3rem; margin: 0 0 1rem 0; }}
                    p {{ font-size: 1.2rem; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>❌</h1>
                    <h1>Connection Failed</h1>
                    <p>Error: {params['error'][0]}</p>
                    <p>Please return to your terminal and try again.</p>
                </div>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

    def log_message(self, format, *args):
        """Suppress HTTP server logs"""
        pass


def find_free_port():
    """Find a free port on localhost"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


class LocalOAuthServer:
    """Local HTTP server to handle OAuth callbacks"""

    def __init__(self, port=None):
        self.port = port or find_free_port()
        self.server = None
        self.thread = None

    def start(self):
        """Start the OAuth callback server"""
        self.server = HTTPServer(('localhost', self.port), OAuthCallbackHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        return self.port

    def wait_for_code(self, timeout=120):
        """Wait for the authorization code (with timeout)"""
        import time
        start = time.time()

        while OAuthCallbackHandler.auth_code is None:
            if time.time() - start > timeout:
                raise TimeoutError("OAuth flow timed out. Please try again.")
            time.sleep(0.5)

        code = OAuthCallbackHandler.auth_code
        OAuthCallbackHandler.auth_code = None  # Reset for next use
        return code

    def stop(self):
        """Stop the OAuth callback server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
