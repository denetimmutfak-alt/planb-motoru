#!/usr/bin/env python3
"""
Crypto Corporate-Style Data for Enhanced ULTRA Analysis
"""

CRYPTO_CORPORATE_DATA = {
    "BTC-USD": {
        "genesis_date": "2009-01-03",  # Genesis block
        "creator_known": False,
        "halving_cycle": 4,  # 4 yılda bir
        "next_halving": "2028-04-20",
        "major_forks": [
            {"date": "2017-08-01", "name": "Bitcoin Cash", "type": "hard_fork"},
            {"date": "2017-10-24", "name": "Bitcoin Gold", "type": "hard_fork"},
            {"date": "2018-11-15", "name": "Bitcoin SV", "type": "hard_fork"}
        ],
        "protocol_upgrades": [
            {"date": "2017-08-23", "name": "SegWit", "impact": "high"},
            {"date": "2021-11-14", "name": "Taproot", "impact": "high"}
        ],
        "foundation": None,
        "astro_weight": 0.6  # Kısıtlı astroloji
    },
    
    "ETH-USD": {
        "genesis_date": "2015-07-30",  # Ethereum launch
        "creator": "Vitalik Buterin",
        "creator_birthday": "1994-01-31",
        "foundation_date": "2014-07-01",  # Ethereum Foundation
        "major_upgrades": [
            {"date": "2016-07-20", "name": "DAO Fork", "impact": "critical"},
            {"date": "2020-12-01", "name": "Beacon Chain", "impact": "high"},
            {"date": "2021-08-05", "name": "London (EIP-1559)", "impact": "high"},
            {"date": "2022-09-15", "name": "The Merge", "impact": "critical"},
            {"date": "2023-04-12", "name": "Shanghai", "impact": "high"}
        ],
        "development_cycles": "quarterly",  # EIP cycles
        "astro_weight": 0.8  # Daha güçlü astroloji
    },
    
    "ADA-USD": {
        "genesis_date": "2017-09-29",
        "creator": "Charles Hoskinson", 
        "creator_birthday": "1987-11-05",
        "foundation_date": "2015-01-01",  # IOHK/Input Output
        "major_upgrades": [
            {"date": "2020-07-29", "name": "Shelley", "impact": "high"},
            {"date": "2021-09-12", "name": "Alonzo (Smart Contracts)", "impact": "critical"},
            {"date": "2022-09-22", "name": "Vasil", "impact": "medium"}
        ],
        "research_based": True,
        "academic_cycles": True,
        "astro_weight": 0.7
    },
    
    "DOGE-USD": {
        "genesis_date": "2013-12-06",
        "creators": ["Billy Markus", "Jackson Palmer"],
        "foundation": None,
        "meme_factor": True,
        "elon_influence": True,  # Elon tweets etkisi
        "major_events": [
            {"date": "2021-01-28", "name": "Reddit Pump", "impact": "critical"},
            {"date": "2021-05-08", "name": "SNL Elon", "impact": "critical"}
        ],
        "astro_weight": 0.3  # Çok kısıtlı
    }
}

def get_crypto_corporate_score(symbol: str) -> dict:
    """Crypto için corporate-style score hesapla"""
    if symbol not in CRYPTO_CORPORATE_DATA:
        return {"score": 50.0, "weight": 0.3}
    
    data = CRYPTO_CORPORATE_DATA[symbol]
    
    # Genesis date astrology
    genesis_score = calculate_genesis_astrology(data["genesis_date"])
    
    # Creator astrology (if available)
    creator_score = 50.0
    if "creator_birthday" in data:
        creator_score = calculate_creator_astrology(data["creator_birthday"])
    
    # Upgrade cycle astrology
    upgrade_score = calculate_upgrade_cycles(data.get("major_upgrades", []))
    
    # Combine scores
    final_score = (genesis_score * 0.4 + creator_score * 0.3 + upgrade_score * 0.3)
    
    return {
        "score": final_score,
        "weight": data["astro_weight"],
        "components": {
            "genesis": genesis_score,
            "creator": creator_score, 
            "upgrades": upgrade_score
        }
    }

def calculate_genesis_astrology(date_str: str) -> float:
    """Genesis date için astroloji hesapla"""
    # Implement actual astrology calculation
    from datetime import datetime
    date = datetime.strptime(date_str, "%Y-%m-%d")
    
    # Basit implementasyon - gerçekte daha karmaşık olacak
    day_of_year = date.timetuple().tm_yday
    lunar_cycle = day_of_year % 29.5  # Ay döngüleri
    
    score = 50 + (lunar_cycle - 14.75) * 2  # -14.75 to +14.75 range
    return max(0, min(100, score))

def calculate_creator_astrology(birthday_str: str) -> float:
    """Creator birthday astrolojisi"""
    from datetime import datetime
    birthday = datetime.strptime(birthday_str, "%Y-%m-%d")
    
    # Güneş burcu etkisi
    month = birthday.month
    sun_sign_scores = {
        1: 65, 2: 60, 3: 70, 4: 55, 5: 75, 6: 68,
        7: 72, 8: 67, 9: 63, 10: 58, 11: 77, 12: 62
    }
    
    return sun_sign_scores.get(month, 50)

def calculate_upgrade_cycles(upgrades: list) -> float:
    """Protocol upgrade timing astrolojisi"""
    if not upgrades:
        return 50.0
    
    # Son 2 yıldaki upgrade'lerin timing analizi
    from datetime import datetime, timedelta
    now = datetime.now()
    recent_upgrades = [
        u for u in upgrades 
        if datetime.strptime(u["date"], "%Y-%m-%d") > now - timedelta(days=730)
    ]
    
    if not recent_upgrades:
        return 45.0  # Eski upgrade'ler
    
    # Impact bazlı scoring
    impact_scores = {"critical": 80, "high": 70, "medium": 60, "low": 50}
    scores = [impact_scores.get(u["impact"], 50) for u in recent_upgrades]
    
    return sum(scores) / len(scores)

if __name__ == "__main__":
    # Test
    btc_score = get_crypto_corporate_score("BTC-USD")
    eth_score = get_crypto_corporate_score("ETH-USD")
    
    print(f"BTC Corporate Score: {btc_score}")
    print(f"ETH Corporate Score: {eth_score}")