#!/usr/bin/env python3
from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
import os
import datetime
import os.path
app = FastAPI()

filename = ""
@app.get('/screenshot/{domain}')
async def screenshot(domain : str, response_class=FileResponse):
    global filename
    
    current_time = datetime.datetime.now()
    used_time = f"-{current_time.hour}-{current_time.minute}-{current_time.second}"
    filename = f"{domain}{used_time}.jpg"
    os.system(f'wkhtmltoimage {domain} {filename}')
    
   # response = RedirectResponse(url=f"/getfile/{filename}")
    #return response
    return {"filename": filename}

@app.get('/getfile/{filename}')
async def getfile(filename: str, response_class=FileResponse):
    return FileResponse(f'{filename}')
   #  try:
           # file_exists = os.path.exists(filename)
           # print(file_exists)
           # if true:
            
            #return FileResponse(f'{filename}')
            #file_exists = exists(path_to_file)
                #while contents := file.file.read(1024 * 1024):
                 #   f.write(contents)
                #    else:
                     #   return {"message": "There was an error get file"}
                    
        #except Exception:
            #return {"message": "There was an error get file"}
        #finally:
         ##   file.file.close()

      #  return {"message": f"Successfully uploaded {file.filename}"}
