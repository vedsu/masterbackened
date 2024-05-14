# Order Component
from app import mongo

class Order:

    @staticmethod
    def view_order():
        order_list =[]
        
        try:
            order_list = list(mongo.db.order_data.find({}))
            return order_list
        
        except Exception as e:
            return {"success": False, "message": str(e)}
        

    @staticmethod
    def order_data(o_id):

        try:
            order = list(mongo.db.order_data.find({"id": o_id}))
            return order
        
        except Exception as e:
            return None
