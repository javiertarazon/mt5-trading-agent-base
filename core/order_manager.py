"""
Order Manager - Gestión de órdenes de trading
"""
import MetaTrader5 as mt5
import logging
from typing import Optional, Dict
from enum import Enum

logger = logging.getLogger(__name__)


class OrderType(Enum):
    """Tipos de orden"""
    BUY = mt5.ORDER_TYPE_BUY
    SELL = mt5.ORDER_TYPE_SELL
    BUY_LIMIT = mt5.ORDER_TYPE_BUY_LIMIT
    SELL_LIMIT = mt5.ORDER_TYPE_SELL_LIMIT
    BUY_STOP = mt5.ORDER_TYPE_BUY_STOP
    SELL_STOP = mt5.ORDER_TYPE_SELL_STOP


class OrderManager:
    """Gestiona la creación y modificación de órdenes"""

    def __init__(self, mt5_connector):
        self.connector = mt5_connector
        self.magic_number = 123456

    def send_market_order(
        self,
        symbol: str,
        order_type: OrderType,
        volume: float,
        sl: float = 0.0,
        tp: float = 0.0,
        comment: str = ""
    ) -> Optional[Dict]:
        """
        Envía una orden de mercado

        Args:
            symbol: Símbolo a operar
            order_type: Tipo de orden (BUY/SELL)
            volume: Tamaño del lote
            sl: Stop Loss
            tp: Take Profit
            comment: Comentario

        Returns:
            Resultado de la orden o None si falla
        """
        if not self.connector.connected:
            logger.error("No conectado a MT5")
            return None

        symbol_info = self.connector.get_symbol_info(symbol)
        if not symbol_info:
            return None

        price = symbol_info['ask'] if order_type == OrderType.BUY else symbol_info['bid']

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type.value,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": self.magic_number,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"❌ Error enviando orden: {result.comment}")
            return None

        logger.info(f"✅ Orden ejecutada - Ticket: {result.order}, Precio: {result.price}")
        return {
            'ticket': result.order,
            'volume': result.volume,
            'price': result.price,
            'comment': result.comment
        }

    def close_position(self, ticket: int) -> bool:
        """
        Cierra una posición por ticket

        Args:
            ticket: Número de ticket de la posición

        Returns:
            True si cerró exitosamente
        """
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"Posición {ticket} no encontrada")
            return False

        position = position[0]

        # Determinar tipo de orden de cierre opuesta
        close_type = mt5.ORDER_TYPE_SELL if position.type == 0 else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(position.symbol).bid if close_type == mt5.ORDER_TYPE_SELL else mt5.symbol_info_tick(position.symbol).ask

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": self.magic_number,
            "comment": "Cerrar posición",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"❌ Error cerrando posición: {result.comment}")
            return False

        logger.info(f"✅ Posición {ticket} cerrada")
        return True

    def modify_position(self, ticket: int, new_sl: float = 0.0, new_tp: float = 0.0) -> bool:
        """
        Modifica SL/TP de una posición

        Args:
            ticket: Número de ticket
            new_sl: Nuevo Stop Loss
            new_tp: Nuevo Take Profit

        Returns:
            True si modificó exitosamente
        """
        position = mt5.positions_get(ticket=ticket)
        if not position:
            return False

        position = position[0]

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": position.symbol,
            "position": ticket,
            "sl": new_sl,
            "tp": new_tp,
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Error modificando posición: {result.comment}")
            return False

        logger.info(f"✅ Posición {ticket} modificada - SL: {new_sl}, TP: {new_tp}")
        return True
