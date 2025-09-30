import plotly.express as px

def must_have_skills(df, column):
    column_titles = {
        "must_have_work_exp": "Arbetslivserfarenhet",
        "must_have_edu_level": "Utbildningsnivå",
        "must_have_skills": "Efterfrågade skills"
    }

    total = len(df)

    df_excluded = df[df[column] != "ej specificerad"]
    excluded_count = total - len(df_excluded)

    top_values = (
        df_excluded.groupby(column)
          .size()
          .reset_index(name="Antal") 
          .sort_values("Antal", ascending=False)
          .head(10)
    )

    fig = px.pie(
        top_values,
        values="Antal",                 
        names=column,                   
        title=f"Topp 10 {column_titles.get(column, column)}"
    )

    if total > 0:
        excluded_pct = round(excluded_count / total * 100, 1)
    else:
        excluded_pct = 0

    return fig, excluded_pct
