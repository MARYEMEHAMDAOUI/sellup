import streamlit as st

def render():
    st.markdown("## ◫ Produits")
    st.caption("Catalogue et gestion des stocks")
    st.divider()

    products = st.session_state.products
    low_stock = [p for p in products if p["stock"] <= p["minStock"]]

    if low_stock:
        st.warning(f"⚠️ **{len(low_stock)} produit(s)** en stock critique !")
        st.divider()

    # ── Add product ───────────────────────────────────
    with st.expander("＋ Nouveau produit"):
        pc = st.columns(2)
        p_name  = pc[0].text_input("Nom *",       key="np_name")
        p_ref   = pc[1].text_input("Référence *", key="np_ref")
        p_cat   = pc[0].text_input("Catégorie",   key="np_cat")
        p_price = pc[1].number_input("Prix HT (MAD)", min_value=0.0, step=10.0, key="np_price")
        pc2 = st.columns(3)
        p_stock    = pc2[0].number_input("Stock initial", min_value=0, step=1, key="np_stock")
        p_minstock = pc2[1].number_input("Stock minimum", min_value=0, step=1, key="np_minstk")
        p_tva      = pc2[2].selectbox("TVA", [0, 7, 10, 14, 20], index=4, key="np_tva")

        if st.button("✓ Créer le produit", type="primary"):
            if not p_name.strip() or not p_ref.strip():
                st.error("Nom et référence requis.")
            else:
                new_id = max((p["id"] for p in products), default=0) + 1
                st.session_state.products.append({
                    "id": new_id, "name": p_name, "ref": p_ref, "category": p_cat,
                    "price": p_price, "stock": p_stock, "minStock": p_minstock, "tva": p_tva
                })
                st.success(f"Produit '{p_name}' créé !")
                st.rerun()

    # ── Filters ───────────────────────────────────────
    col_s, col_cat = st.columns([2, 1])
    with col_s:
        search = st.text_input("🔍 Rechercher", placeholder="Nom ou référence...")
    with col_cat:
        categories = ["Toutes"] + list({p["category"] for p in products})
        cat_filter = st.selectbox("Catégorie", categories)

    filtered = products
    if search:
        q = search.lower()
        filtered = [p for p in filtered if q in p["name"].lower() or q in p["ref"].lower()]
    if cat_filter != "Toutes":
        filtered = [p for p in filtered if p["category"] == cat_filter]

    st.markdown(f"**{len(filtered)}** produit(s)")
    st.divider()

    # ── Product cards ─────────────────────────────────
    for p in filtered:
        low  = p["stock"] <= p["minStock"]
        pct  = int(p["stock"] / max(p["minStock"] * 3, 1) * 100)
        pct  = min(pct, 100)
        bar_color = "#EF4444" if low else ("#F59E0B" if pct < 50 else "#10B981")
        ttc  = round(p["price"] * (1 + p["tva"] / 100), 2)

        with st.expander(
            f"{'⚠️ ' if low else ''} **{p['name']}** — {p['ref']} — {p['price']:,} MAD HT",
            expanded=False
        ):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Prix HT",  f"{p['price']:,} MAD")
            c2.metric("Prix TTC", f"{ttc:,} MAD",  f"TVA {p['tva']}%")
            c3.metric("Stock",    p["stock"],        delta=p["stock"] - p["minStock"],
                      delta_color="inverse" if low else "normal")
            c4.metric("Catégorie", p["category"])

            # Stock bar
            st.markdown(f"""
            <div style='margin:8px 0;'>
                <div style='display:flex; justify-content:space-between; font-size:12px; color:#475569; margin-bottom:4px;'>
                    <span>Stock : {p["stock"]} / Min : {p["minStock"]}</span>
                    <span style='color:{bar_color}; font-weight:700;'>{"⚠ Stock critique" if low else "✓ OK"}</span>
                </div>
                <div style='background:#1E2D42; border-radius:4px; height:8px;'>
                    <div style='width:{pct}%; background:{bar_color}; border-radius:4px; height:100%;'></div>
                </div>
            </div>""", unsafe_allow_html=True)

            # Edit
            st.markdown("---")
            with st.expander("✎ Modifier"):
                ec = st.columns(2)
                e_name  = ec[0].text_input("Nom",       value=p["name"],     key=f"ep_name_{p['id']}")
                e_price = ec[1].number_input("Prix HT", value=float(p["price"]), step=10.0, key=f"ep_price_{p['id']}")
                e_stock = ec[0].number_input("Stock",   value=int(p["stock"]), step=1, key=f"ep_stock_{p['id']}")
                e_min   = ec[1].number_input("Stock min", value=int(p["minStock"]), step=1, key=f"ep_min_{p['id']}")
                if st.button("💾 Sauvegarder", key=f"ep_save_{p['id']}"):
                    st.session_state.products = [
                        {**x, "name": e_name, "price": e_price, "stock": e_stock, "minStock": e_min}
                        if x["id"] == p["id"] else x
                        for x in st.session_state.products
                    ]
                    st.success("Produit mis à jour !")
                    st.rerun()

            if st.button("🗑 Supprimer", key=f"del_prod_{p['id']}", type="secondary"):
                st.session_state.products = [x for x in st.session_state.products if x["id"] != p["id"]]
                st.success(f"Produit '{p['name']}' supprimé.")
                st.rerun()
