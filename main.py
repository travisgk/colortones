import colortones


def main():
    text_str = """
    你好。
    你好吗？
    很好, 谢谢。
    你叫什么名字？
    很高兴认识你。
    拜拜。
    """

    paragraph = colortones.process_text(text_str)
    scheme = colortones.load_color_scheme("default")
    print(paragraph.to_color_str(key="hanzi", color_scheme=scheme))
    print(paragraph.to_color_str(key="pinyin", color_scheme=scheme))
    print(paragraph.to_color_str(key="zhuyin", color_scheme=scheme))
    print(paragraph.to_color_str(key="ipa-root", color_scheme=scheme))


if __name__ == "__main__":
    main()
