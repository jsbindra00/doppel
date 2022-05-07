



from tkinter.filedialog import askopenfilename, asksaveasfilename

from InputExecutor import InputExecutor
from InputTracker import InputTracker
from documentutil import writeFile

from docutil import DocUtil

import os
import sys
import glfw
import OpenGL.GL as gl
import imgui
from imgui.integrations.glfw import GlfwRenderer
import tkinter as tk
tk.Tk().withdraw()



             
path_to_font = None  # "path/to/font.ttf"

opened_state = True                                           

      






class Application:
    def __init__(self):
        self.tracker_ = InputTracker()
        self.executor_ = InputExecutor()
        self.tracking_file_contents = ""
        self.tracking_file_dir = ""


        self.active_gui_elements = {
        "begin_tracking_button" : True,
        "begin_executing_button": True,
        "file_viewer" : True

        }


    def BrowseFiles(self):
        file_name = tk.filedialog.askopenfilename(initialdir = "/",
                                            title = "Select a File",
                                            filetypes = (("Text files",
                                                            "*.txt*"),
                                                        ("all files",
                                                            "*.*")))
        return file_name

    def StartTracking(self):
        self.tracker_.startTracking(writeFile,track_mouse=True, track_keyboard=True, print_events=True)
        self.tracker_.Join()
    def Execute(self):
        self.executor_.execute("./trackingres.txt", print_events=True)



    def impl_glfw_init(self):
        width, height = 1600, 900
        window_name = "minimal ImGui/GLFW3 example"

        if not glfw.init():
            print("Could not initialize OpenGL context")
            sys.exit(1)

        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

        window = glfw.create_window(int(width), int(height), window_name, None, None)
        glfw.make_context_current(window)

        if not window:
            glfw.terminate()
            print("Could not initialize Window")
            sys.exit(1)

        return window



    def frame_commands(self):
        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        io = imgui.get_io()

        if io.key_ctrl and io.keys_down[glfw.KEY_Q]:
            sys.exit(0)


    # TOP NAVIGATION BAR
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", enabled=True):
                clicked_open, selected_open = imgui.menu_item("Open Tracking File", "Ctrl+O", selected=False, enabled=True)
                if clicked_open:
                    file_name = self.BrowseFiles()
                    if DocUtil.ItemExists(file_name): 
                        self.tracking_file_contents = open(file_name, "r").read()

                clicked_quit, selected_quit = imgui.menu_item("Quit", "Ctrl+Q", False, True)
                if clicked_quit:
                    sys.exit(0)
                imgui.end_menu()
            imgui.end_main_menu_bar()
        imgui.begin("Example: item groups")
        imgui.begin_group()


        if self.active_gui_elements["file_viewer"]:
            imgui.begin("Active Tracking File")
            imgui.text_unformatted(self.tracking_file_contents)
            imgui.end()
        # visual-example::
        # :auto_layout:
        # :height: 80
        # :width: 300
        # imgui.begin("Example: text with label")
        # imgui.label_text("my label", "my text")
        # imgui.end()
        #     imgui.label_text("foo", "bar" * 20)
        #     imgui.begin("Example: item groups")
        #     imgui.begin_group()
        #     imgui.text("First group (buttons):")
        #     imgui.button("Button A")
        #     imgui.button("Button B")
        #     imgui.end_group()
        #     imgui.new_line()
            
        #     imgui.begin_group()
        #     imgui.text("Second group (text and bullet texts):")
        #     imgui.bullet_text("Bullet A")
        #     imgui.bullet_text("Bullet B")
        #     imgui.end_group()
        #     imgui.end()



        if self.active_gui_elements["begin_tracking_button"]:
            # imgui.begin("Example: tooltip")
            tracking = imgui.button("Begin Tracking")
            if imgui.is_item_hovered():
                imgui.begin_tooltip()
                imgui.text("Track")
                imgui.end_tooltip()
            if tracking:
                self.StartTracking()
            # imgui.end()

        if self.active_gui_elements["begin_executing_button"]:
            executing = imgui.button("Begin Executing")
            if imgui.is_item_hovered():
                imgui.begin_tooltip()
                imgui.text("Execute")
                imgui.end_tooltip()
            if executing:
                
                self.Execute()

        imgui.end_group()
        imgui.end()



    def render_frame(self,impl, window, font):
        glfw.poll_events()
        impl.process_inputs()
        imgui.new_frame()

        gl.glClearColor(0.1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        if font is not None:
            imgui.push_font(font)
        self.frame_commands()
        if font is not None:
            imgui.pop_font()

        imgui.render()
        impl.render(imgui.get_draw_data())
        glfw.swap_buffers(window)

    def Start(self):
        imgui.create_context()
        window = self.impl_glfw_init()

        impl = GlfwRenderer(window)

        io = imgui.get_io()
        jb = io.fonts.add_font_from_file_ttf(path_to_font, 30) if path_to_font is not None else None
        impl.refresh_font_texture()

        while not glfw.window_should_close(window):
            self.render_frame(impl, window, jb)

        impl.shutdown()
        glfw.terminate()


        pass
        









    # if active["popup"]:
    #     imgui.begin("Example: simple popup")
    #     if imgui.button("select"):
    #         imgui.open_popup("select-popup")
    #     imgui.same_line()
    #     if imgui.begin_popup("select-popup"):
    #         imgui.text("Select one")
    #         imgui.separator()
    #         imgui.selectable("One")
    #         imgui.selectable("Two")
    #         imgui.selectable("Three")
    #         imgui.end_popup()
    #     imgui.end()

    # if active["popup modal"]:
    #     imgui.begin("Example: simple popup modal")
    #     if imgui.button("Open Modal popup"):
    #         imgui.open_popup("select-popup-modal")
    #     imgui.same_line()
    #     if imgui.begin_popup_modal("select-popup-modal")[0]:
    #         imgui.text("Select an option:")
    #         imgui.separator()
    #         imgui.selectable("One")
    #         imgui.selectable("Two")
    #         imgui.selectable("Three")
    #         imgui.end_popup()
    #     imgui.end()

    # if active["popup context window"]:
    #     imgui.begin("Example: popup context window")
    #     if imgui.begin_popup_context_window():
    #         imgui.selectable("Clear")
    #         imgui.end_popup()
    #     imgui.end()

    # if active["popup context void"]:
    #     if imgui.begin_popup_context_void():
    #         imgui.selectable("Clear")
    #         imgui.end_popup()


    # if active["group"]:



  




















if __name__ == "__main__":
    app = Application()
    app.Start()


