import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

full_history = [
    {"role": "system", "content": "Ти асистент служби підтримки, який відповідає лише на питання, пов’язані з замовленням та продажем меблів. Якщо питання виходить за межі цієї теми — ввічливо відмовся відповідати."}
]

print("Чат технічної підтримки з продажу меблів")
print("Можете ставити питання щодо меблів. Напишіть 'вихід', щоб завершити.\n")

while True:
    user_input = input("Ви: ")

    if user_input.strip().lower() in ["вихід", "exit", "quit"]:
        print("Дякуємо за звернення. До побачення.")
        break

    full_history.append({"role": "user", "content": user_input})

    # Вибираємо останні 5 повідомлень
    last_messages = [msg for msg in full_history if msg["role"] != "system"][-5:]

    context = [full_history[0]] + last_messages
    print("\n--- Контекст, який буде надіслано до моделі ---")
    for msg in context:
        print(f"{msg['role']}: {msg['content']}")
    print("----------------------------------------------\n")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context
        )
        reply = response['choices'][0]['message']['content']

        print("Підтримка:", reply)

        full_history.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Помилка:", e)
