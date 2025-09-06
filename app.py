from flask import Flask, request, jsonify, send_file
from celery import Celery
import os

app = Flask(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhosrt:6379/0'
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
    #read and write placehoder
    with open(file_path, "rb") as f:
        content = f.read()
    with open(output_path, "wb") as f:
        f.write(content)
    return output_path ### 'here is our zip file'

@app.route("/")
def index():
    ###may need some work
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    ### maybe parse the so instead of file.docx.zip just file.zip
    output_path = os.path.join(PROCESSED_FOLDER, f"processed_{file.filename}") 
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