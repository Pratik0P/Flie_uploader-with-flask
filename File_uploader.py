from flask import Flask, request, render_template_string
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload a File</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f7fa;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #fff;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 500px;
        }
        h1 {
            text-align: center;
            font-size: 2rem;
            color: #333;
        }
        input[type="file"] {
            display: block;
            margin: 20px auto;
            padding: 10px;
            font-size: 1rem;
            background-color: #f1f1f1;
            border: 2px solid #ccc;
            border-radius: 5px;
            width: 100%;
            cursor: pointer;
        }
        input[type="submit"] {
            display: block;
            width: 100%;
            padding: 12px;
            font-size: 1.1rem;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
        }
        input[type="submit"]:hover {
            background-color: #45a049;
        }
        .message {
            text-align: center;
            font-size: 1.2rem;
            color: #333;
            margin-top: 20px;
        }
        .error {
            color: #e74c3c;
        }
        .success {
            color: #2ecc71;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Upload Your File</h1>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file">  <!-- File selection -->
            <input type="submit" value="Upload File">  <!-- Button to upload -->
        </form>
        <div class="message">
            {% if message %}
                <p class="{{ message_class }}">{{ message }}</p>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_FORM)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return render_template_string(HTML_FORM, message="No file selected", message_class="error"), 400

    file = request.files['file']
    
    if file.filename == '':
        return render_template_string(HTML_FORM, message="No file selected", message_class="error"), 400

    
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  
    file.save(file_path)

    return render_template_string(HTML_FORM, message=f"File uploaded successfully: {file.filename}", message_class="success")

if __name__ == '__main__':
    app.run(debug=True)
