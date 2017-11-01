import unittest
from event import GlobalEvent, GlobalDictModEvent

class Test_Event(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.ls = []
        self.callable0_cntr = 0
        self.callable1_cntr = 0

    def callable0(self, event, **kwargs):
        self.ls.append(0)
        if self.callable0_cntr == 0:
            self.assertEqual(kwargs['name'], 'GlobalEventInst0')
        elif self.callable0_cntr == 1:
            self.assertEqual(kwargs['name'], 'GlobalEventInst1')
        self.callable0_cntr += 1

    def callable1(self, event, **kwargs):
        self.ls.append(1)
        if self.callable1_cntr == 0:
            self.assertEqual(kwargs['name'], 'GlobalEventInst0')
        elif self.callable1_cntr == 1:
            self.assertEqual(kwargs['name'], 'GlobalEventInst1')
        self.callable1_cntr += 1

    def test_event_01(self):
        GlobalEvent.subscribe(self.callable0)
        GlobalEvent.subscribe(self.callable1)
        event0 = GlobalEvent()
        event0.fire(name = 'GlobalEventInst0')
        event1 = GlobalEvent()
        event1.fire(name = 'GlobalEventInst1')

        self.assertListEqual(self.ls, [0,1,0,1])

        event3 = GlobalDictModEvent()
        event3.fire()

        self.assertListEqual(self.ls, [0,1,0,1])

    pass
