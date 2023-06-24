import yaml

class InvalidPrompt(ValueError):
    """ Raised when the prompt is invalid """
    pass

def load_character_info(filename="personalities.txt") -> dict:
    """ Load the character info """
    with open(filename, 'r') as file:
        # Load the YAML content
        yaml_data = yaml.load(file, Loader=yaml.FullLoader)
    return yaml_data

def adapt_prompt(character_info: dict) -> str:
    """ Adapt the prompt to the character info """
    prompt_to_return = character_info.get("prompt")

    if len(prompt_to_return) < 1 or prompt_to_return is None:
        raise InvalidPrompt("Please check the prompt file and try again.")
    if "{input}" not in prompt_to_return \
        or "{history}" not in prompt_to_return:
        raise InvalidPrompt("The prompt should at least contain {input} and {history}")

    # Check the key and do the replacements
    for info in ["name", "pronoun", "age", "gender_type", "personnalities", "not_personnalities"]:
        if f"{{{info}}}" not in prompt_to_return:
            pass
            # raise InvalidPrompt(f"The prompt should at least contain {{{info}}}")

        # join the lists
        if type(character_info.get(info)) == list:
            character_info[info] = ", ".join(character_info.get(info))

        prompt_to_return = prompt_to_return.replace(f"{{{info}}}", str(character_info.get(info)))
    return prompt_to_return
