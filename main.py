from fastapi import FastAPI
import nest_asyncio
from pyngrok import ngrok
import uvicorn
import os
import asyncio
import yaml

### 함수 선언
def convertIndexToName(photoIndexList):
  yamlfile = yaml.safe_load(open("./yolov5/Fruits-and-Vegetables-3/data.yaml"))
  photoNameList = set()
  for i in photoIndexList:
    photoNameList.add(yamlfile['names'][int(i)])
  return photoNameList

def createDetectFile(detectImageCommandStr):
  os.system(detectImageCommandStr)

def getPhotoIndex(file_path) :
  food_list = []
  with open(file_path, "r") as f :
    example = f.readlines()
    for line in example:
      food = line[0:2]
      food_list.append(food)
  photoIndexList = food_list
  return food_list


## FastAPI
app = FastAPI()

@app.get("/")
# async def root():
def root():
    return {"message": "Hello World"}

imgUrl = ""

@app.get("/items/")
async def read_item(imageUrl: str = ""):
  imgUrl = imageUrl
  detectImageCommandStr = "python detect.py --save-txt --weights /yolov5/best.pt --img 416 --conf 0.4 --source " + imageUrl
  createDetectFile(detectImageCommandStr)

  # yaml에서 과일의 인덱스 번호 뽑기
  sliceImgUrl = imageUrl[0:len(imageUrl)-4]
  getPhotoIndex("./yolov5/runs/detect/exp/labels/"+"15834_3150_1449"+".txt")

  # 과일 이름 리턴
  return convertIndexToName(getPhotoIndex("./yolov5/runs/detect/exp/labels/"+"15834_3150_1449"+".txt"))

# TODO: 서버에서 받은 사진을 detect한 후에 생성된 txt 파일을 가져오기
# 문제.. 파일이 생성되기 전에 txt 파일을 가져옴
# await 잘 써서 동기처리 해야함

@app.get("/test")
async def test():
  return {"test"}

# ngrok_tunnel = ngrok.connect(8000)
# print('Public URL:', ngrok_tunnel.public_url)
# nest_asyncio.apply()
# uvicorn.run(app, port=8000)