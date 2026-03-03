import streamlit as st

def render():
    st.markdown("## ◎ Clients")
    st.caption("Gestion du portefeuille clients")
    st.divider()

    clients = st.session_state.clients
    sales   = st.session_state.sales

    # ── Add client ───────────────────────────────────
    with st.expander("＋ Nouveau client"):
        fc = st.columns(2)
        n_name  = fc[0].text_input("Nom *",      key="nc_name")
        n_email = fc[1].text_input("Email *",     key="nc_email")
        n_phone = fc[0].text_input("Téléphone",   key="nc_phone")
        n_city  = fc[1].text_input("Ville",       key="nc_city")
        n_addr  = st.text_input("Adresse",        key="nc_addr")
        nc2 = st.columns(2)
        n_type = nc2[0].selectbox("Type", ["Entreprise","Particulier"], key="nc_type")
        n_ice  = nc2[1].text_input("ICE (Entreprise)", key="nc_ice")

        if st.button("✓ Créer le client", type="primary"):
            if not n_name.strip() or not n_email.strip():
                st.error("Nom et email requis.")
            else:
                new_id = max((c["id"] for c in clients), default=0) + 1
                from datetime import date
                st.session_state.clients.append({
                    "id": new_id, "name": n_name, "email": n_email,
                    "phone": n_phone, "city": n_city, "address": n_addr,
                    "type": n_type, "ice": n_ice,
                    "createdAt": str(date.today())
                })
                st.success(f"Client '{n_name}' créé !")
                st.rerun()

    # ── Search ───────────────────────────────────────
    search = st.text_input("🔍 Rechercher", placeholder="Nom, ville, email...")
    filtered = [c for c in clients if search.lower() in (c["name"]+c["city"]+c["email"]).lower()] if search else clients

    st.markdown(f"**{len(filtered)}** client(s)")
    st.divider()

    for c in filtered:
        client_sales = [s for s in sales if s["clientId"] == c["id"]]
        ca = sum(s["total"] for s in client_sales)
        type_color = "#0EA5E9" if c["type"] == "Entreprise" else "#10B981"

        with st.expander(f"**{c['name']}** — {c['city']} — {c['type']}", expanded=False):
            det_cols = st.columns(3)
            det_cols[0].markdown(f"📧 **Email**  \n{c['email']}")
            det_cols[1].markdown(f"📞 **Téléphone**  \n{c.get('phone','—')}")
            det_cols[2].markdown(f"📍 **Ville**  \n{c['city']}")

            if c.get("ice"):
                st.markdown(f"🏢 **ICE :** `{c['ice']}`")
            if c.get("address"):
                st.markdown(f"📍 **Adresse :** {c['address']}")

            st.markdown(f"**Client depuis :** {c.get('createdAt','—')}")

            # Stats
            st.divider()
            s_cols = st.columns(3)
            s_cols[0].metric("CA Total",      f"{ca:,.0f} MAD")
            s_cols[1].metric("Nb Ventes",     len(client_sales))
            s_cols[2].metric("Dernière vente", client_sales[0]["date"] if client_sales else "—")

            # Recent sales
            if client_sales:
                st.markdown("**Dernières factures :**")
                import pandas as pd
                df = pd.DataFrame([{
                    "Facture": s["id"], "Date": s["date"],
                    "Total": f"{s['total']:,.2f} MAD",
                    "Statut": s["status"]
                } for s in client_sales[:5]])
                st.dataframe(df, use_container_width=True, hide_index=True)

            # Edit
            st.markdown("---")
            with st.expander("✎ Modifier ce client"):
                ec = st.columns(2)
                e_name  = ec[0].text_input("Nom",       value=c["name"],          key=f"e_name_{c['id']}")
                e_email = ec[1].text_input("Email",     value=c["email"],         key=f"e_email_{c['id']}")
                e_phone = ec[0].text_input("Téléphone", value=c.get("phone",""),  key=f"e_phone_{c['id']}")
                e_city  = ec[1].text_input("Ville",     value=c.get("city",""),   key=f"e_city_{c['id']}")
                e_addr  = st.text_input("Adresse",      value=c.get("address",""),key=f"e_addr_{c['id']}")
                if st.button("💾 Sauvegarder", key=f"e_save_{c['id']}"):
                    st.session_state.clients = [
                        {**x, "name": e_name, "email": e_email, "phone": e_phone, "city": e_city, "address": e_addr}
                        if x["id"] == c["id"] else x
                        for x in st.session_state.clients
                    ]
                    st.success("Client mis à jour !")
                    st.rerun()

            # Delete
            if st.button("🗑 Supprimer", key=f"del_client_{c['id']}", type="secondary"):
                st.session_state.clients = [x for x in st.session_state.clients if x["id"] != c["id"]]
                st.success(f"Client '{c['name']}' supprimé.")
                st.rerun()
