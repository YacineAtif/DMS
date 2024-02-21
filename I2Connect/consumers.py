# I2Connect/consumers.py

import asyncio
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from Sensors.traffic_data import get_simulated_traffic_data
from Sensors.driver_data import get_updated_driver_state_data


class TrafficDataConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keep_running = True
        self.reset_simulation = False  # Instance variable to track reset state

    async def connect(self):
        self.reset_simulation = True  # Reset simulation at start
        await self.accept()
        asyncio.create_task(self.send_data_loop())

    async def send_data_loop(self):
        while self.keep_running:
            traffic_data = get_simulated_traffic_data(reset=self.reset_simulation)  # function to fetch traffic data
            driver_data = get_updated_driver_state_data(reset=self.reset_simulation)

            combined_data = {
                'traffic': traffic_data,
                'driver': driver_data,
            }

            # Once we have reset, set the flag back to False
            if self.reset_simulation:
                self.reset_simulation = False

            await self.send(text_data=json.dumps(combined_data))
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

        if action == 'reset':
            # Reset the simulated data
            self.reset_simulation = True

