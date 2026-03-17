from flask import Flask, request, send_file
from generate_pdf import build_pdf
import tempfile, os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        path = f.name
    build_pdf(path, data)
    return send_file(path, mimetype='application/pdf',
                     as_attachment=True,
                     download_name='audit.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
