"""
Template of Slint for Python
"""
import os, slint, urllib.request, json, pygal
from screeninfo import get_monitors
from pygal.style import DefaultStyle
from . import __path__

views_dir = os.path.join(__path__[0], "ui")

def main():
    ui = slint.load_file(os.path.join(views_dir, "AppWindow.slint"), include_paths = [ views_dir ])

    class App(ui.AppWindow):
        def __init__(self):
            super().__init__()

            screen = [
                monitor
                for monitor in get_monitors()
                if monitor.is_primary
            ][0]
            self.size = slint.ListModel([ 1000, 700 ])
            self.maxSize = slint.ListModel([ screen.width, screen.height ])

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
            
        @slint.callback
        def drawChartCallback(self) -> str:
            chart_style = DefaultStyle()
            chart_style.background = "white"

            line_chart = pygal.Line(style = chart_style)
            line_chart.title = 'Browser usage evolution (in %)'
            line_chart.x_labels = map(str, range(2002, 2013))
            line_chart.add('Firefox', [None, None,    0, 16.6,   25,   31, 36.4, 45.5, 46.3, 42.8, 37.1])
            line_chart.add('Chrome',  [None, None, None, None, None, None,    0,  3.9, 10.8, 23.8, 35.3])
            line_chart.add('IE',      [85.8, 84.6, 84.7, 74.5,   66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
            line_chart.add('Others',  [14.2, 15.4, 15.3,  8.9,    9, 10.4,  8.9,  5.8,  6.7,  6.8,  7.5])
            line_chart.render_to_file(os.path.join(views_dir, "charts", "chart.svg"), width = self.maxSize[0], height = self.maxSize[1])

    app = App()
    app.run()
