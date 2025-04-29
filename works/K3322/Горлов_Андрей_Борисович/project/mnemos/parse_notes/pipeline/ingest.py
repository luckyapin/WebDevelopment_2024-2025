# ingest.py
import re
from pathlib import Path
from typing import Iterator
from datetime import datetime, date
from .models import RawNote


def extract_date_from_text(text: str) -> date | None:
    """
    Извлекает дату из текста в формате # 📅 Дата: YYYY-MM-DD.
    """
    date_pattern = r"# 📅 Дата:\s*(\d{4}-\d{2}-\d{2})"
    match = re.search(date_pattern, text)

    if match:
        return datetime.strptime(match.group(1), "%Y-%m-%d").date()
    return None


def load_notes_from_folder(folder_path: str) -> Iterator[RawNote]:
    """
    Загружает все .md и .txt файлы как RawNote.
    """
    folder = Path(folder_path)
    for file_path in folder.glob("**/*.md"):
        try:
            text = file_path.read_text(encoding="utf-8")
            note_date = extract_date_from_text(text)  # Извлекаем дату из текста

            yield RawNote(
                path=str(file_path),
                text=text,
                created_at=(
                    note_date
                    if note_date
                    else datetime.fromtimestamp(file_path.stat().st_ctime).date()
                ),
            )
        except Exception as e:
            print(f"Ошибка при чтении {file_path}: {e}")


if __name__ == "__main__":
    notes_dir = r"\\LAPTOP-3HCVQOMT\obsi\Дневник с памятью\Дневник"  # Папка с заметками
    for note in load_notes_from_folder(notes_dir):
        print(f"Файл: {note.path}")
        print(f"Создан: {note.created_at}")
        print(f"Текст (первые 100 символов):\n{note.text[:100]}")
        print("-" * 40)
