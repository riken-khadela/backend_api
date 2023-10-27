from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/get_response', methods=['GET'])
def get_response():
    response = {'message': 'Hello, this is a simple API response!'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
