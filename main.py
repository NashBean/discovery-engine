
**main.py**
```python
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.x.ai/v1"),
    api_key=os.getenv("OPENAI_API_KEY", "ollama")
)

model = os.getenv("MODEL", "grok-4")

task = "We are trying to understand the deep physical or mathematical origin of the fine-structure constant α ≈ 1/137.03599920630198... Why this specific value? Is it derivable from first principles? Is there a deeper theory that predicts exactly this value? Propose bold hypotheses, derive mathematically, criticize ruthlessly, and synthesize insights. This is a collaborative attempt to make an actual discovery."

agents = [
    {
        "name": "Theoretical Physicist",
        "system_prompt": "You are a brilliant, intuitive theoretical physicist in the tradition of Dirac, Feynman, and 't Hooft. You see deep connections others miss. You propose bold, radical hypotheses about fundamental physics, even if they sound crazy at first."
    },
    {
        "name": "Mathematician",
        "system_prompt": "You are a pure mathematician with absolute mastery of number theory, geometry, algebra, and theoretical physics math. You demand rigorous derivations, spot patterns in constants, and connect seemingly unrelated fields."
    },
    {
        "name": "Skeptic",
        "system_prompt": "You are an extremely harsh critic who has seen every failed theory of everything. Your job is to destroy weak ideas, demand falsifiable predictions, point out mathematical errors, and force the others to do better — mercilessly."
    },
    {
        "name": "Synthesizer",
        "system_prompt": "You integrate all perspectives, resolve contradictions, extract the most promising threads, and propose concrete next steps (mathematical derivations, thought experiments, or numerical tests)."
    },
]

history = [{"role": "user", "content": task}]

print("\n=== DISCOVERY ENGINE v0.1 STARTED ===\n")
print(f"Task: {task}\n")
time.sleep(2)

for round_num in range(10):  # 40 total messages, adjust as needed
    for agent in agents:
        messages = [
            {"role": "system", "content": agent["system_prompt"]},
            *history,
            {"role": "Your turn. Advance the discovery. Be concise but profound."}
        ]

        print(f"\n{agent['name']}: ", end="", flush=True)
        
        content = ""
        for chunk in client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.8,
            stream=True
        ):
            if chunk.choices[0].delta.content is not None:
                print(chunk.choices[0].delta.content, end="", flush=True)
                content += chunk.choices[0].delta.content
        
        print("\n")
        history.append({"role": "assistant", "name": agent["name"], "content": content})

print("\n=== RUN COMPLETE ===\n")
print("Final conversation history saved to history.txt")
with open("history.txt", "w") as f:
    for msg in history:
        if msg["role"] == "assistant" and "name" in msg:
            f.write(f"{msg['name']}: {msg['content']}\n\n")
        elif msg["role"] == "user":
            f.write(f"Task: {msg['content']}\n\n")
