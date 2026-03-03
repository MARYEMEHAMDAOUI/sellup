import streamlit as st
from data import USERS, PRODUCTS, CLIENTS, SALES

# ── Page config ──────────────────────────────────────
st.set_page_config(
    page_title="Sellup — Gestion Commerciale",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #080C14;
    color: #CBD5E1;
}
h1,h2,h3 { font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important; color: #F1F5F9 !important; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0E1520 !important;
    border-right: 1px solid #1E2D42;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }

/* Main area */
[data-testid="stAppViewContainer"] { background-color: #080C14; }
[data-testid="block-container"] { padding-top: 2rem; }

/* Buttons */
.stButton > button {
    background-color: #0EA5E9 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.15s !important;
}
.stButton > button:hover { background-color: #0284C7 !important; }

/* Inputs */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {
    background-color: #0E1520 !important;
    border: 1px solid #1E2D42 !important;
    border-radius: 8px !important;
    color: #F1F5F9 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Metrics */
[data-testid="metric-container"] {
    background-color: #111927;
    border: 1px solid #1E2D42;
    border-radius: 14px;
    padding: 20px;
}
[data-testid="stMetricValue"] { color: #F1F5F9 !important; font-family: 'Plus Jakarta Sans', sans-serif !important; }
[data-testid="stMetricLabel"] { color: #475569 !important; }

/* DataFrames */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }
.dataframe { background-color: #111927 !important; color: #CBD5E1 !important; }

/* Tabs */
[data-testid="stTabs"] button {
    color: #475569 !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0EA5E9 !important;
    border-bottom-color: #0EA5E9 !important;
}

/* Divider */
hr { border-color: #1E2D42 !important; }

/* Success/error/warning boxes */
.stSuccess { background-color: rgba(16,185,129,0.12) !important; border: 1px solid rgba(16,185,129,0.3) !important; color: #10B981 !important; border-radius: 10px !important; }
.stError   { background-color: rgba(239,68,68,0.12)  !important; border: 1px solid rgba(239,68,68,0.3)  !important; color: #EF4444 !important; border-radius: 10px !important; }
.stWarning { background-color: rgba(245,158,11,0.12) !important; border: 1px solid rgba(245,158,11,0.3) !important; color: #F59E0B !important; border-radius: 10px !important; }
.stInfo    { background-color: rgba(14,165,233,0.12)  !important; border: 1px solid rgba(14,165,233,0.3) !important; color: #0EA5E9 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────
def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.session_state.users    = [u.copy() for u in USERS]
        st.session_state.products = [p.copy() for p in PRODUCTS]
        st.session_state.clients  = [c.copy() for c in CLIENTS]
        st.session_state.sales    = [s.copy() for s in SALES]
        st.session_state.page     = "dashboard"

init_state()

# ═══════════════════════════════════════════════════
#  LOGIN PAGE
# ═══════════════════════════════════════════════════
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 40px 0 20px;'>
            <div style='font-size:48px; margin-bottom:16px;'>⬡</div>
            <h1 style='font-size:32px; font-weight:800; letter-spacing:-1px; margin:0;'>
                Sell<span style='color:#0EA5E9;'>up</span>
            </h1>
            <p style='color:#475569; margin-top:8px;'>Système de Gestion Commerciale</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        with st.container():
            st.markdown("""
            <div style='background:#111927; border:1px solid #1E2D42; border-radius:16px; padding:32px;'>
            """, unsafe_allow_html=True)

            username = st.text_input("Identifiant", placeholder="Ex: admin")
            password = st.text_input("Mot de passe", type="password", placeholder="••••••••")

            if st.button("Se connecter →", use_container_width=True):
                user = next(
                    (u for u in st.session_state.users
                     if u["username"] == username and u["password"] == password and u["active"]),
                    None
                )
                if user:
                    st.session_state.logged_in = True
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("Identifiant ou mot de passe incorrect.")

            st.markdown("""
            <div style='margin-top:20px; padding:12px; background:#0E1520; border-radius:8px; font-size:12px; color:#475569;'>
                <strong style='color:#CBD5E1;'>Comptes démo :</strong><br>
                admin / admin123 &nbsp;·&nbsp; vendeur1 / pass123 &nbsp;·&nbsp; manager / mgr123
            </div>
            """, unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════
def sidebar_nav():
    user = st.session_state.current_user
    nav  = st.session_state

    with st.sidebar:
        # Logo
        st.markdown("""
        <div style='padding:8px 0 20px; border-bottom:1px solid #1E2D42; margin-bottom:16px;'>
            <div style='font-size:22px; font-weight:800; letter-spacing:-0.8px; color:#F1F5F9; font-family:"Plus Jakarta Sans",sans-serif;'>
                Sell<span style='color:#0EA5E9;'>up</span>
            </div>
            <div style='font-size:11px; color:#475569; margin-top:3px; letter-spacing:0.3px;'>Gestion Commerciale</div>
        </div>
        """, unsafe_allow_html=True)

        # Late deliveries badge
        late = sum(
            1 for s in st.session_state.sales
            if s.get("delivery") and
               s["delivery"].get("plannedDate") and
               s["delivery"]["status"] not in ("livrée","annulée") and
               s["delivery"]["plannedDate"] < "2026-03-01"
        )
        low_stock = sum(1 for p in st.session_state.products if p["stock"] <= p["minStock"])

        pages = [
            ("dashboard",   "◈",  "Tableau de Bord"),
            ("new_sale",    "⊞",  "Nouvelle Vente"),
            ("sales",       "◰",  "Ventes"),
            ("livraisons",  "🚚", f"Livraisons {'🔴' if late else ''}"),
            ("clients",     "◎",  "Clients"),
            ("products",    "◫",  f"Produits {'⚠️' if low_stock else ''}"),
            ("reports",     "◷",  "Rapports"),
        ]
        if user["role"] == "admin":
            pages.append(("users", "◉", "Utilisateurs"))

        for page_id, icon, label in pages:
            active = st.session_state.page == page_id
            if st.sidebar.button(
                f"{icon}  {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                type="primary" if active else "secondary"
            ):
                st.session_state.page = page_id
                st.rerun()

        st.sidebar.divider()

        # User card → profile
        role_icons = {"admin": "👑", "manager": "📊", "vendeur": "💼"}
        st.markdown(f"""
        <div style='background:#111927; border:1px solid #1E2D42; border-radius:10px; padding:12px; margin-bottom:10px;'>
            <div style='display:flex; align-items:center; gap:10px;'>
                <div style='width:36px; height:36px; border-radius:9px; background:linear-gradient(135deg,#0EA5E9,#8B5CF6);
                    display:flex; align-items:center; justify-content:center; font-weight:700; font-size:13px; color:white; flex-shrink:0;'>
                    {user['avatar']}
                </div>
                <div>
                    <div style='font-size:13px; font-weight:600; color:#F1F5F9;'>{user['name']}</div>
                    <div style='font-size:11px; color:#475569;'>{role_icons.get(user['role'],'👤')} {user['role'].capitalize()}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("👤  Mon Profil", use_container_width=True,
                             type="primary" if st.session_state.page == "profile" else "secondary"):
            st.session_state.page = "profile"
            st.rerun()

        if st.sidebar.button("⊗  Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.current_user = None
            st.session_state.page = "dashboard"
            st.rerun()

# ═══════════════════════════════════════════════════
#  ROUTER — load the right page module
# ═══════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    sidebar_nav()

    page = st.session_state.page

    if page == "dashboard":
        from pages import pg_dashboard as pg
    elif page == "new_sale":
        from pages import pg_new_sale as pg
    elif page == "sales":
        from pages import pg_sales as pg
    elif page == "livraisons":
        from pages import pg_livraisons as pg
    elif page == "clients":
        from pages import pg_clients as pg
    elif page == "products":
        from pages import pg_products as pg
    elif page == "reports":
        from pages import pg_reports as pg
    elif page == "users":
        from pages import pg_users as pg
    elif page == "profile":
        from pages import pg_profile as pg
    else:
        from pages import pg_dashboard as pg

    pg.render()

if __name__ == "__main__":
    main()
