from flask import Flask, request, jsonify
from flask import render_template_string
import compare_semantics as cs

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare_endpoint():
    data = request.get_json()
    str1 = data.get('str1', '')
    str2 = data.get('str2', '')
    if not str1 or not str2:
        return jsonify({'error': 'Both str1 and str2 are required'}), 400
    result = cs.compare_semantics(str1, str2)
    if result is not None:
        return jsonify({'similarity': float(round(result * 100, 2))})
    else:
        return jsonify({'error': 'Failed to compute similarity'}), 500

# New route for the GUI
@app.route('/')
def index():
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Semantic Similarity Checker</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            textarea { padding: 10px; margin: 5px; width: 100%; max-width: 500px; resize: vertical; }
            #result { margin-top: 20px; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>Semantic Similarity Checker</h1>
        <p>Enter two strings to compute their semantic similarity.</p>
        <textarea id="str1" placeholder="First string" rows="4" cols="50" required></textarea>
        <br>
        <textarea id="str2" placeholder="Second string" rows="4" cols="50" required></textarea>
        <br>
        <button onclick="compareStrings()">Compare</button>
        <div id="result"></div>
        
        <script>
            async function compareStrings() {
                const str1 = document.getElementById('str1').value;
                const str2 = document.getElementById('str2').value;
                if (!str1 || !str2) {
                    document.getElementById('result').innerText = 'Please enter both strings.';
                    return;
                }
                try {
                    const response = await fetch('/compare', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ str1, str2 })
                    });
                    const data = await response.json();
                    if (response.ok) {
                        document.getElementById('result').innerText = `Similarity: ${data.similarity}%`;
                    } else {
                        document.getElementById('result').innerText = `Error: ${data.error}`;
                    }
                } catch (error) {
                    document.getElementById('result').innerText = 'Error: Unable to connect to server.';
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    # Print model info on startup
    print(f"Model name: {cs.model_name}")
    print(f"Model device: {cs.model.device}")
    # Run the Flask app
    app.run(host="0.0.0.0", port=8432, debug=False) #, ssl_context=('cert.pem', 'key.pem'))
