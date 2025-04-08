import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {"role": "system", "content": "Ти розумний український асистент, який відповідає зрозуміло та доброзичливо."}
]

print("Почнемо діалог із ChatGPT 3.5. Напиши 'вихід', щоб завершити.")

while True:
    user_input = input("Ви: ")

    if user_input.strip().lower() in ["вихід", "exit", "quit"]:
        print("Дякую за розмову! До зустрічі.")
        break

    if user_input.strip().lower() == "контекст":
        print("\nКонтекст діалогу:")
        for m in messages:
            role = "Ви" if m["role"] == "user" else "ChatGPT" if m["role"] == "assistant" else "Система"
            print(f"{role}: {m['content']}\n")
        continue
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        reply = response['choices'][0]['message']['content']

        messages.append({"role": "assistant", "content": reply})

        print("ChatGPT:", reply)

    except Exception as e:
        print("Сталася помилка:", e)
