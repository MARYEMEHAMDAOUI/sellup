# ═══════════════════════════════════════════════════
#  SELLUP — Données partagées
# ═══════════════════════════════════════════════════

USERS = [
    {
        "id": 1, "username": "admin", "password": "admin123",
        "name": "Ahmed Benali", "role": "admin", "email": "admin@sellup.ma",
        "avatar": "AB", "active": True, "phone": "0661-100200",
        "city": "Casablanca", "birthDate": "1985-04-12", "joinDate": "2019-01-15",
        "bio": "Fondateur et directeur commercial de Sellup. Passionné par la croissance des ventes."
    },
    {
        "id": 2, "username": "vendeur1", "password": "pass123",
        "name": "Fatima Zahra", "role": "vendeur", "email": "fz@sellup.ma",
        "avatar": "FZ", "active": True, "phone": "0662-300400",
        "city": "Rabat", "birthDate": "1993-08-22", "joinDate": "2021-06-01",
        "bio": "Commerciale senior, spécialisée en grands comptes et fidélisation clients."
    },
    {
        "id": 3, "username": "manager", "password": "mgr123",
        "name": "Karim Idrissi", "role": "manager", "email": "ki@sellup.ma",
        "avatar": "KI", "active": True, "phone": "0663-500600",
        "city": "Marrakech", "birthDate": "1989-11-05", "joinDate": "2020-03-10",
        "bio": "Manager des opérations, supervise les équipes ventes et logistique."
    },
]

PRODUCTS = [
    {"id": 1, "name": "Laptop Pro X1",       "category": "Électronique", "price": 12990, "stock": 45, "minStock": 10, "ref": "LPX-001", "tva": 20},
    {"id": 2, "name": "Casque Audio BT Pro",  "category": "Électronique", "price": 890,   "stock": 120,"minStock": 20, "ref": "CAB-002", "tva": 20},
    {"id": 3, "name": "Bureau Standing",      "category": "Mobilier",     "price": 3990,  "stock": 8,  "minStock": 5,  "ref": "BST-003", "tva": 20},
    {"id": 4, "name": "Chaise Ergonomique",   "category": "Mobilier",     "price": 5490,  "stock": 22, "minStock": 8,  "ref": "CHE-004", "tva": 20},
    {"id": 5, "name": 'Moniteur 27"',         "category": "Électronique", "price": 3290,  "stock": 60, "minStock": 15, "ref": "MON-005", "tva": 20},
    {"id": 6, "name": "Imprimante Laser",     "category": "Bureautique",  "price": 2190,  "stock": 3,  "minStock": 5,  "ref": "IMP-006", "tva": 20},
]

CLIENTS = [
    {"id": 1, "name": "Maroc Tech SARL",   "email": "contact@maroctech.ma","phone": "0522-123456","city": "Casablanca","ice": "001234567000012","address": "123 Bd Anfa, Casablanca",       "type": "Entreprise",  "createdAt": "2024-01-15"},
    {"id": 2, "name": "Entreprise Soleil", "email": "info@soleil.ma",       "phone": "0537-654321","city": "Rabat",      "ice": "009876543000034","address": "45 Av Hassan II, Rabat",        "type": "Entreprise",  "createdAt": "2024-03-10"},
    {"id": 3, "name": "Youssef El Amrani", "email": "youssef@gmail.com",    "phone": "0661-234567","city": "Marrakech",  "ice": "",              "address": "12 Rue Zitoun, Marrakech",      "type": "Particulier", "createdAt": "2024-06-20"},
    {"id": 4, "name": "Atlas Group SA",    "email": "sales@atlasgroup.ma",  "phone": "0539-345678","city": "Fès",        "ice": "007654321000056","address": "89 Quartier Industriel, Fès",   "type": "Entreprise",  "createdAt": "2023-11-05"},
]

SALES = [
    {
        "id": "FAC-2026-001", "clientId": 1, "clientName": "Maroc Tech SARL",
        "items": [{"productId": 1, "name": "Laptop Pro X1", "qty": 2, "price": 12990, "tva": 20}],
        "subtotal": 25980, "tva": 5196, "discount": 0, "discountPct": 0, "total": 31176,
        "payments": [{"mode": "virement", "label": "Virement", "amount": 31176, "pct": 100}],
        "paymentSummary": "Virement 100%", "status": "payée",
        "date": "2026-02-10", "vendeur": "Fatima Zahra", "notes": "",
        "delivery": {
            "status": "livrée", "plannedDate": "2026-02-18",
            "shippedDate": "2026-02-16", "deliveredDate": "2026-02-17",
            "address": "123 Bd Anfa, Casablanca", "carrier": "Amana Express",
            "trackingNum": "AM2026021600123", "notes": "", "cancelReason": ""
        }
    },
    {
        "id": "FAC-2026-002", "clientId": 4, "clientName": "Atlas Group SA",
        "items": [{"productId": 5, "name": 'Moniteur 27"', "qty": 5, "price": 3290, "tva": 20}],
        "subtotal": 16450, "tva": 3290, "discount": 500, "discountPct": 2.6, "total": 19240,
        "payments": [
            {"mode": "virement", "label": "Virement",      "amount": 7696, "pct": 40},
            {"mode": "espèces",  "label": "Espèces",       "amount": 5772, "pct": 30},
            {"mode": "crédit",   "label": "Crédit client", "amount": 5772, "pct": 30},
        ],
        "paymentSummary": "Virement 40% + Espèces 30% + Crédit 30%",
        "status": "en attente", "date": "2026-02-18", "vendeur": "Ahmed Benali", "notes": "",
        "delivery": {
            "status": "expédiée", "plannedDate": "2026-02-28",
            "shippedDate": "2026-02-24", "deliveredDate": "",
            "address": "89 Quartier Industriel, Fès", "carrier": "SMSA",
            "trackingNum": "SM2026022400456", "notes": "Fragile", "cancelReason": ""
        }
    },
    {
        "id": "FAC-2026-003", "clientId": 2, "clientName": "Entreprise Soleil",
        "items": [{"productId": 4, "name": "Chaise Ergonomique", "qty": 3, "price": 5490, "tva": 20}],
        "subtotal": 16470, "tva": 3294, "discount": 0, "discountPct": 0, "total": 19764,
        "payments": [
            {"mode": "chèque",  "label": "Chèque",   "amount": 9882, "pct": 50},
            {"mode": "virement","label": "Virement", "amount": 9882, "pct": 50},
        ],
        "paymentSummary": "Chèque 50% + Virement 50%",
        "status": "payée", "date": "2026-02-25", "vendeur": "Karim Idrissi", "notes": "",
        "delivery": {
            "status": "préparée", "plannedDate": "2026-03-05",
            "shippedDate": "", "deliveredDate": "",
            "address": "45 Av Hassan II, Rabat", "carrier": "",
            "trackingNum": "", "notes": "Livraison en matinée", "cancelReason": ""
        }
    },
]
