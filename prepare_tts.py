import os
import json
from gtts import gTTS
import io
"""
get all the key and value from set_data.json, then convert them to audio files in audios folder.
they all follow this format '{key}, {value} seconds, begin', saved as start_{key}.mp3
then 'the next action, {key}, {value} seconds', saved as next_{key}.mp3"""

def main():
    clear_folder()
    
    # read json file and get all the key and value from it.
    # then convert them to audio files in audios folder.
    # they all follow this format '{key}, {value} seconds, begin', saved as start_{key}.mp3
    # then 'the next action, {key}, {value} seconds', saved as next_{key}.mp3
    with io.open("set_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    
    for key, value in data.items():
        print (key, value)
        text = "{}, {} 秒, 开始！".format(key, value)
        save_audio(text, file_name="start_{}".format(key))
        
        text = "下一个动作，{}, {} 秒, 准备！".format(key, value)
        save_audio(text, file_name="next_{}".format(key))

def clear_folder():
    for file in os.listdir("audios"):
        os.remove("audios/{}".format(file))


def save_audio(text, file_name, is_chinese= True):
    output_language = "zh-cn" if is_chinese else "en"
    tts = gTTS(text, lang=output_language, tld="co.uk", slow=False)

    
    tts.save(f"audios/{file_name}.mp3")



if __name__ == "__main__":
    main()