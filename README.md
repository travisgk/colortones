# colortones
A Python script that colors Chinese characters to match their spoken tone.
This tool provides other transcriptions into zhuyin, pinyin, and the IPA as well.

<br>

# Setup
```
pip install pypinyin jieba
```

<br>

# Example
<img src="https://github.com/travisgk/colortones/blob/main/_demo_output/_sample.png?raw=true">

```
import colortones

# processes the text.
chinese = "老板想买哪种水果？我听不懂。不要打扰我。"
paragraph = colortones.process_text(chinese)

# loads a color scheme.
scheme = colortones.load_color_scheme("default")

# prints colored text to the console.
print(paragraph.to_color_str("hanzi", color_scheme=scheme))
print(paragraph.to_color_str("pinyin", color_scheme=scheme))
print(paragraph.to_color_str("ipa-root", color_scheme=scheme))
print(paragraph.to_color_str("zhuyin-root", color_scheme=scheme))
```
