import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================
# REAL MADRID LEFT-WING TACTICAL SELECTION MODEL
# Decision objective: next-match selection
# Approach: balanced statistical + tactical evaluation
# ============================================================

st.set_page_config(
    page_title="Real Madrid | Tactical Left-Wing Selection",
    page_icon="⚽",
    layout="wide"
)

DATA_DIR = Path(__file__).parent / "data"
PLAYERS = ["Vinícius Júnior", "Yan Diomande"]

# Proposed starting weights. These are decision assumptions, not
# empirically estimated coefficients.
DEFAULT_WEIGHTS = {
    "Attacking threat": 25,
    "Creativity": 25,
    "Ball progression": 20,
    "Defensive contribution": 15,
    "Performance reliability": 15,
}

PRESETS = {
    "Balanced (default)": DEFAULT_WEIGHTS,
    "Direct attacking threat": {
        "Attacking threat": 35, "Creativity": 20,
        "Ball progression": 25, "Defensive contribution": 10,
        "Performance reliability": 10,
    },
    "Possession and creation": {
        "Attacking threat": 15, "Creativity": 35,
        "Ball progression": 25, "Defensive contribution": 10,
        "Performance reliability": 15,
    },
    "Pressing and defensive work": {
        "Attacking threat": 15, "Creativity": 15,
        "Ball progression": 15, "Defensive contribution": 35,
        "Performance reliability": 20,
    },
    "Low-block problem solving": {
        "Attacking threat": 30, "Creativity": 30,
        "Ball progression": 25, "Defensive contribution": 5,
        "Performance reliability": 10,
    },
}

@st.cache_data
def load_data():
    profile = pd.read_csv(DATA_DIR / "player_profile.csv")
    metrics = pd.read_csv(DATA_DIR / "player_metrics.csv")
    matches = pd.read_csv(DATA_DIR / "left_wing_matches.csv")
    matches["date"] = pd.to_datetime(matches["date"])
    return profile, metrics, matches

try:
    profile, raw_metrics, all_matches = load_data()
except Exception as exc:
    st.error(f"Could not load dashboard data: {exc}")
    st.stop()

# ---------- Helpers ----------
def metric_value(metric_name, player):
    row = raw_metrics.loc[raw_metrics["metric"] == metric_name]
    if row.empty:
        return np.nan
    col = "vinicius" if player == PLAYERS[0] else "diomande"
    return pd.to_numeric(row.iloc[0][col], errors="coerce")

def profile_value(player, column):
    row = profile.loc[profile["player"] == player, column]
    return pd.to_numeric(row.iloc[0], errors="coerce") if not row.empty else np.nan

def safe_mean(values):
    vals = pd.to_numeric(pd.Series(values), errors="coerce").dropna()
    return float(vals.mean()) if len(vals) else np.nan

def relative_advantage_score(a, b, higher_is_better=True):
    """
    Symmetric two-player comparison:
    50 = equal, above 50 = advantage for player A, below 50 = advantage for B.
    The score is bounded 0-100 and does not turn every small difference into 0/100.
    Requires both values; missing values stay missing.
    """
    if pd.isna(a) or pd.isna(b):
        return np.nan, np.nan
    a, b = float(a), float(b)
    if not higher_is_better:
        a, b = -a, -b
    denom = abs(a) + abs(b)
    if np.isclose(denom, 0):
        return 50.0, 50.0
    score_a = 50.0 + 50.0 * ((a - b) / denom)
    score_a = float(np.clip(score_a, 0, 100))
    return score_a, 100.0 - score_a

def paired_metric_scores(values, higher_is_better=True):
    """Return comparable scores for both players; never score one-sided data."""
    a, b = values[0], values[1]
    return relative_advantage_score(a, b, higher_is_better)

def fmt(value, digits=2):
    return "—" if pd.isna(value) else f"{value:.{digits}f}"

# ---------- Sidebar ----------
st.title("⚽ Real Madrid | Left-Wing Tactical Selection")
st.caption("Vinícius Júnior vs Yan Diomande · LaLiga 2026/27 · Next-match decision support")

