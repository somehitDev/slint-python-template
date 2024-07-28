"""
Template of Slint for Python
"""
import os, slint, urllib.request, json
from . import __path__

views_dir = os.path.join(__path__[0], "ui")

def main():
    ui = slint.load_file(os.path.join(views_dir, "AppWindow.slint"), style = "fluent", include_paths = [ views_dir ])

    class App(ui.AppWindow):
        @slint.callback
        def homeInitCallback(self):
            print("page `Home` initialized!")

        @slint.callback
        def httpFetchCallback(self, url:str) -> str:
            with urllib.request.urlopen(url) as resp:
                return json.dumps(
                    json.loads(
                        resp.read().decode("utf-8")
                    ),
                    indent = 4
                )

    app = App()
    app.run()
