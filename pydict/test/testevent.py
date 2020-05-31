import unittest
from event import Event, EventSaveAll, EventWordAddRequest

class Test_Event(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.ls = []
        self.callable0_cntr = 0
        self.callable1_cntr = 0
        self.callable2_cntr = 0

    def callable0(self, event, *args, **kwargs):
        self.ls.append(0)
        if self.callable0_cntr == 0:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst0')
        elif self.callable0_cntr == 1:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst1')
        self.callable0_cntr += 1

    def callable1(self, event, *args, **kwargs):
        self.ls.append(1)
        if self.callable1_cntr == 0:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst0')
        elif self.callable1_cntr == 1:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst1')
        self.callable1_cntr += 1

    def callable2(self, event, *args, **kwargs):
        self.ls.append(2)
        if self.callable2_cntr == 0:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst0')
        elif self.callable2_cntr == 1:
            self.assertEqual(kwargs['name'], 'EventSaveAllInst1')
        self.callable2_cntr += 1

    def test_event_01(self):
        with self.assertRaises(NotImplementedError) as context:
            event = Event()
            self.assertIn('Event shall not instantiated because it is an abstract class.', self.context.exception)


    def test_event_02(self):
        EventSaveAll.subscribe(self.callable0)
        EventSaveAll.subscribe(self.callable1)
        Event.subscribe(self.callable2)
        event0 = EventSaveAll()
        event0.fire(name = 'EventSaveAllInst0')
        event1 = EventSaveAll()
        event1.fire(name = 'EventSaveAllInst1')

        self.assertListEqual(self.ls, [0,1,2,0,1,2])

