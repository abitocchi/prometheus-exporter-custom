from prometheus_client import start_http_server, Counter
from flask import Flask

PROM_ACADEMY_COUNTER = Counter(
    'prom_academy_exporter_counter',
    'Counter for /academy requests'
)

app = Flask(__name__)

@app.route('/academy', methods=['GET'])
def academy():
    PROM_ACADEMY_COUNTER.inc()
    return "Academy counter incremented!\n"

if __name__ == "__main__":
    start_http_server(8000)

    app.run(host='0.0.0.0', port=8080)
