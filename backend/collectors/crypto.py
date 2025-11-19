import requests
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from ..models import CryptoMetric

logger = logging.getLogger(__name__)

class CryptoCollector:
    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        # CoinGecko API no requiere API key para uso básico
        pass

    def collect_crypto(self, db: Session, crypto_ids: list = None) -> list[CryptoMetric]:

        if crypto_ids is None:
            # Solo las 6 más importantes por market cap
            crypto_ids = ["bitcoin", "ethereum", "cardano", "solana", "binancecoin", "ripple"]

        # Limitar a máximo 6 criptos
        crypto_ids = crypto_ids[:6]

        metrics = []

        try:
            # CoinGecko permite múltiples IDs en una sola petición
            ids_str = ",".join(crypto_ids)
            url = f"{self.BASE_URL}/coins/markets"

            params = {
                "vs_currency": "usd",
                "ids": ids_str,
                "order": "market_cap_desc",
                "per_page": len(crypto_ids),
                "page": 1,
                "sparkline": False,
                "locale": "en"
            }

            logger.info(f"Colectando datos de criptomonedas: {crypto_ids}")
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()

            for coin in data:
                crypto_metric = CryptoMetric(
                    date=datetime.utcnow(),
                    symbol=coin.get("symbol", "").upper(),
                    name=coin.get("name", ""),
                    current_price=coin.get("current_price", 0),
                    market_cap=coin.get("market_cap", 0),
                    market_cap_rank=coin.get("market_cap_rank", 0),
                    total_volume=coin.get("total_volume", 0),
                    high_24h=coin.get("high_24h", 0),
                    low_24h=coin.get("low_24h", 0),
                    price_change_24h=coin.get("price_change_24h", 0),
                    price_change_percentage_24h=coin.get("price_change_percentage_24h", 0),
                    circulating_supply=coin.get("circulating_supply", 0),
                    total_supply=coin.get("total_supply", 0)
                )

                db.add(crypto_metric)
                metrics.append(crypto_metric)

            db.commit()

            for metric in metrics:
                db.refresh(metric)

            logger.info(f"Datos de {len(metrics)} criptomonedas guardados exitosamente")
            return metrics

        except requests.exceptions.RequestException as e:
            logger.error(f"Error al colectar datos de criptomonedas: {str(e)}")
            db.rollback()
            raise
        except Exception as e:
            logger.error(f"Error inesperado: {str(e)}")
            db.rollback()
            raise

    def collect_top_cryptos(self, db: Session, limit: int = 6) -> list[CryptoMetric]:
        """
        Colecta las top N criptomonedas por market cap
        """
        try:
            url = f"{self.BASE_URL}/coins/markets"

            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": limit,
                "page": 1,
                "sparkline": False,
                "locale": "en"
            }

            logger.info(f"Colectando top {limit} criptomonedas")
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()

            data = response.json()
            metrics = []

            for coin in data:
                crypto_metric = CryptoMetric(
                    date=datetime.utcnow(),
                    symbol=coin.get("symbol", "").upper(),
                    name=coin.get("name", ""),
                    current_price=coin.get("current_price", 0),
                    market_cap=coin.get("market_cap", 0),
                    market_cap_rank=coin.get("market_cap_rank", 0),
                    total_volume=coin.get("total_volume", 0),
                    high_24h=coin.get("high_24h", 0),
                    low_24h=coin.get("low_24h", 0),
                    price_change_24h=coin.get("price_change_24h", 0),
                    price_change_percentage_24h=coin.get("price_change_percentage_24h", 0),
                    circulating_supply=coin.get("circulating_supply", 0),
                    total_supply=coin.get("total_supply", 0)
                )

                db.add(crypto_metric)
                metrics.append(crypto_metric)

            db.commit()

            for metric in metrics:
                db.refresh(metric)

            logger.info(f"Top {len(metrics)} criptomonedas guardadas exitosamente")
            return metrics

        except Exception as e:
            logger.error(f"Error al colectar top criptomonedas: {str(e)}")
            db.rollback()
            raise
