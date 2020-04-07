# Kyanit (Core) - httpsrv module
# Copyright (C) 2020 Zsolt Nagy
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


# This is a minimal HTTP server module.

# NOTES ON HEADERS
# No headers are taken into account, rather they are passed to callbacks and it's the user's
# responsibility to do something with them.
# Connection: close is always added to response headers.
# Content-type: text/plain is the default content type.

# NOTES ON URLS
# Only the unreserved characters are allowed in the URL, plus the forward slash and the percent
# character for percent-encoding, but only the reserved characters and the space are un-encoded
# after parsing by default.
# Supported percent-encoded symbols can be extended by means of add_symbol(perc_enc, symbol).
# More info on URLs and percent-encoding here: https://en.wikipedia.org/wiki/Percent-encoding
# If the request URL is not all-ASCII, you will get an instant closure of connection with no
# response. (Behavior observed on ESP8266.)

# NOTES ON URL RESOLVING
# Callbacks are assigned to regex rules. Only one such regex rule should match for any given URL,
# otherwise unexpected behavior may occur.

# NOTES ON CONTENT TYPES
# text/plain, text/html and application/json are available as CT_PLAIN, CT_HTML and CT_JSON.
# Others can be returned via the callbacks. No check is done on the returned content type.

# NOTES ON RESPONSE STATUSES
# Only statuses 200 and 500 are supported by default.
# This can be extended, by means of add_status(num, status_str). Ex.: add_status(204, 'No Content')
# No checks are done on the added statuses, it's the user's responsibility that they conform to
# HTTP standards.

# NOTES ON METHODS
# Only GET, POST, PUT, PATCH, DELETE, and OPTIONS is supported, and HEAD is implemented
# automatically. For HEAD, the respective callback for GET will be called, response will be sent
# with the body discarded.
# GET / is implemented by default returning a 200 OK with an 'OK' in the body as JSON.
# This of course can be overriden by another callback.
# OPTIONS is not implemented by default.

# NOTES ON CALLBACKS
# Callbacks can be registered to methods and URLs. URL space is separate per method, which means
# that a URL needs to be registered for every method that's supported on that URL.

"""
# `kyanit.httpsrv` module

This module is a minimal HTTP server implementation.

Here's a simple example in `code.py`, which renders the text `Hello from Kyanit!` on the URL
`<Kyanit IP>/page` (where `<Kyanit IP>` is the IP address of the Kyanit board):

```python
from kyanit import controls, runner, httpsrv

def render_page(method, loc, params, headers, conn, addr):
    return httpsrv.response(200, 'Hello from Kyanit!')

@controls()
def main():
    http_server = httpsrv.HTTPServer(80)
    http_server.register('GET', '^/page$', render_page)
    runner.create_task('httpsrv', http_server.catch_requests)

@controls()
def cleanup(exception):
    pass
```

See the `HTTPServer` class and module function documentations for details on usage.
"""

import sys
import uio
import ure
import ujson
import uerrno
import socket
import uasyncio


_http_ver = 'HTTP/1.1'

_statuses = {
    200: 'OK',
    404: 'Not Found',
    500: 'Internal Server Error',
}

_percent_encodings = {
    '%20': ' ', '%21': '!', '%23': '#', '%24': '$', '%25': '%', '%26': '&', '%27': "'", '%28': '(',
    '%29': ')', '%2A': '*', '%2B': '+', '%2C': ',', '%2F': '/', '%3A': ':', '%3B': ';', '%3D': '=',
    '%3F': '?', '%40': '@', '%5B': '[', '%5D': ']'
}

CT_PLAIN = 'text/plain'
CT_HTML = 'text/html'
CT_JSON = 'application/json'


def add_status(num, status_str):
    """
    By default only `200 OK`, `404 Not Found` and `500 Internal Server Error` HTTP status codes are
    available in `kyanit.httpsrv`.

    You may extend this by adding statuses with this function, where `num` is the status code number
    (int) and `status_str` is the string. Example: `add_status(204, 'No Content')`
    
    You are responsible for making the added statuses compliant to HTTP spec.
    For a list of compliant status codes, see:
    https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html
    """

    global _statuses

    if num not in _statuses:
        _statuses[num] = status_str


def add_symbol(perc_enc, symbol):
    global _percent_encodings

    if perc_enc not in _percent_encodings:
        _percent_encodings[perc_enc] = symbol


def unencode(string):
    if not string:
        return string
    
    new_str = string
    for perc_enc in _percent_encodings:
        new_str = new_str.replace(perc_enc, _percent_encodings[perc_enc])
    return new_str


def response(status, body='', content_type=CT_PLAIN, headers={}):
    return {
        'status': status,
        'body': body,
        'content_type': content_type,
        'headers': headers
    }


