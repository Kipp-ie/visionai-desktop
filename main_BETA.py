from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow
from ollama import chat
from ollama import ChatResponse
from cv2 import *

messages = []
USER = 'user'
ASSISTANT = 'assistant'

response_begin: ChatResponse = chat(model='openhermes', messages=[
    {
      'role': 'user',
      'content': "You are a personal assistant, the user just opened the application, greet them please and keep it short.",
    },
  ])
print(response_begin.message.content)
while True:
  prompt = input("")
  cam_port = 0
  cam = VideoCapture(cam_port)
  result, image = cam.read()
  if result:
    imshow("img", image)
    imwrite("img.png", image)
    waitKey(0)
    destroyWindow("img")

  response2: ChatResponse = chat(model='moondream', messages=[
    {
      'role': 'user',
      'content': "Describe the image",
      'images': ["./img.png"]
    },
  ])

  print("Vision model report: " + response2.message.content + "\n")

  response: ChatResponse = chat(model='openhermes', messages=messages + [
    {
      'role': 'user',
      'content': "Context: You are a personal assistant, you have access to a camera, don't mention what you can see in the camera if it isn't useful to the prompt, the feed is now seeing: " + response2.message.content + ". Prompt: " + prompt,
    },
  ])
  print("LLM Report: " + response.message.content)
  messages += [
    {'role': 'user', 'content': prompt},
    {'role': 'assistant', 'content': response.message.content},
  ]