with st.sidebar:
    st.header("Selection controls")
    selected_scenario = st.selectbox("Match-plan scenario", list(PRESETS.keys()), index=0)
    st.caption("Choose the tactical requirement you expect from the left winger. These presets change the model weights; they do not represent opponent-specific evidence.")
    st.divider()
    st.subheader("Model weights")
    preset = PRESETS[selected_scenario]
    weights = {}
    for dimension, default in preset.items():
        weights[dimension] = st.slider(
            dimension, min_value=0, max_value=50, value=int(default), step=5
        )
    weight_total = sum(weights.values())
    st.caption(f"Selected weights total: {weight_total}%")
    if weight_total == 0:
        st.warning("Set at least one dimension above zero.")

matches = all_matches[all_matches["player"].isin(PLAYERS)].copy()
matches["goal_contributions"] = matches["goals"] + matches["assists"]

# Match-derived LW summary is the authoritative position-specific source.
lw_summary = matches.groupby("player").agg(
    lw_starts=("date", "count"),
    lw_minutes=("minutes", "sum"),
    lw_average_rating=("rating", "mean"),
    lw_rating_std=("rating", "std"),
    lw_median_rating=("rating", "median"),
    lw_goals=("goals", "sum"),
    lw_assists=("assists", "sum"),
    lw_goal_contributions=("goal_contributions", "sum"),
).reindex(PLAYERS)

# ---------- Metric groups ----------
# These leaderboard metrics are current-season snapshots and are not
# position-filtered. They are labelled as season-wide / provisional.
dimension_metrics = {
    "Attacking threat": [
        ("xG", True, "Expected goals"),
        ("shots_per90", True, "Shots per 90"),
        ("shots_on_target_per90", True, "Shots on target per 90"),
    ],
    "Creativity": [
        ("xA", True, "Expected assists"),
        ("chances_created", True, "Chances created"),
        ("big_chances_created", True, "Big chances created"),
    ],
    "Ball progression": [
        ("successful_dribbles_per90", True, "Successful dribbles per 90"),
        ("accurate_passes_per90", True, "Accurate passes per 90 (volume)"),
        ("line_breaking_passes_per90", True, "Line-breaking passes per 90"),
    ],
    "Defensive contribution": [
        ("defensive_actions_per90", True, "Defensive actions per 90"),
        ("tackles_per90", True, "Tackles per 90"),
        ("recoveries_per90", True, "Recoveries per 90"),
    ],
}

# Build dimension scores from the metrics that actually exist.
metric_rows = []
dimension_raw = {p: {} for p in PLAYERS}
for dimension, items in dimension_metrics.items():
    for metric, higher, label in items:
        values = [metric_value(metric, p) for p in PLAYERS]
        score_a, score_b = paired_metric_scores(values, higher)
        scores = [score_a, score_b]
        # Only include a metric when both players have a reported value.
        if pd.notna(score_a) and pd.notna(score_b):
            for i, player in enumerate(PLAYERS):
                metric_rows.append({
                    "Dimension": dimension,
                    "Metric": label,
                    "Player": player,
                    "Reported value": values[i],
                    "Pairwise score": scores[i],
                    "Source metric": metric,
                })
    for player in PLAYERS:
        player_rows = [r["Pairwise score"] for r in metric_rows
                       if r["Dimension"] == dimension and r["Player"] == player]
        dimension_raw[player][dimension] = safe_mean(player_rows)

# Reliability: average match rating, lower rating volatility, and sample depth.
# Small-sample shrinkage pulls mean ratings toward a neutral 7.5 reference.
reliability_raw = {}
for player in PLAYERS:
    s = lw_summary.loc[player]
    n = int(s["lw_starts"]) if pd.notna(s["lw_starts"]) else 0
    mean_rating = s["lw_average_rating"]
    rating_std = s["lw_rating_std"]
    shrink_mean = ((n * mean_rating) + (3 * 7.5)) / (n + 3) if n and pd.notna(mean_rating) else np.nan
    reliability_raw[player] = {
        "shrunken_rating": shrink_mean,
        "rating_stability": -rating_std if pd.notna(rating_std) else np.nan,
        "sample_depth": min(n / 8, 1.0) * 100,
    }

reliability_components = {
    "rating": paired_metric_scores(
        [reliability_raw[p]["shrunken_rating"] for p in PLAYERS], True
    ),
    "stability": paired_metric_scores(
        [reliability_raw[p]["rating_stability"] for p in PLAYERS], True
    ),
    "sample": paired_metric_scores(
        [reliability_raw[p]["sample_depth"] for p in PLAYERS], True
    ),
}
for i, p in enumerate(PLAYERS):
    component_scores = [pair[i] for pair in reliability_components.values()]
    dimension_raw[p]["Performance reliability"] = safe_mean(component_scores)

