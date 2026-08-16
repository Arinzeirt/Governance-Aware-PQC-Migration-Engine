import streamlit as st


PRODUCTS = [

    {
        "id": "cipherscan",
        "vendor": "QuantumGenie",
        "product": "CipherScan™",
        "category": "AI-POWERED CRYPTO DISCOVERY",
        "description": (
            "Discover and inventory cryptographic assets across "
            "code, infrastructure, certificates, keys and endpoints."
        ),
        "capabilities": [
            "Cryptographic inventory",
            "TLS & certificate discovery",
            "Repository & code analysis",
            "Dependency mapping",
            "CBOM generation",
        ],
        "accent": "#2F81F7",
        "icon": "⌕",
        "real": True,
    },

    {
        "id": "ciphernova",
        "vendor": "QuantumGenie",
        "product": "CipherNova™",
        "category": "AI-POWERED REMEDIATION",
        "description": (
            "Translate identified cryptographic exposure into "
            "validated remediation and migration workflows."
        ),
        "capabilities": [
            "Remediation guidance",
            "PQC migration workflows",
            "Context-aware validation",
            "Review-ready changes",
            "Implementation support",
        ],
        "accent": "#8B5CF6",
        "icon": "✦",
        "real": True,
    },

    {
        "id": "archiq",
        "vendor": "SecureStack",
        "product": "ArchiQ™",
        "category": "ENTERPRISE ARCHITECTURE INTELLIGENCE",
        "description": (
            "Model and analyse complex enterprise environments "
            "to support quantum migration architecture."
        ),
        "capabilities": [
            "Environment modelling",
            "Dependency analysis",
            "Migration architecture",
            "Impact assessment",
            "Scenario planning",
        ],
        "accent": "#18B6C9",
        "icon": "⌘",
        "real": False,
    },

    {
        "id": "governiq",
        "vendor": "TrustLedger",
        "product": "GovernIQ™",
        "category": "GOVERNANCE & ASSURANCE",
        "description": (
            "Strengthen governance, risk and compliance throughout "
            "the quantum migration lifecycle."
        ),
        "capabilities": [
            "PQC governance framework",
            "Risk management",
            "Regulatory alignment",
            "Policy orchestration",
            "Audit & assurance",
        ],
        "accent": "#F59E0B",
        "icon": "✓",
        "real": False,
    },

]


def _product_image(product):

    accent = product["accent"]

    st.markdown(
        f"""
<div style="
    height:150px;
    border-radius:7px;
    margin-bottom:12px;
    position:relative;
    overflow:hidden;
    background:
        radial-gradient(
            circle at 50% 50%,
            {accent}55 0%,
            transparent 38%
        ),
        linear-gradient(
            135deg,
            #071426 0%,
            #0B1830 50%,
            #07101F 100%
        );
    border:1px solid {accent}30;
">

<div style="
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    width:82px;
    height:82px;
    border:1px solid {accent}80;
    border-radius:50%;
    box-shadow:
        0 0 0 18px {accent}10,
        0 0 0 36px {accent}07;
">

<div style="
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    font-size:2rem;
    color:{accent};
    font-weight:800;
">
{product["icon"]}
</div>

</div>

<div style="
    position:absolute;
    top:12px;
    left:13px;
    font-size:0.58rem;
    letter-spacing:1.3px;
    color:{accent};
    font-weight:800;
">
EQMP PARTNER PRODUCT
</div>

</div>
""",
        unsafe_allow_html=True,
    )


