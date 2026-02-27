"""
MT5 Trading Agent - Punto de entrada principal
"""
import logging
import sys
from datetime import datetime
from core.mt5_connector import MT5Connector
from core.order_manager import OrderManager, OrderType
from risk.risk_calculator import RiskCalculator
from config.settings import MT5_CONFIG, RISK_CONFIG, TRADING_CONFIG

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Función principal del bot"""
    logger.info("=" * 80)
    logger.info("🤖 MT5 TRADING AGENT INICIANDO")
    logger.info("=" * 80)

    # Inicializar componentes
    connector = MT5Connector()

    # Conectar a MT5
    success = connector.connect(
        login=MT5_CONFIG['login'],
        password=MT5_CONFIG['password'],
        server=MT5_CONFIG['server']
    )

    if not success:
        logger.error("❌ No se pudo conectar a MT5. Abortando.")
        sys.exit(1)

    # Inicializar gestores
    order_manager = OrderManager(connector)
    risk_calc = RiskCalculator(
        risk_per_trade=RISK_CONFIG['risk_per_trade'],
        max_drawdown=RISK_CONFIG['max_drawdown'],
        max_daily_loss=RISK_CONFIG['max_daily_loss']
    )

    # Mostrar información de cuenta
    balance = connector.get_account_balance()
    equity = connector.get_account_equity()
    logger.info(f"💰 Balance: ${balance:.2f} | Equity: ${equity:.2f}")

    # Obtener posiciones abiertas
    positions = connector.get_positions()
    logger.info(f"📊 Posiciones abiertas: {len(positions)}")

    # Ejemplo de uso: Obtener info de símbolo
    symbol = TRADING_CONFIG['default_symbol']
    symbol_info = connector.get_symbol_info(symbol)

    if symbol_info:
        logger.info(f"📈 {symbol} - Bid: {symbol_info['bid']}, Ask: {symbol_info['ask']}, Spread: {symbol_info['spread']}")

    # AQUÍ IRÍA LA LÓGICA DE TU ESTRATEGIA
    # Ejemplo básico (comentado para evitar trades accidentales):

    # # Calcular tamaño de lote
    # entry_price = symbol_info['ask']
    # stop_loss = entry_price - 0.0050  # 50 pips de SL
    # 
    # lot_size = risk_calc.calculate_lot_size(
    #     balance=balance,
    #     entry_price=entry_price,
    #     stop_loss=stop_loss,
    #     symbol_info=symbol_info,
    #     order_type="BUY"
    # )
    # 
    # # Calcular múltiples TP
    # tp_levels = risk_calc.calculate_multi_tp(
    #     entry_price=entry_price,
    #     stop_loss=stop_loss,
    #     ratios=[1.5, 2.0, 3.0],
    #     order_type="BUY"
    # )
    # 
    # logger.info(f"Lot size calculado: {lot_size}")
    # logger.info(f"TP levels: {tp_levels}")
    # 
    # # Enviar orden (DESCOMENTAR SOLO EN DEMO)
    # # result = order_manager.send_market_order(
    # #     symbol=symbol,
    # #     order_type=OrderType.BUY,
    # #     volume=lot_size,
    # #     sl=stop_loss,
    # #     tp=tp_levels[0],
    # #     comment="Test order"
    # # )

    logger.info("=" * 80)
    logger.info("✅ Bot ejecutado correctamente")
    logger.info("=" * 80)

    # Desconectar
    connector.disconnect()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Bot detenido por el usuario")
    except Exception as e:
        logger.error(f"❌ Error fatal: {str(e)}", exc_info=True)
