from __future__ import annotations

PLUGIN_PARITY_RULES = {
    'agent-context': {
        'short_description_source_skill': 'agent-context-guide',
        'default_prompt_source_skills': [
            'agent-context-guide',
            'agent-context-init',
            'agent-context-verify',
        ],
    },
    'apple-craft': {
        'short_description_source_skill': 'apple-craft',
        'default_prompt_source_skills': [
            'apple-craft',
            'apple-review',
            'apple-harness',
        ],
    },
}


def short_description_source_skill(plugin_name: str, skill_names: list[str]) -> str | None:
    if plugin_name in PLUGIN_PARITY_RULES:
        return PLUGIN_PARITY_RULES[plugin_name].get('short_description_source_skill')
    if len(skill_names) == 1:
        return skill_names[0]
    return None


def default_prompt_source_skills(plugin_name: str, skill_names: list[str]) -> list[str]:
    if plugin_name in PLUGIN_PARITY_RULES:
        return list(PLUGIN_PARITY_RULES[plugin_name].get('default_prompt_source_skills', []))
    if len(skill_names) == 1:
        return [skill_names[0]]
    return []
