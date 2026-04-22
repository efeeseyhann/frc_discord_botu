import json
import os
import random
from datetime import datetime

# Teams.json dosyasının tam yolu (utils klasöründen iki üst dizin -> data klasörü)
TEAMS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'teams.json')


# ============================================================
# Temel Okuma / Yazma
# ============================================================

def load_teams() -> dict:
    """
    teams.json dosyasını okur ve bir sözlük olarak döndürür.
    - Dosya yoksa: otomatik olarak boş bir teams.json oluşturur.
    - JSON bozuksa: bozuk veriyi silmeden {} döner, terminale uyarı basar.
    """
    if not os.path.exists(TEAMS_FILE):
        # Dosya hiç oluşturulmamışsa ilk seferinde boş oluştur
        save_teams({})
        return {}

    try:
        with open(TEAMS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("⚠️ [team_database] teams.json okunamadı (JSON formatı bozuk). Boş sözlük döndürülüyor.")
        return {}
    except FileNotFoundError:
        return {}


def save_teams(data: dict) -> None:
    """
    Verilen sözlüğü teams.json dosyasına kaydeder.
    data klasörü yoksa otomatik oluşturur.
    """
    os.makedirs(os.path.dirname(TEAMS_FILE), exist_ok=True)
    with open(TEAMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# ============================================================
# Takım Ekleme
# ============================================================

def add_team(team_number: int, team_name: str, country: str, city: str,
             rookie_or_veteran: str, registered_by_user_id: int | str,
             description: str = None) -> bool:
    """
    Yeni bir takımı global veritabanına ekler.
    - Aynı team_number zaten kayıtlıysa: ekleme yapmaz, False döner.
    - Başarılıysa True döner.
    """
    data = load_teams()
    key = str(team_number)

    if key in data:
        return False  # Bu takım numarası zaten kayıtlı, tekrar ekleme

    now = datetime.now().isoformat()

    data[key] = {
        "team_number": int(team_number),
        "team_name": str(team_name),
        "country": str(country),
        "city": str(city),
        "rookie_or_veteran": str(rookie_or_veteran),
        "description": str(description) if description else "",
        "registered_by_user_id": str(registered_by_user_id),
        "created_at": now,
        "updated_at": now   # İlk eklemede created_at ile aynı
    }

    save_teams(data)
    return True


# ============================================================
# Takım Sorgulama
# ============================================================

def get_team(team_number: int | str) -> dict | None:
    """
    Belirli bir takım numarasına ait veriyi döndürür.
    Bulunamazsa None döner.
    """
    data = load_teams()
    return data.get(str(team_number), None)


def team_exists(team_number: int | str) -> bool:
    """Takım numarasının veritabanında kayıtlı olup olmadığını kontrol eder."""
    return get_team(team_number) is not None


def search_teams_by_name(keyword: str) -> list:
    """
    Takım adında belirtilen anahtar kelimeyi (büyük/küçük harf duyarsız) içeren
    tüm takımları liste olarak döndürür.
    """
    data = load_teams()
    keyword_lower = keyword.lower()
    return [
        team for team in data.values()
        if keyword_lower in team.get("team_name", "").lower()
    ]


def search_teams_by_country(country: str) -> list:
    """Belirtilen ülkedeki tüm takımları döndürür (büyük/küçük harf duyarsız)."""
    data = load_teams()
    country_lower = country.lower()
    return [
        team for team in data.values()
        if team.get("country", "").lower() == country_lower
    ]


def search_teams_by_city(city: str) -> list:
    """Belirtilen şehirdeki tüm takımları döndürür (büyük/küçük harf duyarsız)."""
    data = load_teams()
    city_lower = city.lower()
    return [
        team for team in data.values()
        if team.get("city", "").lower() == city_lower
    ]


def get_all_teams() -> list:
    """Veritabanındaki tüm takımları liste olarak döndürür."""
    return list(load_teams().values())


def get_team_count() -> int:
    """Toplam kayıtlı takım sayısını döndürür."""
    return len(load_teams())


def get_random_team() -> dict | None:
    """
    Veritabanından rastgele bir takım döndürür.
    Veritabanı boşsa None döner.
    """
    teams = get_all_teams()
    if not teams:
        return None
    return random.choice(teams)


# ============================================================
# Takım Güncelleme
# ============================================================

def update_team(team_number: int | str, **fields) -> bool:
    """
    Mevcut bir takımın belirtilen alanlarını günceller ve updated_at'i yeniler.
    Yalnızca izin verilen alanlar güncellenir (team_number ve ID alanları korunur).

    Örnek kullanım:
        update_team(10998, city="Ankara", description="Yeni açıklama")

    Takım bulunamazsa False, başarılıysa True döner.
    """
    data = load_teams()
    key = str(team_number)

    if key not in data:
        return False

    ALLOWED_FIELDS = {"team_name", "country", "city", "rookie_or_veteran", "description"}

    for field, value in fields.items():
        if field in ALLOWED_FIELDS:
            data[key][field] = str(value)

    # Her güncellemede zaman damgasını yenile
    data[key]["updated_at"] = datetime.now().isoformat()

    save_teams(data)
    return True


# ============================================================
# Takım Silme
# ============================================================

def delete_team(team_number: int | str) -> bool:
    """
    Takımı veritabanından kalıcı olarak siler.
    Bulunamazsa False, başarılıysa True döner.
    """
    data = load_teams()
    key = str(team_number)

    if key not in data:
        return False

    del data[key]
    save_teams(data)
    return True
