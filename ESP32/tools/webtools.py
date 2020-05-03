"""
.. module:: tools.webtools
   :platform: Unix, Windows
   :synopsis: Connective tools for external communication over the web.

.. moduleauthor:: Pablo Crotti <pablo.crotti@outlook.com>

"""

import json

from var.static import SERVER_URL, DEVICE_DATA
import usocket
#import signal

# request and get functions taken from: https://github.com/micropython/micropython-lib/blob/master/urequests/urequests.py
# The request function needed to be fixed (closed the socket at the end of the request) to avoid overloading the
# socket when using the request function in a loop.
# Being import github urequests functions:


def request(method, url, data=None, json=None, headers={}):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json is not None:
            assert data is None
            import ujson
            data = ujson.dumps(json)
            s.write(b"Content-Type: application/json\r\n")
        if data:
            s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"\r\n")
        if data:
            s.write(data)

        l = s.readline()
        # print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            # print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except OSError:
        s.close()
        raise
    s.close()
    # resp = Response(s)
    # resp.status_code = status
    # resp.reason = reason
    # return resp


def get(url, **kw):
    return request("GET", url, **kw)


# End import.


class TimeoutException(Exception):
    def __init__(self, signum):
        self.signum = 'Signal handler called with signal: {}'.format(signum)

    def __str__(self):
        return repr(self.signum)


def timeout(s):
    """ Time out decorator. The decorator prevents a function to exceed s seconds in runtime.
    """
    def handler(signum, frame):
        raise TimeoutException(signum)
    # Beginning of the wrapper.

    def wrapper(f):
        def outer_func(*args, **kwargs):
            # Set the signal to execute the handler in case the alarm is triggered.
            signal.signal(signal.SIGALRM, handler)
            # Set the timer on the alarm for s seconds.
            signal.alarm(s)
            try:
                # Execute the outer function.
                outerfunc_output = f(*args, **kwargs)
            finally:
                # Reset the alarm to 0 (i.e., cancel the alarm).
                signal.alarm(0)
            # Return the outer function output to the system.
            return outerfunc_output
        # Return the outer function.
        return outer_func
    return wrapper


# Signal library not working at the moment. @timeout(60)
def post_data(input_data):
    """ Send the input_data to the API server via a GET method.

    :param input_data: Dictionary with the data needed to be sent to the API server.
    :type input_data: Dictionary
    """
    # Update the DEVICE_DATA dictionary with the input_data.
    DEVICE_DATA.update(input_data)
    get(SERVER_URL, data=json.dumps(DEVICE_DATA))
