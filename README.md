# Real Madrid Left-Wing Tactical Selection

**Vinícius Júnior vs Yan Diomande | LaLiga 2026/27**

## Overview

Who should start at left wing for Real Madrid?

This project develops a data-driven tactical selection framework comparing Vinícius Júnior and Yan Diomande using FotMob-derived performance data.

Rather than relying exclusively on goals, assists or player ratings, the analysis evaluates five tactical dimensions:

- Attacking threat
- Creativity
- Ball progression
- Defensive contribution
- Performance reliability

## Research Questions

1. Who offers the strongest overall left-wing profile?
2. Does the preferred player change under different tactical scenarios?
3. How sensitive is the selection to tactical weighting assumptions?
4. Under what conditions does Diomande become the preferred option?

## Methodology

The project combines:

- Position-specific match analysis.
- Per-90 performance metrics.
- Relative-advantage scoring.
- Weighted tactical selection.
- Five predefined tactical scenarios.
- Monte Carlo weight-distribution robustness testing.

The weight-distribution experiment investigates how frequently each player leads under different plausible tactical priorities.

## Key Findings

- Vinícius leads four of five predefined tactical scenarios.
- Diomande leads the pressing and defensive-work scenario.
- Vinícius has stronger attacking-threat and creativity scores.
- Diomande has stronger progression and defensive-contribution scores.
- The broad weight-distribution experiment favours Diomande more frequently.

These results are exploratory and do not establish a permanent selection hierarchy.

## Sample Definition

| Measure | Vinícius | Diomande |
|---|---:|---:|
| Verified LW starts | 7 | 5 |
| LW minutes | 565 | 434 |
| LW goals | 1 | 3 |
| LW assists | 3 | 1 |
| LW goal contributions | 4 | 4 |

## Technology Stack

- Python
- Pandas
- NumPy
- Plotly
- Streamlit
- FotMob-derived data

## Running the Dashboard
real-madrid-left-wing-tactical-selection/
│
├── app57.py
├── requirements.txt
│
└── data/
    ├── player_profile.csv
    ├── player_metrics.csv
    └── left_wing_matches.csv
```

## Limitations

The study uses a small number of verified left-wing starts. Some tactical metrics are season-wide rather than position-specific. The weight distributions represent modelling assumptions, not actual coaching preferences or probabilities of match success.

## Research Status

Exploratory tactical selection model developed. Further validation using position-specific metrics, opponent tactical profiles and team-level impact analysis is required.
