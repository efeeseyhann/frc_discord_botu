import json
import os
from datetime import datetime

GUILDS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'guilds.json')

def load_guild_data():
    """
    Tüm guild verilerini guilds.json dosyasından okur. 
    Dosya veya dizin yoksa otomatik olarak güvenli bir şekilde döner.
    """
    if not os.path.exists(GUILDS_FILE):
        return {}
        
    try:
        with open(GUILDS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Dosya bozuksa veya okunamazsa boş sözlük döndür
        return {}

def save_guild_data(data):
    """
    Verilen sözlüğü (dictionary) guilds.json dosyasına kaydeder.
    Gerekli klasörlerin (data/) var olduğundan emin olur.
    """
    os.makedirs(os.path.dirname(GUILDS_FILE), exist_ok=True)
    with open(GUILDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_guild_config(guild_id):
    """
    Belirtilen guild_id'ye ait FRC konfigürasyonlarını döndürür.
    Eğer hiç kayıt yoksa boş bir sözlük {} döner.
    """
    data = load_guild_data()
    return data.get(str(guild_id), {})

def set_guild_config(guild_id, team_name, team_number, role_id=None):
    """
    Bir guild için FRC takım kurulum bilgilerini ilk defa kaydeder veya baştan yazar.
    """
    data = load_guild_data()
    guild_id_str = str(guild_id)
    
    if guild_id_str not in data:
        data[guild_id_str] = {}
        
    data[guild_id_str]["team_name"] = str(team_name)
    data[guild_id_str]["team_number"] = str(team_number)  # Standartlaştırmak için string tutulur
    data[guild_id_str]["setup_completed"] = True
    data[guild_id_str]["updated_at"] = datetime.now().isoformat()
    
    if role_id is not None:
        data[guild_id_str]["role_id"] = role_id
        
    save_guild_data(data)

def update_team_name(guild_id, new_name):
    """Yalnızca belirlilen sunucunun takım ismini günceller."""
    data = load_guild_data()
    guild_id_str = str(guild_id)
    
    if guild_id_str in data:
        data[guild_id_str]["team_name"] = str(new_name)
        data[guild_id_str]["updated_at"] = datetime.now().isoformat()
        save_guild_data(data)

def update_team_number(guild_id, new_number):
    """Yalnızca belirlilen sunucunun takım numarasını günceller."""
    data = load_guild_data()
    guild_id_str = str(guild_id)
    
    if guild_id_str in data:
        data[guild_id_str]["team_number"] = str(new_number)
        data[guild_id_str]["updated_at"] = datetime.now().isoformat()
        save_guild_data(data)

def is_setup_complete(guild_id):
    """
    Guild için kurulumun tamamlanıp tamamlanmadığını kontrol eder.
    Böylece komut bloklarında if is_setup_complete(guild_id): şeklinde temiz kullanılabilir.
    """
    conf = get_guild_config(guild_id)
    return conf.get("setup_completed", False)