def _product_card(product):

    _product_image(product)

    capabilities = "".join(
        f"<li>{item}</li>"
        for item in product["capabilities"]
    )

    prototype = ""

    if not product["real"]:

        prototype = """
<div style="
    display:inline-block;
    margin-bottom:7px;
    padding:3px 7px;
    border:1px solid rgba(245,158,11,.25);
    border-radius:4px;
    font-size:0.58rem;
    color:#C89A45;
    letter-spacing:.7px;
    font-weight:700;
">
PROTOTYPE PARTNER PRODUCT
</div>
"""

    st.markdown(
        f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:12px;
    background:rgba(7,16,31,.35);
">

{prototype}

<div style="
    font-size:0.63rem;
    letter-spacing:1px;
    color:{product["accent"]};
    font-weight:800;
    margin-bottom:5px;
">
{product["vendor"]}
</div>

<div style="
    font-size:1.02rem;
    font-weight:800;
    color:#F5F7FA;
    margin-bottom:3px;
">
{product["product"]}
</div>

<div style="
    font-size:0.61rem;
    letter-spacing:.7px;
    color:#7F91A6;
    font-weight:750;
    margin-bottom:9px;
">
{product["category"]}
</div>

<div style="
    color:#AEBCCE;
    font-size:0.73rem;
    line-height:1.5;
    min-height:66px;
">
{product["description"]}
</div>

<div style="
    border-top:1px solid rgba(255,255,255,.07);
    margin-top:9px;
    padding-top:8px;
">

<ul style="
    margin:0;
    padding-left:17px;
    color:#8FA1B5;
    font-size:0.69rem;
    line-height:1.65;
">
{capabilities}
</ul>

</div>

<div style="
    border-top:1px solid rgba(255,255,255,.07);
    margin-top:10px;
    padding-top:9px;
    font-size:0.67rem;
    color:#718096;
">
Powered by
<strong style="color:#D5DCE5;">
{product["vendor"]}
</strong>
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    if st.button(
        "View Product →",
        key=f"marketplace_view_{product['id']}",
        use_container_width=True,
    ):

        st.session_state[
            "marketplace_product"
        ] = product["id"]

        st.rerun()


def _product_detail(product):

    if st.button(
        "← Back to Marketplace",
        key="marketplace_back",
    ):

        st.session_state.pop(
            "marketplace_product",
            None,
        )

        st.rerun()

    st.markdown(
        f"""
<div style="
    margin-top:18px;
    margin-bottom:22px;
">

<div style="
    font-size:0.65rem;
    letter-spacing:1.2px;
    color:{product["accent"]};
    font-weight:800;
    margin-bottom:7px;
">
{product["category"]}
</div>

<div style="
    font-size:1.8rem;
    font-weight:800;
">
{product["product"]}
</div>

<div style="
    font-size:0.86rem;
    color:#8FA1B5;
    margin-top:5px;
">
Powered by {product["vendor"]}
</div>

</div>
""",
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        [1.35, 1],
        gap="large",
    )

    with left:

        _product_image(product)

        st.markdown(
            f"""
<div style="
    font-size:0.86rem;
    line-height:1.6;
    color:#AEBCCE;
">
{product["description"]}
</div>
""",
            unsafe_allow_html=True,
        )

    with right:

        st.markdown(
            """
<div style="
    font-size:0.72rem;
    letter-spacing:1px;
    color:#7F91A6;
    font-weight:750;
    margin-bottom:9px;
">
CAPABILITIES
</div>
""",
            unsafe_allow_html=True,
        )

        for capability in product["capabilities"]:

            st.markdown(
                f"""
<div style="
    padding:9px 0;
    border-bottom:1px solid rgba(255,255,255,.07);
    color:#D5DCE5;
    font-size:0.78rem;
">
{capability}
</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        """
<div style="
    margin-top:22px;
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:16px;
">
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<div style="
    font-size:0.74rem;
    color:#7F91A6;
    letter-spacing:.8px;
    font-weight:750;
    margin-bottom:6px;
">
EQMP RELEVANCE
</div>

<div style="
    font-size:0.78rem;
    color:#AEBCCE;
    line-height:1.5;
">
This product can be surfaced by EQMP when enterprise
discovery identifies requirements aligned with
<strong>{product["category"].title()}</strong>.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


def show():

    # =========================================================
    # Authentication
    # =========================================================

    if not st.session_state.get(
        "eqmp_authenticated",
        False,
    ):

        st.session_state.page = "login"
        st.rerun()

    # =========================================================
    # Product detail
    # =========================================================

    selected_id = st.session_state.get(
        "marketplace_product"
    )

    selected_product = next(
        (
            product
            for product in PRODUCTS
            if product["id"] == selected_id
        ),
        None,
    )

    if selected_product:

        _product_detail(
            selected_product
        )

        return

    # =========================================================
    # Partner Products
    # =========================================================

    st.markdown(
        """
<div style="
    margin-top:28px;
    margin-bottom:5px;
    font-size:0.78rem;
    letter-spacing:1.2px;
    font-weight:750;
    color:#7F91A6;
">
PARTNER PRODUCTS
</div>

<div style="
    color:#8FA1B5;
    font-size:0.76rem;
    line-height:1.5;
    margin-bottom:13px;
">
Specialist products from the EQMP partner network.
Each product addresses a defined enterprise capability.
</div>
""",
        unsafe_allow_html=True,
    )

    # =========================================================
    # Four product cards
    # =========================================================

    row_one = st.columns(
        2,
        gap="medium",
    )

    with row_one[0]:

        _product_card(
            PRODUCTS[0]
        )

    with row_one[1]:

        _product_card(
            PRODUCTS[1]
        )

    row_two = st.columns(
        2,
        gap="medium",
    )

    with row_two[0]:

        _product_card(
            PRODUCTS[2]
        )

    with row_two[1]:

        _product_card(
            PRODUCTS[3]
        )

    # =========================================================
    # Partner workflow
    # =========================================================

    st.markdown(
        """
<div style="
    margin-top:18px;
    margin-bottom:8px;
    font-size:0.72rem;
    letter-spacing:1px;
    font-weight:750;
    color:#7F91A6;
">
HOW EQMP USES THE PARTNER NETWORK
</div>
""",
        unsafe_allow_html=True,
    )

    one, two, three, four = st.columns(
        4,
        gap="medium",
    )

    workflow = [

        (
            "01",
            "Discovery",
            "Identify enterprise requirements and exposure.",
        ),

        (
            "02",
            "Match Capability",
            "Determine the specialist capability required.",
        ),

        (
            "03",
            "Select Product",
            "Surface relevant partner products.",
        ),

        (
            "04",
            "Execute & Govern",
            "Use the product within EQMP oversight.",
        ),

    ]

    for column, item in zip(
        (one, two, three, four),
        workflow,
    ):

        with column:

            number, title, description = item

            st.markdown(
                f"""
<div style="
    border:1px solid rgba(255,255,255,.10);
    border-radius:8px;
    padding:12px;
    min-height:105px;
">

<div style="
    font-size:0.62rem;
    color:#2F81F7;
    font-weight:800;
    margin-bottom:5px;
">
{number}
</div>

<div style="
    font-size:0.78rem;
    font-weight:750;
    margin-bottom:4px;
">
{title}
</div>

<div style="
    color:#8FA1B5;
    font-size:0.68rem;
    line-height:1.45;
">
{description}
</div>

</div>
""",
                unsafe_allow_html=True,
            )

    st.markdown(
        '<div style="height:10px"></div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "Return to Command Center",
        key="marketplace_return",
    ):

        st.session_state.page = "command_center"
        st.rerun()
