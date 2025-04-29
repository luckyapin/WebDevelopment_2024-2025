from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Literal, Union
from datetime import date, datetime


class RawNote(BaseModel):
    path: str
    text: str
    created_at: datetime | None = None


class BaseParsedFragment(BaseModel):
    model_config = ConfigDict(
        json_encoders={date: lambda v: v.isoformat()},  # Сериализация дат
        populate_by_name=True,  # Разрешить alias-ы
    )
    fragment_type: Optional[str] = None
    original_title: Optional[str] = None
    note_date: Optional[date] = None
    source_file: Optional[str] = Field(None, alias="note_path")


# Специализированные модели
class Person(BaseModel):
    name: str
    role: Optional[str] = None  # например: "я", "коллега", "друг"


class SubEvent(BaseModel):
    text: str
    people: Optional[List[Person]] = None
    tags: Optional[List[str]] = None
    emotion: Optional[str] = None  # например: "радость", "усталость"

    class Config:
        arbitrary_types_allowed = True


class EventGroup(BaseModel):
    text: str
    parts: List[SubEvent]
    people: Optional[List[Person]] = None
    tags: Optional[List[str]] = None
    emotion: Optional[str] = None  # например: "радость", "усталость"


class EventFragment(BaseParsedFragment):
    type: Literal["event"] = "event"
    created_at: Optional[datetime] = None
    target_date: Optional[datetime] = None
    groups: List[EventGroup]
    people: Optional[List[Person]] = None  # общие участники
    tags: Optional[List[str]] = None
    emotion: Optional[str] = None
    importance: Optional[int] = Field(default=3, ge=1, le=5)


class ThoughtPart(BaseModel):
    text: str
    tags: Optional[List[str]] = None
    emotion: Optional[str] = None


class ThoughtFragment(BaseParsedFragment):
    type: Literal["thought"] = "thought"
    created_at: Optional[datetime] = None
    target_date: Optional[datetime] = None
    main_thought: str  # основная мысль или общее суждение
    groups: Optional[List[ThoughtPart]] = None
    tags: Optional[List[str]] = None
    emotion: Optional[str] = None
    importance: Optional[int] = Field(default=3, ge=1, le=5)
    people: Optional[List[str]] = None  # если в размышлениях упоминаются люди


class PlanTask(BaseModel):
    text: str  # текст задачи
    parts: Optional[List["PlanTask"]] = None  # вложенные подзадачи
    tags: Optional[List[str]] = None  # теги для задачи
    people: Optional[List[str]] = None  # кто вовлечён
    deadline: Optional[date] = None  # личный срок этой подзадачи
    priority: Optional[Literal["высокий", "средний", "низкий"]] = (
        None  # приоритет подзадачи
    )
    emotion: Optional[str] = None  # эмоция, если есть ожидания/чувства


class PlanFragment(BaseParsedFragment):
    type: Literal["plan"] = "plan"
    created_at: Optional[datetime] = None
    target_date: Optional[date] = None  # общий срок выполнения плана
    groups: List[PlanTask]  # список корневых задач
    priority: Literal["высокий", "средний", "низкий"] = "средний"
    tags: Optional[List[str]] = None
    people: Optional[List[str]] = None


class IdeaPart(BaseModel):
    text: str  # текст части
    tags: Optional[List[str]] = None  # теги части
    emotion: Optional[str] = None  # эмоция части


class IdeaFragment(BaseParsedFragment):
    type: Literal["idea"] = "idea"
    created_at: Optional[datetime] = None
    domain: Optional[str] = None  # область применения
    parts: Optional[List[IdeaPart]] = None  # возможные действия
    urgency: Literal["срочно", "отложить", "долгосрочное"] = (
        "долгосрочное"  # уровень срочности
    )
    tags: Optional[List[str]] = None  # общие теги
    emotion: Optional[str] = None  # эмоция по поводу идеи
    people: Optional[List[str]] = None  # связанные люди


# Основной тип для Union
ParsedFragment = Union[EventFragment, ThoughtFragment, PlanFragment, IdeaFragment]


class TextFragment(BaseModel):
    title: str
    content: str
    note_path: str
    note_date: datetime  # Добавьте это поле в ваш класс
