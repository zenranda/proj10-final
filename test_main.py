###
#Various nose tests. If you want to adapt this for your own use, be aware that the start/end block list has a very specific formatting.
###
import get_freebusy
import arrow
from operator import itemgetter

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



def test_free_times():      #Given a sample list, check to see if it's getting free/busy blocks correctly
    print("RESULTS:")
    print(get_freebusy.get_freebusy([['2016-11-20T08:30:00-08:00', '2016-11-20T010:30:00-08:00'], ['2016-11-20T11:00:00-08:00', '2016-11-20T15:00:00-08:00'], ['2016-11-20T16:30:00-08:00', '2016-11-20T19:00:00-08:00'], ['2016-11-24T13:30:00-08:00', '2016-11-24T16:00:00-08:00'], ['2016-11-21T15:00:00-08:00', '2016-11-21T18:30:00-08:00']], arrow.get('2016-11-23T16:00:00'), arrow.get('2016-11-24T04:00:00')))
    print(get_freebusy.get_freebusy([], arrow.get('2016-11-20T20:00:00'),arrow.get('2016-11-24T04:00:00')))

    ranges = [['2016-11-20T08:30:00-08:00', '2016-11-20T010:30:00-08:00'], ['2016-11-20T11:00:00-08:00', '2016-11-20T15:00:00-08:00'], ['2016-11-20T16:30:00-08:00', '2016-11-20T19:00:00-08:00'], ['2016-11-24T13:30:00-08:00', '2016-11-24T16:00:00-08:00'], ['2016-11-21T15:00:00-08:00', '2016-11-21T18:30:00-08:00']]
    start = arrow.get('2016-11-23T16:00:00')
    end = arrow.get('2016-11-24T04:00:00')

    assert get_freebusy.get_freebusy(ranges, start, end) == [['At 2016-11-20 from 08:00:00 to 08:30:00', 'At 2016-11-20 from 10:30:00 to 11:00:00', 'At 2016-11-20 from 15:00:00 to 16:30:00', 'At 2016-11-20 from 19:00:00 to 20:00:00', 'At 2016-11-21 from 08:00:00 to 15:00:00', 'At 2016-11-21 from 18:00:00 to 20:00:00', 'At 2016-11-24 from 08:00:00 to 13:30:00', 'At 2016-11-24 from 16:00:00 to 20:00:00'], ['At 2016-11-20 from 08:30:00 to 10:30:00', 'At 2016-11-20 from 11:00:00 to 15:00:00', 'At 2016-11-20 from 16:30:00 to 19:00:00', 'At 2016-11-21 from 15:00:00 to 18:00:00', 'At 2016-11-24 from 13:30:00 to 16:00:00']]
  
  
    ranges = []
    start = arrow.get('2016-11-20T20:00:00')
    end = arrow.get('2016-11-24T04:00:00')
    
    assert get_freebusy.get_freebusy(ranges, start, end) == [[], []]
    
    
def test_overlap():         #tests if the program can handle dates that overlap/intersect
    ranges = [['2016-11-22T11:00:00-08:00', '2016-11-22T16:00:00-08:00'], ['2016-11-23T12:00:00-08:00', '2016-11-23T15:30:00-08:00']]
    start = arrow.get('2016-11-20T16:00:00')
    end = arrow.get('2016-11-24T04:00:00')
    
    assert get_freebusy.get_freebusy(ranges, start, end) == [['At 2016-11-22 from 08:00:00 to 11:00:00', 'At 2016-11-22 from 16:00:00 to 20:00:00', 'At 2016-11-23 from 08:00:00 to 11:00:00', 'At 2016-11-23 from 18:30:00 to 20:00:00'], ['At 2016-11-22 from 11:00:00 to 16:00:00', 'At 2016-11-23 from 11:00:00 to 18:30:00']]

    
def test_db():
    assert collection != None
    collection.insert({"type" : "freebusy", "entry" : [["entry 1"], ["entry 2"]]})
    assert base_size < collection.count()
    collection.remove({"entry" : [["entry 1"], ["entry 2"]]})
    assert base_size == collection.count()
    
