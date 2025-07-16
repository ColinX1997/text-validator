import re


# 直接解析规则描述
def parse_rule(description):
    match = re.search(r"(\d+) characters in total", description)
    if match:
        total_chars = int(match.group(1))
        pattern = f"^(?!.{{0,{total_chars-1}}}$).{{{total_chars}}}$"
        return re.compile(pattern)
    else:
        raise ValueError("Invalid description: total count missing.")


# 测试
rule = "20 characters in total, composed of digits and spaces"
regex = parse_rule(rule)
input_strings = ["12345678901234567890", "1234567890123456789", "12345678901234567890 "]

for s in input_strings:
    print(f"'{s}' matches rule: {bool(regex.match(s))}")
