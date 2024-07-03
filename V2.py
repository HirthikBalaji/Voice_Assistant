import ollama
from main import talk, take_command

stop = ['.', '?', '!', ":", ";"]


def LLM_START():
    g = ollama.generate('dolphin-mistral:7b-v2', 'Hello! Am Hirthik! nice to meet you!', stream=True)
    response = message = ''
    for chunk in g:
        print(chunk['response'], end='', flush=True)
        response += chunk['response']
        message += chunk['response']
        for st in stop:
            if st in chunk['response']:
                talk(response)
                response = ''
    return message


def LLM():
    with open('system.md') as file:
        system = file.read()
    messages = [
        {
            'role': 'system',
            'content': system
        },
        {
            'role': 'user',
            'content': take_command()
        }
    ]
    Continue = True
    while Continue:
        g = ollama.chat('dolphin-mistral:7b-v2', messages=messages, stream=True)
        response = message = ''
        for chunk in g:
            print(chunk['message']['content'], end='', flush=True)
            response += chunk['message']['content']
            message += chunk['message']['content']
            for st in stop:
                if st in chunk['message']['content']:
                    talk(response)
                    response = ''
        assis = {
            'role': 'assistant',
            'content': message
        }
        messages.append(assis)
        user = {
            'role': 'user',
            'content': take_command()
        }
        messages.append(user)
        if "#quit" in message.lower():
            return


LLM_START()
LLM()
