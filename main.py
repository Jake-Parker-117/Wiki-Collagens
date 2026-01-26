from flask import Flask, render_template, request, send_from_directory
from Collagens import fastaread, get_cols, label_cols
from waitress import serve
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/Collagens", methods=["POST"])
def collagens():
    #if "fasta_seqs" not in request.files:
        #return "Please upload a file"
    
    
    cols = request.files['fasta_seqs']    
    input_fasta = os.path.join(UPLOAD_DIR, "input.fasta")
    cols.save(input_fasta)
    
    col_txt = os.path.join(OUTPUT_DIR, "col.txt")
    col_html = os.path.join(OUTPUT_DIR, "col_html.html")
    
    fastaread(input_fasta, "flat.fasta")
    get_cols("flat.fasta", col_txt)
    label_cols(col_txt, col_html)
    
    #counting  sequences in origninal fasta file
    with open("flat.fasta") as yfile:
        seq_num = 0
        for yline in yfile:
            if yline.startswith(">"):
                seq_num += 1
    
    #counting  sequences that are over the 27AA length requirement (ie. are in the col.txt file)
    with open(col_txt) as xfile:
        col_num = 0
        for line in xfile:
            if line.startswith(">"):
                col_num += 1
    
    return render_template(
        "collagens.html",
        title="Collagens Found!",
        seqs=seq_num,
        collagen_num=col_num
        )

@app.route("/outputs/<path:filename>")
def outputs(filename):
    return send_from_directory("outputs", filename)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)