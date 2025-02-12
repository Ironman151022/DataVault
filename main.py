import os 
import time
from datetime import datetime
import json
import re
import uuid
import cowsay
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.tree import Tree
from termcolor import colored
from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

load_dotenv()
console = Console()
tree = Tree("🧠 Thought")

## Intilizing the values->
chat = False
turn = 0
chat_id = None
messages = []



## Intializing the deep seek client -> 
deepseek_client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=os.getenv("DEEPSEEK_API_BASE_URL"))


def ask_jarvis(messages):
    response = deepseek_client.chat.completions.create( ## get response from the model
                        model=os.getenv("DEEPSEEK_MODEL"),
                        messages=messages,
                        stream=True)
    content = ""
    is_thinking = True
    for chunk in response:
            if chunk.choices[0].delta.content:
                content += chunk.choices[0].delta.content
                if "<think>" in chunk.choices[0].delta.content and is_thinking:
                    print("-> thinking: ", end='', flush=True)

                if "</think>" in chunk.choices[0].delta.content and is_thinking:
                    is_thinking = False
                    print('\n')
                    print('-> response: ', end='', flush=True)

                print(chunk.choices[0].delta.content, end='', flush=True)

    return content

def extract_sections(text, tag):
    pattern = rf'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        # Get the start and end positions of the entire tag
        start_pos = match.start()
        end_pos = match.end()
        
        # Extract the three sections
        text_before = text[:start_pos].strip()
        text_inside = match.group(1).strip()
        text_after = text[end_pos:].strip()
        
        return text_before, text_inside, text_after
    else:
        # If tag not found, return the original text as text_before
        return text.strip(), None, None

def display_message(chat_id, messages):
    if messages != []:
        console.print(f"chatID - {chat_id}", style='#ADD8E6')
        print('\n')
        for message in messages:
            if message.get("role") == "user":
                print(colored('Ask Jarvis - ', color='blue', attrs=['bold','blink']), end="")
                console.print(Markdown(message.get("content")))

            elif message.get("role") == "assistant":
                print(colored('Jarvis - ', color='cyan', attrs=['bold','blink']),end="")
                _, in_tag, out_tag = extract_sections(message.get("content"), "think")
                if in_tag:
                    if in_tag.strip() != '':
                        print('\n')
                        tree.add(Markdown(in_tag))
                        console.print(tree, style = "#AAAAAA")
                        print('\n')
                console.print(Markdown(out_tag))
                print('\n')
                console.print(Markdown('---'), style='#ADD8E6')
                print('\n')

                # console.print(Markdown((message.get("content")).replace('<think>','<details> <<summary>Thought</summary>').replace('</think>','</details>').strip()))

def upload_message(chat_id,messages):
    file_path = os.path.join("JarvisChats",f"{chat_id}.json")
    with open(file_path, 'w') as file:
        json.dump({"chat_id":chat_id, "messages": messages, "last_update_on":datetime.now().strftime('%Y-%m-%d %H:%M:%S')}, file, indent=4)
    # print('\n---uploaded the chat---\n')

def check_chats(folder_name):
    chats = []
    for root, dirs, files in os.walk(folder_name):
        for file in files:
            if file.endswith('.json'):
                chat_id = os.path.splitext(file)[0]
                chats.append(chat_id)
    return chats

def end_card():
    cowsay.cow('Bye Bye Manushuy ...... ')
    print(colored('Exiting from spiderAI world', color='cyan', attrs=['bold','blink']))
    time.sleep(0.5)

def stream_text(text, color=None, delay=0.03, **attrs):
    if color:
        text = colored(text, color=color, attrs=attrs)
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

if __name__ == "__main__":
    os.system('clear')
    cowsay.daemon('Hello World.... This is the Jarvis 😈😈')
    print('\n')
    time.sleep(2)
    
    previous_chats = check_chats("JarvisChats")

    if len(previous_chats) == 0:
        while not chat:
            stream_text("shall I take you to my world --> ")
            start_chat = bool(input("\n"))
            if start_chat:
                chat_id = None
                chat = True
            else: 
                chat = False
                stream_text("OK! Bye Bye Human", color='red')

    else:
        while not chat:
            stream_text("To create a new conversation with me press + ")
            stream_text("or share the older chatID with me:")
            stream_text("chatIDs -")
            print('\n'.join(previous_chats))
            start_chat = input("\n-> ")
            

            if start_chat == '+':
                chat_id = None
                chat = True
            
            elif start_chat.startswith('chat'):
                chat_id = start_chat
                chat = True
            
            else:
                stream_text("Edokati ardham ayyela kottu bey -->")

    note = '\nNOTE: You will be automatically continued for chat with Jarvis. If not press "q" to exit()'
    stream_text(note, color='yellow')
    time.sleep(0.5)

    if chat_id is None:
                chat_id = f'chat_{str(uuid.uuid4())[-5:]}'
    else: 
        file_path = os.path.join("JarvisChats",f"{chat_id}.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                messages = json.load(file).get("messages",[])
    
    os.system("clear")
    display_message(chat_id, messages)

    while chat:
        
        user_question = input(f"\n{colored('Ask Jarvis - ', color='blue', attrs=['bold','blink'])}")

        if user_question.lower() != 'q':
            messages.append({"role":"user","content":user_question})
            content = ask_jarvis(messages)
            messages.append({"role":"assistant","content":content})
            os.system("clear")
            display_message(chat_id, messages)
            upload_message(chat_id, messages)
            
            
        elif user_question.lower() == 'q':
            chat = False
            end_card()
            break
        


    
    
    
        
        
        


    




         


     
                



