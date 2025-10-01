#!/usr/bin/env python3
"""
Commodity Corporate-Style Data for Enhanced ULTRA Analysis
"""

COMMODITY_CORPORATE_DATA = {
    "GC=F": {  # Gold Futures
        "name": "Gold",
        "discovery_era": "ancient",
        "modern_trading_start": "1974-12-31",  # Gold trading legalized in US
        "major_exchanges": [
            {"name": "COMEX", "established": "1933-01-01"},
            {"name": "LBMA", "established": "1919-01-01"}
        ],
        "major_events": [
            {"date": "1971-08-15", "name": "Nixon Shock", "impact": "critical"},
            {"date": "1980-01-21", "name": "Gold Peak $850", "impact": "critical"},
            {"date": "2008-09-15", "name": "Lehman Crisis", "impact": "high"},
            {"date": "2020-03-15", "name": "COVID Crisis", "impact": "high"}
        ],
        "cycles": {
            "solar_sensitivity": 0.7,  # Güneş döngülerine duyarlılık
            "seasonal": "autumn_strong",  # Sonbahar güçlü
            "central_bank_cycles": "quarterly"
        },
        "astro_weight": 0.6
    },
    
    "CL=F": {  # Crude Oil Futures
        "name": "Crude Oil",
        "modern_trading_start": "1983-03-30",  # NYMEX WTI futures
        "major_exchanges": [
            {"name": "NYMEX", "established": "1872-01-01"},
            {"name": "ICE", "established": "2000-05-01"}
        ],
        "geopolitical_events": [
            {"date": "1973-10-17", "name": "Oil Embargo", "impact": "critical"},
            {"date": "1990-08-02", "name": "Gulf War", "impact": "critical"},
            {"date": "2001-09-11", "name": "9/11", "impact": "high"},
            {"date": "2020-04-20", "name": "Negative Oil", "impact": "critical"}
        ],
        "seasonal_cycles": {
            "driving_season": "summer_high",
            "heating_season": "winter_high",
            "refinery_maintenance": "spring_low"
        },
        "astro_weight": 0.5
    },
    
    "SI=F": {  # Silver Futures
        "name": "Silver", 
        "modern_trading_start": "1963-07-01",  # COMEX silver futures
        "major_events": [
            {"date": "1980-01-18", "name": "Hunt Brothers Squeeze", "impact": "critical"},
            {"date": "2008-09-15", "name": "Financial Crisis", "impact": "high"},
            {"date": "2021-01-28", "name": "Reddit Silver Squeeze", "impact": "medium"}
        ],
        "industrial_cycles": True,
        "monetary_metal": True,
        "astro_weight": 0.6
    },
    
    "ZW=F": {  # Wheat Futures
        "name": "Wheat",
        "modern_trading_start": "1877-01-01",  # Chicago Board of Trade
        "seasonal_cycles": {
            "planting": "spring",
            "harvest": "summer", 
            "storage": "autumn",
            "consumption": "winter"
        },
        "weather_sensitivity": 0.9,
        "major_events": [
            {"date": "2008-06-01", "name": "Food Crisis", "impact": "critical"},
            {"date": "2022-02-24", "name": "Ukraine War", "impact": "critical"}
        ],
        "astro_weight": 0.4
    }
}

def get_commodity_corporate_score(symbol: str) -> dict:
    """Emtia için corporate-style score hesapla"""
    if symbol not in COMMODITY_CORPORATE_DATA:
        return {"score": 50.0, "weight": 0.3}
    
    data = COMMODITY_CORPORATE_DATA[symbol]
    
    # Exchange establishment astrology
    exchange_score = calculate_exchange_astrology(data.get("major_exchanges", []))
    
    # Historical events timing
    events_score = calculate_historical_events(data.get("major_events", []))
    
    # Seasonal/cyclical patterns
    cycle_score = calculate_commodity_cycles(data)
    
    # Weather/geopolitical sensitivity
    sensitivity_score = calculate_sensitivity_factors(data)
    
    final_score = (
        exchange_score * 0.2 + 
        events_score * 0.3 + 
        cycle_score * 0.3 +
        sensitivity_score * 0.2
    )
    
    return {
        "score": final_score,
        "weight": data["astro_weight"],
        "components": {
            "exchanges": exchange_score,
            "events": events_score,
            "cycles": cycle_score,
            "sensitivity": sensitivity_score
        }
    }

