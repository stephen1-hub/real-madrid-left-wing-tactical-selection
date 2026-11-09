# ⚽ Real Madrid Left-Wing Tactical Selection Model

**Vinícius Júnior vs Yan Diomande**

An exploratory football analytics project evaluating two left-wing profiles through performance metrics, match ratings, positional deployment and tactical considerations.

[![Live Dashboard](https://img.shields.io/badge/Streamlit-Live%20Dashboard-red?logo=streamlit)](https://real-madrid-left-wing-tactical-selection-oa296memfc6junsuraemb.streamlit.app/)

---

## 1. Project Overview

Who offers the stronger statistical profile for Real Madrid's left-wing position: Vinícius Júnior or Yan Diomande?

This project investigates that question through football data analytics.

Rather than relying exclusively on reputation, goals or assists, the analysis compares both players using match-level performance data, attacking contributions, positional deployment and FotMob match ratings.

The objective is to develop an evidence-based framework for understanding their strengths, differences and potential tactical suitability for Real Madrid.

## 2. Research Questions

The analysis addresses four main questions:

1. How do Vinícius Júnior and Yan Diomande compare across key attacking metrics?
2. What differences exist in their attacking profiles and contributions?
3. Which player demonstrates stronger performance indicators when deployed as a starting left winger?
4. How robust are the selection conclusions under different evaluation scenarios?

---

## 3. Key Findings

The findings below are based on the LaLiga 2026/27 sample available at the time of data collection.

### 3.1 Overall Match Involvement

| Metric | Vinícius Júnior | Yan Diomande |
|---|---:|---:|
| Appearances | 8 | 12 |
| Minutes played | 585 | 714 |
| Starts | 7 | 7 |

**Key observation:** Both players recorded seven starts. However, Diomande accumulated more appearances and total playing time.

### 3.2 Performance as a Starting Left Winger

To improve positional relevance, the comparison isolates appearances in which each player started at left wing.

| Metric | Vinícius Júnior | Yan Diomande |
|---|---:|---:|
| Starts at LW | 7 | 5 |
| Minutes at LW | 565 | 434 |
| Goals | 1 | 3 |
| Assists | 3 | 1 |
| Goal contributions | 4 | 4 |
| G+A per 90 | 0.637 | 0.829 |

**Key observation:**

Both players recorded four goal contributions in their respective starting-left-wing samples.

However, Diomande produced those contributions in 434 minutes, compared with Vinícius's 565 minutes.

His goal-contribution rate was approximately 30% higher in this sample.

This suggests a stronger early production rate for Diomande in the selected sample, although it does not establish that he is the better overall player.

### 3.3 Positional Versatility

Diomande also featured as a starting right winger.

| Metric | Diomande at RW |
|---|---:|
| Starts | 2 |
| Minutes | 161 |
| Goals | 0 |
| Assists | 1 |
| G+A per 90 | 0.559 |

This provides an additional indication of his involvement across both wide positions.

### 3.4 Match Rating Comparison

FotMob match ratings provide another perspective on individual performance.

| Rating metric | Vinícius Júnior | Yan Diomande |
|---|---:|---:|
| Average rating | 7.586 | 8.160 |
| Median rating | 7.80 | 8.10 |
| Standard deviation | 0.756 | 0.631 |
| Ratings of 8.0 or higher | 2/7 | 4/5 |
| Rating range | 6.5–8.6 | 7.2–8.9 |

**Key observation:**

Diomande recorded a higher average and median match rating in the starting-left-wing sample.

His ratings also showed lower dispersion, indicating less variation within this small sample.

However, Vinícius has a larger sample of starting appearances at left wing. This difference must be considered when interpreting the results.

---

## 4. What Do the Findings Tell Us?

Three important observations emerge:

**1. Goal-contribution efficiency**

Diomande recorded the higher goal-contribution rate per 90 minutes in the starting-left-wing sample.

**2. Match performance**

Diomande recorded a higher average FotMob rating and more ratings of 8.0 or higher within the available sample.

**3. Sample size and context**

Vinícius has a larger starting-left-wing sample. Further observations are needed before making a definitive comparison.

The results suggest that Diomande presents an interesting statistical profile, but statistical superiority in a limited sample does not automatically translate into tactical superiority.

---

## 5. Analytical Methodology

The project follows a structured football analytics workflow:

1. **Data collection:** Gathering player and match-level performance information.
2. **Data preparation:** Cleaning and organising the datasets.
3. **Performance analysis:** Comparing relevant attacking indicators.
4. **Positional filtering:** Isolating starting-left-wing appearances.
5. **Metric calculation:** Evaluating goal contributions per 90 minutes.
6. **Rating analysis:** Comparing average ratings, medians and standard deviations.
7. **Tactical interpretation:** Evaluating the findings in the context of Real Madrid's left-wing requirements.

---

## 6. Interactive Dashboard

The Streamlit application brings the analysis together in an interactive environment.

### Dashboard Features

- Player profile comparisons.
- Key performance indicators.
- Attacking performance visualisations.
- Goal and assist analysis.
- Match-level performance analysis.
- Positional comparisons.
- Tactical selection insights.
- Scenario and robustness analysis.

### Explore the Live Dashboard

**[Launch the Real Madrid Left-Wing Tactical Selection Dashboard](https://real-madrid-left-wing-tactical-selection-oa296memfc6junsuraemb.streamlit.app/)**

---

## 7. Project Structure

```text
real-madrid-left-wing-tactical-selection/
│
├── app57.py
├── requirements.txt
├── README.md
│
└── data/
    ├── .gitkeep
    ├── player_profile.csv
    ├── player_metrics.csv
    └── left_wing_matches.csv
```

---

## 8. Technologies Used

| Technology | Application |
|---|---|
| Python | Data analysis and application development |
| Pandas | Data cleaning and manipulation |
| NumPy | Numerical computations |
| Streamlit | Interactive dashboard |
| Plotly | Interactive visualisations |
| Git and GitHub | Version control and project hosting |

---

## 9. Running the Application Locally

Clone the repository:

```bash
git clone https://github.com/stephen1-hub/real-madrid-left-wing-tactical-selection.git
```

Navigate to the project directory:

```bash
cd real-madrid-left-wing-tactical-selection
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run app57.py
```

---

## 10. Limitations and Interpretation

The findings should be interpreted with the following considerations:

- The comparison uses a relatively small number of starting appearances.
- The players' samples cover different match periods.
- FotMob ratings are provider-generated indicators and do not capture every aspect of individual performance.
- Goal contributions per 90 minutes can fluctuate considerably in small samples.
- Tactical suitability also depends on role, opposition quality, team structure, off-ball movement and responsibilities not fully represented by the available metrics.

Consequently, this analysis is an exploratory performance comparison rather than a definitive recruitment verdict.

---

## 11. Conclusion

The numbers create an interesting debate.

Diomande leads the available starting-left-wing sample in goal contributions per 90 minutes and average match rating. Vinícius provides a larger sample of starting appearances and remains an important benchmark for evaluating the position.

The central question is not simply who has the better numbers.

It is:

**Which player profile best supports Real Madrid's tactical requirements?**

Data does not replace football judgement. It makes that judgement more informed.

---

## Author

**Stephen Yaw Ayamah**

Football Data Analyst | Opposition Analysis | Performance Analytics

**Build → Analyse → Explain → Visualise → Publish.**
