# Speaker Component

from app import mongo
class Speaker():

    @staticmethod
    def view_speaker():
        
        speaker_list =[]
        
        try:
            speaker_list = list(mongo.db.speaker_data.find({}))
            return speaker_list
        
        except Exception as e:
            return {"success":True, "message":str(e)}
        
    @staticmethod
    def create_speaker(speaker_data):

        try:
            mongo.db.speaker_data.insert_one(speaker_data)
            return {"success": True, "message": "Speaker created successfully"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def data_speaker(s_id):

        try:
            speaker = list(mongo.db.speaker_data.find({"id":s_id}))
            return speaker
        except Exception as e:
            return None
    

    @staticmethod
    def edit_speaker(s_id, speaker_status):

        try:
            mongo.db.speaker_data.update_one({"id":s_id}, {"$set":{"status": speaker_status}})
            return {"success": True, "message":"status update successfull"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def update_speaker(s_id, speaker_data):

        try:
            mongo.db.speaker_data.update_one({"id":s_id}, {"$set": speaker_data})
            return {"success": True, "message": "speaker update successfull"}
        
        except Exception as e:
            return {"success":False, "message": str(e)}
        
    @staticmethod
    def delete_speaker(s_id):
        
        try:
            mongo.db.speaker_data.delete_one({"id":s_id})
            return {"success": True, "message": "speaker deletion successful"}
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        
    @staticmethod
    def update_history(s_name, webinar_topic):

        try:
            result= mongo.db.speaker_data.update_one({
               {"name": s_name,},{"$addToSet":{"history":webinar_topic}}
           })
            return result.modified_count
        except Exception as e:
            return {"success":False, "message":str(e)}

