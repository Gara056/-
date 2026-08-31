#!/usr/bin/env python3
"""Generate monetization analysis PDF for the user."""

from fpdf import FPDF
from pathlib import Path

OUTPUT = Path("/opt/cursor/artifacts/monetizaciya-analiz-napravleniya.pdf")
FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


class AnalysisPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=18)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Стр. {self.page_no()}", align="C")

    def add_title_page(self):
        self.add_page()
        self.set_font("DejaVuB", "", 22)
        self.set_text_color(25, 25, 25)
        self.multi_cell(0, 12, "Анализ монетизации\nзнаний и опыта", align="C")
        self.ln(6)
        self.set_font("DejaVu", "", 11)
        self.set_text_color(80, 80, 80)
        self.multi_cell(
            0,
            7,
            "Персональный разбор направлений развития\n"
            "на основе 10 вопросов и ответов\n\n"
            "Дата: 31 августа 2026",
            align="C",
        )
        self.ln(10)
        self.set_draw_color(200, 200, 200)
        self.line(30, self.get_y(), 180, self.get_y())

    def h1(self, text: str):
        self.ln(4)
        self.set_x(self.l_margin)
        self.set_font("DejaVuB", "", 14)
        self.set_text_color(20, 60, 120)
        self.multi_cell(0, 8, text)
        self.ln(2)

    def h2(self, text: str):
        self.ln(2)
        self.set_x(self.l_margin)
        self.set_font("DejaVuB", "", 11)
        self.set_text_color(40, 40, 40)
        self.multi_cell(0, 7, text)
        self.ln(1)

    def body(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text: str):
        self.set_x(self.l_margin)
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, f"- {text}")

    def table_row(self, cols, widths, bold=False):
        font = "DejaVuB" if bold else "DejaVu"
        self.set_font(font, "", 9)
        x0 = self.l_margin
        y0 = self.get_y()
        row_lines = []
        for col, w in zip(cols, widths):
            row_lines.append(self.multi_cell(w, 6, col, split_only=True))
        row_h = max(len(line) for line in row_lines) * 6
        if y0 + row_h > 270:
            self.add_page()
            y0 = self.get_y()
        for i, (col, w) in enumerate(zip(cols, widths)):
            x = x0 + sum(widths[:i])
            self.set_xy(x, y0)
            self.multi_cell(w, row_h, col, border=1, align="L")
        self.set_xy(x0, y0 + row_h)


