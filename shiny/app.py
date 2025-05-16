from shiny import App, ui, render, reactive, req
import pandas as pd
import math

# Load and preprocess dataset
df = pd.read_csv("data/classified_bracero_quotes.csv")
df["Quote"] = df["Quote"].astype(str)

# Pre-filter: remove greetings and questions (likely from interviewers)
df = df[
    ~df["Quote"].str.lower().str.contains(r"\bbuenos días\b|\bbuenas tardes\b") &
    ~df["Quote"].str.contains(r"\?")
].reset_index(drop=True)

# Dropdown options
topic_choices = ["Todos"] + sorted(df["Topic"].dropna().unique())
interviewee_choices = ["Todos"] + sorted(df["Interviewee"].dropna().unique())

QUOTES_PER_PAGE = 10

app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select("topic", "Selecciona un tema:", topic_choices, selected="Todos"),
        ui.input_select("interviewee", "Selecciona entrevistado:", interviewee_choices),
        ui.input_action_button("prev", "⬅ Anterior"),
        ui.input_action_button("next", "Siguiente ➡"),
        ui.output_text("page_info")
    ),
    ui.output_ui("quote_output"),
    title=ui.tags.div(
        ui.tags.h2(
            [
                "Citas del ",
                ui.tags.a("Archivo Historia del Bracero",
                    href="https://braceroarchive.org",
                    target="_blank",
                    style="color: #1a73e8; text-decoration: none;"
                )
            ],
            style="font-family: 'Segoe UI', sans-serif; font-weight: 600; font-size: 1.8rem; margin-bottom: 0.2rem;"
        )
    )
)

def server(input, output, session):
    current_page = reactive.Value(1)
    prev_clicks = reactive.Value(0)
    next_clicks = reactive.Value(0)

    @reactive.Calc
    def filtered_data():
        dff = df.copy()
        if input.topic() != "Todos":
            dff = dff[dff["Topic"] == input.topic()]
        if input.interviewee() != "Todos":
            dff = dff[dff["Interviewee"] == input.interviewee()]
        return dff.reset_index(drop=True)

    @reactive.effect
    def reset_page_on_filter():
        _ = input.topic()
        _ = input.interviewee()
        current_page.set(1)

    @reactive.effect
    def track_next_clicks():
        clicks = input.next()
        if clicks > next_clicks.get():
            next_clicks.set(clicks)
            total_pages = max(1, math.ceil(len(filtered_data()) / QUOTES_PER_PAGE))
            current_page.set(min(current_page.get() + 1, total_pages))

    @reactive.effect
    def track_prev_clicks():
        clicks = input.prev()
        if clicks > prev_clicks.get():
            prev_clicks.set(clicks)
            current_page.set(max(current_page.get() - 1, 1))

    @output
    @render.text
    def page_info():
        total = len(filtered_data())
        page = current_page.get()
        max_page = max(1, math.ceil(total / QUOTES_PER_PAGE))
        return f"Página {page} de {max_page} ({total} citas encontradas)"

    @output
    @render.ui
    def quote_output():
        data = filtered_data()
        total = len(data)
        page = current_page.get()
        start = (page - 1) * QUOTES_PER_PAGE
        end = start + QUOTES_PER_PAGE

        if total == 0:
            return ui.tags.p("⚠️ No se encontraron citas con los filtros actuales.")

        quotes = [ui.tags.p(f"Mostrando citas {start + 1} a {min(end, total)} de {total}:")]
        for _, row in data.iloc[start:end].iterrows():
            quotes.append(
                ui.tags.div(
                    ui.tags.blockquote(f'"{row["Quote"]}"'),
                    ui.tags.p(f'{row["Interviewee"]} — Entrevista #{row["Interview #"]}, Tema: {row["Topic"]}'),
                    ui.tags.hr()
                )
            )
        return quotes

app = App(app_ui, server)