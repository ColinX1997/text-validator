import json, re


class Validator:
    def __init__(self, config_file="config\\validation_rules.json"):
        with open(config_file) as f:
            self.rules = json.load(f)["rules"]
            self.validation_functions = {
                "is_numeric": self.is_numeric,
                "is_characters": self.is_characters,
                "is_leading_zero_digit": self.is_leading_zero_digit,
                "is_character_spaces": self.is_character_spaces,
                "is_digit_spaces": self.is_digit_spaces,
                "is_character_sharp": self.is_character_sharp,
                "is_digit_sharp": self.is_digit_sharp,
            }

    def validate_rule(self, rule_name, value):
        rule = next(
            (r for r in self.rules if r["id"] == str(rule_name).split("-")[1]), None
        )
        if rule:
            validation_function = self.validation_functions[
                rule["validate"]["function"]
            ]
            length = int(str(rule_name.split("-")[0]))
            if length != len(value):
                return "Length not correct"
            return validation_function(value, rule["validate"]["error_message"])
        return "Rule not found"

    def is_numeric(self, value, error_message):
        if not value.isdigit():
            return error_message
        return "Correct~"

    def is_characters(self, value, error_message):
        if not re.match(r"^[\w\s]+$", value):
            return error_message
        return "Correct~"

    def is_leading_zero_digit(self, value, error_message):
        if not value.isdigit() or not value[0] == "0":
            return error_message
        return "Correct~"

    def is_character_spaces(self, value, error_message):
        num_spaces = value.count(" ")
        parts = str(value).split(" ")
        if str(value).strip() == "":
            return f"Correct~ {num_spaces} spaces exist"
        elif not re.match(r"^[\w\s]+$", parts[0]):
            return f"The first part is not characters"
        elif value[-1] != " " and num_spaces != 0:
            return f"The second part is not spaces"
        return f"Correct~ {num_spaces} spaces exist"

    def is_digit_spaces(self, value, error_message):
        num_spaces = value.count(" ")
        parts = str(value).split(" ")
        if str(value).strip() == "":
            return f"Correct~ {num_spaces} spaces exist"
        elif not parts[0].isdigit():
            return f"The first part is not digits"
        elif value[-1] != " " and num_spaces != 0:
            return f"The second part is not spaces"

        return f"Correct~ {num_spaces} spaces exist"

    def is_character_sharp(self, value, error_message):
        if value[-1] != "#":
            return error_message
        return "Correct~"

    def is_digit_sharp(self, value, error_message):
        if value[-1] != "#":
            return error_message
        return "Correct~"

    def is_part_number(self, value, error_message):
        parts = str(value).split("-")
        new_value = value.replace("-", "")
        if new_value.isdigit() and len(parts[0]) == 7 and len(parts[1] == 2):
            return error_message
        return "Correct~"
