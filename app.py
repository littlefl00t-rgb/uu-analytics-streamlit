import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Аналитика UU 25–26", layout="wide")

@st.cache_data
def load_ooo():
    return pd.read_excel("uu_long_metrics_ooo.xlsx")

@st.cache_data
def load_vo():
    return pd.DataFrame()  # заглушка под ВО

@st.cache_data
def load_spo():
    return pd.DataFrame()  # заглушка под СПО

st.title("Аналитика UU 25–26")

main_direction = st.selectbox(
    "Направление",
    ["ООО", "ВО", "СПО"],
    index=0,
)

if main_direction == "ООО":
    df = load_ooo()
    if df.empty:
        st.error("Нет данных для ООО (uu_long_metrics_ooo.xlsx пустой или не найден).")
        st.stop()

    st.subheader("ООО: ДПО / Среднесрок / Интенсив")

    all_schools = ["Все школы"] + sorted(df["Школа"].dropna().unique())
    all_formats = ["Все форматы"] + sorted(df["Формат"].dropna().unique())
    all_faculties = ["Все факультеты"] + sorted(df["Факультет"].dropna().unique())
    all_programs = ["Все программы"] + sorted(df["Программа/курс"].dropna().unique())
    all_metric_cats = [
        "CSI",
        "NPS",
        "Response rate",
        "Retention",
        "Отчисляемость",
        "Академы",
        "Transformation Rate",
        "TER",
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        school = st.selectbox("Школа", all_schools)

    with col2:
        fmt = st.selectbox("Формат (ДПО / Среднесрок / Интенсив)", all_formats)

    with col3:
        faculty = st.selectbox("Факультет", all_faculties)

    program = st.selectbox("Программа/курс", all_programs)
    metric_cat = st.selectbox("Категория метрик", all_metric_cats)

    dff = df.copy()
    dff = dff[dff["Категория метрики"] == metric_cat]

    if school != "Все школы":
        dff = dff[dff["Школа"] == school]

    if fmt != "Все форматы":
        dff = dff[dff["Формат"] == fmt]

    if faculty != "Все факультеты":
        dff = dff[dff["Факультет"] == faculty]

    if program != "Все программы":
        dff = dff[dff["Программа/курс"] == program]

    if dff.empty:
        st.warning("Для выбранных фильтров нет данных.")
        st.stop()

    st.subheader(f"{metric_cat} — ООО")

    view_type = st.radio(
        "Что смотреть?",
        ["По школам", "По форматам", "По программам"],
        horizontal=True,
    )

    if view_type == "По школам":
        agg = (
            dff.groupby("Школа")["Значение"]
            .mean()
            .reset_index()
            .sort_values("Значение", ascending=True)
        )
        fig = px.bar(
            agg,
            x="Значение",
            y="Школа",
            orientation="h",
            title=f"{metric_cat} по школам",
        )

    elif view_type == "По форматам":
        agg = (
            dff.groupby("Формат")["Значение"]
            .mean()
            .reset_index()
            .sort_values("Значение", ascending=True)
        )
        fig = px.bar(
            agg,
            x="Значение",
            y="Формат",
            orientation="h",
            title=f"{metric_cat} по форматам (ДПО / Среднесрок / Интенсив)",
        )

    else:  # По программам
        agg = (
            dff.groupby("Программа/курс")["Значение"]
            .mean()
            .reset_index()
            .sort_values("Значение", ascending=True)
        )
        fig = px.bar(
            agg,
            x="Значение",
            y="Программа/курс",
            orientation="h",
            title=f"{metric_cat} по программам",
        )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Таблица")

    st.dataframe(
        dff.sort_values(["Школа", "Формат", "Факультет", "Программа/курс"]),
        use_container_width=True,
    )

elif main_direction == "ВО":
    df_vo = load_vo()
    st.info("Блок ВО подключим, когда будет готов файл для ВО.")

else:  # СПО
    df_spo = load_spo()
    st.info("Блок СПО подключим, когда будет готов файл для СПО.")