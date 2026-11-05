"""Local Streamlit adaptation of the ECONET notebook dashboard."""
import streamlit as st
import matplotlib.pyplot as plt
from analysis import load_data, summarise

st.set_page_config(page_title="ECONET | Water Data", page_icon="💧")
st.title("ECONET — Water Data Explorer")
st.caption("Hackathon prototype · exploratory analysis")
uploaded = st.file_uploader("Upload water measurements", type=["csv", "xlsx"])
if uploaded is None:
    st.info("Upload a file with Characteristic Name, Result Value and Result Unit columns.")
    st.stop()
try:
    data = load_data(uploaded)
except (ValueError, OSError) as exc:
    st.error(str(exc))
    st.stop()

for column, label in [("Monitoring Location State", "State"), ("Monitoring Location Name", "Location")]:
    if column in data:
        options = sorted(data[column].dropna().astype(str).unique().tolist())
        selected = st.multiselect(label, options)
        if selected:
            data = data[data[column].astype(str).isin(selected)]
if data.empty:
    st.info("No measurements match these filters.")
    st.stop()

characteristic = st.selectbox("Characteristic", sorted(data["Characteristic Name"].unique()))
data = data[data["Characteristic Name"] == characteristic]
unit = st.selectbox("Unit", sorted(data["Result Unit"].unique()))
data = data[data["Result Unit"] == unit]
st.dataframe(summarise(data), hide_index=True)
fig, ax = plt.subplots()
ax.hist(data["Result Value"], bins=min(20, max(1, len(data))))
ax.set_xlabel(f"{characteristic} ({unit})")
ax.set_ylabel("Number of measurements")
st.pyplot(fig)
plt.close(fig)

if "Activity Start Date" in data:
    dated = data.dropna(subset=["Activity Start Date"]).sort_values("Activity Start Date")
    if not dated.empty:
        st.subheader("Individual measurements over time")
        st.scatter_chart(dated, x="Activity Start Date", y="Result Value")
st.dataframe(data, hide_index=True)
st.caption("Different units stay separate. These summaries do not determine water safety or rank pollutants.")
