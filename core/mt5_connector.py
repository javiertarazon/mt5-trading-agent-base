"""
MT5 Connector - Conexión y operaciones con MetaTrader 5
"""
import MetaTrader5 as mt5
import logging
from typing import Optional, List, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class MT5Connector:
    """Gestiona la conexión y operaciones con MT5"""

    def __init__(self):
        self.connected = False
        self.account_info = None

    def connect(self, login: int, password: str, server: str, timeout: int = 10000) -> bool:
        """
        Conecta con MT5

        Args:
            login: Número de cuenta
            password: Contraseña
            server: Servidor del broker
            timeout: Timeout en ms

        Returns:
            bool: True si conectó exitosamente
        """
        if not mt5.initialize():
            logger.error(f"Error inicializando MT5: {mt5.last_error()}")
            return False

        authorized = mt5.login(login=login, password=password, server=server, timeout=timeout)

        if authorized:
            self.connected = True
            self.account_info = mt5.account_info()
            logger.info(f"✅ Conectado a MT5 - Cuenta: {login}, Balance: {self.account_info.balance}")
            return True
        else:
            logger.error(f"❌ Error de autenticación: {mt5.last_error()}")
            return False

    def disconnect(self):
        """Desconecta de MT5"""
        mt5.shutdown()
        self.connected = False
        logger.info("Desconectado de MT5")

    def get_symbol_info(self, symbol: str) -> Optional[Dict]:
        """Obtiene información del símbolo"""
        if not self.connected:
            logger.error("No conectado a MT5")
            return None

        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Símbolo {symbol} no encontrado")
            return None

        return {
            'name': symbol_info.name,
            'bid': symbol_info.bid,
            'ask': symbol_info.ask,
            'spread': symbol_info.spread,
            'point': symbol_info.point,
            'digits': symbol_info.digits,
            'volume_min': symbol_info.volume_min,
            'volume_max': symbol_info.volume_max,
            'volume_step': symbol_info.volume_step
        }

    def get_account_balance(self) -> float:
        """Retorna el balance de la cuenta"""
        if not self.connected:
            return 0.0
        account = mt5.account_info()
        return account.balance if account else 0.0

    def get_account_equity(self) -> float:
        """Retorna el equity de la cuenta"""
        if not self.connected:
            return 0.0
        account = mt5.account_info()
        return account.equity if account else 0.0

    def get_positions(self, symbol: Optional[str] = None) -> List[Dict]:
        """
        Obtiene posiciones abiertas

        Args:
            symbol: Filtrar por símbolo (None = todas)

        Returns:
            Lista de posiciones
        """
        if not self.connected:
            return []

        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()

        if positions is None:
            return []

        return [
            {
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == 0 else 'SELL',
                'volume': pos.volume,
                'price_open': pos.price_open,
                'price_current': pos.price_current,
                'sl': pos.sl,
                'tp': pos.tp,
                'profit': pos.profit,
                'magic': pos.magic
            }
            for pos in positions
        ]

    def check_connection(self) -> bool:
        """Verifica si la conexión está activa"""
        if not self.connected:
            return False
        return mt5.account_info() is not None
