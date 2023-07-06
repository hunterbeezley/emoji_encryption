from flask import Flask, request, render_template
import random
import pyperclip
import json

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, object) and hasattr(obj, '__html__'):
            return obj.__html__()
        return super().default(obj)

def generate_random_mapping():
    emojis = ['😀', '😃', '😄', '😁', '😆', '😅', '😂', '🤣', '😊', '😇',
              '🙂', '🙃', '😉', '😌', '😍', '🥰', '😘', '😗', '😙', '😚',
              '😋', '😛', '😝', '😜', '🤪', '🤨', '🔒']
    random_emojis = random.sample(emojis, len(emojis))
    mapping = {}
    for i in range(26):
        mapping[chr(ord('a') + i)] = random_emojis[i]
    mapping[' '] = random_emojis[26]
    return mapping

def text_to_emoji(text, mapping):
    emojis_string = ''
    for char in text:
        char_lower = char.lower()
        if char_lower in mapping:
            emojis_string += mapping[char_lower]
        else:
            emojis_string += char
    return emojis_string

def emoji_to_text(emojis, reverse_mapping):
    text = ''
    for emoji in emojis:
        if emoji in reverse_mapping:
            text += reverse_mapping[emoji]
        else:
            text += emoji
    return text

mapping = {}

@app.route('/', methods=['GET', 'POST'])
def home():
    global mapping

    if request.method == 'POST':
        if 'encrypt' in request.form:
            text = request.form['text']
            mapping = generate_random_mapping()
            encrypted_text = text_to_emoji(text, mapping)
            pyperclip.copy(encrypted_text)
            return render_template('index.html', encrypted_text=encrypted_text, mapping=json.dumps(mapping, cls=CustomJSONEncoder))
        elif 'decrypt' in request.form:
            if mapping:
                emoji_string = request.form['emoji_string']
                reverse_mapping = {v: k for k, v in mapping.items()}
                decrypted_text = emoji_to_text(emoji_string, reverse_mapping)
                return render_template('index.html', decrypted_text=decrypted_text, mapping=json.dumps(mapping, cls=CustomJSONEncoder))
            else:
                return render_template('index.html', error_message='No mapping available. Please encrypt a text first.')

    return render_template('index.html', mapping=json.dumps(mapping, cls=CustomJSONEncoder))

if __name__ == '__main__':
    app.run(debug=True)
