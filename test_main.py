###
#Various nose tests. If you want to adapt this for your own use, be aware that the start/end block list has a very specific formatting.
###
import date_chopper
import arrow

from pymongo import MongoClient
import secrets.admin_secrets
import secrets.client_secrets
MONGO_CLIENT_URL = "mongodb://{}:{}@localhost:{}/{}".format(
    secrets.client_secrets.db_user,
    secrets.client_secrets.db_user_pw,
    secrets.admin_secrets.port, 
    secrets.client_secrets.db)

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, secrets.client_secrets.db)
    collection = db.dated
    base_size = collection.count() #current size of the db, for comparison later

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)  

def test_overlap():      #Given a sample list, check to see if its dates overlap at all
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00']]
    assert (date_chopper.date_overlap(ranges)) == False
    
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00'], ['2016-11-20T16:00:00', '2016-11-20T17:00:00'], ['2016-11-20T17:00:00', '2016-11-20T19:00:00']]
    assert (date_chopper.date_overlap(ranges)) == True
    
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T10:30:00', '2016-11-20T13:00:00'], ['2016-11-20T13:00:00', '2016-11-20T14:00:00'], ['2016-11-20T14:10:00', '2016-11-20T16:00:00']]
    assert (date_chopper.date_overlap(ranges)) == True
  
def test_underlap():         #tests if the program can detect start times that go out of bounds
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00']]
    start = arrow.get('2016-11-20T05:00:00')
    assert (date_chopper.date_underlap(ranges, start)) == True
    
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00']]
    start = arrow.get('2016-11-20T10:00:00')
    assert (date_chopper.date_underlap(ranges, start)) == False
    
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00']]
    start = arrow.get('2016-11-20T16:00:00')
    assert (date_chopper.date_underlap(ranges, start)) == False
    
    ranges = [['2016-11-20T08:30:00', '2016-11-20T10:30:00'], ['2016-11-20T11:00:00', '2016-11-20T15:00:00']]
    start = arrow.get('2016-11-20T10:00:00')
    assert (date_chopper.date_underlap(ranges, start)) == True
    
    
def test_db():                      #tests basic DB operation
    assert collection != None
    collection.insert({"type" : "freebusy", "entry" : [["entry 1"], ["entry 2"]]})
    assert base_size < collection.count()
    collection.remove({"entry" : [["entry 1"], ["entry 2"]]})
    assert base_size == collection.count()
    
