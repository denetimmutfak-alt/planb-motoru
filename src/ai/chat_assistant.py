"""
PlanB Motoru - AI Chat Assistant
Kullanıcıya kendi verileri üzerinde soru sorma imkanı
"""
import json
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from src.utils.logger import log_info, log_error, log_debug
from src.portfolio.portfolio_manager import portfolio_manager
from src.analysis.financial_analysis import FinancialAnalyzer
from src.visualization.heatmap_generator import heatmap_generator
from src.visualization.sentiment_gauge import sentiment_gauge

class AIChatAssistant:
    """AI Chat Assistant - Kullanıcı sorularını yanıtlama"""
    
    def __init__(self):
        self.financial_analyzer = FinancialAnalyzer()
        self.portfolio_manager = portfolio_manager
        self.heatmap_generator = heatmap_generator
        self.sentiment_gauge = sentiment_gauge
        
        # Soru türleri ve yanıt şablonları
        self.question_patterns = {
            'portfolio_performance': [
                r'portföy.*performans', r'portföy.*getiri', r'portföy.*kar', r'portföy.*zarar',
                r'portfolio.*performance', r'portfolio.*return', r'portfolio.*profit', r'portfolio.*loss'
            ],
            'portfolio_value': [
                r'portföy.*değer', r'portföy.*toplam', r'portföy.*bakiye',
                r'portfolio.*value', r'portfolio.*total', r'portfolio.*balance'
            ],
            'position_analysis': [
                r'pozisyon.*analiz', r'hisse.*analiz', r'sembol.*analiz',
                r'position.*analysis', r'stock.*analysis', r'symbol.*analysis'
            ],
            'risk_metrics': [
                r'risk.*metrik', r'var.*hesapla', r'drawdown', r'volatilite',
                r'risk.*metric', r'var.*calculate', r'volatility'
            ],
            'sector_analysis': [
                r'sektör.*analiz', r'sektör.*performans', r'heatmap',
                r'sector.*analysis', r'sector.*performance'
            ],
            'sentiment_analysis': [
                r'sentiment.*analiz', r'market.*sentiment', r'gauge',
                r'sentiment.*analysis', r'market.*mood'
            ],
            'technical_analysis': [
                r'teknik.*analiz', r'rsi', r'macd', r'bollinger',
                r'technical.*analysis', r'technical.*indicator'
            ],
            'prediction': [
                r'tahmin', r'öngörü', r'beklenti', r'gelecek',
                r'prediction', r'forecast', r'expectation', r'future'
            ],
            'comparison': [
                r'karşılaştır', r'kıyasla', r'vs', r'versus',
                r'compare', r'comparison'
            ],
            'recommendation': [
                r'öner', r'tavsiye', r'ne.*yapmalı', r'nasıl.*yapmalı',
                r'recommend', r'advice', r'what.*should', r'how.*should'
            ]
        }
        
        self.response_templates = {
            'portfolio_performance': self._analyze_portfolio_performance,
            'portfolio_value': self._analyze_portfolio_value,
            'position_analysis': self._analyze_position,
            'risk_metrics': self._analyze_risk_metrics,
            'sector_analysis': self._analyze_sector,
            'sentiment_analysis': self._analyze_sentiment,
            'technical_analysis': self._analyze_technical,
            'prediction': self._analyze_prediction,
            'comparison': self._analyze_comparison,
            'recommendation': self._provide_recommendation
        }
    
    def process_question(self, question: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Kullanıcı sorusunu işle ve yanıtla"""
        try:
            # Soruyu temizle ve normalize et
            clean_question = self._clean_question(question)
            
            # Soru türünü belirle
            question_type = self._classify_question(clean_question)
            
            # Sembolleri çıkar
            symbols = self._extract_symbols(clean_question)
            
            # Yanıt oluştur
            response = self._generate_response(question_type, clean_question, symbols, user_context)
            
            return {
                'question': question,
                'clean_question': clean_question,
                'question_type': question_type,
                'extracted_symbols': symbols,
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'confidence': self._calculate_confidence(question_type, symbols)
            }
            
        except Exception as e:
            log_error(f"Chat assistant soru işleme hatası: {e}")
            return {
                'question': question,
                'error': str(e),
                'response': "Üzgünüm, sorunuzu anlayamadım. Lütfen daha açık bir şekilde sorun.",
                'timestamp': datetime.now().isoformat()
            }
    
    def _clean_question(self, question: str) -> str:
        """Soruyu temizle"""
        try:
            # Küçük harfe çevir
            clean = question.lower()
            
            # Türkçe karakterleri normalize et
            replacements = {
                'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u'
            }
            
            for tr_char, en_char in replacements.items():
                clean = clean.replace(tr_char, en_char)
            
            # Gereksiz karakterleri temizle
            clean = re.sub(r'[^\w\s]', ' ', clean)
            clean = re.sub(r'\s+', ' ', clean).strip()
            
            return clean
            
        except Exception as e:
            return question.lower()
    
    def _classify_question(self, question: str) -> str:
        """Soru türünü sınıflandır"""
        try:
            best_match = None
            best_score = 0
            
            for question_type, patterns in self.question_patterns.items():
                score = 0
                for pattern in patterns:
                    if re.search(pattern, question):
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_match = question_type
            
            return best_match if best_match else 'general'
            
        except Exception as e:
            return 'general'
    
    def _extract_symbols(self, question: str) -> List[str]:
        """Soru içinden sembolleri çıkar"""
        try:
            symbols = []
            
            # BIST sembolleri
            bist_pattern = r'\b[A-Z]{3,5}\.IS\b'
            symbols.extend(re.findall(bist_pattern, question.upper()))
            
            # NASDAQ sembolleri
            nasdaq_pattern = r'\b[A-Z]{1,5}\b'
            nasdaq_matches = re.findall(nasdaq_pattern, question.upper())
            
            # Yaygın hisse sembolleri
            common_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'BTC', 'ETH']
            for match in nasdaq_matches:
                if match in common_stocks:
                    symbols.append(match)
            
            # Kripto sembolleri
            crypto_pattern = r'\b(BTC|ETH|ADA|DOT|SOL|AVAX|MATIC|ATOM)\b'
            symbols.extend(re.findall(crypto_pattern, question.upper()))
            
            return list(set(symbols))  # Duplikatları kaldır
            
        except Exception as e:
            return []
    
    def _generate_response(self, question_type: str, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Yanıt oluştur"""
        try:
            if question_type in self.response_templates:
                response_func = self.response_templates[question_type]
                return response_func(question, symbols, user_context)
            else:
                return self._generate_general_response(question, symbols, user_context)
                
        except Exception as e:
            log_error(f"Yanıt oluşturma hatası: {e}")
            return "Üzgünüm, bu soruya yanıt veremiyorum. Lütfen farklı bir şekilde sorun."
    
    def _analyze_portfolio_performance(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Portföy performans analizi"""
        try:
            portfolios = self.portfolio_manager.get_all_portfolios()
            
            if not portfolios:
                return "Henüz portföyünüz bulunmuyor. Önce bir portföy oluşturun."
            
            response_parts = []
            
            for portfolio_name in portfolios:
                portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
                if portfolio:
                    # Portföy değeri hesapla
                    total_value = portfolio.cash
                    for symbol, position in portfolio.positions.items():
                        total_value += position['quantity'] * position['current_price']
                    
                    # Performans hesapla
                    initial_value = portfolio.initial_capital
                    performance_pct = ((total_value - initial_value) / initial_value * 100) if initial_value > 0 else 0
                    
                    response_parts.append(
                        f"**{portfolio_name} Portföyü:**\n"
                        f"• Toplam Değer: {total_value:,.2f} TL\n"
                        f"• Başlangıç: {initial_value:,.2f} TL\n"
                        f"• Performans: %{performance_pct:.2f}\n"
                        f"• Nakit: {portfolio.cash:,.2f} TL\n"
                        f"• Pozisyon Sayısı: {len(portfolio.positions)}"
                    )
            
            return "\n\n".join(response_parts) if response_parts else "Portföy performansı hesaplanamadı."
            
        except Exception as e:
            return f"Portföy performans analizi hatası: {str(e)}"
    
    def _analyze_portfolio_value(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Portföy değer analizi"""
        try:
            portfolios = self.portfolio_manager.get_all_portfolios()
            
            if not portfolios:
                return "Henüz portföyünüz bulunmuyor."
            
            total_portfolio_value = 0
            portfolio_details = []
            
            for portfolio_name in portfolios:
                portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
                if portfolio:
                    portfolio_value = portfolio.cash
                    for symbol, position in portfolio.positions.items():
                        portfolio_value += position['quantity'] * position['current_price']
                    
                    total_portfolio_value += portfolio_value
                    portfolio_details.append(f"• {portfolio_name}: {portfolio_value:,.2f} TL")
            
            response = f"**Toplam Portföy Değeri: {total_portfolio_value:,.2f} TL**\n\n"
            response += "Portföy Detayları:\n" + "\n".join(portfolio_details)
            
            return response
            
        except Exception as e:
            return f"Portföy değer analizi hatası: {str(e)}"
    
    def _analyze_position(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Pozisyon analizi"""
        try:
            if not symbols:
                return "Hangi hisse için analiz yapmak istiyorsunuz? Sembol belirtin (örn: AAPL, BTC)."
            
            symbol = symbols[0]
            response_parts = []
            
            # Portföydeki pozisyonu bul
            portfolios = self.portfolio_manager.get_all_portfolios()
            position_found = False
            
            for portfolio_name in portfolios:
                portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
                if portfolio and symbol in portfolio.positions:
                    position = portfolio.positions[symbol]
                    position_found = True
                    
                    # Pozisyon detayları
                    quantity = position['quantity']
                    current_price = position['current_price']
                    avg_price = position['avg_price']
                    total_value = quantity * current_price
                    pnl = (current_price - avg_price) * quantity
                    pnl_pct = ((current_price - avg_price) / avg_price * 100) if avg_price > 0 else 0
                    
                    response_parts.append(
                        f"**{symbol} Pozisyonu ({portfolio_name}):**\n"
                        f"• Miktar: {quantity:.2f}\n"
                        f"• Güncel Fiyat: {current_price:.2f}\n"
                        f"• Ortalama Fiyat: {avg_price:.2f}\n"
                        f"• Toplam Değer: {total_value:,.2f} TL\n"
                        f"• Kar/Zarar: {pnl:,.2f} TL (%{pnl_pct:.2f})"
                    )
            
            if not position_found:
                response_parts.append(f"{symbol} için portföyünüzde pozisyon bulunamadı.")
            
            return "\n\n".join(response_parts)
            
        except Exception as e:
            return f"Pozisyon analizi hatası: {str(e)}"
    
    def _analyze_risk_metrics(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Risk metrikleri analizi"""
        try:
            portfolios = self.portfolio_manager.get_all_portfolios()
            
            if not portfolios:
                return "Risk analizi için portföy bulunamadı."
            
            response_parts = []
            
            for portfolio_name in portfolios:
                portfolio = self.portfolio_manager.get_portfolio(portfolio_name)
                if portfolio and portfolio.positions:
                    # Basit risk metrikleri
                    total_value = portfolio.cash
                    position_values = []
                    
                    for symbol, position in portfolio.positions.items():
                        position_value = position['quantity'] * position['current_price']
                        total_value += position_value
                        position_values.append(position_value)
                    
                    # Konsantrasyon riski
                    if position_values:
                        max_position = max(position_values)
                        concentration_risk = (max_position / total_value * 100) if total_value > 0 else 0
                        
                        response_parts.append(
                            f"**{portfolio_name} Risk Metrikleri:**\n"
                            f"• Toplam Değer: {total_value:,.2f} TL\n"
                            f"• Pozisyon Sayısı: {len(portfolio.positions)}\n"
                            f"• En Büyük Pozisyon: %{concentration_risk:.1f}\n"
                            f"• Nakit Oranı: %{(portfolio.cash / total_value * 100):.1f}"
                        )
            
            return "\n\n".join(response_parts) if response_parts else "Risk metrikleri hesaplanamadı."
            
        except Exception as e:
            return f"Risk analizi hatası: {str(e)}"
    
    def _analyze_sector(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Sektör analizi"""
        try:
            # Simüle edilmiş sektör verileri
            sector_data = {
                'Technology': {'return': 5.2, 'volatility': 2.1, 'volume': 1.5},
                'Finance': {'return': 3.8, 'volatility': 1.8, 'volume': 1.2},
                'Healthcare': {'return': 4.1, 'volatility': 1.9, 'volume': 1.3},
                'Energy': {'return': 2.3, 'volatility': 2.5, 'volume': 1.8},
                'Consumer': {'return': 3.5, 'volatility': 1.6, 'volume': 1.1}
            }
            
            response_parts = ["**Sektör Performans Analizi:**\n"]
            
            for sector, data in sector_data.items():
                response_parts.append(
                    f"• **{sector}:**\n"
                    f"  - Getiri: %{data['return']:.1f}\n"
                    f"  - Volatilite: %{data['volatility']:.1f}\n"
                    f"  - Hacim Oranı: {data['volume']:.1f}x"
                )
            
            # En iyi ve en kötü sektörler
            best_sector = max(sector_data.items(), key=lambda x: x[1]['return'])
            worst_sector = min(sector_data.items(), key=lambda x: x[1]['return'])
            
            response_parts.append(
                f"\n**Öne Çıkanlar:**\n"
                f"• En İyi Performans: {best_sector[0]} (%{best_sector[1]['return']:.1f})\n"
                f"• En Düşük Performans: {worst_sector[0]} (%{worst_sector[1]['return']:.1f})"
            )
            
            return "\n".join(response_parts)
            
        except Exception as e:
            return f"Sektör analizi hatası: {str(e)}"
    
    def _analyze_sentiment(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Sentiment analizi"""
        try:
            if symbols:
                symbol = symbols[0]
                # Simüle edilmiş sentiment verileri
                sentiment_data = {
                    'overall_score': 65,
                    'twitter_score': 70,
                    'news_score': 60,
                    'reddit_score': 65,
                    'confidence': 0.75
                }
                
                return (
                    f"**{symbol} Sentiment Analizi:**\n"
                    f"• Genel Skor: {sentiment_data['overall_score']}/100\n"
                    f"• Twitter: {sentiment_data['twitter_score']}/100\n"
                    f"• Haberler: {sentiment_data['news_score']}/100\n"
                    f"• Reddit: {sentiment_data['reddit_score']}/100\n"
                    f"• Güven: %{sentiment_data['confidence']*100:.0f}\n"
                    f"• Durum: {'Pozitif' if sentiment_data['overall_score'] > 60 else 'Negatif' if sentiment_data['overall_score'] < 40 else 'Nötr'}"
                )
            else:
                return (
                    "**Genel Market Sentiment:**\n"
                    "• Genel Skor: 58/100\n"
                    "• Twitter: 62/100\n"
                    "• Haberler: 55/100\n"
                    "• Reddit: 57/100\n"
                    "• Durum: Nötr-Pozitif"
                )
            
        except Exception as e:
            return f"Sentiment analizi hatası: {str(e)}"
    
    def _analyze_technical(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Teknik analiz"""
        try:
            if not symbols:
                return "Teknik analiz için sembol belirtin (örn: AAPL, BTC)."
            
            symbol = symbols[0]
            
            # Simüle edilmiş teknik veriler
            technical_data = {
                'rsi': 45,
                'macd_signal': 'bullish',
                'sma_20': 150.5,
                'sma_50': 148.2,
                'current_price': 152.3,
                'bollinger_position': 'middle'
            }
            
            return (
                f"**{symbol} Teknik Analiz:**\n"
                f"• RSI: {technical_data['rsi']} ({'Aşırı satım' if technical_data['rsi'] < 30 else 'Aşırı alım' if technical_data['rsi'] > 70 else 'Nötr'})\n"
                f"• MACD: {technical_data['macd_signal'].title()}\n"
                f"• SMA 20: {technical_data['sma_20']:.2f}\n"
                f"• SMA 50: {technical_data['sma_50']:.2f}\n"
                f"• Güncel Fiyat: {technical_data['current_price']:.2f}\n"
                f"• Bollinger: {technical_data['bollinger_position'].title()}\n"
                f"• Trend: {'Yükseliş' if technical_data['current_price'] > technical_data['sma_20'] > technical_data['sma_50'] else 'Düşüş' if technical_data['current_price'] < technical_data['sma_20'] < technical_data['sma_50'] else 'Yatay'}"
            )
            
        except Exception as e:
            return f"Teknik analiz hatası: {str(e)}"
    
    def _analyze_prediction(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Tahmin analizi"""
        try:
            if not symbols:
                return "Tahmin için sembol belirtin (örn: AAPL, BTC)."
            
            symbol = symbols[0]
            
            # Simüle edilmiş tahmin verileri
            prediction_data = {
                'predicted_price': 158.5,
                'current_price': 152.3,
                'confidence': 0.72,
                'timeframe': '1 hafta',
                'direction': 'bullish'
            }
            
            price_change = ((prediction_data['predicted_price'] - prediction_data['current_price']) / prediction_data['current_price'] * 100)
            
            return (
                f"**{symbol} Tahmin Analizi:**\n"
                f"• Güncel Fiyat: {prediction_data['current_price']:.2f}\n"
                f"• Tahmin Edilen: {prediction_data['predicted_price']:.2f}\n"
                f"• Beklenen Değişim: %{price_change:.1f}\n"
                f"• Yön: {prediction_data['direction'].title()}\n"
                f"• Zaman Dilimi: {prediction_data['timeframe']}\n"
                f"• Güven: %{prediction_data['confidence']*100:.0f}\n"
                f"• Öneri: {'Alım' if price_change > 2 else 'Satım' if price_change < -2 else 'Bekle'}"
            )
            
        except Exception as e:
            return f"Tahmin analizi hatası: {str(e)}"
    
    def _analyze_comparison(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Karşılaştırma analizi"""
        try:
            if len(symbols) < 2:
                return "Karşılaştırma için en az 2 sembol belirtin (örn: AAPL vs MSFT)."
            
            symbol1, symbol2 = symbols[0], symbols[1]
            
            # Simüle edilmiş karşılaştırma verileri
            comparison_data = {
                symbol1: {'price': 152.3, 'change': 2.1, 'volume': 1.5},
                symbol2: {'price': 245.8, 'change': -1.2, 'volume': 1.2}
            }
            
            return (
                f"**{symbol1} vs {symbol2} Karşılaştırması:**\n\n"
                f"**{symbol1}:**\n"
                f"• Fiyat: {comparison_data[symbol1]['price']:.2f}\n"
                f"• Değişim: %{comparison_data[symbol1]['change']:.1f}\n"
                f"• Hacim: {comparison_data[symbol1]['volume']:.1f}x\n\n"
                f"**{symbol2}:**\n"
                f"• Fiyat: {comparison_data[symbol2]['price']:.2f}\n"
                f"• Değişim: %{comparison_data[symbol2]['change']:.1f}\n"
                f"• Hacim: {comparison_data[symbol2]['volume']:.1f}x\n\n"
                f"**Sonuç:**\n"
                f"• Daha İyi Performans: {symbol1 if comparison_data[symbol1]['change'] > comparison_data[symbol2]['change'] else symbol2}\n"
                f"• Daha Yüksek Hacim: {symbol1 if comparison_data[symbol1]['volume'] > comparison_data[symbol2]['volume'] else symbol2}"
            )
            
        except Exception as e:
            return f"Karşılaştırma analizi hatası: {str(e)}"
    
    def _provide_recommendation(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Öneri sağla"""
        try:
            if not symbols:
                return (
                    "**Genel Öneriler:**\n"
                    "• Portföyünüzü çeşitlendirin\n"
                    "• Risk yönetimi uygulayın\n"
                    "• Düzenli analiz yapın\n"
                    "• Duygusal kararlar vermeyin\n"
                    "• Uzun vadeli düşünün"
                )
            
            symbol = symbols[0]
            
            # Simüle edilmiş öneri verileri
            recommendation_data = {
                'action': 'HOLD',
                'reason': 'Teknik göstergeler karışık sinyal veriyor',
                'target_price': 160.0,
                'stop_loss': 145.0,
                'confidence': 0.65
            }
            
            return (
                f"**{symbol} Önerisi:**\n"
                f"• Aksiyon: {recommendation_data['action']}\n"
                f"• Sebep: {recommendation_data['reason']}\n"
                f"• Hedef Fiyat: {recommendation_data['target_price']:.2f}\n"
                f"• Stop Loss: {recommendation_data['stop_loss']:.2f}\n"
                f"• Güven: %{recommendation_data['confidence']*100:.0f}\n\n"
                f"**Risk Uyarısı:** Bu öneri sadece bilgilendirme amaçlıdır. Yatırım kararlarınızı kendi araştırmanıza dayandırın."
            )
            
        except Exception as e:
            return f"Öneri oluşturma hatası: {str(e)}"
    
    def _generate_general_response(self, question: str, symbols: List[str], user_context: Dict[str, Any]) -> str:
        """Genel yanıt oluştur"""
        try:
            return (
                "Merhaba! PlanB Motoru AI Asistanıyım. Size şu konularda yardımcı olabilirim:\n\n"
                "• **Portföy Analizi:** 'Portföyümün performansı nasıl?'\n"
                "• **Hisse Analizi:** 'AAPL analizi yap'\n"
                "• **Risk Metrikleri:** 'Risk analizi yap'\n"
                "• **Sektör Analizi:** 'Teknoloji sektörü nasıl?'\n"
                "• **Sentiment:** 'BTC sentiment analizi'\n"
                "• **Teknik Analiz:** 'AAPL teknik analiz'\n"
                "• **Tahmin:** 'MSFT tahmini'\n"
                "• **Karşılaştırma:** 'AAPL vs MSFT'\n"
                "• **Öneriler:** 'Ne yapmalıyım?'\n\n"
                "Hangi konuda yardım istiyorsunuz?"
            )
            
        except Exception as e:
            return "Merhaba! Size nasıl yardımcı olabilirim?"
    
    def _calculate_confidence(self, question_type: str, symbols: List[str]) -> float:
        """Güven seviyesini hesapla"""
        try:
            confidence = 0.5  # Başlangıç güveni
            
            # Soru türü güveni
            if question_type != 'general':
                confidence += 0.3
            
            # Sembol varlığı güveni
            if symbols:
                confidence += 0.2
            
            return min(1.0, confidence)
            
        except Exception as e:
            return 0.5
    
    def get_conversation_history(self, user_id: str = 'default') -> List[Dict[str, Any]]:
        """Konuşma geçmişini getir"""
        try:
            # Basit in-memory geçmiş (gerçek uygulamada veritabanı kullanılmalı)
            if not hasattr(self, 'conversation_history'):
                self.conversation_history = {}
            
            return self.conversation_history.get(user_id, [])
            
        except Exception as e:
            return []
    
    def save_conversation(self, user_id: str, question: str, response: Dict[str, Any]):
        """Konuşmayı kaydet"""
        try:
            if not hasattr(self, 'conversation_history'):
                self.conversation_history = {}
            
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Son 50 konuşmayı tut
            self.conversation_history[user_id].append({
                'question': question,
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
            
            if len(self.conversation_history[user_id]) > 50:
                self.conversation_history[user_id] = self.conversation_history[user_id][-50:]
            
        except Exception as e:
            log_error(f"Konuşma kaydetme hatası: {e}")

# Global AI chat assistant instance
ai_chat_assistant = AIChatAssistant()

