# I2Connect/consumers.py

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Sensors.traffic_data import get_simulated_traffic_data


class TrafficDataConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keep_running = True
        self.reset_simulation = False  # Instance variable to track reset state

    async def connect(self):
        print("Conection OK ")
        await self.accept()
        asyncio.create_task(self.send_data_loop())

    async def send_data_loop(self):
        while self.keep_running:
            data = get_simulated_traffic_data(reset=self.reset_simulation)  # function to fetch traffic data

            # Once we have reset, set the flag back to False
            if self.reset_simulation:
                self.reset_simulation = False

            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(1)  # Adjust as needed

    async def disconnect(self, close_code):
        await self.close()  # Close the WebSocket connection

    async def receive(self, text_data):

        text_data_json = json.loads(text_data)
        action = text_data_json['action']

        if action == 'stop':
            # Implement logic to stop the simulation
            self.keep_running = False
            self.reset_simulation = True

        if action == 'start':
            # Logic to start the simulation
            self.keep_running = True
            self.reset_simulation = True
            asyncio.create_task(self.send_data_loop())

        if action == 'pause':
            # Implement logic to pause the simulation
            self.keep_running = False

        if action == 'resume':
            # Logic to start the simulation
            self.keep_running = True
            asyncio.create_task(self.send_data_loop())
