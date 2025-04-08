import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

full_history = [
    {"role": "system", "content": "Ти український помічник, який відповідає чітко і доброзичливо."}
]

print("Чат з обмеженим контекстом (3 останні пари). Напиши 'вихід' для завершення.")

while True:
    user_input = input("👤 Ви: ")

    if user_input.strip().lower() in ["вихід", "exit", "quit"]:
        print("До побачення!")
        break

    full_history.append({"role": "user", "content": user_input})

    # Знаходимо останні 3 пари user + assistant (всього до 6 повідомлень)
    last_pairs = []
    for msg in reversed(full_history[1:]):  # без system
        if msg["role"] in ["user", "assistant"]:
            last_pairs.insert(0, msg)
        if len(last_pairs) == 6:
            break

    # Формуємо контекст з system + останні 3 пари
    context = [full_history[0]] + last_pairs

    print("\nКонтекст, що надсилається в API:")
    for m in context:
        role = "Ви" if m["role"] == "user" else "ChatGPT" if m["role"] == "assistant" else "Система"
        print(f"{role}: {m['content']}")
    print("------")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=context
        )

        reply = response['choices'][0]['message']['content']
        print("ChatGPT:", reply)

        # Додаємо відповідь до історії
        full_history.append({"role": "assistant", "content": reply})

    except Exception as e:
        print("Помилка:", e)
