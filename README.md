# Real Madrid Left-Wing Tactical Selection Model

## Project Overview

This project evaluates two left-wing options for Real Madrid: **Vinícius Júnior and Yan Diomande**.

The objective is to assess how each player's statistical profile, attacking contribution and tactical characteristics could influence Real Madrid's left-wing selection.

Rather than relying solely on goals and assists, the analysis considers a broader set of performance indicators to support a more evidence-based player comparison.

## Research Questions

1. How do Vinícius Júnior and Yan Diomande compare across key attacking metrics?
2. What differences exist in their attacking profiles and contributions?
3. Which player offers characteristics that may better suit Real Madrid's left-wing requirements?
4. How robust are the selection conclusions under different evaluation scenarios?

## Analytical Approach

The project follows a structured football analytics workflow:

- **Data preparation:** Organising player and match-level performance data.
- **Performance analysis:** Comparing relevant attacking and contribution metrics.
- **Player profiling:** Examining the strengths and differences in each player's statistical profile.
- **Tactical evaluation:** Interpreting the findings in the context of Real Madrid's left-wing role.
- **Scenario analysis:** Exploring how different evaluation assumptions affect the selection assessment.

Key Findings

The analysis focuses on the LaLiga 2026/27 sample available at the time of data collection.

1. Overall match involvement

Metric

Vinícius Júnior

Yan Diomande

Appearances

8

12

Minutes played

585

714

Starts

7

7

Both players recorded seven starts, although Diomande accumulated more total appearances and minutes.

2. Performance as a starting left winger

To make the comparison more positionally relevant, the analysis isolates their appearances when starting at left wing.

Metric

Vinícius Júnior

Yan Diomande

Starts at LW

7

5

Minutes at LW

565

434

Goals

1

3

Assists

3

1

Goal contributions

4

4

G+A per 90

0.637

0.829

Key observation: Both players recorded four goal contributions in their starting-left-wing samples.

However, Diomande produced those four contributions in 434 minutes, compared with Vinícius's 565 minutes.

His goal-contribution rate was approximately 30% higher in this sample.

This is an encouraging early signal, not proof that Diomande is the better player.

3. Positional versatility

Diomande also featured as a starting right winger:

Metric

Diomande at RW

Starts

2

Minutes

161

Goals

0

Assists

1

G+A per 90

0.559

This provides an additional indication of his involvement across the two wide positions.

4. Match rating consistency

FotMob match ratings provide another perspective on performance.

Rating metric

Vinícius Júnior

Yan Diomande

Average rating

7.586

8.160

Median rating

7.80

8.10

Standard deviation

0.756

0.631

Ratings of 8.0 or higher

2/7

4/5

Rating range

6.5–8.6

7.2–8.9

## Dashboard Features

The Streamlit application provides:

- Player profile comparisons.
- Key performance indicators.
- Attacking performance visualisations.
- Match-level analysis.
- Tactical selection insights.
- Scenario and robustness analysis.
# Dashboard link: https://real-madrid-left-wing-tactical-selection-oa296memfc6junsuraemb.streamlit.app/

## Project Structure

```text
real-madrid-left-wing-tactical-selection/
├── app57.py
├── requirements.txt
├── README.md
└── data/
    ├── .gitkeep
    ├── player_profile.csv
    ├── player_metrics.csv
    └── left_wing_matches.csv
```

## Technologies

- Python
- Pandas
- NumPy
- Streamlit
- Plotly
- Data visualisation and statistical analysis

## Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/stephen1-hub/real-madrid-left-wing-tactical-selection.git
```

Move into the project directory:

```bash
cd real-madrid-left-wing-tactical-selection
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app57.py
```

## Deployment

The application is designed for deployment using Streamlit Community Cloud.

Repository: [GitHub Project](https://github.com/stephen1-hub/real-madrid-left-wing-tactical-selection)

## Important Note

This is an analytical decision-support project. Statistical
