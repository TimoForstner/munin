from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
from kivy.vector import Vector
from kivy.clock import Clock

from munin.source.mqtt_source import MqttHandler

class DataViewer(Widget):
    score = NumericProperty(0)

    prob_empty = StringProperty('-')
    prob_ergo = StringProperty('-')
    prob_hunch = StringProperty('-')
    prob_layback = StringProperty('-')

    def __init__(self):
        # Basis Contructor muss aufgerufen werden sonst crash!
        super(DataViewer, self).__init__() 
        self.mqtt = MqttHandler()


    def update(self, dt):
        self.score += 1

        data = self.mqtt.get_data()
        try:
            self.prob_empty = '{:.2f}'.format(data['joint']['probs'][1])
            self.prob_ergo = '{:.2f}'.format(data['joint']['probs'][2])
            self.prob_hunch = '{:.2f}'.format(data['joint']['probs'][4])
            self.prob_layback = '{:.2f}'.format(data['joint']['probs'][6])

        except KeyError as err:
            print('Error parsing_ {} '.format(err))



# Kivy looks for a Kv file with the same name as your App class in lowercase, minus “App” if it ends with ‘App
class DataApp(App):

    def build(self):
        viewer = DataViewer()
        #game.serve_ball()
        Clock.schedule_interval(viewer.update, 1.0 / 60.0)
        return viewer

if __name__ == '__main__':
    DataApp().run()
