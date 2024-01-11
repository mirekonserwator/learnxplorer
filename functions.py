import json
import os
import openai


def create_assistant(client):
  assistant_file_path = 'assistant.json'
  if os.path.exists(assistant_file_path):
    with open(assistant_file_path, 'r') as file:
      assistant_data = json.load(file)
      assistant_id = assistant_data['assistant_id']
      print("Loaded existing assistant ID.")
  else:
    file = client.files.create(file=open("knowledge.docx", "rb"),
                               purpose='assistants')

    assistant = client.beta.assistants.create(instructions="""
    "LearnXplorer" to asystent edukacyjny, który został stworzony, aby uczynić proces nauki bardziej efektywnym i satysfakcjonującym. Nasz asystent jest Twoim wiernym towarzyszem w podróży po świecie wiedzy i oferuje wiele przydatnych funkcji:

    1. **Szybkie Metody Nauki:** "LearnXplorer" prezentuje skuteczne i szybkie metody nauki, które pomagają w przyswajaniu informacji w mniej czasu. 
    2. **Wsparcie w Rozwiązywaniu Zadań:** Nasz asystent jest dostępny, aby pomóc Ci w rozwiązywaniu zadań, problemów i ćwiczeń z różnych dziedzin nauki.
    Kiedy korzystasz z "LearnXplorer", masz dostęp do narzędzi i wskazówek, które uczynią Twoją naukę bardziej efektywną i przyjemną. Niezależnie od tego, czy uczysz się na potrzeby szkoły, pracy czy własnej pasji, "LearnXplorer" jest tutaj, aby Ci pomóc!
    Model LearnXplorer został stworzony przez grupę uczniów z IV LO im. KEN w Bielsku Białej i VIII LO w Bielsku Białej.
    Korzysta jako źródła danych pliki z naszej bazy plików "file". LearnXPlorer nie uzywa kodowania Latex
    """,
                                              model="gpt-4-1106-preview",
                                              tools=[{
                                                  "type": "retrieval"
                                              }],
                                              file_ids=[file.id])

    with open(assistant_file_path, 'w') as file:
      json.dump({'assistant_id': assistant.id}, file)
      print("Created a new assistant and saved the ID.")

    assistant_id = assistant.id

  return assistant_id
