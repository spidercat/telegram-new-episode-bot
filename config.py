Parents = ["Maxim", "Ola"]
Kids = ["Nitay", "Naama", "Idan"]
Family = Parents + Kids

Guests = ["Ido", "Ori", "Hagai"]

Whoami = {
    "Maxim": "Ты отец.",
    "Ola": "Мать ты.",
    "Nitay": "You are a nagging, little monster also known as Nitay.",
    "Ido": "Ido, you're an esteemed guest of Grabarnik family bot.",
    "Ori": "Ori the Hush Hash, you're an esteemed guest of Grabarnik family bot.",
    "Hagai": "Hagai, you're a friend and an esteemed colleague."
}

storage = {
    "Common": {
        "EPISODES_DIR": "Pending-Series",
        "TARGET_DIR": "Cartoon Series"
    },
    "Nitay": {
        "EPISODES_DIR": "Pending_Nitay",
        "TARGET_DIR": "Nitay Series"
    },
    "Maxim": {
        "EPISODES_DIR": "Pending_Nitay",
        "TARGET_DIR": "Nitay Series"
    }
}

# (optional) global mapping of show name to folder name
SHOW_TO_FOLDER = {
    'Hakalmarim': 'הקלמרים',
    'Kan Garim BeKef': 'כאן גרים בכיף',
    'Aba Metapelet': 'אבא מטפלת'
}
