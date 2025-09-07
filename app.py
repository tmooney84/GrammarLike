from flask import Flask, request, jsonify, send_file, render_template
from celery import Celery
import os

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@celery.task
def process_docx(file_path, out_path):
    #here is where Tony will make the magic happen
    #
    # Get It!
    #
    # chunking to into proofread.sh and append to output file each time
    #      chunking using an nlp-based library to find end of sentence that is close to 400kb and put into
    #           chunk1
    #                                                       chunk1 vvv
    #      llm_string = print(subprocess.run(["echo", chunk1], 
    #               capture_output=True))  
    # 
    #   output_string += llm_string 
    #   f.write(output_string) 
    #read and write placeholder
    with open(file_path, "rb") as f:
        content = f.read()
    with open(output_path, "wb") as f:
        f.write(content)
    return output_path 

@app.route("/")
def index():
    ###may need some work
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    #need to have a unique identifier for the file so maybe file1[UUID].docx
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    ### maybe parse the so instead of file.docx.zip just file.zip
    #timestamp...
    output_path = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}.zip") 
    file.save(file_path)
    task = process_docx.delay(file_path, output_path)
    return jsonify({"task_id": task.id})

@app.route("/status/<task_id>")
def task_status(task_id):
       task = process_docx.AsyncResults(task_id) 
       if task.state == "SUCCESS":
            return jsonify({"status": "done", "download_url": f"/download/{task.id}"})
       return jsonify({"status": task.state})

@app.route("/download/<task_id>")
def download(task_id):
     task = process_docx.AsyncResult(task_id)
     if task.state == "SUCCESS":
          return send_file(task.result, as_attachment=True)
     return "Not ready", 404
###Maybe have this trigger the delete file after the download is finished...

if __name__=="__main__": 
     app.run(host='0.0.0.0', port=3000, debug=True)