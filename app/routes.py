# routing

from flask import request, jsonify, send_file
from app import app
from app import mongo
from app.model_login import Login
from app.model_webinar import Webinar
from app.model_speaker import Speaker
from app.model_order import Order
from bson import Binary
import re
import io
import base64
from PIL import Image

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
    speaker_list = Speaker.view_speaker()
    
    # Speaker name list for drop down menu
    speaker_namedata = []
    
    # Webinar list for display
    webinar_data = []
        
    if request.method in 'GET':
        for speaker in speaker_list:
            speaker_namedata.append(speaker["name"])
        
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
        return jsonify(webinar_data, speaker_namedata)
    
    

@app.route('/webinar_panel/create_webinar', methods= ['POST'])
def create_webinar():
    
    id = len(list(mongo.db.webinar_data.find({}))) + 1
    if request.method in ['POST']:
        webinar_topic = request.json.get("topic")
        speaker = request.json.get("speaker")
        
        webinar_data ={
        
        "id": id,
        
        "topic":webinar_topic,
        "speaker":speaker,
        "industry":request.json.get("industry"),
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
        respone_history_speaker = Speaker.update_history(speaker,webinar_topic)

    return response_create_webinar, respone_history_speaker
    


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
            "name":speaker["name"],
            "email":speaker["email"],
            "industry":speaker["industry"],
            "status":speaker["status"],
            "bio":speaker["bio"],
            }
            speaker_data.append(speaker_dict)
        return jsonify(speaker_data)
    

@app.route('/speaker_panel/create_speaker', methods = ['POST'])
def create_speaker():
    speaker_list = Speaker.view_speaker()
    id = len(speaker_list) +1
    image = None
    
    if request.method in 'POST':
        image_file = request.files.get("photo")
        if image_file:
            image_data = image_file.read()
            image = base64.b64encode(image_data)

        speaker_data ={
            "id": id,
            "name" :request.form.get("name"),
            "email": request.form.get("email"),
            "industry": request.form.get("industry"),
            "contact" : request.form.get("contact"),
            "status":"Active",
            "bio": request.form.get("bio"),
            "history": [],
            "photo":image

        }
        
        response_create_speaker = Speaker.create_speaker(speaker_data)
        return response_create_speaker
    


@app.route('/speaker_panel/<int:s_id>', methods =['GET','PUT', 'PATCH', 'DELETE'])
def update_speaker_panel(s_id):
    
    speaker_data = Speaker.data_speaker(s_id)
    speaker = speaker_data[0]
    image = None
    image_data = speaker.get("photo")
    if image_data:
        binary_data = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(binary_data))

    if request.method in 'GET':
        if speaker:
            history = speaker.get('history')
            
            speaker_dict={
                "id": speaker ["id"],
                "name": speaker ["name"],
                "email":speaker ["email"],
                "industry": speaker ["industry"],
                "status": speaker ["status"],
                "bio": speaker ["bio"],
                "contact" :speaker ["contact"],
                "history": history
            }
            # Convert the bytes into a PIL image
            if image:
                # speaker_dict["photo"] = process_image_data
                # process_image_data = process_image(image_binary)
                # image.show()
                return send_file(image, mimetype='image/jpeg'), speaker_dict
                # return (speaker_dict)
            else:
                return speaker_dict        
    
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
            "photo":binary_data,
            "history": history
        }

        if speaker_dict:
            return Speaker.update_speaker(s_id, speaker_dict)
        
        else:
            return jsonify({"Error": "No data found"}),400
        
    elif request.method in 'DELETE':

        return Speaker.delete_speaker(s_id)


@app.route('/order_panel', methods =['GET'])
def order_panel():
    
    orderlist = Order.view_order()
    if request.method in 'GET':
        order_data = []
        for order in orderlist:
            
            order_dict = {
                "id": order ["id"],
                "orderdate": order["orderdate"],
                "webinardate": order["webinardate"],
                "topic": order["topic"],
                "session": order["sessiion"],
                "customername": order["customername"],
                "customeremail": order["customeremail"],
                "billingemail": order["billingemail"],
                "orderamount": order["amount"],
                "paymentstatus": order["paymentstatus"],
                "country" : order["country"],
                "state" : order["state"],
                "city" : order["city"],
                "zipcode" : order["zipcode"],
                "address": order["address"]

            }

            order_data.append(order_dict)
        return jsonify(order_data), 200

@app.route('/order_panel/<int:o_id>', methods = ['GET'])
def order_detail(o_id):
    
    order_data = Order.order_data(o_id)
    order = order_data[0]
    
    if request.method in 'GET':
        if order:
           
            order_dict = {
                "id": order ["id"],
                "orderdate": order["orderdate"],
                "webinardate": order["webinardate"],
                "topic": order["topic"],
                "session": order["sessiion"],
                "customername": order["customername"],
                "customeremail": order["customeremail"],
                "billingemail": order["billingemail"],
                "orderamount": order["amount"],
                "paymentstatus": order["paymentstatus"],
                "country" : order["country"],
                "state" : order["state"],
                "city" : order["city"],
                "zipcode" : order["zipcode"],
                "address": order["address"]

            }


            document = order["document"]
            if document:
                pdf_content_b64 = base64.b64encode(document).decode('utf-8')

                
                return send_file(pdf_content_b64, as_attachment=True, download_name='oder_catalog.pdf'), order_dict
            else:
                return order_dict



