import streamlit as st
import pandas as pd

def render():
    st.markdown("## ◷ Rapports")
    st.caption("Analyses et statistiques commerciales")
    st.divider()

    sales    = st.session_state.sales
    products = st.session_state.products
    clients  = st.session_state.clients

    # ── Period filter ────────────────────────────────
    period = st.selectbox("Période", ["Ce mois", "3 derniers mois", "Tout"], index=0)

    today = "2026-03-01"
    if period == "Ce mois":
        p_sales = [s for s in sales if s["date"][:7] == today[:7]]
    elif period == "3 derniers mois":
        p_sales = [s for s in sales if s["date"] >= "2025-12-01"]
    else:
        p_sales = sales

    paid    = [s for s in p_sales if s["status"] == "payée"]
    pending = [s for s in p_sales if s["status"] == "en attente"]
    revenue = sum(s["total"] for s in paid)
    avg     = revenue / len(paid) if paid else 0

    # ── KPIs ─────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 CA Payé",       f"{revenue:,.0f} MAD")
    k2.metric("📄 Ventes Totales", len(p_sales))
    k3.metric("⏳ En attente",      len(pending))
    k4.metric("📊 Panier moyen",    f"{avg:,.0f} MAD")

    st.divider()

    col_l, col_r = st.columns(2)

    with col_l:
        # ── CA by vendor ──
        st.markdown("### 👥 CA par Vendeur")
        vendors: dict = {}
        for s in p_sales:
            v = s.get("vendeur","Inconnu")
            vendors.setdefault(v, {"ca": 0, "count": 0})
            vendors[v]["ca"]    += s["total"]
            vendors[v]["count"] += 1

        if vendors:
            df_v = pd.DataFrame([
                {"Vendeur": k, "CA (MAD)": f"{v['ca']:,.2f}", "Nb ventes": v["count"]}
                for k, v in sorted(vendors.items(), key=lambda x: -x[1]["ca"])
            ])
            st.dataframe(df_v, use_container_width=True, hide_index=True)
        else:
            st.info("Aucune donnée.")

        # ── Payment modes ──
        st.markdown("### 💳 Modes de paiement")
        pay_stats: dict = {}
        for s in p_sales:
            for pm in s.get("payments", []):
                lbl = pm.get("label","—")
                pay_stats.setdefault(lbl, {"amount": 0, "count": 0})
                pay_stats[lbl]["amount"] += pm.get("amount", 0)
                pay_stats[lbl]["count"]  += 1

        if pay_stats:
            total_pay = sum(v["amount"] for v in pay_stats.values())
            for lbl, data in sorted(pay_stats.items(), key=lambda x: -x[1]["amount"]):
                pct = int(data["amount"] / total_pay * 100) if total_pay else 0
                st.markdown(f"""
                <div style='background:#111927; border:1px solid #1E2D42; border-radius:8px; padding:12px; margin-bottom:6px;'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:5px;'>
                        <span style='color:#F1F5F9; font-weight:600;'>{lbl}</span>
                        <span style='color:#10B981; font-weight:700;'>{data["amount"]:,.2f} MAD</span>
                    </div>
                    <div style='background:#1E2D42; border-radius:3px; height:5px;'>
                        <div style='width:{pct}%; background:#8B5CF6; border-radius:3px; height:100%;'></div>
                    </div>
                    <div style='color:#475569; font-size:11px; margin-top:4px;'>{pct}% du total · {data["count"]} transaction(s)</div>
                </div>""", unsafe_allow_html=True)

    with col_r:
        # ── Top products ──
        st.markdown("### 📦 Top Produits")
        prod_stats: dict = {}
        for s in p_sales:
            for item in s.get("items",[]):
                n = item["name"]
                prod_stats.setdefault(n, {"qty":0,"revenue":0})
                prod_stats[n]["qty"]     += item["qty"]
                prod_stats[n]["revenue"] += item["qty"]*item["price"]*(1+item["tva"]/100)

        if prod_stats:
            df_p = pd.DataFrame([
                {"Produit": k, "Quantité": v["qty"], "CA TTC": f"{v['revenue']:,.2f} MAD"}
                for k,v in sorted(prod_stats.items(), key=lambda x: -x[1]["revenue"])
            ])
            st.dataframe(df_p, use_container_width=True, hide_index=True)

        # ── Top clients ──
        st.markdown("### 🏆 Top Clients")
        client_stats: dict = {}
        for s in p_sales:
            n = s["clientName"]
            client_stats.setdefault(n, {"ca":0,"count":0})
            client_stats[n]["ca"]    += s["total"]
            client_stats[n]["count"] += 1

        if client_stats:
            df_c = pd.DataFrame([
                {"Client": k, "CA (MAD)": f"{v['ca']:,.2f}", "Nb ventes": v["count"]}
                for k,v in sorted(client_stats.items(), key=lambda x: -x[1]["ca"])
            ])
            st.dataframe(df_c, use_container_width=True, hide_index=True)

    # ── Full sales table ──────────────────────────────
    st.divider()
    st.markdown(f"### 📋 Toutes les ventes ({len(p_sales)})")
    if p_sales:
        df_s = pd.DataFrame([{
            "Facture":   s["id"],
            "Client":    s["clientName"],
            "Vendeur":   s.get("vendeur","—"),
            "Date":      s["date"],
            "Total TTC": f"{s['total']:,.2f} MAD",
            "Statut":    s["status"].upper(),
        } for s in p_sales])
        st.dataframe(df_s, use_container_width=True, hide_index=True)

        # ── Export CSV ──
        csv = df_s.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Exporter CSV", data=csv, file_name="sellup_ventes.csv", mime="text/csv")
