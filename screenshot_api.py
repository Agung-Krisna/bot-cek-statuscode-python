#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse
import os
import datetime
app = FastAPI()

@app.get('/screenshot/{domain}')
async def screenshot(domain : str, response_class=FileResponse):
    current_time = datetime.datetime.now()
    used_time = f"-{current_time.hour}-{current_time.minute}-{current_time.second}"
    os.system(f'wkhtmltoimage {domain} {domain}{used_time}.jpg')
    return FileResponse(f'{domain}{used_time}.jpg')