from pathlib import Path

def load_prompt_template(template_name: str) -> str:
    template_path = Path(__file__).parent / template_name
    with open(template_path, "r") as f:
        return f.read()