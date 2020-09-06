import unittest

class TestStringMethods(unittest.TestCase):       
    def testBuffer(self):
        timeDef=0.5
        count= 160
        self.assertTrue(timeDef<5)
        self.assertTrue(count>150)
        timeDef=1.3
        count= 90
        self.assertTrue(timeDef<5)
        self.assertFalse(count>150)
        timeDef=8.3
        count= 170
        self.assertFalse(timeDef<5)
        self.assertTrue(count>150)
        timeDef=8.3
        count= 90
        self.assertFalse(timeDef<5)
        self.assertFalse(count>150)



if __name__ == '__main__':
    unittest.main()