# Dimension scores are already on a common 0-100 paired-comparison scale.
# Do not min-max rescale them a second time.
score_rows = []
for dimension in DEFAULT_WEIGHTS:
    for p in PLAYERS:
        score_rows.append({
            "Player": p,
            "Dimension": dimension,
            "Score": dimension_raw[p].get(dimension, np.nan),
        })
dimension_scores = pd.DataFrame(score_rows)

# Weighted total uses only available dimensions, with weights renormalized
# across dimensions with data for that player.
model_rows = []
for player in PLAYERS:
    available = dimension_scores[
        (dimension_scores["Player"] == player) &
        (dimension_scores["Score"].notna())
    ]
    weighted_sum, weight_sum = 0.0, 0.0
    for _, r in available.iterrows():
        w = weights.get(r["Dimension"], 0)
        weighted_sum += r["Score"] * w
        weight_sum += w
    total = weighted_sum / weight_sum if weight_sum > 0 else np.nan
    model_rows.append({"Player": player, "Weighted score": total, "Weight coverage": weight_sum})
model = pd.DataFrame(model_rows)

# ---------- Decision summary ----------
st.subheader("Next-match selection assessment")
if weight_total == 0:
    st.info("Adjust the weights in the sidebar to calculate a selection assessment.")
else:
    valid_model = model.dropna(subset=["Weighted score"]).sort_values("Weighted score", ascending=False)
    if len(valid_model) == 2:
        winner = valid_model.iloc[0]
        runner = valid_model.iloc[1]
        gap = winner["Weighted score"] - runner["Weighted score"]
        if gap < 5:
            strength = "Very close"
        elif gap < 15:
            strength = "Moderate separation"
        else:
            strength = "Clear separation on selected weights"
        c1, c2, c3 = st.columns(3)
        c1.metric("Model leader", winner["Player"])
        c2.metric("Weighted score", f'{winner["Weighted score"]:.1f}/100')
        c3.metric("Margin", f'{gap:.1f} points')
        st.info(
            f"**{strength}.** This is a decision-support result under the selected weights, "
            "not a statistically validated prediction of match performance."
        )
    else:
        st.warning("Insufficient metric coverage to calculate a comparison.")

# ---------- Position-specific evidence ----------
st.subheader("Verified left-wing match evidence")
evidence = lw_summary.reset_index().rename(columns={
    "player": "Player", "lw_starts": "LW starts", "lw_minutes": "LW minutes",
    "lw_average_rating": "Mean rating", "lw_median_rating": "Median rating",
    "lw_goals": "LW goals", "lw_assists": "LW assists",
    "lw_goal_contributions": "LW goal contributions",
})
evidence["LW G+A per 90"] = evidence["LW goal contributions"] / evidence["LW minutes"] * 90
st.dataframe(evidence.round(3), use_container_width=True, hide_index=True)

# ---------- Dimension score chart ----------
st.subheader("Tactical dimension comparison")
dim_chart = dimension_scores.dropna(subset=["Score"])
fig = px.bar(
    dim_chart, x="Dimension", y="Score", color="Player", barmode="group",
    text_auto=".0f", range_y=[0, 110],
    title="Relative scores within this two-player comparison"
)
fig.update_layout(yaxis_title="Relative score (0–100)", xaxis_title="")
st.plotly_chart(fig, use_container_width=True)
st.caption(
    "A score of 100 means the stronger value between these two players for that dimension; "
    "50 means equal or unavailable single-player comparison. This is not a league percentile."
)

# ---------- Weighted result table ----------
st.subheader("Weighted selection model")
st.dataframe(
    model.rename(columns={
        "Player": "Player",
        "Weighted score": "Weighted score / 100",
        "Weight coverage": "Available weight points",
    }).round(2),
    use_container_width=True,
    hide_index=True
)

