import streamlit as st
import pandas as pd

STATUS_COLORS = {
    "payée":      "#10B981",
    "en attente": "#F59E0B",
    "annulée":    "#EF4444",
}

def render():
    st.markdown("## ◰ Historique des Ventes")
    st.caption(f"{len(st.session_state.sales)} ventes enregistrées")
    st.divider()

    sales = st.session_state.sales

    # ── Filters ─────────────────────────────────────
    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        search = st.text_input("🔍 Rechercher", placeholder="Client, facture, vendeur...")
    with col_f2:
        status_filter = st.selectbox("Statut", ["Toutes", "payée", "en attente", "annulée"])

    filtered = sales
    if search:
        q = search.lower()
        filtered = [s for s in filtered if q in s["clientName"].lower() or q in s["id"].lower() or q in s.get("vendeur","").lower()]
    if status_filter != "Toutes":
        filtered = [s for s in filtered if s["status"] == status_filter]

    st.markdown(f"**{len(filtered)}** résultat(s)")
    st.divider()

    # ── Sales list ───────────────────────────────────
    if not filtered:
        st.info("Aucune vente trouvée.")
        return

    for s in filtered:
        color  = STATUS_COLORS.get(s["status"], "#475569")
        pm_str = s.get("paymentSummary", s.get("payment", "—"))
        has_delivery = bool(s.get("delivery"))
        dlv_status   = s["delivery"]["status"] if has_delivery else ""

        with st.expander(f"**{s['id']}** — {s['clientName']} — {s['total']:,.2f} MAD", expanded=False):
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f"**Client**  \n{s['clientName']}")
            c2.markdown(f"**Date**  \n{s['date']}")
            c3.markdown(f"**Vendeur**  \n{s.get('vendeur','—')}")
            c4.markdown(f"**Statut**  \n"
                        f"<span style='background:{color}22; color:{color}; border:1px solid {color}44; border-radius:5px; padding:2px 8px; font-size:12px; font-weight:700;'>{s['status'].upper()}</span>",
                        unsafe_allow_html=True)

            st.markdown("---")

            # Items table
            df = pd.DataFrame([{
                "Produit": i["name"], "Qté": i["qty"],
                "Prix HT": f"{i['price']:,} MAD", "TVA": f"{i['tva']}%",
                "Total TTC": f"{i['qty']*i['price']*(1+i['tva']/100):,.2f} MAD"
            } for i in s["items"]])
            st.dataframe(df, use_container_width=True, hide_index=True)

            cols = st.columns(4)
            cols[0].metric("HT",         f"{s['subtotal']:,.2f} MAD")
            cols[1].metric("TVA",        f"{s['tva']:,.2f} MAD")
            cols[2].metric("Remise",     f"-{s['discount']:,.2f} MAD")
            cols[3].metric("TOTAL TTC",  f"{s['total']:,.2f} MAD")

            st.markdown(f"**Paiement :** {pm_str}")
            if s.get("notes"):
                st.markdown(f"📝 *{s['notes']}*")

            # Delivery info
            if has_delivery:
                d = s["delivery"]
                dlv_colors = {"en_attente":"#475569","préparée":"#F59E0B","expédiée":"#0EA5E9","livrée":"#10B981","annulée":"#EF4444"}
                dc = dlv_colors.get(d["status"], "#475569")
                st.markdown(f"""
                <div style='background:rgba(14,165,233,0.08); border:1px solid rgba(14,165,233,0.25); border-radius:10px; padding:14px; margin-top:10px;'>
                    <div style='font-weight:700; color:#0EA5E9; margin-bottom:8px;'>🚚 Livraison</div>
                    <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; font-size:13px;'>
                        <div><span style='color:#475569;'>Statut : </span><span style='background:{dc}22; color:{dc}; border-radius:4px; padding:1px 6px; font-size:11px; font-weight:700;'>{d["status"]}</span></div>
                        <div><span style='color:#475569;'>Prévue : </span><strong style='color:#F1F5F9;'>{d.get("plannedDate","—")}</strong></div>
                        <div><span style='color:#475569;'>Transporteur : </span><strong style='color:#F1F5F9;'>{d.get("carrier","—")}</strong></div>
                        {"<div style='grid-column:1/-1;'><span style='color:#475569;'>Adresse : </span><span style='color:#F1F5F9;'>" + d.get("address","") + "</span></div>" if d.get("address") else ""}
                        {"<div style='grid-column:1/-1;'><span style='color:#475569;'>Suivi : </span><code style='color:#8B5CF6;'>" + d.get("trackingNum","") + "</code></div>" if d.get("trackingNum") else ""}
                    </div>
                </div>""", unsafe_allow_html=True)

            # Actions
            st.markdown("<br>", unsafe_allow_html=True)
            act_cols = st.columns([1, 1, 4])
            with act_cols[0]:
                if s["status"] != "annulée":
                    if st.button("❌ Annuler", key=f"cancel_sale_{s['id']}"):
                        st.session_state.sales = [
                            {**x, "status": "annulée"} if x["id"] == s["id"] else x
                            for x in st.session_state.sales
                        ]
                        st.success(f"Facture {s['id']} annulée.")
                        st.rerun()
