import json
import os
from datetime import datetime
from typing import Optional, Union

# users.json dosyasının tam yolu
USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'users.json')

# Geçerli rol alanları — komutta bunlar dışında kabul etmeyeceğiz
VALID_ROLES = ("software", "mechanical", "electrical", "pr", "mentor", "student", "other")


# ============================================================
# Temel Okuma / Yazma
# ============================================================

def load_users():
    """
    users.json dosyasını okur.
    - Dosya yoksa otomatik olarak boş oluşturur.
    - JSON bozuksa {} döner, terminale uyarı basar.
    """
    if not os.path.exists(USERS_FILE):
        save_users({})
        return {}

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ [user_profile_database] users.json bozuk, boş sözlük döndürülüyor.")
        return {}
    except FileNotFoundError:
        return {}


def save_users(data):
    """Verilen sözlüğü users.json dosyasına kaydeder."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
# Profil Oluşturma / Güncelleme
# ============================================================

def get_or_create_profile(user_id, display_name):
    """
    Kullanıcı profili varsa döndürür, yoksa boş bir profil oluşturur.
    Her çağrıda display_name güncellenir.
    """
    data = load_users()
    key = str(user_id)

    if key not in data:
        now = datetime.now().isoformat()
        data[key] = {
            "user_id": str(user_id),
            "display_name": display_name,
            "role_area": None,
            "team_number": None,
            "country": None,
            "short_bio": None,
            "created_at": now,
            "updated_at": now
        }
    else:
        # Kullanıcı adı değişmiş olabilir, güncelleyelim
        data[key]["display_name"] = display_name

    save_users(data)
    return data[key]


def get_profile(user_id):
    """Kullanıcı profilini döndürür. Kayıt yoksa None döner."""
    data = load_users()
    return data.get(str(user_id), None)


def update_profile_field(user_id, display_name, **fields):
    """
    Belirtilen profil alanlarını günceller, updated_at'i yeniler.

    Örnek:
        update_profile_field(123456, "Ali", role_area="software", country="Turkey")
    """
    profile = get_or_create_profile(user_id, display_name)
    data = load_users()
    key = str(user_id)

    ALLOWED_FIELDS = {"role_area", "team_number", "country", "short_bio", "display_name"}

    for field, value in fields.items():
        if field in ALLOWED_FIELDS:
            data[key][field] = value

    data[key]["updated_at"] = datetime.now().isoformat()
    save_users(data)
    return data[key]


def get_user_count():
    """Toplam kayıtlı kullanıcı sayısını döndürür."""
    return len(load_users())
