import spacy
import regex as re

# 载入Spacy英文预训练模型
nlp = spacy.load("en_core_web_sm")


# 解析规则描述并生成正则表达式模式
def parse_rule(description):
    doc = nlp(description)
    pattern = ""
    digits = 0
    letters = 0
    in_digits = False
    in_letters = False
    total_count = None
    total_found = False

    for token in doc:
        if token.text.isdigit():
            if in_digits:
                digits = int(token.text)
            elif in_letters:
                letters = int(token.text)
            elif total_found:
                total_count = int(token.text)
                total_found = False
        elif token.text.lower() in ["digits", "digit"]:
            in_digits = True
        elif token.text.lower() in ["letters", "letter", "characters", "character"]:
            in_letters = True
        elif token.text.lower() in ["and"] and in_digits and not in_letters:
            # 遇到 "and" 且前面是数字规则，此时应将数字规则加入模式并重置
            pattern += f"\\d{{{digits}}}"
            digits = 0
            in_digits = False
        elif token.text.lower() in ["space"]:
            pattern += " "
        elif token.text.lower() in ["total"]:
            # 总计规则处理
            if total_count is not None:
                raise ValueError(
                    f"Invalid description: '{description}'. Duplicate total count found."
                )
            total_found = True
        elif token.text.lower() in ["composed", "of", "in"]:
            # 忽略这些词，它们对正则表达式生成没有影响
            continue
        else:
            # 遇到非关键字，视为文本描述，不应影响正则表达式生成
            continue

    # 确保字母规则被添加到模式中
    if in_letters:
        pattern += f"[a-zA-Z]{{{letters}}}"

    # 处理总计规则
    if total_count is not None:
        pattern = f"^(?!.{{0,{total_count-1}}}$).{{{total_count}}}$"
    else:
        if "total" in description.lower():
            raise ValueError(
                f"Invalid description: '{description}'. Missing total count after 'total'."
            )

    print(f"Generated pattern: {pattern}")
    return pattern if re.compile(pattern) else None


# 编译正则表达式
def generate_regex(description):
    pattern = parse_rule(description)
    regex = re.compile(pattern)
    print(f"Compiled regex: {regex.pattern}")
    return regex


# 验证输入字符串是否符合描述
def validate_input(description, input_string):
    regex = generate_regex(description)
    match_result = bool(regex.match(input_string))
    print(f"Input: '{input_string}' | Match: {match_result}")
    return match_result


# 测试函数
if __name__ == "__main__":
    descriptions = [
        "3 digits and 2 characters",
        "20 characters, composed of digits and spaces",
        "5 letters and 3 digits",
    ]
    input_strings = ["123ab", "12345678901234567890", "abcde123"]

    for desc, inp in zip(descriptions, input_strings):
        print(
            f"Description: '{desc}' | Input: '{inp}' -> Valid: {validate_input(desc, inp)}"
        )
