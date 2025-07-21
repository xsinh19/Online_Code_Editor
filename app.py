from flask import Flask, request, jsonify, render_template
import subprocess
import os

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

def get_file_extension(language):
    extensions = {
        'javascript': '.js',
        'python': '.py',
        'cpp': '.cpp'
    }
    return extensions.get(language, '')

def execute_code_with_language(filename, language):
    if language == 'javascript':
        return subprocess.run(['node', filename], capture_output=True, text=True)
    elif language == 'python':
        return subprocess.run(['python', filename], capture_output=True, text=True)
    elif language == 'cpp':
        executable = filename.replace('.cpp', '')
        subprocess.run(['g++', filename, '-o', executable])
        return subprocess.run(['./' + executable], capture_output=True, text=True)

@app.route('/execute', methods=['POST'])
def execute_code():
    code = request.form['code']
    language = request.form['language']
    filename = 'temp' + get_file_extension(language)
    with open(filename, 'w') as file:
        file.write(code)
    result = execute_code_with_language(filename, language)
    os.remove(filename)
    return jsonify({'output': result.stdout, 'error': result.stderr})

if __name__ == '__main__':
    app.run(debug=True)
