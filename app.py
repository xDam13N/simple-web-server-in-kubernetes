from http.server import BaseHTTPRequestHandler, HTTPServer
from prometheus_client import start_http_server as start_prometheus_exporter
from prometheus_client import Counter
import os
import time

REQUESTS = Counter('py_hnts_requests_total', 'Total number of requests to this webserver', ['method','status'])

def get_root(self):
  REQUESTS.labels('GET', '200').inc()
  self.send_response(200)
  self.send_header("Content-type", "text/plain")
  self.end_headers()
  hostname = 'Hostname: ' + os.uname()[1] + '\n'
  timestamp = 'Timestamp: ' + str(int(time.time())) + '\n'
  self.wfile.write(hostname.encode())
  self.wfile.write(timestamp.encode())

class HttpGetHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/':
      get_root(self)
    else:
      REQUESTS.labels('GET', '404').inc()
      self.send_response(404)
      self.send_header("Content-type", "text/plain")
      self.end_headers() 
      self.wfile.write("Not found".encode())

if __name__ == "__main__":
  start_prometheus_exporter(8081)
  server = HTTPServer(('', 8080), HttpGetHandler)
  print("Prometheus metrics available on port 8081 /metrics")
  print("HTTP server available on port 8080")
  server.serve_forever()