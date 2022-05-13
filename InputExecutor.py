from pynput import keyboard
from pynput import mouse
import InputTracker
from queue import Queue
from pynput.keyboard import Key
from threading import Thread
import time
import documentutil
from enum import Enum

# ███╗░░██╗░░███╗░░░██████╗░██╗░░██╗████████╗██████╗░██╗██████╗░██████╗░██████╗░
# ████╗░██║░████║░░██╔════╝░██║░░██║╚══██╔══╝██╔══██╗██║██╔══██╗╚════██╗██╔══██╗
# ██╔██╗██║██╔██║░░██║░░██╗░███████║░░░██║░░░██████╔╝██║██║░░██║░█████╔╝██████╔╝
# ██║╚████║╚═╝██║░░██║░░╚██╗██╔══██║░░░██║░░░██╔══██╗██║██║░░██║░╚═══██╗██╔══██╗
# ██║░╚███║███████╗╚██████╔╝██║░░██║░░░██║░░░██║░░██║██║██████╔╝██████╔╝██║░░██║
# ╚═╝░░╚══╝╚══════╝░╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═════╝░╚═════╝░╚═╝░░╚═╝
# DISCLAIMER: i am not responsible for what you choose to do with my code. have fun.


class InputExecutor:
    def pressKey(self, event):
        key_button = event.getAttribute(
            InputTracker.EventAttribute.KEY_PRESS.name)
        if "Key" in key_button:
            key_button = eval(key_button)
        self.keyboard_controller.press(key_button)

    def releaseKey(self, event):
        key_button = event.getAttribute(
            InputTracker.EventAttribute.KEY_RELEASE.name)
        if "Key" in key_button:
            key_button = eval(key_button)
        self.keyboard_controller.release(key_button)

    def runScript(self, evnt):
        print("Running Injected Script...")

        file_directory_str = evnt.getAttribute(InputTracker.EventAttribute.FILE_NAME.name)
        print("Opening " + file_directory_str + "...")
        documentutil.open_file(file_directory_str)


    def scroll(self, event):
        amount = int(event.getAttribute(
            InputTracker.EventAttribute.SCROLL_OFFSET.name))
        self.mouse_controller.position = (event.getAttribute(
            InputTracker.EventAttribute.POSITION_X.name), event.getAttribute(InputTracker.EventAttribute.POSITION_Y.name))

        if event.type == InputTracker.EventType.SCROLL_LEFT or event.type == InputTracker.EventType.SCROLL_RIGHT:
            self.mouse_controller.scroll(amount, 0)
        else:
            self.mouse_controller.scroll(0, amount)

    def clickMouse(self, event):
        self.mouse_controller.position = (event.getAttribute(
            InputTracker.EventAttribute.POSITION_X.name), event.getAttribute(InputTracker.EventAttribute.POSITION_Y.name))
        self.mouse_controller.press(mouse.Button.left)

    def releaseMouse(self, event):
        self.mouse_controller.position = (event.getAttribute(
            InputTracker.EventAttribute.POSITION_X.name), event.getAttribute(InputTracker.EventAttribute.POSITION_Y.name))
        self.mouse_controller.release(mouse.Button.left)

    def moveMouse(self, event_info):
        pass

    def __init__(self):
        self.processingQueue = Queue()
        self.event_handlers = {
            InputTracker.EventType.KEYPRESSED: self.pressKey,
            InputTracker.EventType.KEYRELEASED: self.releaseKey,
            InputTracker.EventType.SCROLL_DOWN: self.scroll,
            InputTracker.EventType.SCROLL_UP: self.scroll,
            InputTracker.EventType.SCROLL_LEFT: self.scroll,
            InputTracker.EventType.SCROLL_RIGHT: self.scroll,
            InputTracker.EventType.MOUSECLICKED: self.clickMouse,
            InputTracker.EventType.MOUSERELEASED: self.releaseMouse,
            InputTracker.EventType.MOUSEMOVED: self.moveMouse,
            InputTracker.EventType.INJECT_SCRIPT: self.runScript,
            InputTracker.EventType.KILL: self.kill
        }
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()

    def kill(self, event):
        self.active = False
    def __renderEvent(self, file_string):
        event_information = file_string.split("$")
        return InputTracker.Event(InputTracker.EventType[event_information[0]], eval(event_information[1]))

    def handleEvent(self, event):
        if self.print_events:
            print("EXECUTING EVENT: " + event.__str__())
        self.event_handlers[InputTracker.EventType(event.type)](event)

    def processQueue(self):
        while self.active:
            event = self.processingQueue.get()
            elapsed_time = time.time() - self.t_start
            event_fire_time = float(
                event.attributes[InputTracker.EventAttribute.TIME_INVOKED.name])
            if elapsed_time < event_fire_time:
                time.sleep(event_fire_time - elapsed_time)
            self.handleEvent(event)
            


    def execute(self, file_path, print_events=True):
        self.print_events = print_events
        self.t_start = time.time()
        print(self.t_start)
        self.active = True

        queue_processor = Thread(target=self.processQueue)
        queue_processor.start()


        with open(file_path, "r") as file:
            lines = [line.rstrip('\n') for line in file]
            for line in lines:
                self.processingQueue.put(self.__renderEvent(line))
        queue_processor.join()

