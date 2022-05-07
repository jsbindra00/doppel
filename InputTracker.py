from anyio import wait_socket_readable
from pynput import mouse
from pynput import keyboard
from threading import Event, Thread
from enum import Enum
import time
import queue
#
#             _____          _ _____      _         
#            |____ |        | |  _  |    | |        
#   _____   __   / /_ __ ___| | |/' | ___| | ___ __ 
#  / _ \ \ / /   \ \ '__/ __| |  /| |/ __| |/ / '__|
# | (_) \ V /.___/ / | | (__| \ |_/ / (__|   <| |   
#  \___/ \_/ \____/|_|  \___|_|\___/ \___|_|\_\_|   
#
#
# I am not responsible for any damages that you inflict on any system with my code. This code is for educational purposes only.

class EventType(Enum):
    NONE = -1
    KEYPRESSED = 0
    KEYRELEASED = 1
    SCROLL_UP = 2
    SCROLL_DOWN = 3
    SCROLL_LEFT = 4
    SCROLL_RIGHT = 5
    MOUSECLICKED = 6
    MOUSERELEASED = 7
    MOUSEMOVED = 8
    INJECT_SCRIPT = 9
    KILL = 10

class EventAttribute(Enum):
    POSITION_X = 0
    POSITION_Y = 1
    KEY_PRESS = 2
    KEY_RELEASE = 3
    SCROLL_OFFSET = 4
    TIME_INVOKED = 5
    BUTTON_TYPE = 6
    FILE_NAME = 7
    NONE = 8

class Event:
    def __init__(self, event_type, event_dict):
        self.type = EventType(event_type)
        self.attributes = event_dict 
    def __str__(self):
        return self.type.name + "$" + str(self.attributes)
    def getAttribute(self, attribute_type):
        return self.attributes[attribute_type]
    
class InputTracker:
    def __init__(self):
        self.event_queue = queue.Queue()
        self.file_buffer = ""
        self.active = False   

    def generateEvent(start_time, evnt_type, args):
        return Event(evnt_type, InputTracker.packageAttributes(start_time, args))
    def packageAttributes(start_time, args):
        res = {}
        res[str(EventAttribute.TIME_INVOKED).replace("EventAttribute.", "")] = time.time() - start_time
        for i in range(0, len(args) - 1):
            res[str(args[i]).replace("EventAttribute.", "")] = str(args[i+1]).replace("\'", "")
        return res

    def registerEvent(self, event_type, *args):
        if event_type == EventType.NONE: return

        attribute_dict = InputTracker.packageAttributes(self.start_time, args)
        self.event_queue.put(Event(event_type, attribute_dict))
    
    def processEventQueue(self):
        while self.active:
            event = self.event_queue.get()
            if event == None: continue
            if event.type == EventType.KILL:
                self.active = False
                
            event_info = event.__str__()
            if self.print_events:
                print(event_info)
            self.file_buffer = self.file_buffer + event_info + "\n"
            

    
    def on_move(self,x, y):
        self.registerEvent(EventType.MOUSEMOVED, EventAttribute.POSITION_X, x, EventAttribute.POSITION_Y, y)
        return self.active

    def on_click(self,x, y, button, pressed):
        event_type = EventType.MOUSECLICKED if pressed else EventType.MOUSERELEASED
        self.registerEvent(event_type, EventAttribute.POSITION_X, x, EventAttribute.POSITION_Y, y, EventAttribute.BUTTON_TYPE, button)
        return self.active
     

    def on_scroll(self,x, y, dx, dy):
        (scroll_dir, off) = (EventType.SCROLL_UP, dy) if dy > 0 else (EventType.SCROLL_DOWN,dy) if dy < 0 else (EventType.SCROLL_LEFT,dx) if dx < 0 else (EventType.SCROLL_RIGHT,dx) 
        self.registerEvent(scroll_dir, EventAttribute.POSITION_X, x, EventAttribute.POSITION_Y, y, EventAttribute.SCROLL_OFFSET, off)
        return self.active

    
    def on_press(self,key):
        if key == keyboard.Key.f11 and self.previous_button == keyboard.Key.ctrl_l:
            self.registerEvent(EventType.KILL, EventAttribute.NONE, EventAttribute.NONE)
        else: self.registerEvent(EventType.KEYPRESSED, EventAttribute.KEY_PRESS, key)
        self.previous_button = key
        return self.active

    def on_release(self, key):
        self.registerEvent(EventType.KEYRELEASED,EventAttribute.KEY_RELEASE, key)
        return self.active
    
    def startTracking(self, event_saver,track_mouse = True, track_keyboard = True, print_events = True):
        self.file_buffer = ""
        self.print_events = print_events
        self.trackMouse_ = track_mouse
        self.trackKey_ = track_keyboard
        self.eventSaver_ = event_saver
        if track_mouse:
            #create listening thread
            self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_scroll=self.on_scroll)
            self.mouse_listener.start()


        if track_keyboard:
            self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

            self.keyboard_listener.start()
            self.previous_button = None
         
        self.active = True  
        self.start_time = time.time()
        self.queue_processor = Thread(target=self.processEventQueue)
        self.queue_processor.start()

        

        
    def Join(self):
        if self.trackMouse_: self.mouse_listener.join()
        if self.trackKey_: self.keyboard_listener.join()
        self.queue_processor.join()

        # if event_saver is not None:
        self.eventSaver_(self.file_buffer, "./trackingres.txt")