# ---------- Metric audit ----------
with st.expander("Inspect the metrics driving each dimension"):
    if metric_rows:
        audit = pd.DataFrame(metric_rows)
        st.dataframe(
            audit.sort_values(["Dimension", "Metric", "Player"]),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No leaderboard metrics were available.")

# ---------- Scenario interpretation ----------
st.subheader("Tactical interpretation")
interpretations = {
    "Attacking threat": "Shot generation and expected-goal involvement. This does not fully capture shot quality, movement or tactical access to the box.",
    "Creativity": "Chance creation and expected-assist involvement. These are output indicators, not a complete measure of decision quality.",
    "Ball progression": "Dribbling, passing volume and line-breaking passes. Accurate passes per 90 is a volume measure, not a pass-accuracy percentage.",
    "Defensive contribution": "Defensive actions, tackles and recoveries. These can overlap conceptually and should not be summed as independent events.",
    "Performance reliability": "Match ratings, rating variation and the number of verified LW starts. The rating mean is shrunk toward 7.5 using a small-sample prior of three matches."
}
for dimension in DEFAULT_WEIGHTS:
    st.markdown(f"**{dimension}.** {interpretations[dimension]}")

# ---------- Sensitivity ----------
st.subheader("Weight sensitivity")
st.write("This tests whether the model leader changes across the predefined tactical weight profiles.")
sensitivity_rows = []
for preset_name, preset_weights in PRESETS.items():
    vals = {}
    for p in PLAYERS:
        rows = dimension_scores[dimension_scores["Player"] == p]
        score_map = dict(zip(rows["Dimension"], rows["Score"]))
        usable = [(score_map.get(d), w) for d, w in preset_weights.items()
                  if pd.notna(score_map.get(d)) and w > 0]
        denom = sum(w for _, w in usable)
        vals[p] = sum(s * w for s, w in usable) / denom if denom else np.nan
    leader = max(vals, key=lambda k: vals[k] if pd.notna(vals[k]) else -np.inf)
    sensitivity_rows.append({
        "Scenario": preset_name,
        "Vinícius score": vals[PLAYERS[0]],
        "Diomande score": vals[PLAYERS[1]],
        "Scenario leader": leader,
    })
sensitivity = pd.DataFrame(sensitivity_rows)
st.dataframe(sensitivity.round(1), use_container_width=True, hide_index=True)

# ---------- Monte Carlo weight robustness ----------
st.subheader("Monte Carlo tactical-weight robustness")
st.write(
    "This experiment samples plausible non-negative tactical weight combinations "
    "and tests how often each player leads. It explores the model's assumptions; "
    "it does not estimate real-world probabilities of match success."
)

mc1, mc2 = st.columns(2)
with mc1:
    n_simulations = st.selectbox(
        "Weight combinations",
        [1000, 5000, 10000, 50000, 100000],
        index=2
    )
with mc2:
    concentration = st.selectbox(
        "Weight distribution",
        ["Broad variation", "Moderate variation", "Near-balanced variation"],
        index=0
    )

alpha_map = {
    "Broad variation": 1.0,
    "Moderate variation": 3.0,
    "Near-balanced variation": 10.0,
}
alpha = alpha_map[concentration]

dims = list(DEFAULT_WEIGHTS.keys())
score_a = np.array([
    dimension_raw[PLAYERS[0]].get(d, np.nan) for d in dims
], dtype=float)
score_b = np.array([
    dimension_raw[PLAYERS[1]].get(d, np.nan) for d in dims
], dtype=float)

paired_available = np.isfinite(score_a) & np.isfinite(score_b)
if paired_available.sum() < 2:
    st.warning("Insufficient paired tactical dimensions for a meaningful weight experiment.")
else:
    rng = np.random.default_rng(20261109)
    sampled_weights = rng.dirichlet(
        np.full(int(paired_available.sum()), alpha),
        size=int(n_simulations)
    )
    score_differences = score_a[paired_available] - score_b[paired_available]
    simulated_margins = sampled_weights @ score_differences

    vini_win = float(np.mean(simulated_margins > 1e-9))
    diomande_win = float(np.mean(simulated_margins < -1e-9))
    tie_rate = float(np.mean(np.abs(simulated_margins) <= 1e-9))

    r1, r2, r3 = st.columns(3)
    r1.metric("Vinícius leads", f"{vini_win:.1%}")
    r2.metric("Diomande leads", f"{diomande_win:.1%}")
    r3.metric("Near-ties", f"{tie_rate:.1%}")

    st.caption(
        f"{int(n_simulations):,} simulated weight combinations · "
        f"Dirichlet α={alpha:g} · seed=20261109 · "
        f"{int(paired_available.sum())}/5 paired dimensions included"
    )

    distribution = pd.DataFrame({
        "Weighted-score margin (Vinícius − Diomande)": simulated_margins
    })
    fig = px.histogram(
        distribution,
        x="Weighted-score margin (Vinícius − Diomande)",
        nbins=45,
        title="Distribution of simulated selection margins"
    )
    fig.add_vline(x=0, line_dash="dash", line_color="white")
    fig.update_layout(yaxis_title="Number of weight combinations")
    st.plotly_chart(fig, use_container_width=True)

    q = np.percentile(simulated_margins, [5, 25, 50, 75, 95])
    st.write({
        "5th percentile margin": round(float(q[0]), 2),
        "25th percentile margin": round(float(q[1]), 2),
        "Median margin": round(float(q[2]), 2),
        "75th percentile margin": round(float(q[3]), 2),
        "95th percentile margin": round(float(q[4]), 2),
    })

    st.markdown("**When does each player tend to lead?**")
    weight_frame = pd.DataFrame(
        sampled_weights,
        columns=[d for d, ok in zip(dims, paired_available) if ok]
    )
    weight_frame["Vinícius leads"] = simulated_margins > 0
    condition_rows = []
    for dimension in weight_frame.columns.drop("Vinícius leads"):
        weight_bins = pd.qcut(
            weight_frame[dimension], q=5, duplicates="drop"
        )
        grouped = weight_frame.groupby(weight_bins, observed=True)["Vinícius leads"].mean()
        for interval, win_share in grouped.items():
            condition_rows.append({
                "Dimension": dimension,
                "Weight band": str(interval),
                "Vinícius lead frequency": win_share,
                "Diomande lead frequency": 1 - win_share,
            })
    condition_table = pd.DataFrame(condition_rows)
    st.dataframe(
        condition_table.assign(
            **{
                "Vinícius lead frequency": condition_table["Vinícius lead frequency"].map(lambda x: f"{x:.1%}"),
                "Diomande lead frequency": condition_table["Diomande lead frequency"].map(lambda x: f"{x:.1%}"),
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Interpretation: these percentages describe how often a player leads under "
        "the chosen mathematical distribution of weights. They are not probabilities "
        "that the player will perform better in the next match."
    )

# ---------- Match log ----------
with st.expander("View verified left-wing match log"):
    st.dataframe(
        matches[["player", "date", "opponent", "position", "minutes", "goals", "assists", "rating"]]
        .sort_values(["player", "date"]),
        use_container_width=True,
        hide_index=True
    )

# ---------- Limitations ----------
with st.expander("Methodology, assumptions and limitations"):
    st.markdown("""
    **Decision objective:** next-match left-wing selection.  
    **Approach:** balanced statistical and tactical decision support.

    **Critical data distinction**
    - The match log contains verified left-wing starts: Vinícius 7; Diomande 5.
    - Ratings, minutes and goal contributions in the evidence table are calculated from those LW starts only.
    - The FotMob leaderboard metrics in `player_metrics.csv` are season-level snapshot values, not verified LW-only values. They are used as contextual indicators, not position-specific proof.
    - The Diomande leaderboard snapshot used 630 minutes, while the reconciled profile shows 714 minutes. Per-90 snapshot metrics therefore remain provisional.

    **Scoring design**
    - Each metric uses a symmetric paired relative-advantage score; it is not a league percentile.
    - Dimension scores average available metrics. Missing values are omitted, not set to zero.
    - Dimension weights are user-defined assumptions and are renormalized over available dimensions.
    - Reliability uses match ratings, rating variation and LW-start sample depth. The rating mean is shrunk toward 7.5 with a three-match prior to reduce overreaction to small samples.
    - Scenario presets are tactical hypotheses. No opponent-specific tactical data is included.

    **What this model cannot yet establish**
    - It cannot identify which player is better against a particular opponent or defensive structure.
    - It does not measure team performance with each player starting at LW, off-ball runs, pressing triggers, positional rotations, weak-foot usage or coach instructions.
    - The samples are small and non-contemporaneous. The result is descriptive decision support, not causal evidence or a validated forecast.
    """)

st.divider()
st.caption(
    "Real Madrid left-wing selection model · LaLiga 2026/27 · "
    "Refresh source data and validate assumptions before operational use."
)
