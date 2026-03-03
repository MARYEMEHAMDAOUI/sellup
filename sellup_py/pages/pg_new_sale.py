import streamlit as st
from datetime import date, datetime

PAYMENT_MODES = [
    {"id": "espèces",  "label": "💵 Espèces",       "color": "#10B981"},
    {"id": "virement", "label": "🏦 Virement",       "color": "#0EA5E9"},
    {"id": "chèque",   "label": "📄 Chèque",         "color": "#F59E0B"},
    {"id": "carte",    "label": "💳 Carte bancaire",  "color": "#8B5CF6"},
    {"id": "crédit",   "label": "⏳ Crédit client",   "color": "#EF4444"},
]

def render():
    st.markdown("## ⊞ Nouvelle Vente")
    st.caption("Créez une nouvelle facture en 3 étapes")
    st.divider()

    # ── State init ──────────────────────────────────
    if "nv_step"     not in st.session_state: st.session_state.nv_step     = 1
    if "nv_client"   not in st.session_state: st.session_state.nv_client   = None
    if "nv_cart"     not in st.session_state: st.session_state.nv_cart     = {}
    if "nv_discount_pct" not in st.session_state: st.session_state.nv_discount_pct = 0.0
    if "nv_notes"    not in st.session_state: st.session_state.nv_notes    = ""
    if "nv_payments" not in st.session_state: st.session_state.nv_payments = [{"mode": "espèces", "label": "Espèces", "pct": 100}]
    if "nv_delivery" not in st.session_state:
        st.session_state.nv_delivery = {"needed": True, "plannedDate": None, "carrier": "", "address": "", "notes": ""}
    if "nv_confirmed_invoice" not in st.session_state: st.session_state.nv_confirmed_invoice = None

    step = st.session_state.nv_step

    # ── Step indicator ───────────────────────────────
    cols = st.columns(3)
    labels = ["1 · Sélectionner Client", "2 · Ajouter Produits", "3 · Confirmer & Payer"]
    for i, (col, label) in enumerate(zip(cols, labels)):
        active = (i + 1 == step)
        done   = (i + 1 < step)
        color  = "#0EA5E9" if active else ("#10B981" if done else "#1E2D42")
        text_c = "#F1F5F9" if active or done else "#475569"
        col.markdown(f"""
        <div style='background:{"rgba(14,165,233,0.15)" if active else "#111927"}; border:1px solid {color};
             border-radius:10px; padding:12px 16px; text-align:center;'>
            <span style='color:{text_c}; font-weight:{"700" if active else "400"}; font-size:13px;'>
                {"✓ " if done else ""}{label}
            </span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Confirmed invoice view ────────────────────────
    if st.session_state.nv_confirmed_invoice:
        _show_invoice(st.session_state.nv_confirmed_invoice)
        if st.button("← Retour au tableau de bord"):
            _reset_sale()
            st.session_state.page = "dashboard"
            st.rerun()
        return

    # ═══════════════ STEP 1: CLIENT ═══════════════════
    if step == 1:
        st.markdown("### 👥 Sélectionnez un client")
        search = st.text_input("🔍 Rechercher", placeholder="Nom du client...")
        clients = [c for c in st.session_state.clients if search.lower() in c["name"].lower()] if search else st.session_state.clients

        for c in clients:
            selected = st.session_state.nv_client and st.session_state.nv_client["id"] == c["id"]
            border = "#0EA5E9" if selected else "#1E2D42"
            bg     = "rgba(14,165,233,0.1)" if selected else "#111927"
            st.markdown(f"""
            <div style='background:{bg}; border:1.5px solid {border}; border-radius:12px; padding:16px 20px; margin-bottom:8px;'>
                <div style='font-size:15px; font-weight:700; color:#F1F5F9;'>{c["name"]}</div>
                <div style='color:#475569; font-size:12px; margin-top:4px;'>
                    📍 {c["city"]} &nbsp;·&nbsp; 📧 {c["email"]} &nbsp;·&nbsp;
                    <span style='background:{"rgba(14,165,233,0.15)" if c["type"]=="Entreprise" else "rgba(16,185,129,0.12)"}; color:{"#0EA5E9" if c["type"]=="Entreprise" else "#10B981"}; border-radius:5px; padding:2px 8px; font-size:11px; font-weight:700;'>{c["type"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"✓ Choisir — {c['name']}", key=f"sel_client_{c['id']}"):
                st.session_state.nv_client = c
                st.session_state.nv_step   = 2
                st.rerun()

    # ═══════════════ STEP 2: CART ═══════════════════
    elif step == 2:
        col_prod, col_cart = st.columns([1.6, 1])

        with col_prod:
            st.markdown("### 🛍️ Catalogue produits")
            search = st.text_input("🔍 Rechercher produit", placeholder="Nom ou référence...")
            products = [p for p in st.session_state.products if search.lower() in p["name"].lower()] if search else st.session_state.products

            for p in products:
                in_cart = st.session_state.nv_cart.get(p["id"], 0)
                low = p["stock"] <= p["minStock"]
                st.markdown(f"""
                <div style='background:#111927; border:1px solid {"#F59E0B44" if low else "#1E2D42"}; border-radius:12px; padding:14px 18px; margin-bottom:8px;'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <div>
                            <div style='font-size:14px; font-weight:600; color:#F1F5F9;'>{p["name"]}</div>
                            <div style='color:#475569; font-size:12px;'>{p["ref"]} · {p["category"]} · Stock: {p["stock"]} {"⚠️" if low else "✓"}</div>
                        </div>
                        <div style='text-align:right;'>
                            <div style='font-size:14px; font-weight:700; color:#0EA5E9;'>{p["price"]:,} MAD</div>
                            <div style='font-size:11px; color:#475569;'>TVA {p["tva"]}% · {"✓ en panier" if in_cart else ""}</div>
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

                btn_cols = st.columns([1, 1, 2])
                with btn_cols[0]:
                    if st.button("＋", key=f"add_{p['id']}", disabled=p["stock"] <= 0):
                        cur = st.session_state.nv_cart.get(p["id"], 0)
                        if cur < p["stock"]:
                            st.session_state.nv_cart[p["id"]] = cur + 1
                            st.rerun()
                with btn_cols[1]:
                    if in_cart > 0 and st.button("－", key=f"rem_{p['id']}"):
                        if in_cart <= 1:
                            del st.session_state.nv_cart[p["id"]]
                        else:
                            st.session_state.nv_cart[p["id"]] = in_cart - 1
                        st.rerun()

        with col_cart:
            st.markdown(f"### 🛒 Panier ({len(st.session_state.nv_cart)})")
            cart = st.session_state.nv_cart
            products_map = {p["id"]: p for p in st.session_state.products}

            if not cart:
                st.info("Aucun produit ajouté")
            else:
                subtotal = 0
                tva_total = 0
                for pid, qty in cart.items():
                    p = products_map[pid]
                    line_ht  = p["price"] * qty
                    line_ttc = line_ht * (1 + p["tva"] / 100)
                    subtotal  += line_ht
                    tva_total += line_ht * p["tva"] / 100
                    st.markdown(f"""
                    <div style='background:#0E1520; border:1px solid #1E2D42; border-radius:8px; padding:10px 14px; margin-bottom:6px;'>
                        <div style='font-size:13px; font-weight:600; color:#F1F5F9;'>{p["name"]}</div>
                        <div style='display:flex; justify-content:space-between; margin-top:4px;'>
                            <span style='color:#475569; font-size:12px;'>{p["price"]:,} × {qty}</span>
                            <span style='color:#10B981; font-weight:700; font-size:13px;'>{line_ttc:,.2f} MAD</span>
                        </div>
                    </div>""", unsafe_allow_html=True)

                st.markdown(f"""
                <div style='background:#111927; border:1px solid #1E2D42; border-radius:10px; padding:14px; margin-top:10px;'>
                    <div style='display:flex; justify-content:space-between; font-size:12px; color:#475569; margin-bottom:4px;'>
                        <span>Sous-total HT</span><span>{subtotal:,.2f} MAD</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; font-size:12px; color:#475569; margin-bottom:8px;'>
                        <span>TVA</span><span>{tva_total:,.2f} MAD</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; font-size:17px; font-weight:800; color:#F1F5F9; border-top:1px solid #1E2D42; padding-top:10px;'>
                        <span>Total TTC</span><span style='color:#10B981;'>{subtotal+tva_total:,.2f} MAD</span>
                    </div>
                </div>""", unsafe_allow_html=True)

                if st.button("Continuer →", use_container_width=True, type="primary"):
                    st.session_state.nv_step = 3
                    st.rerun()

        if st.button("← Retour", key="back_step2"):
            st.session_state.nv_step = 1
            st.rerun()

    # ═══════════════ STEP 3: PAYMENT ═══════════════════
    elif step == 3:
        cart          = st.session_state.nv_cart
        products_map  = {p["id"]: p for p in st.session_state.products}
        client        = st.session_state.nv_client

        subtotal  = sum(products_map[pid]["price"] * qty for pid, qty in cart.items())
        tva_total = sum(products_map[pid]["price"] * qty * products_map[pid]["tva"] / 100 for pid, qty in cart.items())
        base_total = subtotal + tva_total

        col_form, col_recap = st.columns([1.5, 1])

        with col_form:
            # ── Recap cart ──
            st.markdown("### 🧾 Récapitulatif")
            for pid, qty in cart.items():
                p = products_map[pid]
                ttc = p["price"] * qty * (1 + p["tva"] / 100)
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #1E2D42;'>
                    <span style='color:#CBD5E1; font-size:13px;'>{p["name"]} × {qty}</span>
                    <span style='color:#10B981; font-weight:600; font-size:13px;'>{ttc:,.2f} MAD</span>
                </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # ── Discount ──
            st.markdown("### 🏷️ Remise")
            disc_cols = st.columns(2)
            with disc_cols[0]:
                disc_pct = st.number_input("Pourcentage (%)", min_value=0.0, max_value=100.0,
                                            value=float(st.session_state.nv_discount_pct), step=0.5, format="%.1f")
                disc_amt = round(base_total * disc_pct / 100, 2)
                st.caption(f"→ Montant : **{disc_amt:,.2f} MAD**")
            with disc_cols[1]:
                disc_amt_input = st.number_input("Montant (MAD)", min_value=0.0, max_value=float(base_total),
                                                   value=disc_amt, step=10.0, format="%.2f", key="disc_amt_input")
                if abs(disc_amt_input - disc_amt) > 0.5:
                    disc_pct = round(disc_amt_input / base_total * 100, 2) if base_total > 0 else 0
                    disc_amt = disc_amt_input
                st.caption(f"→ Pourcentage : **{disc_pct:.1f}%**")
            st.session_state.nv_discount_pct = disc_pct
            total = base_total - disc_amt

            # ── Payments ──
            st.markdown("### 💳 Modes de paiement")
            pm_ids = [m["id"] for m in PAYMENT_MODES]
            pm_labels = {m["id"]: m["label"] for m in PAYMENT_MODES}

            payments = st.session_state.nv_payments
            allocated = sum(p.get("amount", 0) for p in payments)
            remaining = round(total - allocated, 2)

            for i, pm in enumerate(payments):
                pm_cols = st.columns([1.5, 1, 1, 0.4])
                with pm_cols[0]:
                    mode = st.selectbox("Mode", pm_ids, index=pm_ids.index(pm["mode"]),
                                        format_func=lambda x: pm_labels[x], key=f"pm_mode_{i}")
                    pm["mode"]  = mode
                    pm["label"] = next(m["label"].split(" ",1)[1] for m in PAYMENT_MODES if m["id"] == mode)
                with pm_cols[1]:
                    pct = st.number_input("% ", 0.0, 100.0, float(pm.get("pct", 0)), 1.0, key=f"pm_pct_{i}")
                    pm["pct"]    = pct
                    pm["amount"] = round(total * pct / 100, 2)
                with pm_cols[2]:
                    amt = st.number_input("MAD ", 0.0, float(total) * 2, float(pm.get("amount", 0)), 10.0, key=f"pm_amt_{i}")
                    if abs(amt - pm["amount"]) > 0.5:
                        pm["amount"] = amt
                        pm["pct"]    = round(amt / total * 100, 2) if total else 0
                with pm_cols[3]:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if len(payments) > 1 and st.button("✕", key=f"rm_pm_{i}"):
                        payments.pop(i)
                        st.session_state.nv_payments = payments
                        st.rerun()

            if st.button("＋ Ajouter un mode"):
                payments.append({"mode": "espèces", "label": "Espèces", "pct": 0, "amount": 0})
                st.session_state.nv_payments = payments
                st.rerun()

            if st.button("⚡ Solde restant →"):
                if payments:
                    payments[-1]["amount"] = round(remaining, 2)
                    payments[-1]["pct"]    = round(remaining / total * 100, 2) if total else 0
                    st.session_state.nv_payments = payments
                    st.rerun()

            allocated = sum(p.get("amount", 0) for p in payments)
            remaining = round(total - allocated, 2)
            balanced  = abs(remaining) < 0.05

            if balanced:
                st.success("✓ Paiement équilibré")
            elif remaining > 0:
                st.warning(f"⚠ Reste à affecter : {remaining:,.2f} MAD")
            else:
                st.error(f"⚠ Dépassement de {abs(remaining):,.2f} MAD")

            # ── Delivery ──
            st.markdown("### 🚚 Livraison")
            delivery = st.session_state.nv_delivery
            delivery["needed"] = st.toggle("Programmer une livraison", value=delivery.get("needed", True))

            if delivery["needed"]:
                d_cols = st.columns(2)
                with d_cols[0]:
                    delivery["plannedDate"] = st.date_input("📅 Date prévue *",
                        value=delivery.get("plannedDate") or date.today(), min_value=date.today())
                with d_cols[1]:
                    delivery["carrier"] = st.text_input("🚚 Transporteur",
                        value=delivery.get("carrier", ""), placeholder="Amana, SMSA, DHL...")
                delivery["address"] = st.text_input("📍 Adresse",
                    value=delivery.get("address") or client.get("address", ""),
                    placeholder="Adresse de livraison...")
                delivery["notes"]   = st.text_input("📝 Instructions",
                    value=delivery.get("notes", ""), placeholder="Fragile, livrer le matin...")
            else:
                st.info("✋ Retrait sur place — pas de livraison")

            # ── Notes ──
            st.markdown("### 📝 Notes")
            st.session_state.nv_notes = st.text_area("Notes de commande", value=st.session_state.nv_notes, height=80)

        # ── Recap sidebar ──
        with col_recap:
            st.markdown("### 📊 Récapitulatif final")
            st.markdown(f"""
            <div style='background:#111927; border:1px solid #1E2D42; border-radius:14px; padding:20px;'>
                <div style='font-size:13px; color:#475569; margin-bottom:12px;'>Client</div>
                <div style='font-size:15px; font-weight:700; color:#F1F5F9; margin-bottom:16px;'>{client["name"]}</div>
                <div style='display:flex; justify-content:space-between; font-size:13px; padding:6px 0; border-bottom:1px solid #1E2D42;'>
                    <span style='color:#475569;'>Sous-total HT</span><span style='color:#CBD5E1;'>{subtotal:,.2f} MAD</span>
                </div>
                <div style='display:flex; justify-content:space-between; font-size:13px; padding:6px 0; border-bottom:1px solid #1E2D42;'>
                    <span style='color:#475569;'>TVA</span><span style='color:#CBD5E1;'>{tva_total:,.2f} MAD</span>
                </div>
                {"" if disc_amt == 0 else f"""
                <div style='display:flex; justify-content:space-between; font-size:13px; padding:6px 0; border-bottom:1px solid #1E2D42;'>
                    <span style='color:#475569;'>Remise ({disc_pct:.1f}%)</span><span style='color:#8B5CF6;'>- {disc_amt:,.2f} MAD</span>
                </div>"""}
                <div style='display:flex; justify-content:space-between; font-size:18px; font-weight:800; padding:12px 0;'>
                    <span style='color:#F1F5F9;'>TOTAL TTC</span><span style='color:#10B981;'>{total:,.2f} MAD</span>
                </div>
            </div>""", unsafe_allow_html=True)

            delivery_ok = not delivery["needed"] or (delivery.get("plannedDate") is not None)
            can_confirm = balanced and bool(cart) and delivery_ok

            if not can_confirm:
                if not balanced:
                    st.warning("⚠ Équilibrez le paiement")
                if delivery["needed"] and not delivery.get("plannedDate"):
                    st.warning("⚠ Date de livraison requise")

            if st.button("✓ Confirmer la Vente", use_container_width=True,
                         type="primary", disabled=not can_confirm):
                _confirm_sale(cart, products_map, client, subtotal, tva_total,
                              disc_amt, disc_pct, total, payments, delivery)
                st.rerun()

        if st.button("← Modifier le panier"):
            st.session_state.nv_step = 2
            st.rerun()


def _confirm_sale(cart, products_map, client, subtotal, tva_total, disc_amt, disc_pct, total, payments, delivery):
    from datetime import date as d_cls
    user     = st.session_state.current_user
    sale_num = len(st.session_state.sales) + 1
    has_credit = any(p["mode"] == "crédit" for p in payments)

    planned_str = delivery["plannedDate"].strftime("%Y-%m-%d") if isinstance(delivery.get("plannedDate"), d_cls) else str(delivery.get("plannedDate",""))

    new_sale = {
        "id": f"FAC-2026-{sale_num:03d}",
        "clientId":   client["id"],
        "clientName": client["name"],
        "items": [
            {"productId": pid, "name": products_map[pid]["name"],
             "qty": qty, "price": products_map[pid]["price"], "tva": products_map[pid]["tva"]}
            for pid, qty in cart.items()
        ],
        "subtotal": round(subtotal, 2),
        "tva":      round(tva_total, 2),
        "discount": round(disc_amt, 2),
        "discountPct": disc_pct,
        "total":    round(total, 2),
        "payments": [{"mode": p["mode"], "label": p["label"], "amount": p["amount"], "pct": p["pct"]} for p in payments],
        "paymentSummary": " + ".join(f"{p['label']} {p['pct']:.0f}%" for p in payments),
        "status": "en attente" if has_credit else "payée",
        "date":   str(date.today()),
        "vendeur": user["name"],
        "notes":   st.session_state.nv_notes,
        "delivery": {
            "status":        "en_attente",
            "plannedDate":   planned_str,
            "shippedDate":   "",
            "deliveredDate": "",
            "address":       delivery.get("address",""),
            "carrier":       delivery.get("carrier",""),
            "trackingNum":   "",
            "notes":         delivery.get("notes",""),
            "cancelReason":  "",
        } if delivery.get("needed") else None,
    }

    # Update stock
    for pid, qty in cart.items():
        st.session_state.products = [
            {**p, "stock": p["stock"] - qty} if p["id"] == pid else p
            for p in st.session_state.products
        ]

    st.session_state.sales.insert(0, new_sale)
    st.session_state.nv_confirmed_invoice = new_sale
    st.session_state.nv_step = 4


def _show_invoice(inv):
    st.markdown("## ✅ Vente Confirmée")
    st.success(f"Facture **{inv['id']}** créée avec succès !")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style='background:#111927; border:1px solid #1E2D42; border-radius:12px; padding:20px;'>
            <div style='font-size:11px; color:#475569; text-transform:uppercase; margin-bottom:8px;'>Facturé à</div>
            <div style='font-size:15px; font-weight:700; color:#F1F5F9;'>{inv["clientName"]}</div>
            <div style='color:#475569; font-size:12px; margin-top:4px;'>Vendeur : {inv["vendeur"]}</div>
            <div style='color:#475569; font-size:12px;'>Date : {inv["date"]}</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        status_color = "#10B981" if inv["status"] == "payée" else "#F59E0B"
        st.markdown(f"""
        <div style='background:#111927; border:1px solid #1E2D42; border-radius:12px; padding:20px;'>
            <div style='font-size:11px; color:#475569; text-transform:uppercase; margin-bottom:8px;'>Facture</div>
            <div style='font-size:20px; font-weight:800; color:#0EA5E9;'>{inv["id"]}</div>
            <div style='margin-top:8px;'><span style='background:{status_color}22; color:{status_color}; border:1px solid {status_color}44; border-radius:5px; padding:3px 10px; font-size:12px; font-weight:700;'>{inv["status"].upper()}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    import pandas as pd
    df = pd.DataFrame([{
        "Produit": item["name"], "Qté": item["qty"],
        "Prix HT": f"{item['price']:,} MAD",
        "TVA": f"{item['tva']}%",
        "Total TTC": f"{item['qty']*item['price']*(1+item['tva']/100):,.2f} MAD"
    } for item in inv["items"]])
    st.dataframe(df, use_container_width=True, hide_index=True)

    cols = st.columns(3)
    cols[0].metric("Sous-total HT", f"{inv['subtotal']:,.2f} MAD")
    cols[1].metric("TVA", f"{inv['tva']:,.2f} MAD")
    cols[2].metric("TOTAL TTC", f"{inv['total']:,.2f} MAD")

    st.markdown("**Modes de règlement :**")
    for p in inv["payments"]:
        st.markdown(f"- {p['label']} : **{p['pct']:.0f}%** → {p['amount']:,.2f} MAD")

    if inv.get("delivery"):
        d = inv["delivery"]
        st.info(f"🚚 Livraison prévue le **{d['plannedDate']}**"
                + (f" via {d['carrier']}" if d.get("carrier") else "")
                + (f" · {d['address']}" if d.get("address") else ""))


def _reset_sale():
    for key in ["nv_step","nv_client","nv_cart","nv_discount_pct",
                "nv_notes","nv_payments","nv_delivery","nv_confirmed_invoice"]:
        if key in st.session_state:
            del st.session_state[key]
