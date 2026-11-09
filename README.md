# Real Madrid Left-Wing Tactical Selection Model

## Run on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If you already have a virtual environment and dependencies installed, run:

```powershell
py -m streamlit run app.py
```

## Files

- `app.py`: Streamlit tactical selection model.
- `data/player_profile.csv`: player season profile and reconciled minutes.
- `data/player_metrics.csv`: FotMob leaderboard snapshot metrics.
- `data/left_wing_matches.csv`: verified left-wing start match log.

## Important interpretation notes

- The match log supports position-specific left-wing ratings, minutes and goal contributions.
- The leaderboard snapshot metrics are season-level and are not confirmed as left-wing-only.
- Diomande's leaderboard snapshot used 630 minutes while the reconciled profile shows 714; snapshot per-90 metrics remain provisional.
- Relative scores compare only Vinícius and Diomande. They are not league percentiles.
- Weights are transparent user assumptions, not empirically fitted coefficients.
- The tool is decision support, not a validated prediction model.


## Scoring engine update (v2)
Metric comparisons use a symmetric bounded relative-advantage score:
- 50 means the two values are equal.
- Above 50 favours the first player; below 50 favours the second.
- The two player scores sum to 100 for each metric.
- Small differences remain small; the model no longer min-max stretches every two-player difference to 0 and 100.
- A metric is compared only when both players have valid values.
- Dimension scores are averaged from paired metric scores and are not rescaled a second time.


## Version 3 — Monte Carlo weight robustness
The dashboard now samples tactical weight combinations using a Dirichlet distribution.
It reports the share of sampled combinations under which each player leads, the
distribution of weighted-score margins, and how lead frequency changes across
weight bands. These are robustness diagnostics for model assumptions, not
probabilities of match outcomes or player success.
