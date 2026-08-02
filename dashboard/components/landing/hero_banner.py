import streamlit as st


def show():

    html = """
<style>

.hero-wrapper{
background:
radial-gradient(circle at top right, rgba(52,152,219,.16), transparent 42%),
radial-gradient(circle at bottom left, rgba(41,128,185,.10), transparent 38%),
linear-gradient(180deg,#081320 0%,#0D1B2A 100%);
border:1px solid rgba(120,170,255,.10);
border-radius:24px;
padding:48px 56px;
margin-top:12px;
margin-bottom:34px;
overflow:hidden;
position:relative;
}

.hero-wrapper:before{
content:"";
position:absolute;
inset:0;
background-image:
linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
background-size:42px 42px;
opacity:.30;
}

.hero-content{
position:relative;
z-index:2;
max-width:900px;
margin:auto;
text-align:center;
}

.hero-label{
color:#4DA3FF;
font-size:12px;
font-weight:700;
letter-spacing:2px;
text-transform:uppercase;
margin-bottom:16px;
}

.hero-title{
color:white;
font-size:50px;
font-weight:800;
line-height:1.15;
margin-bottom:18px;
}

.hero-title span{
color:#4DA3FF;
}

.hero-text{
color:#C8D4DF;
font-size:18px;
line-height:1.65;
max-width:760px;
margin:auto;
}

</style>

<div class="hero-wrapper">

<div class="hero-content">

<div class="hero-label">
ENET TECHNOLOGIES • GOVERNANCE-AWARE POST-QUANTUM SECURITY
</div>

<div class="hero-title">
Enterprise <span>Quantum Migration</span><br>
Platform
</div>

<div class="hero-text">
Discover cryptographic assets across your enterprise, evaluate post-quantum readiness,
generate executive reports and build a governance-driven migration strategy using a
research-backed platform designed for modern organisations.
</div>

</div>

</div>
"""

    st.markdown(html, unsafe_allow_html=True)
