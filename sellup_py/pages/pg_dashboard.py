import streamlit as st
from datetime import datetime, date

def render():
    sales    = st.session_state.sales
    products = st.session_state.products
    clients  = st.session_state.clients

    st.markdown("## ◈ Tableau de Bord")
    st.caption("Vue d'ensemble de vos performances commerciales")
    st.divider()

    # ── KPI cards ────────────────────────────────────
    total_revenue = sum(s["total"] for s in sales)
    paid_sales    = [s for s in sales if s["status"] == "payée"]
    pending_sales = [s for s in sales if s["status"] == "en attente"]
    low_stock     = [p for p in products if p["stock"] <= p["minStock"]]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Chiffre d'Affaires",  f"{total_revenue:,.0f} MAD", f"{len(paid_sales)} factures payées")
    col2.metric("📦 Ventes totales",       len(sales),                  f"{len(pending_sales)} en attente")
    col3.metric("👥 Clients actifs",        len(clients),               "portefeuille")
    col4.metric("⚠️ Stock critique",        len(low_stock),             "produits sous seuil", delta_color="inverse")

    st.divider()

    col_left, col_right = st.columns([1.5, 1])

    with col_left:
        # ── Sales by vendor ──
        st.markdown("### 👥 CA par Vendeur")
        vendors: dict = {}
        for s in sales:
            v = s.get("vendeur", "Inconnu")
            vendors.setdefault(v, {"revenue": 0, "count": 0})
            vendors[v]["revenue"] += s["total"]
            vendors[v]["count"]   += 1

        for vendor, data in sorted(vendors.items(), key=lambda x: -x[1]["revenue"]):
            pct = int(data["revenue"] / total_revenue * 100) if total_revenue else 0
            st.markdown(f"""
            <div style='background:#111927; border:1px solid #1E2D42; border-radius:10px; padding:14px 18px; margin-bottom:10px;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                    <span style='color:#F1F5F9; font-weight:600;'>{vendor}</span>
                    <span style='color:#10B981; font-weight:700;'>{data["revenue"]:,.0f} MAD</span>
                </div>
                <div style='background:#1E2D42; border-radius:4px; height:6px;'>
                    <div style='width:{pct}%; background:#0EA5E9; border-radius:4px; height:100%;'></div>
                </div>
                <div style='color:#475569; font-size:11px; margin-top:5px;'>{data["count"]} vente(s) · {pct}% du CA</div>
            </div>
            """, unsafe_allow_html=True)

        # ── Top products ──
        st.markdown("### 📦 Produits les plus vendus")
        prod_stats: dict = {}
        for s in sales:
            for item in s.get("items", []):
                n = item["name"]
                prod_stats.setdefault(n, {"qty": 0, "revenue": 0})
                prod_stats[n]["qty"]     += item["qty"]
                prod_stats[n]["revenue"] += item["qty"] * item["price"] * (1 + item["tva"] / 100)

        top = sorted(prod_stats.items(), key=lambda x: -x[1]["revenue"])[:5]
        if top:
            max_rev = top[0][1]["revenue"]
            for name, data in top:
                pct = int(data["revenue"] / max_rev * 100)
                st.markdown(f"""
                <div style='background:#111927; border:1px solid #1E2D42; border-radius:10px; padding:14px 18px; margin-bottom:10px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:8px;'>
                        <span style='color:#F1F5F9;'>{name}</span>
                        <span style='color:#8B5CF6; font-weight:700;'>{data["qty"]} unités</span>
                    </div>
                    <div style='background:#1E2D42; border-radius:4px; height:6px;'>
                        <div style='width:{pct}%; background:linear-gradient(90deg,#0EA5E9,#8B5CF6); border-radius:4px; height:100%;'></div>
                    </div>
                    <div style='color:#475569; font-size:11px; margin-top:5px;'>{data["revenue"]:,.0f} MAD de CA</div>
                </div>
                """, unsafe_allow_html=True)

    with col_right:
        # ── Alerts ──
        if low_stock:
            st.markdown("### ⚠️ Alertes Stock")
            for p in low_stock:
                st.markdown(f"""
                <div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:12px 16px; margin-bottom:8px;'>
                    <div style='color:#EF4444; font-weight:600; font-size:13px;'>⚠ {p["name"]}</div>
                    <div style='color:#CBD5E1; font-size:12px; margin-top:4px;'>Stock : <strong>{p["stock"]}</strong> / Min : {p["minStock"]}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Recent sales ──
        st.markdown("### 🧾 Dernières Ventes")
        STATUS_COLORS = {"payée": "#10B981", "en attente": "#F59E0B", "annulée": "#EF4444"}
        for s in sales[:5]:
            color = STATUS_COLORS.get(s["status"], "#475569")
            st.markdown(f"""
            <div style='background:#111927; border:1px solid #1E2D42; border-radius:10px; padding:14px 16px; margin-bottom:8px;'>
                <div style='display:flex; justify-content:space-between;'>
                    <span style='color:#0EA5E9; font-family:monospace; font-size:12px; font-weight:700;'>{s["id"]}</span>
                    <span style='background:{color}22; color:{color}; border:1px solid {color}44; border-radius:5px; padding:2px 8px; font-size:11px; font-weight:700;'>{s["status"].upper()}</span>
                </div>
                <div style='color:#F1F5F9; font-size:13px; font-weight:600; margin-top:4px;'>{s["clientName"]}</div>
                <div style='display:flex; justify-content:space-between; margin-top:4px;'>
                    <span style='color:#475569; font-size:12px;'>{s["date"]}</span>
                    <span style='color:#10B981; font-weight:700; font-size:13px;'>{s["total"]:,.2f} MAD</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Pending deliveries ──
        late_deliveries = [
            s for s in sales
            if s.get("delivery") and
               s["delivery"].get("plannedDate") and
               s["delivery"]["status"] not in ("livrée", "annulée") and
               s["delivery"]["plannedDate"] < "2026-03-01"
        ]
        if late_deliveries:
            st.markdown("### 🚚 Livraisons en retard")
            for s in late_deliveries:
                st.markdown(f"""
                <div style='background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.3); border-radius:10px; padding:12px 16px; margin-bottom:8px;'>
                    <div style='color:#EF4444; font-weight:600;'>{s["clientName"]}</div>
                    <div style='color:#CBD5E1; font-size:12px;'>Prévue le : {s["delivery"]["plannedDate"]} · {s["id"]}</div>
                </div>
                """, unsafe_allow_html=True)
