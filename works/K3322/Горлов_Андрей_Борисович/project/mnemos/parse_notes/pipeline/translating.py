from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama


class StructuredNoteParser:
    def __init__(self, model_name="gemma3:4b"):
        self.llm = Ollama(model=model_name)
        self.template = """
        [Задание]
        Разбери сырую заметку на смысловые блоки и заполни JSON-шаблон. 
        Используй только информацию из заметки. Если данных для поля нет - оставь null.

        [Шаблон JSON с объяснениями]
        {json_template}

        [Сырая заметка]
        {raw_note}

        [Требования]
        - Сохрани оригинальную структуру JSON
        - Используй markdown для выделения JSON
        - Не добавляй посторонних комментариев

        [Результат]
        """

        self.prompt = PromptTemplate(
            template=self.template, input_variables=["json_template", "raw_note"]
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def parse_note(self, raw_note: str, json_template: str) -> dict:
        response = self.chain.invoke(
            {"json_template": json_template, "raw_note": raw_note}
        )
        return self._extract_json(response["text"])

    def _extract_json(self, text: str) -> dict:
        import json

        try:
            # Ищем JSON в тексте ответа
            start = text.find("{")
            end = text.rfind("}") + 1
            json_str = text[start:end]
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"Ошибка парсинга JSON: {e}")


# Пример использования
if __name__ == "__main__":
    # Пример JSON-шаблона с объяснениями
    json_template_example = """
    {
        "event": {
            "description": "Название мероприятия или события",
            "required": true
        },
        "date": {
            "description": "Дата в формате YYYY-MM-DD",
            "format": "date"
        },
        "participants": {
            "description": "Список участников",
            "type": "array"
        },
        "location": {
            "description": "Место проведения",
            "default": null
        }
    }
    """

    raw_note_example = """
    Встреча по проекту Nexus состоится 2024-02-15 в центральном офисе. 
    Участники: Анна Петрова, Игорь Смирнов и Мария Иванова. 
    Обсуждаем этапы разработки и бюджет.
    """

    parser = StructuredNoteParser(model_name="gemma3:4b")
    result = parser.parse_note(raw_note_example, json_template_example)
    print(result)
