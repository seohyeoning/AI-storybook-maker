from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from plyer import filechooser
from reportlab.pdfgen import canvas
from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import requests 
import pygame
from io import BytesIO
import tempfile

load_dotenv('C:/Users/user/Desktop/psh/수업자료/2501/gpt/gpt.env')
api_key = os.getenv('API_KEY')
client = OpenAI(api_key = api_key)


# Load KV file
Builder.load_file('C:/Users/user/Desktop/psh/project/KIVY/StoryBook_maker/myapp.kv')

class MyApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.pages = []  # List to store the story pages
        self.current_page_index = 0  # Index to track the current page
        self.created_stroy = None
        
    def text_to_speech(self):
        page_text = self.ids.story_output_page.text.strip() # 불필요한 공백으로 인한 오류 방지

        if not page_text:
            print("No text available for TTS.")
            return

        try:
            # 현재 페이지 이름 가져오기
            if self.pages:
                current_page_name = self.pages[self.current_page_index]['page_name'].replace(" ", "_")
            else:
                current_page_name = "unknown_page"

            # 음성 파일명 설정
            audio_file_path = Path(__file__).parent / f"{current_page_name}_speech.mp3"

            # OpenAI TTS API 호출
            audio_response = client.audio.speech.create(
                model="tts-1",
                voice="shimmer",
                input=page_text
            )

            # 임시 파일 생성
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") # 1. 실행중 생긴 음성 데이터를 임시파일에 생성 
            temp_file.write(audio_response.content)
            temp_file.close()

            # 임시 파일을 지정된 경로로 이동
            os.rename(temp_file.name, audio_file_path) # 2. os.rename으로 경로를 변경해 저장

            # Pygame으로 음성 재생
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # 재생이 끝날 때까지 대기
                pass

            print(f"Audio saved at: {audio_file_path}")

        except Exception as e:
            print(f"TTS 오류 발생: {str(e)}")

                
    def generate_story(self, step):
        if step == "story":
            input_story = f"{self.ids.story_input.text}"

            prompt = (
                "아래 입력을 참고하여, 어린이를 위한 4쪽짜리 그림책 이야기를 작성해주세요. "
                "각 페이지는 간결하고 감성적으로 작성되며, 어린이가 이해하기 쉬운 언어를 사용해주세요. "
                "입력에 따라 창의적으로 이야기를 구성해주세요.\n\n"
                "### 입력:\n"
                f"{input_story}\n\n"
                "### 형식:\n"
                "- 페이지 1: 이야기를 시작하는 도입부.\n"
                "- 페이지 2: 주요 캐릭터가 만나는 순간.\n"
                "- 페이지 3: 캐릭터들이 함께 시간을 보내며 즐거워하는 모습.\n"
                "- 페이지 4: 이야기를 마무리하며 따뜻한 교훈을 전달.\n\n"
                "페이지별 텍스트를 아래 형식에 따라 작성해주세요:\n"
                "- 페이지 1: [텍스트]\n"
                "- 페이지 2: [텍스트]\n"
                "- 페이지 3: [텍스트]\n"
                "- 페이지 4: [텍스트]"
            )
            
            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a creative assistant for generating children's storybooks"},
                    {"role": "user", "content": prompt}
                ],
                model="gpt-4",
                temperature=0.7,
                max_tokens=1024
            )
            created_story = response.choices[0].message.content.strip()
            self.ids.story_output.text = created_story
            self.created_stroy = created_story
            print(created_story)
            
        elif step == "book":
            # 페이지별 텍스트와 이미지 초기화
            self.pages = []
            for line in self.created_stroy.split("\n"):
                if line.startswith("- 페이지"):
                    page_key, page_text = line.split(": ", 1)
                    self.pages.append({"page_name": page_key.strip(), "text": page_text.strip()})

            # 첫 페이지 설정
            self.current_page_index = 0
            self.update_page_display()

            # 페이지별 이미지 생성
            for page in self.pages:
                self.generate_image(page["text"], page["page_name"])
            
                

    def generate_image(self, text, page_name):
        # OpenAI API 프롬프트
        prompt = (
            f"Create an illustration for a children's storybook. The page text is: {text}. "
            "The illustration should match the text and be colorful, warm, and suitable for a children's storybook."
        )
        try:
            # OpenAI API 호출
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt, 
                size="1024x1024",# 1024x1024
                quality="standard", # hd
                n=1, # 이미지 개수
            )

        
            # Fetch the image from the URL
            image_url = response.data[0].url
            # 이미지 다운로드
            image_path = f"{page_name.replace(' ', '_')}.png"
            image_response = requests.get(image_url)
            with open(image_path, "wb") as f:
                f.write(image_response.content)

            # Kivy Image 위젯 업데이트
            self.ids.illustration_output.source = image_path
            print(f"{page_name} image saved and displayed at {image_path}")

        except Exception as e:
            print(f"Error generating image for {page_name}: {e}")

        
    
    def save_to_pdf(self):
        save_path = filechooser.save_file(title="Select path to save PDF", filters=[("PDF files", "*.pdf")])
        if not save_path:
            print("File save dialog was cancelled.")
            return
        if not save_path[0].endswith(".pdf"):
            save_path[0] += ".pdf"
        self.create_pdf(save_path[0])


    def create_pdf(self, save_path):
        try:
            if not self.pages:
                print("No pages available for the PDF.")
                return

            c = canvas.Canvas(save_path)
            c.setFont("Helvetica", 14)

            # 페이지별 처리
            for page in self.pages:
                page_text = page["text"]
                illustration_path = f"{page['page_name'].replace(' ', '_')}.png"

                # 텍스트 추가
                y_position = 750
                lines = page_text.split("\n")
                for line in lines:
                    c.drawString(50, y_position, line)
                    y_position -= 20

                # 이미지 추가
                if os.path.exists(illustration_path):
                    c.drawImage(illustration_path, 50, y_position - 300, width=400, height=300)
                else:
                    print(f"Illustration not found for {page['page_name']}")

                # 페이지 넘김
                c.showPage()

            c.save()
            print(f"PDF saved successfully at: {save_path}")
        except Exception as e:
            print(f"Error creating PDF: {e}")


    def share_pdf(self):
        try:
            # 공유할 PDF 파일 경로
            pdf_path = "generated_book.pdf"  # 기본 경로를 사용하거나 필요한 경로로 변경

            # 파일 존재 여부 확인
            if not os.path.exists(pdf_path):
                print(f"PDF file not found: {pdf_path}")
                return

            # Plyer filechooser로 파일 공유
            filechooser.share(pdf_path)
            print(f"PDF shared successfully: {pdf_path}")

        except Exception as e:
            print(f"Error sharing PDF: {e}")


    def update_page_display(self):
        if self.pages:
            # 현재 페이지 데이터 가져오기
            current_page = self.pages[self.current_page_index]
            self.ids.story_output_page.text = current_page["text"]

            # 이미지 업데이트
            image_path = f"{current_page['page_name'].replace(' ', '_')}.png"
            if os.path.exists(image_path):
                self.ids.illustration_output.source = image_path
            else:
                self.ids.illustration_output.source = ""
        else:
            self.ids.story_output_page.text = "No story available."
            self.ids.illustration_output.source = ""
            
    def next_page(self):
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.update_page_display()
        else:
            print("Already at the last page.")

    def previous_page(self):
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.update_page_display()
        else:
            print("Already at the first page.")

class BookMakerApp(App):
    def build(self):
        return MyApp()

if __name__ == "__main__":
    BookMakerApp().run()
