import pandas as pd

EXCEL_FILE = "Dlyadashborda.xlsx"

SHEETS_CONFIG = [
    {"sheet": "ДПО",         "format": "ДПО"},
    {"sheet": "Среднесроки", "format": "Среднесрок"},
    {"sheet": "Интенсивы",   "format": "Интенсив"},
]

PERIOD = "1 сем 25-26"
NAPRAVLENIE_OOO = "ООО"

METRIC_MAP = {
    "Response Rate": "Response rate",
    "Response Rate %": "Response rate",
    "Response Rate % (отвечаемость)": "Response rate",

    "CSI ППС": "CSI",
    "CSI Куратор 1": "CSI",
    "CSI Программа": "CSI",
    "CSI УО": "CSI",
    "CSI общий": "CSI",

    "NPS": "NPS",

    "Доходимость": "Retention",
    "Retention Rate": "Retention",
    "Retention Rate %": "Retention",

    "отч %": "Отчисляемость",
    "акад %": "Академы",

    "SER (вовлечен)": "Transformation Rate",
    "SER (вовлечен) %": "Transformation Rate",

    "TER %": "TER",
    "TER % (качество студенческого опыта)": "TER",
}

def load_sheet(sheet_name: str) -> pd.DataFrame:
    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name)
    df = df.dropna(how="all").dropna(axis=1, how="all")
    df.columns = [str(c).strip() for c in df.columns]
    return df

long_rows = []

for cfg in SHEETS_CONFIG:
    try:
        df = load_sheet(cfg["sheet"])
    except Exception as e:
        print(f"Лист {cfg['sheet']} не найден или не читается: {e}")
        continue

    for _, row in df.iterrows():
        school = str(row.get("Школа", "")).strip()
        faculty = str(row.get("Факультет", "")).strip()
        program = str(row.get("Программа/курс", "")).strip()

        # общий по университету
        if school == "По университету":
            school_norm = "UU"
        else:
            school_norm = school or faculty

        if not school_norm and not program:
            continue

        for raw_col, metric_cat in METRIC_MAP.items():
            real_cols = [c for c in df.columns if raw_col in c]
            if not real_cols:
                continue

            for rc in real_cols:
                value = row.get(rc, None)
                if pd.isna(value):
                    continue

                long_rows.append(
                    {
                        "Период": PERIOD,
                        "Направление": NAPRAVLENIE_OOO,   # ООО
                        "Формат": cfg["format"],          # ДПО / Среднесрок / Интенсив
                        "Школа": school_norm,
                        "Факультет": faculty,
                        "Программа/курс": program,
                        "Метрика исходная": rc,
                        "Категория метрики": metric_cat,
                        "Значение": value,
                    }
                )

long_df = pd.DataFrame(long_rows)

if long_df.empty:
    print("long_df пустой — проверь, совпадают ли названия листов и колонок.")
else:
    long_df["Значение"] = pd.to_numeric(long_df["Значение"], errors="coerce")
    long_df = long_df.dropna(subset=["Значение"])

    long_df.to_excel("uu_long_metrics_ooo.xlsx", index=False)
    print("Готово, создан файл uu_long_metrics_ooo.xlsx с", len(long_df), "строками.")
    print("Форматы:", long_df["Формат"].unique())
    print("Школы:", long_df["Школа"].unique())