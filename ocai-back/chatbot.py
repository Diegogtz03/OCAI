import google.generativeai as genai

genai.configure(api_key="AIzaSyCg-nr4gR-TOJ27425B8OaZmvDIiktcT-E")

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat()

user = ""
while user != "bye":
    user = input("write: ")
    response = chat.send_message(user, session_id="1234")
    print(response.text)

print(chat.history)