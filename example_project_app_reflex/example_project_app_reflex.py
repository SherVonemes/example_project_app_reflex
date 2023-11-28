import reflex as rx
import random
from datetime import datetime
from googletrans import Translator
from reflex.base import Base
from .langs import langs

trans = Translator()


class Message(Base):
    original_text: str
    text: str
    created_at: str
    to_lang: str


class State(rx.State):
    # TODO_project:
    items = ["Поспать", "Еще поспать", "Пойти на пары"]
    new_item: str
    invalid_item: bool = False

    def add_item(self, form_data: dict[str, str]):
        new_item = form_data.pop("new_item")
        if not new_item:
            self.invalid_item = True
            return
        self.items.append(new_item)
        self.invalid_item = False
        return rx.set_value("new_item", "")

    def finish_item(self, item: str):
        self.items.pop(self.items.index(item))

    # Counter_project:
    count = 0

    def increment(self):
        """Increment the count."""
        self.count += 1

    def decrement(self):
        """Decrement the count."""
        self.count -= 1

    def random(self):
        """Randomize the count."""
        self.count = random.randint(0, 100)

    # Translator_project:
    text: str = ""
    messages: list[Message] = []
    lang: str = "Zulu"

    @rx.var
    def output(self) -> str:
        if not self.text.strip():
            return "Перевод"
        translated = trans.translate(self.text, dest=self.lang)
        return translated.text

    def post(self):
        self.messages = [
                            Message(
                                original_text=self.text,
                                text=self.output,
                                created_at=datetime.now().strftime("%B %d, %Y %I:%M %p"),
                                to_lang=self.lang,
                            )
                        ] + self.messages

    # Swears_project:
    swears = ["Выблядок", "Хитровыебанный", "Пидорас", "Хуй", "Пиздабол", "Распиздяй", "Сука", "Дурачок", "Мудачок", "Черт", "Шайтан", "Мудень", "Хабал", "Пыня", "Околотень", "Невеглас"]
    current_swear="Выблядок"

    @rx.var
    def random_swear(self) -> str:
        return self.current_swear

    def generate_swear(self):
        self.current_swear = random.choice(self.swears)

@rx.page(route="/")
def home():
    return rx.vstack(
        rx.heading("Главная Страница"),
        rx.link("Проекты", href="/projects"),
        rx.link("Мемы", href="/memes"),
        rx.link("Об Авторе", href="/author")
    )


@rx.page(route="/projects")
def projects():
    return rx.vstack(
        rx.heading("Проекты на Reflex"),
        rx.link("Счётчик", href="/counter"),
        rx.link("Переводчик", href="/translator"),
        rx.link("Список дел", href="/todo"),
        rx.link("Генератор Ругательств", href="/swear-generator"),
        rx.link("Вернуться на главную", href="/")
    )


@rx.page(route="/memes")
def memes():
    return rx.vstack(
        rx.heading("Страница с Мемами"),
        rx.text("Мем_pepe"),
        rx.image(src="/мем_2.jpg", alt="Фото автора", width=300),
        rx.text("Мем_Стрелков"),
        rx.image(src="/мем_1.jpg", alt="Фото автора", width=400),
        rx.text("Мем_enjoier"),
        rx.image(src="/SCR-20231128-cwny.jpeg", alt="Фото автора", width=400),
        rx.text("Мем_4"),
        rx.circular_progress(
            rx.circular_progress_label(
                "", color="rgb(107,99,246)"
            ),
            is_indeterminate=True,
        ), # Да, это СКАМ
        rx.link("Вернуться на главную", href="/")
    )


@rx.page(route="/author")
def author():
    return rx.container(
        rx.responsive_grid(
            rx.box(
                rx.image(src="/Влад аватарка фото.jpg", alt="Фото автора", width=200),
                height="20em",
                width="12em",
                bg="#f0f0f0",
                display="flex",
                justify_content="center",
                align_items="center"
            ),
            rx.box(
                rx.vstack(
                    rx.text("Семенов Влад", font_size="1.2em", font_weight="bold", text_align="center"),
                    rx.text("ВШЭ ЭАД", font_size="1em", text_align="center"),
                    rx.text("2 курс", font_size="1em", text_align="center")
                ),
                height="10em",
                width="10em",
                bg="lightblue",
                display="flex",
                justify_content="center",
                align_items="center"
            ),
            rx.box(
                rx.vstack(
                    rx.text("Любимые мемы", font_size="1.2em", font_weight="bold", text_align="center"),
                    rx.ordered_list(
                        rx.list_item("Грустный пепе"),
                        rx.list_item("Мем со Стрелковым и мобилизацией"),
                        rx.list_item("Мем с enjoyer and gigachad"),
                        font_size="1em"
                    )
                ),
                height="10em",
                width="10em",
                bg="lightpurple",
                display="flex",
                justify_content="center",
                align_items="center"
            ),
            rx.box(
                rx.link("Главное меню", href="/", font_size="1.2em", font_weight="bold"),
                height="7em",
                width="7em",
                bg="tomato",
                display="flex",
                justify_content="center",
                align_items="center"
            ),
            columns=[2],
            spacing="4",
        ),
        padding="2em",
        bg="#f0f0f0",
        border_radius="1em",
        shadow="lg",
        font_family="'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"  # Улучшил шрифт
    )

