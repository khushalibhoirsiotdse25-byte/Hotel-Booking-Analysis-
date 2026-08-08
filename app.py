import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Hotel Booking Dashboard",
    page_icon="🏨",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background-color: #000000;
    color: white;
}

.main-title {
    text-align: center;
    color: aqua;
    font-size: 38px;
    font-family: "Times New Roman";
    font-weight: bold;
    margin-bottom: 25px;
}

.sub-title {
    text-align: center;
    color: #ff1493;
    font-size: 18px;
    font-family: "Times New Roman";
}

div[data-testid="stMetric"] {
    background-color: #111111;
    border: 1px solid #ff1493;
    padding: 15px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():

    df = pd.read_csv("hotel_bookings.csv")

    # Handle missing values
    df["children"] = pd.to_numeric(
        df["children"],
        errors="coerce"
    ).fillna(0)

    # Convert numeric columns to proper numeric type
    numeric_columns = [
        "adults",
        "babies",
        "adr",
        "lead_time",
        "is_canceled"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    # Fill missing numeric values
    df["adults"] = df["adults"].fillna(0)
    df["babies"] = df["babies"].fillna(0)
    df["adr"] = df["adr"].fillna(0)
    df["lead_time"] = df["lead_time"].fillna(0)
    df["is_canceled"] = df["is_canceled"].fillna(0)

    # Create total guests column
    df["total_guests"] = (
        df["adults"] +
        df["children"] +
        df["babies"]
    )

    return df




df = load_data()



st.markdown(
    '<div class="main-title">🏨Hotel Booking Interactive Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">📊Hotel Booking Data Analysis</div>',
    unsafe_allow_html=True
)


st.sidebar.title("🔎 Dashboard Filters")

hotel_options = {
    "🏖️ Resort Hotel": "Resort Hotel",
    "🏙️ City Hotel": "City Hotel"
}

selected_hotels = st.sidebar.multiselect(
    "🏨 Select Hotel",
    options=list(hotel_options.keys()),
    default=list(hotel_options.keys())
)

hotel_filter = [
    hotel_options[hotel]
    for hotel in selected_hotels
]

filtered_df = df[
    df["hotel"].isin(hotel_filter)
]


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📋Total Bookings",
        f"{len(filtered_df):,}"
    )

with col2:
    st.metric(
        "💲Average ADR",
        f"{filtered_df['adr'].mean():.2f}"
    )

with col3:
    cancellation_rate = filtered_df["is_canceled"].mean() * 100

    st.metric(
        "✖️Cancellation Rate",
        f"{cancellation_rate:.2f}%"
    )

with col4:
    st.metric(
        "🕰️Average Lead Time",
        f"{filtered_df['lead_time'].mean():.1f} days"
    )


country_data = (
    filtered_df
    .groupby("country")
    .size()
    .reset_index(name="Bookings")
    .sort_values(
        "Bookings",
        ascending=False
    )
    .head(25)
)

fig1 = px.bar(
    country_data,
    x="country",
    y="Bookings",
    title="📈Top 25 Countries by Bookings",
    color="Bookings",
    color_continuous_scale="Viridis"
)

fig1.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    xaxis=dict(
        tickangle=-60
    ),
    title_font=dict(
        color="aqua",
        size=20
    )
)


country_pie = (
    filtered_df["country"]
    .value_counts()
    .reset_index()
)

country_pie.columns = [
    "Country",
    "Bookings"
]

fig2 = px.pie(
    country_pie,
    names="Country",
    values="Bookings",
    title="🌍Booking Distribution by Country",
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig2.update_traces(
    textinfo="percent",
    textposition="outside",
    hovertemplate="<b>%{label}</b><br>Bookings: %{value}<br>Percentage: %{percent}<extra></extra>"
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    title_font=dict(
        color="aqua",
        size=20
    ),


    legend=dict(
        font=dict(color="white")
    )
)
fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    title_font=dict(
        color="aqua",
        size=20
    )
)

fig2.update_traces(
    textinfo="percent",
    textposition="inside"
)

fig2.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    title_font=dict(
        color="aqua",
        size=20
    )
)





col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig1,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig2,
        use_container_width=True
)

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

adr_data = (
    filtered_df
    .groupby("arrival_date_month")["adr"]
    .mean()
    .reindex(month_order)
    .reset_index()
)

adr_data.columns = [
    "Month",
    "Average_ADR"
]

fig3 = px.line(
    adr_data,
    x="Month",
    y="Average_ADR",
    markers=True,
    title="📊Average ADR Over Time"
)

fig3.update_traces(
    line=dict(
        color="darkorange",
        width=3
    ),
    marker=dict(
        size=9,
        color="royalblue",
        symbol="diamond"
    )
)

fig3.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    xaxis=dict(
        tickangle=-45
    ),
    title_font=dict(
        color="aqua",
        size=20
    )
)


booking_country = (
    filtered_df
    .groupby("country")
    .size()
    .reset_index(name="Bookings")
    .sort_values(
        "Bookings",
        ascending=False
    )
    .head(25)
)

fig4 = px.histogram(
    booking_country,
    x="country",
    y="Bookings",
    title="📋Booking Distribution",
    color_discrete_sequence=["green"]
)

fig4.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=500,
    xaxis=dict(
        tickangle=-60
    ),
    title_font=dict(
        color="aqua",
        size=20
    )
)


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig3,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig4,
        use_container_width=True
    )



fig5 = px.box(
    filtered_df,
    x="country",
    y="adr",
    title="📉ADR Distribution Box Plot",
    color_discrete_sequence=["purple"]
)

fig5.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=550,
    xaxis=dict(
        tickangle=-60
    ),
    title_font=dict(
        color="aqua",
        size=20
    )
)



scatter_df = filtered_df.copy()

# Keep the graph manageable
if len(scatter_df) > 5000:
    scatter_df = scatter_df.sample(
        5000,
        random_state=42
    )

fig6 = px.scatter(
    scatter_df,
    x="lead_time",
    y="adr",
    color="country",
    size="total_guests",
    hover_name="country",
    title="🕛ADR vs Lead Time by Country",
    color_discrete_sequence=px.colors.qualitative.Vivid
)

fig6.update_layout(
    template="plotly_dark",
    paper_bgcolor="black",
    plot_bgcolor="black",
    height=550,
    title_font=dict(
        color="aqua",
        size=20
    )
)


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        fig5,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        fig6,
        use_container_width=True
    )

st.markdown("""
<hr>

<div style="
text-align:center;
background-color:#E91E63;
color:#4B0082;
padding:15px;
font-family:Times New Roman;
font-size:16px;
">

<b>🏨Dashboard created using Pandas + Plotly + Streamlit📊</b>

</div>
""", unsafe_allow_html=True)
