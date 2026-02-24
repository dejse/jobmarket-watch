# %% [markdown]
# # Job Scrapper

# %%
import re
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup

# %%
today = date.today().isoformat()
link_list = [
    "https://www.karriere.at/jobs/controller/wien",
    "https://www.karriere.at/jobs/controller/linz",
    "https://www.karriere.at/jobs/controller/salzburg",
    "https://www.karriere.at/jobs/controller/graz",
    "https://www.karriere.at/jobs/controller/innsbruck",
    "https://www.karriere.at/jobs/controller/vorarlberg",
]

# %%
# Read existing data or create new DataFrame
try:
    df = pd.read_csv("./data/data.csv")
except FileNotFoundError:
    df = pd.DataFrame(
        columns=["date", "location", "job_count"],
    )
    df = df.astype({"date": str, "location": str, "job_count": int})

# %%
for link in link_list:
    response = None
    max_retries = 3

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(link, headers=headers, timeout=5)
            if response.status_code == 200:
                break
            else:
                print(
                    f"Attempt {attempt + 1}: Status code {response.status_code} from {link}"
                )
        except requests.RequestException as e:
            print(f"Attempt {attempt + 1}: Request failed for {link} - {e}")

    if response is None or response.status_code != 200:
        print(f"Failed to retrieve data from {link} after {max_retries} attempts")
        continue

    # get the content of the css selector .m-jobsListHeader__title
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.select_one(".m-jobsListHeader__title").get_text()
    title = title.strip()

    match = re.search(r"(\d+)", title)
    job_count = int(match.group(1)) if match else 0

    # write to pandas dataframe
    location = link.split("/")[-1]
    new_row = {
        "date": today,
        "location": location.capitalize(),
        "job_count": job_count,
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# %%
# df

# %%
df.to_csv("./data/data.csv", index=False)


# %% 
import plotly.express as px

fig = px.line(
    df,
    x="date",
    y="job_count",
    color="location",
    title="Controller Jobs laut Karriere.at",
    labels={"date": "Date", "job_count": "Job Count", "location": "Location"},
    markers=True,
    template="plotly_white",
)

fig.update_layout(
    hovermode="x unified",
    font=dict(family="Arial, sans-serif", size=12),
    title_font=dict(size=18, color="#2C3E50"),
    xaxis_title_font=dict(size=14, color="#34495E"),
    yaxis_title_font=dict(size=14, color="#34495E"),
    width=800,
    height=500,
    plot_bgcolor="rgba(240, 240, 240, 0.5)",
    paper_bgcolor="white",
)

fig.update_traces(line=dict(width=2.5))

# fig.show()


# %%
fig.write_image("./plot.png", format="png")


