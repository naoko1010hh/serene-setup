#!/usr/bin/env python3
#== Import ==#
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf
import configparser
import json
import subprocess

#== Function ==#
def go(num):
    num = str(num)
    select_window(num)

def run_command(command):
    command = command.split()
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr = subprocess.DEVNULL)
    return result.stdout.decode("utf8")

#== Selct Window ==#
def select_window(num):
    class SelectWindow(Gtk.Window):
        #= __init__ Function =#
        def __init__(self):
            #-- Create Window --#
            Gtk.Window.__init__(self, title="Serene Setup Wizard")
            self.selected = []

            #-- Define lauouts --#
            sub_layout_1 = Gtk.Box(spacing=10)
            sub_layout_2 = Gtk.Box(spacing=10)
            main_layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            
            #-- Generate icons & buttons --#
            for name in select_list:
                #- Generate icon --#
                icon_list = Gtk.ListStore(Pixbuf)
                pixbuf = Gtk.IconTheme.get_default().load_icon(name, 90, 0)
                icon_list.append([pixbuf])
                icon = Gtk.IconView.new()
                icon.set_model(icon_list)
                icon.set_text_column(-1)
                icon.set_pixbuf_column(0)
                icon.set_selection_mode(0)

                #- Geneate Button -#
                button = Gtk.ToggleButton(name)
                button.connect("toggled", self.on_button_toggled, name)
                try:
                    if name in selected[num]:
                        button.set_active(True)
                except:
                    pass

                #- Define layout -#
                layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

                #- Add layout -#
                layout.pack_start(icon, True, True, 0)
                layout.pack_start(button, True, True, 0)

                #- Add sub layout 1 -#
                sub_layout_1.pack_start(layout, True, True, 10)

            #-- Generate Label --#
            #- desc label -#
            desc_label = Gtk.Label()
            desc_label.set_markup("\n\n<big><b>" + desc + "</b></big>")
            desc_label.set_line_wrap(True)
            
            #- copyright
            copyright_label = Gtk.Label()
            copyright_label.set_markup("<small>Copyright (C) 2019-2020 FascodeNetwork</small>")

            #-- Generate Button --#
            #- back button -#
            if not number == 0:
                back = Gtk.Button("前へ")
                back.connect("clicked", self.back)

            if not str(number + 1) in config.options("desc"):
                #- next button -#
                next = Gtk.Button("終了")
                next.connect("clicked", self.end)
            else:
                #- end button -#
                next = Gtk.Button("次へ")
                next.connect("clicked", self.next)

            #-- Add sub layout 2 --#
            if not number == 0:
                sub_layout_2.pack_start(back, True, True, 10)
            
            sub_layout_2.pack_start(next, True, True, 10)
        
            #- Add main layout -#
            main_layout.pack_start(desc_label, True, True, 0)
            main_layout.pack_start(sub_layout_1, True, True, 0)
            main_layout.pack_start(sub_layout_2, True, True, 0)
            main_layout.pack_start(copyright_label, True, True, 10)
        
            #-- Show main layout --#
            self.add(main_layout)
    
        #= Button Function =#
        #-- toggle button --#
        def on_button_toggled(self, button, name):
            if button.get_active():
                self.selected.append(name)
            else:
                self.selected.remove(name)
        
        #-- next button -#
        def next(self, button):
            selected[num] = self.selected
            self.close()
            go(number+1)
        
        #-- back button -#
        def back(self, button):
            selected[num] = self.selected
            self.close()
            go(number-1)
        
        #-- end button --#
        def end(self, button):
            selected[num] = self.selected
            install_list = []
            self.close()
            Gtk.main_quit()
            for key in range(len(config.options("desc"))):
                install_list += selected[str(key)]
            
            print(install_list)
    #= Define =#
    desc = config.get("desc", num)
    number = int(num)
    select_list = []
    select_list = json.loads(config.get("pkg", num))

    #= Run =#
    win = SelectWindow()
    win.show_all()
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()

#== Run ==#
if __name__ == "__main__":
    global selected
    selected = {}
    config = configparser.ConfigParser()
    config.read('serene-setupwizard.conf')
    select_window("0")