@rx.page(route="/counter")
def counter():
    return rx.center(
        rx.vstack(
            rx.heading(State.count),
            rx.hstack(
                rx.button("Decrement", on_click=State.decrement, color_scheme="red"),
                rx.button(
                    "Randomize",
                    on_click=State.random,
                    background_image="linear-gradient(90deg, rgba(255,0,0,1) 0%, rgba(0,176,34,1) 100%)",
                    color="white",
                ),
                rx.button("Increment", on_click=State.increment, color_scheme="green"),
            ),
            rx.vstack(rx.link("Вернуться на главную", href="/")),
            padding="1em",
            bg="#ededed",
            border_radius="1em",
            box_shadow="lg",
        ),
        padding_y="5em",
        font_size="2em",
        text_align="center",
    )


# Translation_functions
def header():
    """Basic instructions to get started."""
    return rx.box(
        rx.text("Translator 🗺", font_size="2rem"),
        rx.text(
            "Translate things and post them as messages!",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def down_arrow():
    return rx.vstack(
        rx.icon(
            tag="arrow_down",
            color="#666",
        )
    )


def text_box(text):
    return rx.text(
        text,
        background_color="#fff",
        padding="1rem",
        border_radius="8px",
    )


def message(message):
    return rx.box(
        rx.vstack(
            text_box(message.original_text),
            down_arrow(),
            text_box(message.text),
            rx.box(
                rx.text(message.to_lang),
                rx.text(" · ", margin_x="0.3rem"),
                rx.text(message.created_at),
                display="flex",
                font_size="0.8rem",
                color="#666",
            ),
            spacing="0.3rem",
            align_items="left",
        ),
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )


def smallcaps(text, **kwargs):
    return rx.text(
        text,
        font_size="0.7rem",
        font_weight="bold",
        text_transform="uppercase",
        letter_spacing="0.05rem",
        **kwargs,
    )


def output():
    return rx.box(
        rx.box(
            smallcaps(
                "Output",
                color="#aeaeaf",
                background_color="white",
                padding_x="0.1rem",
            ),
            position="absolute",
            top="-0.5rem",
        ),
        rx.text(State.output),
        padding="1rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


@rx.page(route="/translator")
def translator():
    return rx.container(
        header(),
        rx.input(
            placeholder="Text to translate",
            on_blur=State.set_text,
            margin_top="1rem",
            border_color="#eaeaef",
        ),
        rx.select(
            list(langs.keys()),
            value=State.lang,
            placeholder="Select a language",
            on_change=State.set_lang,
            margin_top="1rem",
        ),
        output(),
        rx.button("Post", on_click=State.post, margin_top="1rem"),
        rx.vstack(
            rx.foreach(State.messages, message),
            margin_top="2rem",
            spacing="1rem",
            align_items="left",
        ), rx.link("Вернуться к проектам", href="/projects"),
        padding="2rem",
        max_width="600px",
    )


# TODO_functions
def todo_item(item: rx.Var[str]) -> rx.Component:
    return rx.list_item(
        rx.hstack(
            rx.button(
                on_click=lambda: State.finish_item(item),
                height="1.5em",
                background_color="white",
                border="1px solid blue",
            ),
            rx.text(item, font_size="1.25em"),
        )
    )


def todo_list() -> rx.Component:
    return rx.ordered_list(
        rx.foreach(State.items, lambda item: todo_item(item)),
    )


def new_item() -> rx.Component:
    return rx.form(
        rx.input(
            id="new_item",
            placeholder="Add a todo...",
            bg="white",
            is_invalid=State.invalid_item,
        ),
        rx.center(
            rx.button("Add", type_="submit", bg="white"),
        ),
        on_submit=State.add_item,
    )


@rx.page(route="/todo")
def todo():
    return rx.container(
        rx.vstack(
            rx.heading("Todos"),
            new_item(),
            rx.divider(),
            todo_list(),
            bg="#ededed",
            margin="5em",
            padding="1em",
            border_radius="0.5em",
            shadow="lg",
        ),
        rx.link("Вернуться к проектам", href="/projects")
    )



@rx.page(route="/swear-generator")
def swear_generator():
    return rx.vstack(
        rx.heading("Испытай удачу"),
        rx.text(f"Батенька, да вы {State.random_swear}!"),
        rx.button("Тебе повезет", on_click=State.generate_swear),
        rx.link("Вернуться к проектам", href="/projects")
    )


app = rx.App(state=State)
app.add_page(home)
app.add_page(projects)
app.add_page(memes)
app.add_page(author)
app.add_page(counter)
app.add_page(translator)
app.add_page(todo)
app.add_page(swear_generator)

app.compile()
