# routing

from flask import request, jsonify
from app import app
from app import mongo
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from bson import Binary
import re

@app.route('/', methods =['POST'])
def master_login():
    if request.method in 'POST':
        login_email = request.json.get("Email")
        login_password = request.json.get("Password")

        response_login = Login.authenticate(login_email, login_password)
        return response_login



def process_url(topic):
    # Convert the sentence to lowercase
    sentence = topic.lower()
    
    # Remove special characters using regex
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    
    # Replace spaces between words with dashes
    sentence = sentence.replace(' ', '-')
    
    return sentence



@app.route('/webinar_panel', methods = ['GET'])
def webinar_panel():
    
    webinar_list = Webinar.view_webinar()
    if request.method in 'GET':
        webinar_data = []
        for webinar in webinar_list:
            webinar_dict ={
        
        "id":webinar["id"],

        "topic":webinar["topic"],
        "industry":webinar["industry"],
        "speaker":webinar["speaker"],
        "date":webinar["date"],
        "time":webinar["time"],
        "timeZone":webinar["timeZone"],
        "duration":webinar["duration"],
        "category":webinar["category"],
        
        "sessionLive":webinar["sessionLive"],
        "priceLive":webinar["priceLive"],
        "urlLive":webinar["urlLive"],
        
        "sessionRecording":webinar["sessionRecording"],
        "priceRecording":webinar["priceRecording"],
        "urlRecording":webinar["urlRecording"],

        "sessionDigitalDownload":webinar["sessionDigitalDownload"],
        "priceDigitalDownload":webinar["priceDigitalDownload"],
        "urlDigitalDownload":webinar["urlDigitalDownload"],
        
        "sessionTranscript":webinar["sessionTranscript"],
        "priceTranscript":webinar["priceTranscript"],
        "urlTranscript":webinar["urlTranscript"],

        "status":webinar["status"],
        "webinar_url": webinar["webinar_url"],
        "description":webinar["description"],
            
            }
            
            webinar_data.append(webinar_dict)
        return jsonify(webinar_data)
    
    

@app.route('/webinar_panel/create_webinar', methods= ['POST'])
def create_webinar():
    
    id = len(list(mongo.db.webinar_data.find({}))) + 1
    if request.method in ['POST']:
        
        webinar_data ={
        
        "id": id,
        
        "topic":request.json.get("topic"),
        "industry":request.json.get("industry"),
        "speaker":request.json.get("speaker"),
        "date":request.json.get("date"),
        "time":request.json.get("time"),
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":"Active",
        "webinar_url": process_url(request.json.get("topic")),
        "description":request.json.get("description"),
        }
        response_create_webinar = Webinar.create_webinar(webinar_data)
    return response_create_webinar
    


