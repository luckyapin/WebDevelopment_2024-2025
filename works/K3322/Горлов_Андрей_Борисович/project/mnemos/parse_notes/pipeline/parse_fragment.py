import json
import re

import ollama
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
if __name__ == '__main__':
    from models import (
        TextFragment,
        ParsedFragment,
        EventFragment,
        ThoughtFragment,
        PlanFragment,
        IdeaFragment,
    )
else:
    from .models import (
        TextFragment,
        ParsedFragment,
        EventFragment,
        ThoughtFragment,
        PlanFragment,
        IdeaFragment,
    )
from langchain.output_parsers import PydanticOutputParser
from langchain.schema.runnable import RunnablePassthrough, RunnableBranch
from langchain_ollama import ChatOllama
from langchain.schema.output_parser import StrOutputParser
from typing import Union, Literal, Dict, Any


def classify_fragment_type(title: str) -> str:
    """Определяет тип фрагмента по заголовку"""
    classifier_prompt = PromptTemplate.from_template(
        "Classify the fragment type by its title. Title: {title}."
        " Options: event, thought, plan, idea."
        " Answer ONLY with lowercase type:"
    )

    chain = (
        {"title": RunnablePassthrough()}
        | classifier_prompt
        | ChatOllama(model="gemma3:4b", temperature=0.0)
        | StrOutputParser()
    )
    return chain.invoke(title).strip()


def clean_json(raw) -> str:
    # Удаляем markdown-обёртку
    cleaned = re.sub(r"^```json\n|\n```$", "", raw.content).strip()
    return cleaned
    #try:
    #    data = json.loads(cleaned)
    #except json.JSONDecodeError:
    #    return {}
    #data['note_path'] = None
    #data['note_date'] = None
    #data['title'] = None
    #return str(data)



def parse_fragment(fragment: TextFragment) -> ParsedFragment:
    fragment_type = classify_fragment_type(fragment.title)

    model_map = {
        "event": EventFragment,
        "thought": ThoughtFragment,
        "plan": PlanFragment,
        "idea": IdeaFragment,
    }

    pydantic_model = model_map.get(fragment_type, ParsedFragment)
    parser = PydanticOutputParser(pydantic_object=pydantic_model)

    prompt_template = PromptTemplate(
        template="Извлеки структуру из:\n{content}\n{format_instructions}",
        input_variables=["content"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = (
            {"content": RunnablePassthrough()}
            | prompt_template
            | ChatOllama(model="gemma3:4b", temperature=0.2)
            | RunnableLambda(clean_json)
            | parser
    )

    result = chain.invoke(fragment.content)
    # Добавляем метаданные поверх результата
    result.source_file = fragment.note_path
    result.note_date = fragment.note_date
    result.original_title = fragment.title
    return result


if __name__ == "__main__":
    # Пример использования
    test_fragment = TextFragment(
        title="✨ Интересы и идеи",
        content="""
## ✨ Интересы и идеи
- Задумался над изучением новых методов машинного обучения для улучшения аналитики данных.
- Интересно исследовать, как другие люди используют свои дневники для саморазвития.
""",
        note_path="2025-04-11.md",
        note_date="2025-04-11",
    )

    parsed = parse_fragment(test_fragment)
    print(f"Type: {type(parsed)}")
    print(parsed.model_dump_json(indent=2))
