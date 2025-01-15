# AI-storybook-maker
An interactive Kivy application that helps users create children's storybooks with AI-generated text and illustrations. It allows users to generate creative stories, illustrations, and text-to-speech audio for their storybooks, and export them as PDFs.

# AI 동화책 메이커 📚🤖
아이들을 위한 창의적인 동화책을 손쉽게 제작할 수 있는 Kivy 기반 애플리케이션입니다. AI를 활용하여 이야기를 작성하고, 그림을 생성하며, 음성으로 읽어주는 기능까지 제공합니다.

<details>
<summary>README (한국어)</summary>

## 주요 기능 ✨
- **AI 스토리 생성**: 어린이를 위한 간결하고 감성적인 4페이지 분량의 동화책 이야기를 생성합니다.
- **AI 그림 생성**: 각 페이지에 적합한 따뜻하고 화려한 동화책 이미지를 생성합니다.
- **텍스트 음성 변환(TTS)**: 동화 내용을 음성으로 들려줍니다.
- **PDF 저장 및 공유**: 동화책을 PDF로 저장하고 공유할 수 있습니다.

---

## 사용된 API 및 라이브러리 📋
- **OpenAI API**: GPT-4 모델을 이용한 스토리 생성 및 DALL-E 모델을 이용한 이미지 생성.
- **ReportLab**: PDF 생성.
- **Plyer**: 파일 저장 및 공유.
- **Pygame**: 텍스트 음성 변환(TTS) 출력.
- **Kivy**: GUI 개발.

---

## 설치 및 실행 방법 ⚙️
1. **필요 라이브러리 설치**
   ```bash
   pip install kivy plyer reportlab pygame openai python-dotenv requests
2. **.env 파일 생성**
   - 프로젝트 루트 디렉토리에 ```.env``` 파일을 생성하고 OpenAI API 키를 입력합니다.
3. **어플리케이션 실행**
   ```bash
   python main.py

## 기대 효과 🎯
- **창의력 증진**: AI를 활용한 스토리와 그림 생성으로 창의적인 동화책 제작 가능.
- **시간 절약**: 간단한 입력만으로 완성도 높은 동화책 제작.
- **다양한 활용성**: 부모, 교사, 어린이를 위한 맞춤형 콘텐츠 제작 가능.

## 기여 방법 🤝
1. 이 레포지토리를 포크합니다.
2. 새로운 브랜치를 생성합니다: ```git checkout -b feature/your-feature-name```
3. 변경 사항을 커밋합니다: ```git commit -m 'Add some feature'```
4. 브랜치에 푸시합니다: ```git push origin feature/your-feature-name```
5. 풀 리퀘스트를 생성합니다.

## 라이선스 📝
이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](./LICENSE)를 참조하세요.
</details>

---

<details> <summary>README (English)</summary>
  
## Key Features ✨
- **AI Story Generation**: Generates concise and emotional 4-page storybooks tailored for children.
- **AI Illustration Creation**: Produces colorful and warm storybook illustrations matching each page.
- **Text-to-Speech (TTS)**: Converts the story text into speech for an immersive experience.
- **PDF Save and Share**: Exports storybooks as PDFs for saving and sharing.

---

## APIs and Libraries Used 📋
- **OpenAI API**: GPT-4 for story generation and DALL-E for illustration creation.
- **ReportLab**: PDF generation.
- **Plyer**: File saving and sharing.
- **Pygame**: Text-to-Speech (TTS) audio playback.
- **Kivy**: GUI development.

## Installation and Execution ⚙️
1. **Install Required Libraries**
   ```bash
   pip install kivy plyer reportlab pygame openai python-dotenv requests
   
2. **Create .env File**
   - Create a ```.env``` file in the project root directory and add your OpenAI API key:
3. **Run the Application**
   ```bash
   python main.py

## Benefits 🎯
- **Boost Creativity**: Create imaginative storybooks with AI-generated stories and illustrations.
- **Time-Saving**: Quickly produce high-quality storybooks with minimal input.
- **Versatility**: Suitable for parents, teachers, and children to create personalized content.

## Contribution 🤝
1. Fork this repository.
2. Create a new branch: ```git checkout -b feature/your-feature-name```
3. Commit your changes: ```git commit -m 'Add some feature'```
4. Push to the branch: ```git push origin feature/your-feature-name```
5. Open a pull request.

## 라이선스 📝
This project is licensed under the MIT License. See [LICENSE](./LICENSE) for more details. 
</details>
   
