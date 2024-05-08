# Webinar component

from app import mongo

class Webinar():
    
    @staticmethod
    def view_webinar():
        
        webinar_list =[]
        try: 
        
            webinar_list = list(mongo.db.webinar_data.find({}))
            return webinar_list
        
        except Exception as e:
            return {"success": False, "message": str(e)} 
          
    
    @staticmethod
    def create_webinar(webinar_data):
        
        try:
            mongo.db.webinar_data.insert_one(webinar_data)
            return {"success":True, "message": "webinar created successfully"} 
        
        except Exception as e:
            return {"success":False, "message":str(e)}
    
    @staticmethod
    def data_webinar(w_id):
        
        try: 
            
            webinar = list(mongo.db.webinar_data.find({"id":w_id}))
            return webinar
        
        except Exception as e:
            return None

    @staticmethod
    def update_webinar(w_id, webinar_data):
        
        try:
            
            mongo.db.webinar_data.update_one({"id":w_id},{"$set": webinar_data})
            return {"success":True, "message":"webinar update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        

    @staticmethod
    def edit_webinar(w_id, webinar_status):
        
        try:
            
            mongo.db.webinar_data.update_one({"id":w_id},{"$set": {"status": webinar_status}})
            return {"success":True, "message":"status update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}

    @staticmethod
    def delete_webinar(w_id):
        
        try: 
            mongo.db.webinar_data.delete_one({"id":w_id})
            return {"success":True,"message": " deleted sucessfully"}
        
        except Exception as e:
            return {"success":False, "message": str(e)}
    
