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

## Dashboard Features

The Streamlit application provides:

- Player profile comparisons.
- Key performance indicators.
- Attacking performance visualisations.
- Match-level analysis.
- Tactical selection insights.
- Scenario and robustness analysis.

## Project Structure

```text
real-madrid-left-wing-tactical-selection/
│
├── app57.py
├── requirements.txt
├── README.md
│
└── data/
    ├── left_wing_matches.csv
    ├── player_metrics.csv
    └── player_profile.csv
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
