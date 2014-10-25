# -*- coding: utf-8 -*-
#!/usr/bin/env python
from multiprocessing import Process, freeze_support

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import subprocess
import time
import threading
from os import O_NONBLOCK, read
import tempfile
import os
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '400')
import psutil


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)


class Root(FloatLayout):
    loadfile = ObjectProperty(None)
    savefile = ObjectProperty(None)
    text_input = ObjectProperty(None)

    def dismiss_popup(self):
        self._popup.dismiss()

    def show_load(self):
        content = LoadDialog(load=self.install, cancel=self.dismiss_popup)
        self._popup = Popup(
            title="Load file", content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def install(self, path, filename):
        self.dismiss_popup()
        thread = threading.Thread(
            target=self.thread_install, args=(path, filename))
        thread.setDaemon(True)
        thread.start()

    def thread_install(self, path, filename):
        try:
            PROCNAME = "adb"

            for proc in psutil.process_iter():
                if proc.name() == PROCNAME:
                    proc.kill()

            f = tempfile.TemporaryFile()
            adbPath = "'" + os.path.dirname(os.path.realpath(__file__)) + "/adb'"
            apkFilePath = "'" + os.path.join(path, filename[0]) + "'"

            #killServerCommand = adbPath + " kill-server"
            installCommand = adbPath + " install -r " + apkFilePath
            command = installCommand + "\n"
            proc = subprocess.Popen(command, shell=True, stdout=f, stderr=f)
            self.addText(command)
            self.addText(u"Now installing...Please wait 10 second...")
            time.sleep(10)
            proc.terminate()
            # wait for the process to terminate otherwise the output is garbled
            proc.wait()

            # print saved output
            f.seek(0)  # rewind to the beginning of the file
            for line in str(f.read()).split("\n"):
                self.addText(line)
            f.close()
        except Exception, e:
            raise e

    def addText(self, text):
        self.text_input.text = self.text_input.text + text + "\n\n"


class ApkInstaller(App):
    pass


Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == '__main__':
    freeze_support()
    ApkInstaller().run()
