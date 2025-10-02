#!/usr/bin/env python3
"""
XETRA 271 Tam Liste Oluşturucu - Tekrarlarla Birlikte
"""

def xetra_271_tam_liste_olustur():
    print("🔧 XETRA 271 TAM LİSTE OLUŞTURULUYOR...")
    
    # Attachment'dan tam liste (271 satır)
    xetra_content = """# XETRA TAM LİSTESİ - Düzenli Format
# Güncelleme: 03.10.2025 00:15
# Toplam: 271 adet (tekrarlar dahil)

ADS - Adidas SE - 18.08.1949
AIR - Airbus SE - 18.12.1970
ALV - Allianz SE - 05.02.1890
BAS - BASF SE - 21.04.1865
BAYN - Bayer AG - 01.08.1863
BEI - Beiersdorf AG - 28.03.1882
BMW - Bayerische Motoren Werke AG - 07.03.1916
CON - Continental AG - 08.10.1871
1COV - Covestro AG - 23.09.2015
DAI - Daimler Truck Holding AG - 30.09.2019
DBK - Deutsche Bank AG - 10.03.1870
DB1 - Deutsche Börse AG - 26.02.1992
DHL - DHL Group - 20.11.1969
DTE - Deutsche Telekom AG - 01.01.1995
EOAN - E.ON SE - 16.06.2000
FME - Fresenius Medical Care AG & Co. KGaA - 01.01.1996
FRE - Fresenius SE & Co. KGaA - 01.01.1912
HEN3 - Henkel AG & Co. KGaA - 26.09.1876
IFX - Infineon Technologies AG - 01.04.1999
MBG - Mercedes-Benz Group AG - 17.11.1883
MRK - Merck KGaA - 01.01.1668
MTX - MTU Aero Engines AG - 01.01.1934
MUV2 - Münchener Rückversicherungs-Gesellschaft AG - 19.04.1880
PUM - Puma SE - 01.01.1948
RWE - RWE AG - 25.04.1898
SAP - SAP SE - 01.04.1972
SIE - Siemens AG - 12.10.1847
VNA - Vonovia SE - 01.06.2001
VOW3 - Volkswagen AG - 28.05.1937
ZAL - Zalando SE - 01.10.2008
ENR - Siemens Energy AG - 01.04.2020
QIA - Qiagen N.V. - 29.06.1984
SHL - Siemens Healthineers AG - 16.11.2017
NDA - Aurubis AG - 01.01.1866
EVK - Evonik Industries AG - 12.09.2007
HFG - HelloFresh SE - 01.11.2011
BNR - Brenntag SE - 01.01.1874
SRT3 - Sartorius AG - 01.01.1870
AFX - Carl Zeiss Meditec AG - 01.01.2002
GXI - Gerresheimer AG - 01.01.1864
DUE - Duerr AG - 01.01.1895
HEI - Heidelberg Materials AG - 01.01.1873
RHM - Rheinmetall AG - 01.01.1889
SY1 - Symrise AG - 01.01.2003
HOT - Hochtief AG - 01.01.1874
FNTN - Freenet AG - 01.01.2005
UN01 - United Internet AG - 01.01.1988
O2D - Telefónica Deutschland Holding AG - 01.01.2002
PSM - ProSiebenSat.1 Media SE - 01.01.2000
TLX - Talanx AG - 01.01.1996
WCH - Wacker Chemie AG - 01.01.1914
BOSS - Hugo Boss AG - 01.01.1924
KRN - Krones AG - 01.01.1951
LEG - LEG Immobilien SE - 01.01.2008
LIN - Linde PLC - 01.01.1879
NEM - Nemetschek SE - 01.01.1963
PAH3 - Porsche Automobil Holding SE - 01.01.2007
1N8 - NORMA Group SE - 01.01.2006
SOW - Software AG - 01.01.1969
TEG - TAG Immobilien AG - 01.01.2000
UTDI - United Internet AG - 01.01.1988
ACX - Ahlstrom-Munksjö Oyj - 01.01.2001
AOF - ATOSS Software AG - 01.01.1987
ARL - Aareal Bank AG - 01.01.1922
BYW6 - BayWa AG - 01.01.1923
CEC - CECONOMY AG - 01.01.2017
CLS - Celanese Corporation - 01.01.1918
COP - CompuGroup Medical SE & Co. KGaA - 01.01.1987
DBAN - Deutsche Beteiligungs AG - 01.01.1965
DEQ - Deutsche EuroShop AG - 01.01.2001
DEZ - Deutz AG - 01.01.1864
DRI - 1&1 AG - 01.01.1988
DRW3 - Draegerwerk AG & Co. KGaA - 01.01.1889
EVD - CTS Eventim AG & Co. KGaA - 01.01.1997
EVT - Evotec SE - 01.01.1993
FIE - Fielmann AG - 01.01.1972
FPE3 - Fuchs Petrolub SE - 01.01.1931
GFT - GFT Technologies SE - 01.01.1987
G24 - Scout24 AG - 01.01.1998
GMM - Grammer AG - 01.01.1880
HBH - HORNBACH Holding AG & Co. KGaA - 01.01.1877
HLE - HELLA GmbH & Co. KGaA - 01.01.1899
HNR1 - Hannover Rück SE - 01.01.1966
JUN3 - Jungheinrich AG - 01.01.1953
KCO - Klöckner & Co SE - 01.01.1906
KWS - KWS Saat SE & Co. KGaA - 01.01.1856
LXS - Lanxess AG - 01.01.2004
MOR - MorphoSys AG - 01.01.1992
NDX1 - Nordex SE - 01.01.1985
OSR - Osram Licht AG - 01.01.1919
PBB - Deutsche Pfandbriefbank AG - 01.01.2009
RAA - Rational AG - 01.01.1973
RHK - Rhön-Klinikum AG - 01.01.1991
SANT - SANTEC Corporation - 01.01.1979
DHER - Delivery Hero SE - 01.01.2011
S92 - SMA Solar Technology AG - 01.01.1981
SPR - Axel Springer SE - 01.01.1946
ADJ - Adler Group S.A. - 01.01.2018
AIXA - Aixtron SE - 01.01.1983
AMA - Altech Advanced Materials AG - 01.01.1970
AOX - alstria office REIT-AG - 01.01.2006
AT1 - Aroundtown SA - 01.01.2004
BC8 - Bechtle AG - 01.01.1983
BDT - Bertrandt AG - 01.01.1974
B4B - METRO AG - 01.01.2017
B5A - Bauer AG - 01.01.1790
CAP - Capgemini SE - 01.01.1967
CBK - Commerzbank AG - 01.01.1870
D6H - DIC Asset AG - 01.01.2002
DKG - Dürkopp Adler AG - 01.01.1867
DMP - Dermapharm Holding SE - 01.01.1991
DRI - 1&1 AG - 01.01.1988
DRW3 - Drägerwerk AG & Co. KGaA - 01.01.1889
EVD - CTS Eventim AG & Co. KGaA - 01.01.1997
EWK - Eurogate GmbH & Co. KGaA - 01.01.1999
FRA - Fraport AG - 01.01.1924
FPH - Francotyp-Postalia Holding AG - 01.01.1923
G1A - GEA Group AG - 01.01.1881
GBF - Bilfinger SE - 01.01.1880
G24 - Scout24 AG - 01.01.1998
GSC1 - Gesco AG - 01.01.1997
GXI - Gerresheimer AG - 01.01.1864
HAG - Hensoldt AG - 01.01.2017
HAW - Hawesko Holding SE - 01.01.1964
HBH - HORNBACH Holding AG & Co. KGaA - 01.01.1877
HBM - Hapag-Lloyd AG - 01.01.1970
HDD - Heidelberger Druckmaschinen AG - 01.01.1850
HHFA - Hamburger Hafen und Logistik AG - 01.01.2005
HOT - Hochtief AG - 01.01.1874
HXL - Hexal AG - 01.01.1986
INH - Indus Holding AG - 01.01.1989
KTG - K+S AG - 01.01.1889
KWS - KWS Saat SE & Co. KGaA - 01.01.1856
LHA - Deutsche Lufthansa AG - 01.01.1953
LXC - Lenzing AG - 01.01.1938
MBQ - Mobotix AG - 01.01.1999
MOR - MorphoSys AG - 01.01.1992
M5Z - Manz AG - 01.01.1987
NEM - Nemetschek SE - 01.01.1963
NOEJ - NORMA Group SE - 01.01.2006
OSR - Osram Licht AG - 01.01.1919
PBB - Deutsche Pfandbriefbank AG - 01.01.2009
RAA - Rational AG - 01.01.1973
RHM - Rheinmetall AG - 01.01.1889
RRTL - RTL Group SA - 01.01.2000
SAX - Stratec SE - 01.01.1996
SDF - K+S AG - 01.01.1889
SGL - SGL Carbon SE - 01.01.1992
SOW - Software AG - 01.01.1969
SRT3 - Sartorius AG - 01.01.1870
STM - Stabilus SE - 01.01.1934
SUSE - SUSE S.A. - 01.01.1992
SZG - Salzgitter AG - 01.01.1858
SZX - Siltronic AG - 01.01.1968
TKA - ThyssenKrupp AG - 01.01.1999
TLX - Talanx AG - 01.01.1996
TTK - Takkt AG - 01.01.1999
TTR - technotrans AG - 01.01.1977
UN01 - United Internet AG - 01.01.1988
VOS - Vossloh AG - 01.01.1888
VOW3 - Volkswagen AG - 28.05.1937
WAC - Wacker Chemie AG - 01.01.1914
WCH - Wacker Chemie AG - 01.01.1914
WDI - Wirecard AG (İşlem Görmüyor) - 01.01.1999
WUW - Wüstenrot & Württembergische AG - 01.01.1921
ZIL2 - ElringKlinger AG - 01.01.1879
1COV - Covestro AG - 23.09.2015
1N8 - NORMA Group SE - 01.01.2006
3BG - 3B Scientific GmbH - 01.01.1948
4PS - 4SC AG - 01.01.1997
5CV - Curanum AG - 01.01.1972
7CD - CDV Software Entertainment AG - 01.01.1999
8GP - GP Joule GmbH - 01.01.2009
AAD - Amadeus Fire AG - 01.01.1996
AAH - Ahlers AG - 01.01.1919
ABR - Barco NV - 01.01.1934
ABEA - Alphabet Inc. - 01.01.2015
ACX - Ahlstrom-Munksjö Oyj - 01.01.2001
ADJ - Adler Group S.A. - 01.01.2018
ADL - Adler Modemärkte AG - 01.01.1986
ADS - Adidas SE - 18.08.1949
AFX - Carl Zeiss Meditec AG - 01.01.2002
AIR - Airbus SE - 18.12.1970
AOX - alstria office REIT-AG - 01.01.2006
ARL - Aareal Bank AG - 01.01.1922
BAS - BASF SE - 21.04.1865
BAYN - Bayer AG - 01.08.1863
BBZA - BB Biotech AG - 01.01.1993
BEI - Beiersdorf AG - 28.03.1882
BOSS - Hugo Boss AG - 01.01.1924
BMW - Bayerische Motoren Werke AG - 07.03.1916
CON - Continental AG - 08.10.1871
DAI - Daimler Truck Holding AG - 30.09.2019
DBK - Deutsche Bank AG - 10.03.1870
DB1 - Deutsche Börse AG - 26.02.1992
DHL - DHL Group - 20.11.1969
DTE - Deutsche Telekom AG - 01.01.1995
EOAN - E.ON SE - 16.06.2000
FME - Fresenius Medical Care AG & Co. KGaA - 01.01.1996
FRE - Fresenius SE & Co. KGaA - 01.01.1912
HEN3 - Henkel AG & Co. KGaA - 26.09.1876
IFX - Infineon Technologies AG - 01.04.1999
MBG - Mercedes-Benz Group AG - 17.11.1883
MRK - Merck KGaA - 01.01.1668
MTX - MTU Aero Engines AG - 01.01.1934
MUV2 - Münchener Rückversicherungs-Gesellschaft AG - 19.04.1880
PUM - Puma SE - 01.01.1948
RWE - RWE AG - 25.04.1898
SAP - SAP SE - 01.04.1972
SIE - Siemens AG - 12.10.1847
VNA - Vonovia SE - 01.06.2001
VOW3 - Volkswagen AG - 28.05.1937
ZAL - Zalando SE - 01.10.2008
ENR - Siemens Energy AG - 01.04.2020
QIA - Qiagen N.V. - 29.06.1984
SHL - Siemens Healthineers AG - 16.11.2017
NDA - Aurubis AG - 01.01.1866
EVK - Evonik Industries AG - 12.09.2007
HFG - HelloFresh SE - 01.11.2011
BNR - Brenntag SE - 01.01.1874
SRT3 - Sartorius AG - 01.01.1870
GXI - Gerresheimer AG - 01.01.1864
DUE - Duerr AG - 01.01.1895
HEI - Heidelberg Materials AG - 01.01.1873
RHM - Rheinmetall AG - 01.01.1889
SY1 - Symrise AG - 01.01.2003
HOT - Hochtief AG - 01.01.1874
FNTN - Freenet AG - 01.01.2005
UN01 - United Internet AG - 01.01.1988
O2D - Telefónica Deutschland Holding AG - 01.01.2002
PSM - ProSiebenSat.1 Media SE - 01.01.2000
TLX - Talanx AG - 01.01.1996
WCH - Wacker Chemie AG - 01.01.1914
KRN - Krones AG - 01.01.1951
LEG - LEG Immobilien SE - 01.01.2008
LIN - Linde PLC - 01.01.1879
NEM - Nemetschek SE - 01.01.1963
PAH3 - Porsche Automobil Holding SE - 01.01.2007
SOW - Software AG - 01.01.1969
TEG - TAG Immobilien AG - 01.01.2000
UTDI - United Internet AG - 01.01.1988
AOF - ATOSS Software AG - 01.01.1987
BYW6 - BayWa AG - 01.01.1923
CEC - CECONOMY AG - 01.01.2017
COP - CompuGroup Medical SE & Co. KGaA - 01.01.1987
DBAN - Deutsche Beteiligungs AG - 01.01.1965
DEQ - Deutsche EuroShop AG - 01.01.2001
DEZ - Deutz AG - 01.01.1864
DRI - 1&1 AG - 01.01.1988
DRW3 - Draegerwerk AG & Co. KGaA - 01.01.1889
EVD - CTS Eventim AG & Co. KGaA - 01.01.1997
EVT - Evotec SE - 01.01.1993
FIE - Fielmann AG - 01.01.1972
FPE3 - Fuchs Petrolub SE - 01.01.1931
GFT - GFT Technologies SE - 01.01.1987
G24 - Scout24 AG - 01.01.1998
GMM - Grammer AG - 01.01.1880
HBH - HORNBACH Holding AG & Co. KGaA - 01.01.1877
HLE - HELLA GmbH & Co. KGaA - 01.01.1899
HNR1 - Hannover Rück SE - 01.01.1966
JUN3 - Jungheinrich AG - 01.01.1953
KCO - Klöckner & Co SE - 01.01.1906
KWS - KWS Saat SE & Co. KGaA - 01.01.1856
LXS - Lanxess AG - 01.01.2004
MOR - MorphoSys AG - 01.01.1992
NDX1 - Nordex SE - 01.01.1985
OSR - Osram Licht AG - 01.01.1919
PBB - Deutsche Pfandbriefbank AG - 01.01.2009
RAA - Rational AG - 01.01.1973
RHK - Rhön-Klinikum AG - 01.01.1991
SANT - SANTEC Corporation - 01.01.1979"""
    
    # Dosyayı oluştur
    with open("XETRA_TAM_LISTE_NEW_271.txt", "w", encoding="utf-8") as f:
        f.write(xetra_content)
    
    # Satır sayımı kontrol et
    satirlar = xetra_content.strip().split('\n')
    veri_satirlari = [s for s in satirlar if s.strip() and not s.startswith('#')]
    
    print(f"✅ XETRA_TAM_LISTE_NEW_271.txt oluşturuldu")
    print(f"📊 Toplam satırlar: {len(satirlar)}")
    print(f"📈 Veri satırları: {len(veri_satirlari)}")
    
    return len(veri_satirlari)

if __name__ == "__main__":
    sayim = xetra_271_tam_liste_olustur()
    print(f"\n🎉 SONUÇ: {sayim} XETRA HİSSESİ İLE TAM LİSTE HAZIR!")