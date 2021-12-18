

import streamlit as st
import pandas as pd
import numpy as np

import io
import requests

from PIL import Image,ImageDraw,ImageFont


st.title('Jun First Appppp')


st.write('データフレーム')
st.write("データフレーム")

st.write(
  pd.DataFrame({
    '1st column':[1,2,3,4],
    '2st column':[10,20,300,4000]
  })
)

###マジックコマンド↓
"""
# My First App
こんな感じでコマンドを使用できる。Markdown対応。

"""

if st.checkbox('Show DataFrame'):
  chart_df=pd.DataFrame(
    np.random.randn(20,3),
    columns=['a','b','c']
  )

  st.line_chart(chart_df)


###文字入れ用関数
def add_text_to_omage(img,text,font_path,font_size,font_color,height,width,maxlength=740):
# def add_text_to_omage(img,text,font_path,font_size,font_color,height,width):
    position=(width,height)
    font=ImageFont.truetype(font_path,font_size)
    draw=ImageDraw.Draw(img)
    
    draw.text(position,text,font_color,font=font)
    # draw.text(position,text,font_color)
    
    return img



###
st.title('顔認識アプリ')

####face api key
subscription_key='91c7b7e6b0ab4d9a9f038e7a75be2935'
assert subscription_key
face_api_url='https://20211207-az-sai.cognitiveservices.azure.com/face/v1.0/detect'


uploaded_file=st.file_uploader("choose image...",type='jpg')

if uploaded_file is not None:
  img=Image.open(uploaded_file)
  
  # img=Image.open('azure_info/face06.jpg')
  # with open('azure_info/face06.jpg','rb') as f:
  #     binary_img=f.read()

  ####バイナリ形式で画像取得
  with io.BytesIO() as output:
      img.save(output,format='JPEG')
      binary_img=output.getvalue()  ##バイナリ取得
  
  
  ####face apiで画像の解析実行
  headers={
      'Content-Type':'application/octet-stream',
      'Ocp-Apim-Subscription-Key': subscription_key
  }

  params={
      'returnFaceId':'true',
      'returnFaceAttributes':'age,gender,headPose,smile,facialHair,makeup'
  }

  res=requests.post(face_api_url,params=params,headers=headers,data=binary_img)
  
  
  ####解析結果をjson形式で取得
  results=res.json()

  ####複数人分for
  for result in results:
      rect=result['faceRectangle']
      # rect
      age=result['faceAttributes']['age']
      age=str(int(age))
      # age
      gender=result['faceAttributes']['gender']
      
      draw = ImageDraw.Draw(img)
      
      
      ####rectangle draw
      draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='green',width=10)

      ####age draw
      text_age=age
      font_path='arial.ttf'
      font_size=int(rect['width']/5)
      font_color=(240,240,240)
      height=rect['top']-int(rect['width']/5)
      width=rect['left']
      img=add_text_to_omage(img,text_age,font_path,font_size,font_color,height,width)

      ####gender draw
      text_gender=gender
      font_path='arial.ttf'
      font_size=int(rect['width']/5)
      font_color=(240,240,240)
      height=rect['top']-int(rect['width']/5)
      width=rect['left']+int(rect['width']/5*1.5)
      img=add_text_to_omage(img,text_gender,font_path,font_size,font_color,height,width)
  
  
  st.image(img, caption='Uploaded Image.',use_column_width=True)





















