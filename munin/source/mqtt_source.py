import json

import paho.mqtt.client as mqtt


class MqttHandler:

    def __init__(self):
        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.connect("192.168.178.83", 1883, 60)

        # Start in new thread without blocking:
        client.loop_start()

        self._data = {}


    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe("/device/dc00002/eval")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        # print(msg.topic+" "+str(msg.payload))

        str_data = msg.payload.decode('utf-8')

        try:
            data = json.loads(str_data)

            # data['cnt'] = data['header']['cnt']
            # data['acc_x'] = data['acc']['x']
            # data['acc_y'] = data['acc']['y']
            # data['acc_z'] = data['acc']['z']
            # data['time'] = data['header']['time']
            # del data['acc']

            print('Data: {}'.format(data))

            self._data = data

        except json.JSONDecodeError as err:
            print('Decode error with message:\n{}'.format(str_data))

    def get_data(self):
        return self._data

if __name__ == '__main__':

    import time

    MqttHandler()

    time.sleep(10)
