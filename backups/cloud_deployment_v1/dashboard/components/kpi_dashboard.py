import streamlit as st


def show_kpi_dashboard():

    st.markdown("### Enterprise KPI Dashboard")

    st.markdown("""
<style>

.kpi-card{

background:#1E293B;

border:1px solid #334155;

border-radius:12px;

padding:18px;

text-align:center;

min-height:145px;

}

.kpi-title{

color:#CBD5E1;

font-size:14px;

font-weight:600;

margin-bottom:12px;

}

.kpi-value{

color:#F8FAFC;

font-size:34px;

font-weight:700;

margin-bottom:10px;

}

.kpi-desc{

color:#94A3B8;

font-size:13px;

}

</style>
""", unsafe_allow_html=True)

    metrics = [

        ("Assets Discovered","573","Enterprise Assets"),

        ("Overall Risk","HIGH","Current Exposure"),

        ("Migration Readiness","18%","Organization Score"),

        ("Critical Assets","59","Priority Systems"),

        ("Compliance Status","Review Required","Regulatory Posture"),

        ("Assessment Confidence","92%","Analysis Confidence"),

    ]

    cols = st.columns(6)

    for col, metric in zip(cols, metrics):

        title, value, desc = metric

        with col:

            st.markdown(f"""
<div class="kpi-card">

<div class="kpi-title">

{title}

</div>

<div class="kpi-value">

{value}

</div>

<div class="kpi-desc">

{desc}

</div>

</div>
""", unsafe_allow_html=True)
