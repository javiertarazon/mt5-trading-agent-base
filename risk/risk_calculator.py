"""
Risk Calculator - Cálculo de tamaño de lotes y gestión de riesgo
"""
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class RiskCalculator:
    """Calcula tamaños de posición basados en riesgo"""

    def __init__(
        self,
        risk_per_trade: float = 0.02,
        max_drawdown: float = 0.10,
        max_daily_loss: float = 0.05
    ):
        """
        Args:
            risk_per_trade: % de balance a arriesgar por operación (0.02 = 2%)
            max_drawdown: Drawdown máximo permitido (0.10 = 10%)
            max_daily_loss: Pérdida diaria máxima (0.05 = 5%)
        """
        self.risk_per_trade = risk_per_trade
        self.max_drawdown = max_drawdown
        self.max_daily_loss = max_daily_loss
        self.daily_pnl = 0.0

    def calculate_lot_size(
        self,
        balance: float,
        entry_price: float,
        stop_loss: float,
        symbol_info: Dict,
        order_type: str = "BUY"
    ) -> float:
        """
        Calcula el tamaño de lote basado en riesgo

        Args:
            balance: Balance de cuenta
            entry_price: Precio de entrada
            stop_loss: Precio de stop loss
            symbol_info: Info del símbolo (point, volume_min, volume_step, etc)
            order_type: "BUY" o "SELL"

        Returns:
            Tamaño de lote calculado
        """
        # Calcular distancia en pips
        if order_type == "BUY":
            distance_points = abs(entry_price - stop_loss) / symbol_info['point']
        else:
            distance_points = abs(stop_loss - entry_price) / symbol_info['point']

        if distance_points == 0:
            logger.warning("Stop loss = precio entrada, usando SL mínimo")
            distance_points = 10  # SL mínimo de 10 pips

        # Calcular riesgo en dinero
        risk_amount = balance * self.risk_per_trade

        # Calcular valor por punto
        # Para Forex: 1 lote = $10 por pip (standard), 0.1 = $1 por pip
        # Esta fórmula es simplificada, ajustar según broker
        point_value = 10.0  # Valor por pip para 1 lote estándar

        # Calcular tamaño de lote
        lot_size = risk_amount / (distance_points * point_value)

        # Ajustar a límites del símbolo
        lot_size = max(symbol_info['volume_min'], lot_size)
        lot_size = min(symbol_info['volume_max'], lot_size)

        # Redondear al step del símbolo
        step = symbol_info['volume_step']
        lot_size = round(lot_size / step) * step

        logger.info(f"📊 Lot Size calculado: {lot_size} (Risk: {self.risk_per_trade*100}%, SL distance: {distance_points:.1f} pips)")
        return lot_size

    def calculate_dynamic_sl(
        self,
        entry_price: float,
        atr_value: float,
        multiplier: float = 2.0,
        order_type: str = "BUY"
    ) -> float:
        """
        Calcula Stop Loss dinámico basado en ATR

        Args:
            entry_price: Precio de entrada
            atr_value: Valor del ATR actual
            multiplier: Multiplicador del ATR (2.0 = 2x ATR)
            order_type: "BUY" o "SELL"

        Returns:
            Precio de Stop Loss
        """
        sl_distance = atr_value * multiplier

        if order_type == "BUY":
            sl_price = entry_price - sl_distance
        else:
            sl_price = entry_price + sl_distance

        return round(sl_price, 5)

    def calculate_multi_tp(
        self,
        entry_price: float,
        stop_loss: float,
        ratios: list = [1.5, 2.0, 3.0],
        order_type: str = "BUY"
    ) -> list:
        """
        Calcula múltiples niveles de Take Profit

        Args:
            entry_price: Precio de entrada
            stop_loss: Precio de stop loss
            ratios: Lista de ratios R:R (ej: [1.5, 2.0, 3.0])
            order_type: "BUY" o "SELL"

        Returns:
            Lista de precios de TP
        """
        sl_distance = abs(entry_price - stop_loss)

        tp_levels = []
        for ratio in ratios:
            if order_type == "BUY":
                tp = entry_price + (sl_distance * ratio)
            else:
                tp = entry_price - (sl_distance * ratio)
            tp_levels.append(round(tp, 5))

        return tp_levels

    def check_daily_limit(self, current_pnl: float, starting_balance: float) -> bool:
        """
        Verifica si se alcanzó el límite de pérdida diaria

        Args:
            current_pnl: PnL actual del día
            starting_balance: Balance inicial del día

        Returns:
            True si se puede seguir operando, False si se alcanzó el límite
        """
        daily_loss_pct = abs(current_pnl) / starting_balance

        if current_pnl < 0 and daily_loss_pct >= self.max_daily_loss:
            logger.warning(f"⚠️ LÍMITE DIARIO ALCANZADO: {daily_loss_pct*100:.2f}% de pérdida")
            return False

        return True

    def check_drawdown(self, peak_balance: float, current_equity: float) -> bool:
        """
        Verifica el drawdown actual

        Args:
            peak_balance: Balance máximo alcanzado
            current_equity: Equity actual

        Returns:
            True si está dentro del límite, False si excedió
        """
        drawdown = (peak_balance - current_equity) / peak_balance

        if drawdown >= self.max_drawdown:
            logger.error(f"🚨 DRAWDOWN MÁXIMO ALCANZADO: {drawdown*100:.2f}%")
            return False

        return True
