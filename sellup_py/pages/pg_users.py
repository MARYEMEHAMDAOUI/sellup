import streamlit as st

ROLES = ["admin", "manager", "vendeur"]
ROLE_ICONS = {"admin": "👑", "manager": "📊", "vendeur": "💼"}
ROLE_COLORS = {"admin": "#8B5CF6", "manager": "#F59E0B", "vendeur": "#0EA5E9"}

def render():
    current_user = st.session_state.current_user

    if current_user["role"] != "admin":
        st.error("🔒 Accès réservé aux administrateurs.")
        return

    st.markdown("## ◉ Gestion des Utilisateurs")
    st.caption(f"{len(st.session_state.users)} utilisateurs · Réservé aux administrateurs")
    st.divider()

    # ── Add user ─────────────────────────────────────
    with st.expander("＋ Nouvel utilisateur"):
        nc = st.columns(2)
        u_name  = nc[0].text_input("Nom complet *",    key="nu_name")
        u_user  = nc[1].text_input("Identifiant *",    key="nu_username")
        u_pwd   = nc[0].text_input("Mot de passe *",   key="nu_pwd", type="password")
        u_email = nc[1].text_input("Email *",          key="nu_email")
        nc2 = st.columns(2)
        u_role   = nc2[0].selectbox("Rôle", ROLES, key="nu_role")
        u_active = nc2[1].toggle("Compte actif", value=True, key="nu_active")

        if st.button("✓ Créer l'utilisateur", type="primary"):
            errs = []
            if not u_name.strip():  errs.append("Nom requis")
            if not u_user.strip():  errs.append("Identifiant requis")
            if not u_pwd.strip():   errs.append("Mot de passe requis")
            if not u_email.strip(): errs.append("Email requis")
            if any(u["username"] == u_user for u in st.session_state.users):
                errs.append("Identifiant déjà utilisé")

            if errs:
                st.error(" · ".join(errs))
            else:
                new_id = max((u["id"] for u in st.session_state.users), default=0) + 1
                avatar = "".join(w[0].upper() for w in u_name.split()[:2])
                from datetime import date
                st.session_state.users.append({
                    "id": new_id, "username": u_user, "password": u_pwd,
                    "name": u_name, "role": u_role, "email": u_email,
                    "avatar": avatar, "active": u_active,
                    "phone": "", "city": "", "birthDate": "", "joinDate": str(date.today()), "bio": ""
                })
                st.success(f"Utilisateur '{u_name}' créé !")
                st.rerun()

    st.divider()

    # ── User list ─────────────────────────────────────
    for u in st.session_state.users:
        is_me = u["id"] == current_user["id"]
        role_color = ROLE_COLORS.get(u["role"], "#475569")
        role_icon  = ROLE_ICONS.get(u["role"], "👤")
        status_color = "#10B981" if u["active"] else "#EF4444"

        with st.expander(
            f"{role_icon} **{u['name']}** — @{u['username']} — {u['role']}"
            + (" *(vous)*" if is_me else ""),
            expanded=False
        ):
            c1, c2, c3 = st.columns(3)
            c1.markdown(f"📧 **Email**  \n{u['email']}")
            c2.markdown(f"🔑 **Identifiant**  \n`{u['username']}`")
            c3.markdown(f"""
            **Statut**  
            <span style='background:{status_color}22; color:{status_color}; border:1px solid {status_color}44;
                border-radius:5px; padding:2px 8px; font-size:12px; font-weight:700;'>
                {"● Actif" if u["active"] else "○ Inactif"}
            </span>""", unsafe_allow_html=True)

            if u.get("phone"): st.markdown(f"📞 {u['phone']}")
            if u.get("city"):  st.markdown(f"📍 {u['city']}")
            if u.get("bio"):   st.markdown(f"💬 *{u['bio']}*")

            st.markdown("---")

            # Edit
            with st.expander("✎ Modifier"):
                ec = st.columns(2)
                e_name  = ec[0].text_input("Nom",    value=u["name"],  key=f"eu_name_{u['id']}")
                e_email = ec[1].text_input("Email",  value=u["email"], key=f"eu_email_{u['id']}")
                e_role  = ec[0].selectbox("Rôle", ROLES, index=ROLES.index(u["role"]), key=f"eu_role_{u['id']}")
                e_activ = ec[1].toggle("Actif", value=u["active"], key=f"eu_active_{u['id']}", disabled=is_me)
                e_phone = ec[0].text_input("Téléphone", value=u.get("phone",""), key=f"eu_phone_{u['id']}")
                e_city  = ec[1].text_input("Ville",     value=u.get("city",""),  key=f"eu_city_{u['id']}")

                if st.button("💾 Sauvegarder", key=f"eu_save_{u['id']}"):
                    if is_me and not e_activ:
                        st.error("Vous ne pouvez pas désactiver votre propre compte.")
                    else:
                        st.session_state.users = [
                            {**x, "name": e_name, "email": e_email, "role": e_role,
                             "active": e_activ, "phone": e_phone, "city": e_city}
                            if x["id"] == u["id"] else x
                            for x in st.session_state.users
                        ]
                        # update current user if editing self
                        if is_me:
                            st.session_state.current_user = next(
                                x for x in st.session_state.users if x["id"] == u["id"]
                            )
                        st.success("Utilisateur mis à jour !")
                        st.rerun()

            if not is_me:
                if st.button("🗑 Supprimer cet utilisateur", key=f"eu_del_{u['id']}", type="secondary"):
                    st.session_state.users = [x for x in st.session_state.users if x["id"] != u["id"]]
                    st.success(f"'{u['name']}' supprimé.")
                    st.rerun()
