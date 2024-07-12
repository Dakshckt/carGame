import pymongo

myClient = pymongo.MongoClient("mongodb://localhost:27017")
mydb = myClient["python"]
mycol = mydb['carGame']



class updateScorce:
    def update(self , score):
        result = mycol.find_one()
        change = { '$set' : {"score" : f"{score}"}}
        answer = mycol.update_one(result , change)
        return answer

    def select(self):
        result = mycol.find_one()
        return result['score']
    
