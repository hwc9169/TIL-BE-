def app(environ, start_response):
    response_body = '\n'.join(['{}: {}'.format(k, environ[k]) for k in environ.keys()])
    response_body = response_body.encode()
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(len(response_body)))]

    start_response(status, response_headers)

    return [response_body]

from wsgiref.simple_server import make_server

httpd = make_server('',  8000, app)
httpd.serve_forever()
