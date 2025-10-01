#!/usr/bin/env python3
"""
🧹 BIST LİSTE TEMİZLEYİCİ
========================
3 farklı formatı temizleyip tek düzen yapar:
- TAB ayrılmış satırları korur
- Çok satırlı bozuk formatı düzeltir  
- Markdown formatını temizler
- Sadece .IS ile biten sembolleri alır
"""

def clean_bist_list():
    """BIST listesini temizle ve düzenle"""
    
    # Orijinal dosyayı oku
    with open("bist liste-kuruluş tarihli-kodlu TAM LİSTE.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    cleaned_data = []
    temp_entry = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Markdown formatını atla
        if line.startswith("|") or line.startswith("┌") or line.startswith("├") or line.startswith("└"):
            continue
            
        # TAB ayrılmış format (doğru format)
        if "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3 and parts[0].strip().endswith(".IS"):
                symbol = parts[0].strip()
                company = parts[1].strip()
                date = parts[2].strip()
                cleaned_data.append(f"{symbol}\t{company}\t{date}")
                
        # Tek satırda .IS ile bitiyor (çok satırlı formatın ilk parçası)
        elif line.endswith(".IS"):
            temp_entry = {"symbol": line}
            
        # Şirket adı (çok satırlı formatın ikinci parçası)
        elif temp_entry.get("symbol") and not temp_entry.get("company"):
            temp_entry["company"] = line
            
        # Tarih (çok satırlı formatın üçüncü parçası)
        elif temp_entry.get("symbol") and temp_entry.get("company") and not temp_entry.get("date"):
            # Tarih formatı kontrolü
            if any(char.isdigit() for char in line) and ("." in line or "/" in line):
                temp_entry["date"] = line
                # Tamam, ekle
                cleaned_data.append(f"{temp_entry['symbol']}\t{temp_entry['company']}\t{temp_entry['date']}")
                temp_entry = {}
    
    # Tekrarları kaldır ve sırala
    cleaned_data = sorted(list(set(cleaned_data)))
    
    # Temizlenmiş dosyayı yaz
    with open("bist_liste_TEMIZ.txt", "w", encoding="utf-8") as f:
        for line in cleaned_data:
            f.write(line + "\n")
    
    print(f"✅ BIST liste temizlendi!")
    print(f"📊 Orijinal satır sayısı: {len(lines)}")
    print(f"📊 Temizlenmiş hisse sayısı: {len(cleaned_data)}")
    print(f"📁 Yeni dosya: bist_liste_TEMIZ.txt")
    
    # İlk 10 satırı göster
    print("\n🔍 İLK 10 SATIR ÖRNEĞİ:")
    for i, line in enumerate(cleaned_data[:10]):
        print(f"{i+1:2d}. {line}")
    
    return len(cleaned_data)

if __name__ == "__main__":
    clean_count = clean_bist_list()
    print(f"\n🎯 SONUÇ: {clean_count} adet temiz BIST hissesi hazır!")