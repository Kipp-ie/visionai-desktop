import flet as ft
from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow
from ollama import chat
from ollama import ChatResponse

messages = []
USER = 'user'
ASSISTANT = 'assistant'

def main(page: ft.Page):
    page.title = "VisionAI Desktop"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    answer = ft.TextField(
            value="Hi, i'm your personal AI assistant, what can i help you with today?",
            multiline=True,
            min_lines=1,
            max_lines=8,
            read_only=True,
        )

    prompt = ft.TextField(label="Prompt",)

    def prompt_send(e):
        messages=[]
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

        print(prompt.value)

        response: ChatResponse = chat(model='openhermes', messages=messages + [
            {
                'role': 'user',
                'content': "Context: You are a personal assistant, you have access to a camera, don't mention what you can see in the camera if it isn't useful to the prompt, the feed is now seeing: " + response2.message.content + ". Prompt: " + prompt.value,
            },
        ])
        answer.value = response.message.content
        messages += [
            {'role': 'user', 'content': prompt.value},
            {'role': 'assistant', 'content': response.message.content},
        ]
        page.update()

    page.add(
        ft.Row(
            [

                answer

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [

                prompt

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        ft.Row(
            [

                ft.FilledButton(text="Send", icon="SEND", on_click=prompt_send)

            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    )

ft.app(main)