def build_pdf() -> Path:
    pdf = AnalysisPDF()
    pdf.add_font("DejaVu", "", FONT_REGULAR)
    pdf.add_font("DejaVuB", "", FONT_BOLD)
    pdf.set_margins(18, 18, 18)

    pdf.add_title_page()
    pdf.add_page()

    # --- Profile ---
    pdf.h1("1. Ваш профиль (по фактам)")
    pdf.body(
        "За 12 лет — одна суперсила в разных отраслях: вход в хаос → выстраивание "
        "процессов, людей, учёта и денег. Параллельное ведение нескольких направлений. "
        "Достижение измеримых результатов (тендер на 3 года, 6 направлений, стройка у друга). "
        "Автоматизация рутины для себя (программа «Стройка»)."
    )
    pdf.h2("Ключевой опыт")
    pdf.bullet("12 лет назад: организация услуг по ОПЗ скважин, 3 человека → тендер на 3 года")
    pdf.bullet("Зам. директора: тендеры, торги, до 6 направлений, продажи оборудования")
    pdf.bullet("Сейчас: стройка у друга — процессы, план-факт, учёт оплат, выплата ЗП")
    pdf.bullet("Продукт: «Стройка» (OpenClaw + ИИ) — учёт, планирование, графики, Excel")

    pdf.h2("Что заряжает")
    pdf.bullet("Понимание систем и адаптация в процесс")
    pdf.bullet("Результат, подкреплённый деньгами")
    pdf.bullet("Взаимодействие с людьми и структурами")
    pdf.bullet("Руководство процессами")
    pdf.bullet("Автоматизация и облегчение рутины")

    pdf.h2("Что раздражает")
    pdf.bullet("Ненадёжные, двуличные, неисполнительные люди")
    pdf.bullet("Когда вышестоящие не видят результата")

    pdf.h2("Текущая ситуация")
    pdf.bullet("Доход: ~8 000 ₽/день у друга на стройке (≈200 000 ₽/мес)")
    pdf.bullet("Обязательные расходы: 200 000 ₽/мес (выход на ноль)")
    pdf.bullet("Цель: 1 000 000 ₽/мес через 6–12 месяцев")
    pdf.bullet("Ресурс: 3–4 часа/день на своё (можно больше при чёткой идее)")
    pdf.bullet("Регионы: Самарская и Оренбургская области")
    pdf.bullet("Ozon и офлайн-точка: готов заморозить/закрыть")

    # --- Math ---
    pdf.add_page()
    pdf.h1("2. Математика цели: 1 млн ₽/мес")
    pdf.body(
        "За 6 месяцев только «спящим продуктом» — маловероятно. "
        "За 12 месяцев — возможно при фокусе и отказе от распыления."
    )
    pdf.ln(2)
    widths = [55, 55, 70]
    pdf.table_row(["Источник", "Доход/мес", "Комментарий"], widths, bold=True)
    pdf.table_row(
        ["Консалтинг (C)", "300–450 тыс.", "2–3 клиента, «порядок на объекте»"],
        widths,
    )
    pdf.table_row(
        ["«Стройка» (A)", "90–250 тыс.", "30–50 подписчиков × 3–5 тыс."],
        widths,
    )
    pdf.table_row(
        ["Стройка у друга", "150–250 тыс.", "Стабильная база или замена"],
        widths,
    )
    pdf.table_row(
        ["HVAC-контроль (B)", "50–150 тыс.", "Замеры, приёмка — add-on"],
        widths,
    )
    pdf.table_row(["ИТОГО", "590к – 1,1 млн", "Реалистичный диапазон"], widths, bold=True)

    pdf.ln(4)
    pdf.body(
        "Пассивный доход на старте: 10–30% (подписка на продукт). "
        "К 18–24 месяцам можно выйти на 40–60%, если не бросить продажи на полпути."
    )

    # --- Directions ---
    pdf.h1("3. Три направления — оценка")
    pdf.h2("A. «Стройка» как продукт — ГЛАВНАЯ СТАВКА")
    pdf.body("Ближе всего к цели «деньги, пока сплю». Уже работает в бою.")
    pdf.bullet("Аудитория: прорабы, ИП, бригады 5–30 чел., мелкие генподрядчики")
    pdf.bullet("Этап 1 (0–3 мес): «Стройка + настройка» — 15–30к + 2–3к/мес")
    pdf.bullet("Этап 2 (3–9 мес): подписка 3–5к/мес")
    pdf.bullet("Этап 3 (9–18 мес): тарифы, интеграции, white-label")
    pdf.bullet("Риск: «не доведу до конца» → лечится дедлайном первого платящего")

    pdf.h2("C. Операционный консалтинг — БЫСТРЫЕ ДЕНЬГИ")
    pdf.body("Упаковка: «Порядок на объекте за 30 дней»")
    pdf.bullet("План-факт, учёт оплат, график людей, регламенты + «Стройка»")
    pdf.bullet("Цена: 80–150к фикс или 50к + % от результата")
    pdf.bullet("Клиенты: знакомые прорабы, бывшие контакты из нефтесервиса, локальные чаты")
    pdf.bullet("Каждый клиент C = пользователь A = кейс = отзыв")

    pdf.h2("B. HVAC / вентиляция — НАДСТРОЙКА, не отдельный бизнес")
    pdf.body(
        "Полная HVAC-компания с нуля — дорого и долго. "
        "Имеет смысл как второй слой после A/C."
    )
    pdf.bullet("Сейчас: замеры Testo, датчики у друга, опыт взаимодействия с людьми")
    pdf.bullet("Формат: приёмка монтажа VRF/каналки, технадзор — 15–40к/объект")
    pdf.bullet("Подключать B: с месяца 2–3, не раньше")

    # --- Cut ---
    pdf.add_page()
    pdf.h1("4. Что резать немедленно")
    pdf.bullet("Ozon и офлайн-точку — не ведут к 1 млн, забирают внимание")
    pdf.bullet("Идею «нужен большой капитал» — для A+C старт 0–50к")
    pdf.bullet("HVAC как «новая профессия с нуля» — отложить, оставить как вертикаль")

    pdf.h1("5. Почему «для других получается, для себя — нет»")
    pdf.body(
        "Цепочка: нет упаковки → не продаёшь → нет кейса → нет уверенности → "
        "кажется, нужен капитал → Ozon/точка «на всякий» → нет фокуса → не доводишь своё.\n\n"
        "Для друга есть конкретная задача и дедлайн. Для себя — «хочу масштабное» без "
        "одного продукта и одного клиента.\n\n"
        "Лекарство: одна ставка, один платящий, одна дата."
    )

    pdf.h1("6. Рекомендуемая траектория: A + B → C")
    pdf.body(
        "Месяц 1–2: A — 1–3 платящих; C — разведка, 10 разговоров\n"
        "Месяц 3–5: A — 10–20 подписчиков; C — 1–2 клиента; B — первый замер\n"
        "Месяц 6–12: A растёт; C — 3–5 клиентов; B — add-on на стройках\n\n"
        "Пассивный доход растёт с A. C — ускоритель. B — увеличивает чек."
    )

    # --- 90 day plan ---
    pdf.h1("7. План на 90 дней (3–4 ч/день)")
    pdf.h2("Месяц 1 — «Первые деньги своим»")
    pdf.bullet("A: демо «Стройки» для чужого прораба; учёт, план-факт, график + Excel")
    pdf.bullet("A: первым 3 клиентам — 990 ₽/мес или 15к + 2к/мес")
    pdf.bullet("C: лист «Порядок на объекте за 30 дней» + 10 разговоров")
    pdf.bullet("B: спросить у 3 человек про контроль VRF/вентиляции")

    pdf.h2("Месяц 2 — «Кейс + повтор»")
    pdf.bullet("1 платящий по A или 1 контракт по C (80к+)")
    pdf.bullet("Записать кейс: было → сделали → результат в цифрах")
    pdf.bullet("B: один платный замер/приёмка, если был запрос")

    pdf.h2("Месяц 3 — «C официально»")
    pdf.bullet("2-й клиент C или 5+ подписчиков A")
    pdf.bullet("Решение по стройке у друга: оставить базу или поднять ставку / уйти при 400к+ от C+A")

    # --- Table formats ---
    pdf.add_page()
    pdf.h1("8. Форматы монетизации — сводка")
    widths2 = [50, 28, 28, 74]
    pdf.table_row(["Формат", "Пассив.", "Скорость", "Ваш fit"], widths2, bold=True)
    pdf.table_row(["SaaS «Стройка»", "4/5", "2/5", "Максимальный"], widths2)
    pdf.table_row(["Консалтинг", "1/5", "5/5", "Максимальный"], widths2)
    pdf.table_row(["HVAC-контроль", "2/5", "3/5", "Средний (пока)"], widths2)
    pdf.table_row(["Ozon / офлайн", "3/5", "1/5", "Нулевой"], widths2)
    pdf.table_row(["Своя HVAC-компания", "2/5", "1/5", "Низкий сейчас"], widths2)
    pdf.table_row(["Обучение / курсы", "4/5", "2/5", "Через 12+ мес"], widths2)

    pdf.ln(4)
    pdf.h1("9. Роль ИИ в вашей модели")
    pdf.body("Не «стать программистом», а усилитель:")
    pdf.bullet("Доработка «Стройки» (как уже делаете)")
    pdf.bullet("КП, регламенты, отчёты для клиентов C")
    pdf.bullet("Позже — «ИИ-помощник прораба» как апселл в продукте")

    pdf.h1("10. Главный вывод")
    pdf.body(
        "Вы — операционный предприниматель без упаковки и одного платящего клиента "
        "на своё имя. Не «без направления».\n\n"
        "Оптимальная ставка:\n"
        "1. «Стройка» — путь к доходу «во сне»\n"
        "2. Консалтинг «порядок на объекте» — деньги и кейсы сейчас\n"
        "3. HVAC-контроль — премиум-надстройка, не новая жизнь с нуля\n\n"
        "1 млн ₽/мес за 12 месяцев — амбициозно, но реалистично при фокусе, "
        "не при трёх полуготовых направлениях."
    )

    pdf.ln(6)
    pdf.set_font("DejaVu", "", 9)
    pdf.set_text_color(100, 100, 100)
    pdf.multi_cell(
        0,
        5,
        "Документ подготовлен на основе диалога из 10 вопросов.\n"
        "Следующие шаги: КП для «Стройки», структура услуги «Порядок за 30 дней», "
        "план первой недели по дням.",
    )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    pdf.output(str(OUTPUT))
    return OUTPUT


if __name__ == "__main__":
    path = build_pdf()
    print(path)
    print(f"Size: {path.stat().st_size} bytes")