@app.route('/webinar_panel/<int:w_id>', methods= ['GET','PUT','PATCH','DELETE'])
def update_webinar_panel(w_id):    
    # w_id = request.json.get("w_id")
    
    webinar_data = Webinar.data_webinar(w_id)
    webinar = webinar_data[0]
    if request.method in ['GET']:
        
        if webinar:    
            webinar_data_dict ={
            
            "id":webinar ["id"],

        "topic":webinar ["topic"],
        "industry":webinar ["industry"],
        "speaker":webinar ["speaker"],
        "date":webinar ["date"],
        "time":webinar ["time"],
        "timeZone":webinar["timeZone"],
        "duration":webinar["duration"],
        "category":webinar["category"],
        
        "sessionLive":webinar ["sessionLive"],
        "priceLive":webinar ["priceLive"],
        "urlLive":webinar ["urlLive"],
        
        "sessionRecording":webinar ["sessionRecording"],
        "priceRecording":webinar ["priceRecording"],
        "urlRecording":webinar ["urlRecording"],

        "sessionDigitalDownload":webinar ["sessionDigitalDownload"],
        "priceDigitalDownload":webinar ["priceDigitalDownload"],
        "urlDigitalDownload":webinar ["urlDigitalDownload"],
        
        "sessionTranscript":webinar ["sessionTranscript"],
        "priceTranscript":webinar ["priceTranscript"],
        "urlTranscript":webinar ["urlTranscript"],

        "status":webinar ["status"],
        "webinar_url": webinar ["webinar_url"],
        "description":webinar ["description"],

        }
            return webinar_data_dict,200
        else:
            return {"success":False, "message":"failed to retrieve webinar info"}

    elif request.method in ['PATCH']:
        
        webinar_status = request.json.get("status")
        
        if webinar_status:
            
            return Webinar.edit_webinar(w_id, webinar_status)
        
        else:
            return jsonify({"Error": "No data found"}),400
        
    elif request.method in ['PUT']:
        
        
        webinar_data = {
        "id":w_id ,
        
        "topic":request.json.get("topic"),
        "industry":request.json.get("industry"),
        "speaker":request.json.get("speaker"),
        "date":request.json.get("date"),
        "time":request.json.get("time"),
        "timeZone":request.json.get("timeZone"),
        "duration":request.json.get("duration"),
        "category":request.json.get("category"),
        
        "sessionLive":request.json.get("sessionLive"),
        "priceLive":request.json.get("priceLive"),
        "urlLive":request.json.get("urlLive"),
        
        "sessionRecording":request.json.get("sessionRecording"),
        "priceRecording":request.json.get("priceRecording"),
        "urlRecording":request.json.get("urlRecording"),

        "sessionDigitalDownload":request.json.get("sessionDigitalDownload"),
        "priceDigitalDownload":request.json.get("priceDigitalDownload"),
        "urlDigitalDownload":request.json.get("urlDigitalDownload"),
        
        "sessionTranscript":request.json.get("sessionTranscript"),
        "priceTranscript":request.json.get("priceTranscript"),
        "urlTranscript":request.json.get("urlTranscript"),

        "status":request.json.get("status"),
        "webinar_url": process_url(request.json.get("topic")),
        "description":request.json.get("description"),
        }
        if webinar_data:
            return Webinar.update_webinar(w_id, webinar_data)
        
        else:
            return jsonify({"Error": "No data found"}),400
        
    elif request.method in ['DELETE']:
         
        return Webinar.delete_webinar(w_id)
    

@app.route('/speaker_panel', methods = ['GET'])
def speaker_panel():
    
    speaker_list = Speaker.view_speaker()
    if request.method in 'GET':
        speaker_data = []
        for speaker in speaker_list:
            speaker_dict ={

            "id":speaker["id"],
            "email":speaker["email"],
            "industry":speaker["industry"],
            "status":speaker["status"],
            "bio":speaker["bio"],
            "photo":speaker["photo"]
            }
            speaker_data.append(speaker_dict)
        return jsonify(speaker_data)
    

@app.route('/speaker_panel/create_speaker', methods = ['POST'])
def create_speaker():
    id = len(list(mongo.db.speaker_dta.find({}))) +1

    if request.method in 'POST':
        # photo_file = request.files.get("photo")
        # if photo_file:

        #     photo_data = photo_file.read()
        #     photo = Binary(photo_data)
        speaker_data ={
            "id": id,
            "email": request.form.get("email"),
            "industry": request.form.get("industry"),
            "status":"Active",
            "bio": request.form.get("bio"),
            "photo":request.form.get("photo"),
            "history": None

        }
        response_create_speaker = Speaker.create_speaker(speaker_data)
        return response_create_speaker
    

@app.route('/speaker_panel/<int:s_id>', methods =['GET','PUT', 'PATCH', 'DELETE'])
def update_speaker_panel(s_id):
    
    speaker_data = Speaker.data_speaker(s_id)
    speaker = speaker_data[0]
    history = []
    
    if request.method in 'GET':
        if speaker:
            history = speaker['history']
            speaker_dict={
                "id": speaker["id"],
                "name": speaker["name"],
                "industry": speaker["industry"],
                "status": speaker["status"],
                "bio": speaker["bio"],
                "photo": speaker["photo"],
                "history": history

            }
            return speaker_dict, 200
        else:
            return {"success":False, "message": "failed to retrieve speaker info"}
        
    elif request.method in "PATCH":

        speaker_status = request.json.get("status")
        
        if speaker_data:
            return Speaker.edit_speaker(s_id, speaker_status)
        
        else:
            return jsonify({"Error": "No data found"}), 400
    
    elif request.method in 'PUT':

        speaker_dict = {
            "id": s_id,
            "name": speaker["name"],
            "industry": speaker["industry"],
            "status": speaker["status"],
            "bio": speaker["bio"],
            "photo": speaker["photo"],
            "history": history
        }

        if speaker_dict:
            return Speaker.update_speaker(s_id, speaker_dict)
        
        else:
            return jsonify({"Error": "No data found"}),400
        
    elif request.method in 'DELETE':

        return Speaker.delete_speaker(s_id)
