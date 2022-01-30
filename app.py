from flask import Flask
from flask import request
import compare

app = Flask(__name__)

@app.route('/compare',methods=['POST'])
def compare_pdf():
    file1 = request.files['f1']
    file2 = request.files['f2']
    return compare.compare(file1,file2)

