import streamlit as st
from datetime import date

DELIVERY_STATUSES = {
    "en_attente":  ("🕐", "#475569", "En attente"),
    "préparée":    ("📦", "#F59E0B", "Préparée"),
    "expédiée":    ("🚚", "#0EA5E9", "Expédiée"),
    "livrée":      ("✅", "#10B981", "Livrée"),
    "annulée":     ("❌", "#EF4444", "Annulée"),
}

TODAY = date(2026, 3, 1)

def delay_days(planned: str, delivered: str, status: str):
    if not planned: return None
    try:
        p = date.fromisoformat(planned)
    except Exception:
        return None
    if status == "annulée":  return None
    if status == "livrée" and delivered:
        try: return (date.fromisoformat(delivered) - p).days
        except: return None
    return (TODAY - p).days

def render():
    st.markdown("## 🚚 Livraisons")
    st.caption("Suivi des expéditions et gestion des délais")
    st.divider()

    sales = [s for s in st.session_state.sales if s.get("delivery")]

    if not sales:
        st.info("Aucune livraison à afficher.")
        return

    # ── KPI counters ────────────────────────────────
    counts = {k: 0 for k in DELIVERY_STATUSES}
    late_count = 0
    for s in sales:
        st._obj = s["delivery"]["status"]
        counts[s["delivery"]["status"]] = counts.get(s["delivery"]["status"], 0) + 1
        d = delay_days(s["delivery"].get("plannedDate",""), s["delivery"].get("deliveredDate",""), s["delivery"]["status"])
        if d is not None and d > 0 and s["delivery"]["status"] not in ("livrée","annulée"):
            late_count += 1

    kpi_cols = st.columns(6)
    kpi_data = list(DELIVERY_STATUSES.items()) + [("retard", ("⏰", "#EF4444", "En retard"))]
    for i, (k, (icon, color, label)) in enumerate(list(DELIVERY_STATUSES.items())):
        cnt = counts.get(k, 0)
        kpi_cols[i].markdown(f"""
        <div style='background:#111927; border:1px solid {color}44; border-radius:12px; padding:14px; text-align:center;'>
            <div style='font-size:20px;'>{icon}</div>
            <div style='font-size:20px; font-weight:800; color:{color}; font-family:"Plus Jakarta Sans",sans-serif;'>{cnt}</div>
            <div style='font-size:11px; color:#475569;'>{label}</div>
        </div>""", unsafe_allow_html=True)
    kpi_cols[5].markdown(f"""
    <div style='background:#111927; border:1px solid {"#EF4444" if late_count else "#1E2D42"}44; border-radius:12px; padding:14px; text-align:center;'>
        <div style='font-size:20px;'>⏰</div>
        <div style='font-size:20px; font-weight:800; color:{"#EF4444" if late_count else "#475569"}; font-family:"Plus Jakarta Sans",sans-serif;'>{late_count}</div>
        <div style='font-size:11px; color:#475569;'>En retard</div>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── Filters ──────────────────────────────────────
    f_cols = st.columns([2, 1])
    with f_cols[0]:
        search = st.text_input("🔍 Rechercher", placeholder="Client ou facture...")
    with f_cols[1]:
        status_filter = st.selectbox("Statut", ["Tous"] + [v[2] for v in DELIVERY_STATUSES.values()])

    status_map_rev = {v[2]: k for k, v in DELIVERY_STATUSES.items()}
    filtered = sales
    if search:
        q = search.lower()
        filtered = [s for s in filtered if q in s["clientName"].lower() or q in s["id"].lower()]
    if status_filter != "Tous":
        key = status_map_rev.get(status_filter)
        if key: filtered = [s for s in filtered if s["delivery"]["status"] == key]

    st.markdown(f"**{len(filtered)}** livraison(s)")
    st.divider()

    # ── Delivery cards ───────────────────────────────
    for s in filtered:
        d = s["delivery"]
        icon, color, label = DELIVERY_STATUSES.get(d["status"], ("📦","#475569","—"))
        delay = delay_days(d.get("plannedDate",""), d.get("deliveredDate",""), d["status"])

        # Delay badge
        if delay is None:
            delay_html = ""
        elif delay < 0:
            delay_html = f"<span style='background:#10B98122; color:#10B981; border-radius:5px; padding:2px 8px; font-size:11px;'>✓ En avance {abs(delay)}j</span>"
        elif delay == 0:
            delay_html = f"<span style='background:#0EA5E922; color:#0EA5E9; border-radius:5px; padding:2px 8px; font-size:11px;'>Dans les temps</span>"
        else:
            delay_html = f"<span style='background:#EF444422; color:#EF4444; border-radius:5px; padding:2px 8px; font-size:11px;'>⚠ Retard +{delay}j</span>"

        # Timeline (only non-cancelled)
        if d["status"] != "annulée":
            steps = [("en_attente","🕐"),("préparée","📦"),("expédiée","🚚"),("livrée","✅")]
            prog_map = {"en_attente":0,"préparée":1,"expédiée":2,"livrée":3}
            cur_prog = prog_map.get(d["status"],0)
            timeline_html = "<div style='display:flex; align-items:flex-start; margin:12px 0;'>"
            for j,(sid,sicon) in enumerate(steps):
                done   = prog_map[sid] <= cur_prog
                active = sid == d["status"]
                sc = DELIVERY_STATUSES[sid][1]
                circle = f"background:{sc}; border:2px solid {sc}; box-shadow:0 0 10px {sc}55;" if done else f"background:transparent; border:2px solid #1E2D42;"
                line_color = sc if done and j < len(steps)-1 else "#1E2D42"
                timeline_html += f"""
                <div style='display:flex; flex-direction:column; align-items:center; flex:{"0" if j==len(steps)-1 else "1"};'>
                    <div style='display:flex; align-items:center; width:100%;'>
                        <div style='width:32px; height:32px; border-radius:50%; {circle} display:flex; align-items:center; justify-content:center; font-size:14px; flex-shrink:0;'>{sicon}</div>
                        {"" if j==len(steps)-1 else f"<div style='flex:1; height:3px; background:{line_color}; margin:0 2px;'></div>"}
                    </div>
                    <div style='font-size:10px; color:{"#F1F5F9" if done else "#475569"}; margin-top:5px; font-weight:{"700" if done else "400"}; text-align:center;'>{DELIVERY_STATUSES[sid][2]}</div>
                </div>"""
            timeline_html += "</div>"
        else:
            timeline_html = ""

        with st.expander(f"{icon} **{s['id']}** — {s['clientName']} — {d['status']}", expanded=False):
            h_cols = st.columns([3, 1])
            with h_cols[0]:
                st.markdown(f"""
                <div style='display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-bottom:8px;'>
                    <span style='background:{color}22; color:{color}; border:1px solid {color}44; border-radius:5px; padding:3px 10px; font-size:12px; font-weight:700;'>{icon} {label}</span>
                    {delay_html}
                    <span style='color:#475569; font-size:12px;'>Total : <strong style='color:#10B981;'>{s["total"]:,.2f} MAD</strong></span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(timeline_html, unsafe_allow_html=True)

            # Info grid
            info_cols = st.columns(3)
            info_cols[0].markdown(f"📅 **Prévue**  \n{d.get('plannedDate','—')}")
            info_cols[1].markdown(f"🚚 **Expédiée**  \n{d.get('shippedDate','—') or '—'}")
            info_cols[2].markdown(f"✅ **Livrée**  \n{d.get('deliveredDate','—') or '—'}")

            if d.get("carrier"):
                st.markdown(f"🏢 **Transporteur :** {d['carrier']}")
            if d.get("trackingNum"):
                st.markdown(f"📦 **Suivi :** `{d['trackingNum']}`")
            if d.get("address"):
                st.markdown(f"📍 **Adresse :** {d['address']}")
            if d.get("notes"):
                st.markdown(f"📝 *{d['notes']}*")
            if d.get("cancelReason"):
                st.error(f"Motif d'annulation : {d['cancelReason']}")

            # Edit delivery
            if d["status"] not in ("livrée","annulée"):
                st.markdown("---")
                st.markdown("**✎ Mettre à jour la livraison**")
                ed_cols = st.columns(2)
                new_status = ed_cols[0].selectbox(
                    "Statut", [k for k in DELIVERY_STATUSES if k != "annulée"],
                    index=list(DELIVERY_STATUSES.keys()).index(d["status"]),
                    format_func=lambda x: f"{DELIVERY_STATUSES[x][0]} {DELIVERY_STATUSES[x][2]}",
                    key=f"dlv_status_{s['id']}"
                )
                new_carrier = ed_cols[1].text_input("Transporteur", value=d.get("carrier",""), key=f"dlv_carrier_{s['id']}")
                new_tracking = st.text_input("N° de suivi", value=d.get("trackingNum",""), key=f"dlv_track_{s['id']}")

                if st.button("💾 Sauvegarder", key=f"dlv_save_{s['id']}"):
                    st.session_state.sales = [
                        {**x, "delivery": {**x["delivery"], "status": new_status, "carrier": new_carrier, "trackingNum": new_tracking}}
                        if x["id"] == s["id"] else x
                        for x in st.session_state.sales
                    ]
                    st.success("Livraison mise à jour !")
                    st.rerun()

                # Cancel
                with st.expander("🚫 Annuler cette livraison"):
                    reason = st.text_input("Motif d'annulation *", key=f"dlv_reason_{s['id']}")
                    if st.button("Confirmer l'annulation", key=f"dlv_cancel_{s['id']}", type="secondary",
                                 disabled=not reason.strip()):
                        st.session_state.sales = [
                            {**x, "status": "annulée", "delivery": {**x["delivery"], "status": "annulée", "cancelReason": reason}}
                            if x["id"] == s["id"] else x
                            for x in st.session_state.sales
                        ]
                        st.success("Livraison annulée.")
                        st.rerun()
