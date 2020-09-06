
#tweet['Time'] <= expiry_interval
#if time <= self.time_limit
#if type(row) is tuple

#XXXXtime: 2020-04-08 22:21:59+00:00  XXXXtime_limit:  2020-04-08 22:22:56+00:00
#XXXXROW: (23, 'Wed Apr 08 22:26:19 +0000 2020', '1248014338696179715', '@realDonaldTrump per Mark Levine we lost 50k people from the flu last year. Projections show 61k is the projection… https://t.co/Rx5Rozd6vZ', 'rsensitivelife1', None, 'realDonaldTrump', 0, 1, 0, 11566, None)
#XXXXtime: 2020-04-08 22:26:19+00:00  XXXXtime_limit:  2020-04-08 22:27:18+00:00

from datetime import datetime, timedelta
import unittest

class TestStringMethods(unittest.TestCase): 
    def testTime1(self):
        tweet=[]
        tweet= datetime.strptime("Sat Feb 21 09:56:09 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        expiry_interval=datetime.strptime("Sat Feb 22 10:00:00 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        self.assertTrue(tweet <= expiry_interval)

        tweet= datetime.strptime("Sat Feb 22 10:00:00 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        expiry_interval= datetime.strptime("Sat Feb 21 09:56:09 +0000 2020", '%a %b %d %H:%M:%S %z %Y')

        self.assertFalse(tweet <= expiry_interval)
    
    def testTime2(self):
        time=datetime.strptime("Sat Feb 21 09:56:09 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        time_limit= datetime.strptime("Sat Feb 22 10:00:00 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        self.assertTrue(time <= time_limit)

        time= datetime.strptime("Sat Feb 22 10:00:00 +0000 2020", '%a %b %d %H:%M:%S %z %Y')
        time_limit= datetime.strptime("Sat Feb 21 09:56:09 +0000 2020", '%a %b %d %H:%M:%S %z %Y')

        self.assertFalse(time <= time_limit)
        
    def testRowType(self):
        row =(23, 'Wed Apr 08 22:26:19 +0000 2020', '1248014338696179715', '@realDonaldTrump per Mark Levine we lost 50k people from the flu last year. Projections show 61k is the projection… https://t.co/Rx5Rozd6vZ', 'rsensitivelife1', None, 'realDonaldTrump', 0, 1, 0, 11566, None)

        self.assertTrue(type(row) is tuple)

        row= None

        self.assertFalse(type(row) is tuple)
        

if __name__ == '__main__':
    unittest.main()
