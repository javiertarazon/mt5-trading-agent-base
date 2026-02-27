"""
Configuración del Trading Agent
IMPORTANTE: NO subir este archivo con credenciales reales a GitHub
"""
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de MT5
MT5_CONFIG = {
    'login': int(os.getenv('MT5_LOGIN', 0)),
    'password': os.getenv('MT5_PASSWORD', ''),
    'server': os.getenv('MT5_SERVER', ''),
}

# Configuración de Risk Management
RISK_CONFIG = {
    'risk_per_trade': float(os.getenv('RISK_PER_TRADE', 0.02)),  # 2% por trade
    'max_drawdown': float(os.getenv('MAX_DRAWDOWN', 0.10)),      # 10% drawdown máximo
    'max_daily_loss': float(os.getenv('MAX_DAILY_LOSS', 0.05)),  # 5% pérdida diaria máxima
}

# Configuración de Trading
TRADING_CONFIG = {
    'default_symbol': os.getenv('DEFAULT_SYMBOL', 'EURUSD'),
    'default_timeframe': os.getenv('DEFAULT_TIMEFRAME', 'H1'),
    'magic_number': int(os.getenv('MAGIC_NUMBER', 123456)),
}

# Símbolos soportados
SYMBOLS = {
    'forex': [
        'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD',
        'NZDUSD', 'EURGBP', 'EURJPY', 'GBPJPY', 'AUDJPY'
    ],
    'crypto': [
        'BTCUSD', 'ETHUSD', 'LTCUSD', 'XRPUSD', 'BCHUSD'
    ],
    'synthetic': [
        'Volatility 10 Index', 'Volatility 25 Index', 'Volatility 50 Index',
        'Volatility 75 Index', 'Volatility 100 Index',
        'Boom 300 Index', 'Boom 500 Index', 'Boom 1000 Index',
        'Crash 300 Index', 'Crash 500 Index', 'Crash 1000 Index'
    ]
}

# Timeframes
TIMEFRAMES = {
    'M1': 1,
    'M5': 5,
    'M15': 15,
    'M30': 30,
    'H1': 60,
    'H4': 240,
    'D1': 1440
}

# Logging
LOG_CONFIG = {
    'level': os.getenv('LOG_LEVEL', 'INFO'),
    'file': os.getenv('LOG_FILE', 'trading_bot.log')
}
