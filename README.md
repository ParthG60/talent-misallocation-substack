# Substack dashboards

Interactive dashboards that accompany posts on [parthsdatastack.substack.com](https://parthsdatastack.substack.com).

Each dashboard sits in its own subfolder with its own `dashboard.py` and `requirements.txt`, deployed separately on Streamlit Community Cloud.

## Dashboards in this repo

| Folder | Post | Deployed at |
|---|---|---|
| [`talent-misallocation/`](./talent-misallocation) | *The Great Talent Misallocation* | _(deploy URL goes here once live)_ |

## Adding a new dashboard

1. Create a new folder at the repo root, e.g. `<topic>/`.
2. Drop `dashboard.py`, `requirements.txt`, and any figures / helper scripts into it.
3. Push to GitHub, deploy on https://share.streamlit.io with *Main file path* = `<topic>/dashboard.py`.

## Run a dashboard locally

```bash
cd <folder>
pip install -r requirements.txt
streamlit run dashboard.py
```
