import unittest

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        pass

    def insert(self):
        actionID= 'a1'
        causlityID = 'nil'
        model ={}
        #model
        self.assertTrue(actionID not in model)
        self.assertEqual(causlityID,'nil')
        actionID = 'a1'
        causlityID = 'a2'
        model = {'a1':[]}
        self.assertFalse(actionID not in model)
        self.assertNotEqual(causlityID, 'nil')


        actionUsername = 'u1'
        causlityID = 'nil'
        causlityUsername = 'u2'
        influence = {'u1':[]}
        #influence set
        self.assertTrue(actionUsername in influence and causlityID == 'nil')
        self.assertFalse(actionUsername not in influence)
        self.assertNotEqual(causlityUsername, 'nil')
        actionUsername = 'u2'
        causlityID = 'a1'
        causlityUsername = 'nil'
        influence = {'u1':[]}
        # influence set
        self.assertFalse(actionUsername in influence and causlityID == 'nil')
        self.assertTrue(actionUsername not in influence)
        self.assertEqual(causlityUsername, 'nil')

        actionUsername = 'u1'
        causlityID = 'a1'
        influence = {'u1': []}
        # influence set
        self.assertFalse(actionUsername in influence and causlityID == 'nil')

        actionUsername = 'u2'
        causlityID = 'nill'
        influence = {'u1': []}
        # influence set
        self.assertFalse(actionUsername in influence and causlityID == 'nil')

    def remove(self):
        actionID= 'a1'
        model ={'a1':[]}
        #model
        self.assertTrue(not model[actionID])
        actionID = 'a1'
        model = {'a1': ['*root*','a2']}
        self.assertFalse(not model[actionID])

        actionID = 'a1'
        actionUsername = 'u1'
        causlityID = 'a1'
        causlityUsername = 'u2'
        influence = {'u2': ['u1']}
        #infuence
        self.assertTrue(actionID == causlityID)
        self.assertNotEqual(causlityID,'nil')
        self.assertTrue(actionUsername in influence[causlityUsername])

        actionID = 'a1'
        actionUsername = 'u1'
        causlityID = 'nil'
        causlityUsername = 'u2'
        influence = {'u2': ['u3']}
        # infuence
        self.assertFalse(actionID == causlityID)
        self.assertEqual(causlityID, 'nil')
        self.assertFalse(actionUsername in influence[causlityUsername])


if __name__ == '__main__':
    unittest.main()
