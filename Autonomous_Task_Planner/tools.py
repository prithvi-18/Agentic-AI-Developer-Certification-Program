def text_generation_tool(prompt: str) -> str:
    """
    Simple wrapper for LLM calls
    """
    # TODO: integrate LLM
    return ""


def completion_check_tool(result: str) -> bool:
    """
    Simple heuristic to check if output is usable
    """
    return bool(result.strip())
