from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
LOG_FILE = os.path.join(os.path.dirname(__file__), 'attack_log.txt')
LINES_PER_PAGE = 50

# Load logs phân trang
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logs')
def get_logs():
    try:
        page = int(request.args.get('page', 1))
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()

        total_lines = len(lines)
        total_pages = (total_lines + LINES_PER_PAGE - 1) // LINES_PER_PAGE
        start = (page - 1) * LINES_PER_PAGE
        end = start + LINES_PER_PAGE
        paginated = lines[start:end]

        return jsonify({
            'logs': paginated,
            'total_pages': total_pages,
            'current_page': page
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Realtime fetch logs mới
@app.route('/latest')
def latest_logs():
    try:
        with open(LOG_FILE, 'r') as f:
            lines = f.readlines()
        latest = lines[-10:]  # 10 dòng mới nhất
        return jsonify({'logs': latest})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
