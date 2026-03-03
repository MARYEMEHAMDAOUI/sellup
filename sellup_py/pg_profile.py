import streamlit as st
from datetime import date

ROLE_CONF = {
    "admin":   {"label": "Administrateur", "color": "#8B5CF6", "icon": "👑"},
    "manager": {"label": "Manager",        "color": "#F59E0B", "icon": "📊"},
    "vendeur": {"label": "Vendeur",        "color": "#0EA5E9", "icon": "💼"},
}

def seniority(join_str: str) -> str:
    if not join_str: return "—"
    try:
        jd  = date.fromisoformat(join_str)
        today = date(2026, 3, 1)
        months = max(0, (today.year - jd.year) * 12 + (today.month - jd.month))
        y, m = divmod(months, 12)
        if y and m: return f"{y} an{'s' if y>1 else ''} {m} mois"
        if y:       return f"{y} an{'s' if y>1 else ''}"
        return f"{m} mois"
    except Exception:
        return "—"

def fmt_date(d: str) -> str:
    if not d: return "Non renseigné"
    try:
        return date.fromisoformat(d).strftime("%d %B %Y")
    except Exception:
        return d

def render():
    current_user = st.session_state.current_user
    user = next((u for u in st.session_state.users if u["id"] == current_user["id"]), current_user)
    role = ROLE_CONF.get(user["role"], {"label": user["role"], "color": "#CBD5E1", "icon": "👤"})

    st.markdown("## 👤 Mon Profil")
    st.caption("Informations personnelles et performances")
    st.divider()

    # ── Performance stats ─────────────────────────────
    my_sales   = [s for s in st.session_state.sales if s.get("vendeur") == user["name"]]
    my_revenue = sum(s["total"] for s in my_sales)
    my_paid    = sum(1 for s in my_sales if s["status"] == "payée")
    my_pending = sum(1 for s in my_sales if s["status"] == "en attente")

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 CA Total",       f"{my_revenue:,.0f} MAD")
    k2.metric("✅ Ventes payées",   my_paid)
    k3.metric("⏳ En attente",       my_pending)
    k4.metric("📈 Total ventes",    len(my_sales))

    st.divider()

    col_left, col_right = st.columns([1, 2])

    # ── Left: Identity card ───────────────────────────
    with col_left:
        status_color = "#10B981" if user.get("active", True) else "#EF4444"
        st.markdown(f"""
        <div style='background:#111927; border:1px solid #1E2D42; border-radius:16px; padding:24px; text-align:center;'>
            <div style='width:80px; height:80px; border-radius:50%; background:linear-gradient(135deg,#0EA5E9,#8B5CF6);
                display:flex; align-items:center; justify-content:center; margin:0 auto 14px;
                font-size:26px; font-weight:800; color:white; letter-spacing:1px;'>
                {user.get("avatar","??")}
            </div>
            <div style='font-size:18px; font-weight:800; color:#F1F5F9; margin-bottom:6px;'>{user["name"]}</div>
            <div style='display:inline-flex; align-items:center; gap:5px; background:{role["color"]}22;
                border:1px solid {role["color"]}44; color:{role["color"]}; border-radius:20px;
                padding:4px 14px; font-size:12px; font-weight:700; margin-bottom:12px;'>
                {role["icon"]} {role["label"]}
            </div><br>
            <div style='display:inline-flex; align-items:center; gap:5px; background:{status_color}22;
                color:{status_color}; border:1px solid {status_color}44; border-radius:20px;
                padding:3px 12px; font-size:12px; font-weight:700;'>
                <div style='width:7px; height:7px; border-radius:50%; background:{status_color};'></div>
                {"Compte actif" if user.get("active",True) else "Compte inactif"}
            </div>
            <div style='border-top:1px solid #1E2D42; margin-top:16px; padding-top:16px;
                display:flex; justify-content:space-around;'>
                <div style='text-align:center;'>
                    <div style='font-size:20px; font-weight:800; color:#0EA5E9;'>{len(my_sales)}</div>
                    <div style='font-size:11px; color:#475569;'>Ventes</div>
                </div>
                <div style='width:1px; background:#1E2D42;'></div>
                <div style='text-align:center;'>
                    <div style='font-size:15px; font-weight:800; color:#10B981;'>{seniority(user.get("joinDate",""))}</div>
                    <div style='font-size:11px; color:#475569;'>Ancienneté</div>
                </div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Dates card
        st.markdown(f"""
        <div style='background:#111927; border:1px solid #1E2D42; border-radius:12px; padding:18px;'>
            <div style='font-size:13px; font-weight:700; color:#F1F5F9; margin-bottom:14px;'>📅 Dates clés</div>
            <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #1E2D42; font-size:13px;'>
                <span style='color:#475569;'>Intégration</span>
                <strong style='color:#F1F5F9;'>{fmt_date(user.get("joinDate",""))}</strong>
            </div>
            <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #1E2D42; font-size:13px;'>
                <span style='color:#475569;'>Date de naissance</span>
                <strong style='color:#F1F5F9;'>{fmt_date(user.get("birthDate",""))}</strong>
            </div>
            <div style='display:flex; justify-content:space-between; padding:8px 0; font-size:13px;'>
                <span style='color:#475569;'>Ancienneté</span>
                <strong style='color:#10B981;'>{seniority(user.get("joinDate",""))}</strong>
            </div>
        </div>""", unsafe_allow_html=True)

    # ── Right: Edit form ──────────────────────────────
    with col_right:
        editing = st.toggle("✎ Modifier mon profil", value=False)
        st.markdown("<br>", unsafe_allow_html=True)

        if editing:
            st.markdown("""
            <div style='background:rgba(14,165,233,0.08); border:1px solid rgba(14,165,233,0.25);
                border-radius:10px; padding:6px 14px; margin-bottom:16px; font-size:12px; color:#0EA5E9;'>
                ✏️ Mode édition activé — les modifications sont enregistrées immédiatement
            </div>""", unsafe_allow_html=True)

        fc = st.columns(2)
        e_name  = fc[0].text_input("Nom complet",     value=user["name"],           disabled=not editing)
        e_email = fc[1].text_input("Email",           value=user["email"],          disabled=not editing)
        e_phone = fc[0].text_input("Téléphone",       value=user.get("phone",""),   disabled=not editing)
        e_city  = fc[1].text_input("Ville",           value=user.get("city",""),    disabled=not editing)

        fc2 = st.columns(2)
        try:
            birth_val = date.fromisoformat(user["birthDate"]) if user.get("birthDate") else None
        except Exception:
            birth_val = None
        try:
            join_val = date.fromisoformat(user["joinDate"]) if user.get("joinDate") else None
        except Exception:
            join_val = None

        e_birth = fc2[0].date_input("Date de naissance", value=birth_val, disabled=not editing)
        e_join  = fc2[1].date_input("Date d'intégration", value=join_val, disabled=not editing or user["role"] != "admin")

        e_bio = st.text_area("Bio / Note personnelle", value=user.get("bio",""),
                             height=100, disabled=not editing,
                             placeholder="Parlez de votre rôle, vos spécialités...")

        # Read-only fields
        st.markdown(f"**Identifiant :** `{user['username']}`  &nbsp;&nbsp; **Rôle :** {role['icon']} {role['label']}")

        if editing:
            if st.button("💾 Sauvegarder les modifications", type="primary", use_container_width=True):
                st.session_state.users = [
                    {**x,
                     "name":      e_name,
                     "email":     e_email,
                     "phone":     e_phone,
                     "city":      e_city,
                     "birthDate": str(e_birth)  if e_birth else "",
                     "joinDate":  str(e_join)   if e_join  else user.get("joinDate",""),
                     "bio":       e_bio,
                    }
                    if x["id"] == user["id"] else x
                    for x in st.session_state.users
                ]
                # Refresh current user
                st.session_state.current_user = next(
                    x for x in st.session_state.users if x["id"] == user["id"]
                )
                st.success("✓ Profil mis à jour avec succès !")
                st.rerun()

        # ── Recent sales ──────────────────────────────
        if my_sales:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("### 📋 Mes dernières ventes")
            import pandas as pd
            STATUS_COLORS = {"payée":"#10B981","en attente":"#F59E0B","annulée":"#EF4444"}
            df = pd.DataFrame([{
                "Facture": s["id"], "Client": s["clientName"],
                "Date": s["date"],
                "Total": f"{s['total']:,.2f} MAD",
                "Statut": s["status"].upper()
            } for s in my_sales[:5]])
            st.dataframe(df, use_container_width=True, hide_index=True)