def readall_from(source, into=None, timeout=None, chunk_size=64):
    if timeout is not None:
        if isinstance(source, socket.socket):
            source.settimeout(timeout)
        if isinstance(into, socket.socket):
            into.settimeout(timeout)
    
    if into is None:
        into = uio.BytesIO()

    data = b''
    while True:
        try:
            if isinstance(source, socket.socket):
                data = source.recv(chunk_size)
            else:
                data = source.read(chunk_size)
            if data:
                into.write(data)
            else:
                break
        except OSError as exc:
            if exc.args[0] == uerrno.ETIMEDOUT:
                if not data:
                    break  # will break on second timeout event
                data = b''
            else:
                raise exc
    
    return into


def send_response(conn, status, body='', content_type=CT_PLAIN, headers={}):
    # discard rest of request
    conn.settimeout(.5)
    while True:
        try:
            if not conn.recv(64):
                break
        except OSError:
            break
    
    response = ('{0} {1} {2}\r\nContent-type: {3}\r\nConnection: close\r\n{4}\r\n{5}'
                .format(_http_ver,
                        status,
                        _statuses[status],
                        content_type,
                        '\r\n'.join(['{}: {}'.format(key, headers[key]) for key in headers] + ['']),
                        body))

    conn.write(response.encode())  # noqa


def error_view(exc):
    exc_details = uio.StringIO()
    sys.print_exception(exc, exc_details)

    if isinstance(exc, OSError):
        exc_msg = uerrno.errorcode[exc.args[0]] \
                  if len(exc.args) > 0 and exc.args[0] in uerrno.errorcode else ''  # noqa
    else:
        exc_msg = exc.args[0] if len(exc.args) > 0 else ''
    
    return response(500, ujson.dumps(
        {
            'error': '{}: {}'.format(exc.__class__.__name__, exc_msg),
            'traceback': [line.strip() for line in exc_details.getvalue().split('\n')
                          if line and 'Traceback' not in line
                          and exc.__class__.__name__ not in line]  # noqa
        }), CT_JSON)


class NoMethodError(Exception):
    pass


class NoCallbackError(Exception):
    pass


class URLInvalidError(Exception):
    pass


class HTTPServer:
    def __init__(self, port):
        self._sock = socket.socket()
        self._sock.bind(socket.getaddrinfo('0.0.0.0', port)[0][-1])
        self._sock.setblocking(False)
        self._sock.listen(1)
        self._timeout = 1  # seconds
        self._callbacks = {
            'GET': {
                '^/$': lambda method, loc, params, headers, conn, addr: (200, '"OK"', CT_JSON)
            }
        }
    
    def close(self):
        self._sock.close()

    def set_timeout(self, timeout):
        self._timeout = timeout

    def register(self, method, location_re, callback):
        if method not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']:
            raise ValueError('method invalid')

        if method in self._callbacks:
            self._callbacks[method][location_re] = callback
        else:
            self._callbacks[method] = {location_re: callback}

    def deregister(self, method, location_re):
        del(self._callbacks[method][location_re])

    def get_registered(self):
        return self._callbacks

    async def processor(self, conn, addr):
        request_line = conn.readline().decode()

        header_lines = []
        while True:
            header_line = conn.readline()
            if header_line == b'\r\n':
                break
            header_lines.append(header_line.decode())

        match = ure.search(
            '([A-Z]+) ((\/[{0}]*)+)\??([{0}|\=|\&]+)? HTTP'.format('a-z|A-Z|0-9|\.|\%|\-|\_|\~'),
            request_line)  # noqa
        
        if not match:
            raise URLInvalidError

        method = match.group(1)
        location = unencode(match.group(2))
        
        # extract query parameters
        params_str = match.group(4)

        if params_str:
            params = {unencode(key): unencode(value) for (key, value) in
                      [(param.split('=')[0], param.split('=')[1]) if '=' in param else (param, None)
                      for param in params_str.split('&')]}
        else:
            params = {}
        
        # extract headers
        if header_lines:
            headers = {key: value for (key, value) in
                       [(line.split(':')[0].strip(), line.split(':')[1].strip())
                        for line in header_lines]}
        else:
            headers = {}
        
        get_head = False
        if method == 'HEAD':
            method = 'GET'
            get_head = True
        
        if method in self._callbacks:
            for location_re in self._callbacks[method]:
                if ure.search(location_re, location) is not None:
                    resp = self._callbacks[method][location_re](
                        method, location, params, headers, conn, addr)
                    if get_head:
                        resp['body'] = ''
                    if resp is not None:
                        send_response(conn, **resp)
                    return
            raise NoCallbackError
        
        else:
            raise NoMethodError

    async def catch_requests(self):
        while True:
            try:
                conn, addr = self._sock.accept()
            
            except OSError:
                # no incomming connections
                await uasyncio.sleep(0)
            
            else:
                conn.settimeout(self._timeout)
                try:
                    await self.processor(conn, addr)
                except Exception as exc:
                    resp = error_view(exc)
                    if resp is not None:
                        send_response(conn, **resp)
                    else:
                        send_response(conn, 500)
                conn.close()
