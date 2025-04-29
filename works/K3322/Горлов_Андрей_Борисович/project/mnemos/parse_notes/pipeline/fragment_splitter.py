# extractors/fragment_splitter.py

import re
from datetime import date
from typing import List
from .models import TextFragment, RawNote


def split_text_by_headers(note: RawNote | None = None) -> List[TextFragment]:
    """
    Делит текст по заголовкам '## ' с сохранением текста под каждым заголовком.
    """
    # нормализуем переносы строк
    text = note.text
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # добавим разделитель в конец, чтобы обработать последний блок
    text += "\n## END_MARKER\n"

    # ищем все заголовки вида '## что-то'
    pattern = r"^## (.*?)\n"
    headers = list(re.finditer(pattern, text, flags=re.MULTILINE))
    fragments = []
    for i in range(len(headers) - 1):
        start = headers[i].end()
        end = headers[i + 1].start()
        title = headers[i].group(1).strip()
        content = text[start:end].strip()
        if title != "END_MARKER":
            fragments.append(
                TextFragment(
                    title=title,
                    content=content,
                    note_path=note.path,
                    note_date=note.created_at,
                )
            )

    return fragments


if __name__ == "__main__":
    sample_text = """
# День

## Утро
Проснулся, попил чай, думал о смысле жизни.

## Встреча
Встретился с Петей, обсудили проект.

## Мысли
Почему я вообще этим занимаюсь?
"""
    raw_note = RawNote(
        path="example_note.txt",
        text=sample_text,
        created_at=date(day=11, month=4, year=2025),
    )
    fragments = split_text_by_headers(raw_note)

    for f in fragments:
        print(f"[{f.title}] {f.content[:50]}")
