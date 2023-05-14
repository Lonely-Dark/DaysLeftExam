#!/usr/bin/env python
# -*- coding: utf8 -*-

# ---Lonely_Dark---
# Python 3.11

import asyncio
import os
import time
import datetime

import aiohttp
import dotenv
import aioschedule as schedule
from json import loads
from loguru import logger


class MyVk:
    def __init__(self):
        """
        Class for simple use vk api
        """

        self.token = dotenv.dotenv_values(f"{os.getcwd()}/.env")['token']
        self.session = aiohttp.ClientSession()
        self.logger = logger

    async def set_status(self, text: str) -> None:
        """
        Set status from text
        :param text: text to set
        :return: None
        """

        url = 'https://api.vk.com/method/status.set'
        params = {'access_token': self.token, 'v': '5.131', 'text': text}
        async with self.session.post(url, data=params) as response:
            data = loads(await response.text())
            self.logger.debug(data)


async def main():
    my_vk = MyVk()

    today = datetime.date.today()
    future = datetime.date(2023, 5, 14)
    diff = (future - today).days

    text = f"Дней до ЕГЭ: {diff}"

    status = await my_vk.set_status(text)


if __name__ == '__main__':
    schedule.every().day.at("00:00").do(main)
    loop = asyncio.get_event_loop()
    while True:
        loop.run_until_complete(schedule.run_pending())
        time.sleep(0.1)