def calculate_exchange_astrology(exchanges: list) -> float:
    """Exchange kuruluş tarihleri astrolojisi"""
    if not exchanges:
        return 50.0
    
    from datetime import datetime
    scores = []
    
    for exchange in exchanges:
        date = datetime.strptime(exchange["established"], "%Y-%m-%d")
        # Jupiter cycle analysis (12 year)
        years_since = (datetime.now() - date).days / 365.25
        jupiter_position = (years_since % 12) / 12 * 360  # degrees
        
        # Jupiter-favorable positions
        if 60 <= jupiter_position <= 120 or 240 <= jupiter_position <= 300:
            score = 70
        elif 0 <= jupiter_position <= 30 or 330 <= jupiter_position <= 360:
            score = 65
        else:
            score = 55
            
        scores.append(score)
    
    return sum(scores) / len(scores)

def calculate_historical_events(events: list) -> float:
    """Tarihsel olayların timing analizi"""
    if not events:
        return 50.0
    
    from datetime import datetime
    current_phase = 50.0
    
    # Son 5 yıldaki major events
    now = datetime.now()
    recent_events = [
        e for e in events 
        if datetime.strptime(e["date"], "%Y-%m-%d").year >= now.year - 5
    ]
    
    if recent_events:
        impact_scores = {"critical": 80, "high": 70, "medium": 60, "low": 50}
        scores = [impact_scores.get(e["impact"], 50) for e in recent_events]
        current_phase = sum(scores) / len(scores)
    
    return current_phase

def calculate_commodity_cycles(data: dict) -> float:
    """Emtia döngüleri analizi"""
    from datetime import datetime
    now = datetime.now()
    month = now.month
    
    # Seasonal scoring
    seasonal_scores = {
        "spring": {1: 45, 2: 50, 3: 65, 4: 70, 5: 75, 6: 70, 
                  7: 65, 8: 60, 9: 55, 10: 50, 11: 45, 12: 40},
        "summer": {1: 40, 2: 45, 3: 50, 4: 55, 5: 65, 6: 75, 
                  7: 80, 8: 75, 9: 65, 10: 55, 11: 45, 12: 40},
        "autumn": {1: 50, 2: 45, 3: 40, 4: 45, 5: 50, 6: 55, 
                  7: 60, 8: 65, 9: 75, 10: 80, 11: 75, 12: 65},
        "winter": {1: 75, 2: 80, 3: 75, 4: 65, 5: 55, 6: 45, 
                  7: 40, 8: 45, 9: 50, 10: 60, 11: 70, 12: 75}
    }
    
    if "seasonal_cycles" in data:
        cycles = data["seasonal_cycles"]
        if isinstance(cycles, dict):
            # Composite seasonal score
            total_score = 0
            count = 0
            for season, pattern in cycles.items():
                if season in seasonal_scores:
                    total_score += seasonal_scores[season][month]
                    count += 1
            return total_score / count if count > 0 else 50.0
        else:
            return seasonal_scores["spring"][month]  # Default
    
    return 50.0

def calculate_sensitivity_factors(data: dict) -> float:
    """Duyarlılık faktörleri"""
    score = 50.0
    
    # Weather sensitivity
    if data.get("weather_sensitivity", 0) > 0.7:
        # Yüksek weather sensitivity = daha volatil = risk
        score += 10
    
    # Geopolitical sensitivity  
    if "geopolitical_events" in data:
        score += 15  # Geopolitical events fazla = aktif piyasa
    
    # Industrial usage
    if data.get("industrial_cycles"):
        score += 5  # Endüstriyel kullanım = stabil talep
    
    return min(100, max(0, score))

if __name__ == "__main__":
    # Test
    gold_score = get_commodity_corporate_score("GC=F")
    oil_score = get_commodity_corporate_score("CL=F")
    
    print(f"Gold Corporate Score: {gold_score}")
    print(f"Oil Corporate Score: {oil_score}")