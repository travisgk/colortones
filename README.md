[<img src="https://github.com/travisgk/chromapinyin/blob/main/_demo_output/demo1.png?raw=true">](https://github.com/travisgk/chromapinyin/blob/main/demo1.py)
# chromapinyin
A Python script for creating HTML tables of various Chinese transcriptions (IPA and zhuyin), with the option to color syllables by their tone.
These can be created by giving chromapinyin text in hanzi and text of its corresponding pinyin.
The program will take the necessary tone changes into account.

<br>

# Setup

### Installation
```
pip install pillow imageio
```
[pillow](https://github.com/python-pillow/Pillow) is used for creating customized pitch graph components.

[imageio](https://github.com/imageio/imageio) is optional. Installing it will enable functionality to modify the GIF animations' speed and/or looping behavior.

<br>

### Handwriting Animation GIFs
chromapinyin can modify handwriting GIFs' speed and looping behavior.

GIF animations from the repository [chinese-char-animations](https://github.com/nmarley/chinese-char-animations) can be downloaded and have its folders ```images``` and ```images_large``` placed under chromapinyin's output directory to (by default) be ```_chroma_res/handwriting/images``` and ```_chroma_res/handwriting/images_large``` respectively.

Then the following can be run (imageio is necessary):
```
import chromapinyin
chromapinyin.process_gifs(fps=5, start_freeze_ms=1000, end_freeze_ms=3500, loops=True)
```

```_chroma_res/handwriting/images``` will be the directory used to source handwriting animations.

The process GIFs function will also rename the files under ```_chroma_res/handwriting/images-large```,
so that this directory can easily be renamed to ```_chroma_res/handwriting/images``` to be used instead.

<br>

# Creating a Stylized Table

The following can be found under [demo2.py](https://github.com/travisgk/chromapinyin/blob/main/demo2.py).
```
import chromapinyin

def main():
    chromapinyin.color_scheme.set_punctuation_RGB((255, 255, 255))
    hanzi = "我不是来自中国。"
    pinyin = "wǒ bùshì láizì zhōngguó."
    word_list = chromapinyin.create_word_list(hanzi, pinyin)

    # defines the 2D table of the syllable aspects to display per syllable.
    categories = [
        ["hanzi", "vertical_zhuyin",],
        [("pinyin", "number_tones",), ("ipa", "no_tones"),],
    ]

    html = ""
    html += "<html>\n<head>\n<style>\n"
    html += "body { background-color: black; }\n</style>\n</head>\n<body>\n"

    # creates an HTML table with styling components placed directly inline
    # and the characters placed to be read horizontally.
    html += chromapinyin.create_stylized_sentence(
        word_list, 
        categories,
        use_css=False,
        vertical=False,
        hide_clause_breaks=False,
        max_n_line_syllables=999
    )
    html += "</body>\n</html>"

    with open("demo2.html", "w", encoding="utf-8") as file:
        file.write(html)

main()
```

The resulting HTML will look like this:
[<img src="https://github.com/travisgk/chromapinyin/blob/main/_demo_output/demo2.png?raw=true">](https://github.com/travisgk/chromapinyin/blob/main/demo2.py)

<br>

### Category Options
Categories of syllable aspects are provided in a 2D table.
These can be any of the following selections:

<table>
	<tr>
		<td><strong>"hanzi"</strong></td>
		<td>the syllable's hanzi character.</td>
	</tr>
	<tr>
		<td><strong>"pinyin"</strong></td>
		<td>the syllable's pinyin character.</td>
	</tr>
	<tr>
		<td><strong>"zhuyin"</strong></td>
		<td>the syllable's zhuyin transcription.</td>
	</tr>
	<tr>
		<td><strong>"vertical_zhuyin"</strong></td>
		<td>the syllable's zhuyin transcription rendered vertically.</td>
	</tr>
	<tr>
		<td><strong>"ipa"</strong></td>
		<td>the syllable's international phonetic alphabet transcription.</td>
	</tr>
	<tr>
		<td><strong>"pitch_graph"</strong></td>
		<td>an HTML embedded graph image of the syllable's spoken tone.</td>
	</tr>
	<tr>
		<td><strong>"handwriting"</strong></td>
		<td>an HTML embedded GIF of the hanzi being written.</td>
	</tr>
	<tr>
		<td><strong>"blank"</strong></td>
		<td>an empty table cell. used to block cell merging.</td>
	</tr>
	<tr>
		<td><strong>None</strong></td>
		<td>used to control how cells merge.</td>
	</tr>
</table>
<br>

### Additional Category Formatting
A category selection can be given in the 2D table as a lone string,
but it can also be given as a tuple in order to provide additional formatting.
<table>
	<tr>
		<td><strong>"grouped"</strong></td>
		<td>this category's cells will be aligned together so that syllables belonging to the same word will be grouped together.</td>
	</tr>
	<tr>
		<td><strong>"split_punctuation"</strong></td>
		<td>only applicable for <strong>"pinyin"</strong> or <strong>"ipa"</strong>.<br>punctuation in this category cell won't be merged with the previous syllable's cell for the same category.</td>
	</tr>
	<tr>
		<td><strong>"number_tones"</strong></td>
		<td>only applicable for <strong>"pinyin"</strong>, <strong>"zhuyin"</strong>, and <strong>"ipa"</strong>.<br>the category's tones will be expressed with a number.</td>
	</tr>
	<tr>
		<td><strong>"no_tones"</strong></td>
		<td>only applicable for <strong>"pinyin"</strong>, <strong>"zhuyin"</strong>, and <strong>"ipa"</strong>.<br>the category's tones won't be rendered at all.</td>
	</tr>
	<tr>
		<td><strong>"no_color"</strong></td>
		<td>coloring styles won't be used.</td>
	</tr>
	<tr>
		<td><strong>"night_mode_GIFs"</strong></td>
		<td>only applicable for <strong>"handwriting"</strong>.<br>this will make the handwriting GIFs use filters to display the GIFs with a black background.<br>this should be used when the user is not using CSS and the night mode filters should be embedded inline directly.</td>
	</tr>
</table>
<br>

### Cell Merging
By default, chromapinyin will merge cells using the ```colspan``` property.
If this is undesired, ```chromapinyin.create_stylized_sentence(...)``` can be called with ```use_colspan=False``` in its parameters.

The following categories 2D table is used for this [demo](https://github.com/travisgk/chromapinyin/blob/main/demo3.py):
```
categories = [
    ["hanzi", "vertical_zhuyin", "pinyin",],
    ["zhuyin", "blank", ("ipa", "no_color", "no_tones",),],
    [("handwriting", "night_mode_GIFs",),],
]
```

The **"blank"** category adds padding to the second row so that **"ipa"** isn't spanned over two columns, while the **"handwriting"** category in the third row will be spanned across all three columns.

With ```max_n_line_syllables=5```, chromapinyin creates the following table:

[<img src="https://github.com/travisgk/chromapinyin/blob/main/_demo_output/demo3.png?raw=true">](https://github.com/travisgk/chromapinyin/blob/main/demo3.py)

<br>

# Color Palettes
chromapinyin provides several default tone color palettes that can be selected.

<br>

# Information in each syllable dictionary
```
import chromapinyin

hanzi = "我买雨伞。"
pinyin = "wǒ mǎi yǔsǎn."
word_list = chromapinyin.create_word_list(hanzi, pinyin)
```
The ```word_list``` list will contain four lists, with each list representing a "word", a group of syllables.
- ```word_list[0]``` will contain one syllable dictionary object corresponding to "wǒ" 
- ```word_list[1]``` will contain one syllable dictionary object corresponding to "mǎi"
- ```word_list[2]``` will contain two syllable dictionary objects corresponding to "yǔ" and "sǎn"
- ```word_list[3]``` will contain one "syllable" dictionary object corresponding to the "."
<br>

Every contained list is occupied by dictionary objects which represent each syllable in a word.
<br>
For example, ```word_list[2][1]``` is a dictionary object with the following keys:
- ```"hanzi": "伞"```
- ```"pinyin": "sǎn"```
- ```"tone_str": "low"```
- ```"tone_num": 3```
- ```"spoken_tone_str": "low"```
- ```"spoken_tone_num": 3```
- ```"inflection_str": "full_low"```
- ```"inflection_num": 6```
- ```"ipa_root": "san"```
- ```"ipa_suffix": "˨˩˦"```
- ```"ipa": "san˨˩˦"```
- ```"zhuyin_prefix": ""```
- ```"zhuyin_root": "ㄙㄢ"```
- ```"zhuyin_suffix": "ˇ"```
- ```"zhuyin": "ㄙㄢˇ"```
<br>
