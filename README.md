# 🤖 MT5 Trading Agent Base

Agente de Trading Automatizado para MetaTrader 5 con Python

## ✨ Características

- 🔌 **Conexión directa con MT5**: Usando la biblioteca oficial MetaTrader5
- 📊 **Múltiples mercados**: Forex, Crypto e Índices Sintéticos
- 🛡️ **Gestión de riesgo avanzada**: Stop Loss dinámico, Take Profit multinivel, cálculo automático de lotes
- 📈 **Estrategias modulares**: Sistema de estrategias plug-and-play
- 🔔 **Indicadores técnicos**: RSI, MACD, Bollinger Bands, ATR y más
- 🎯 **Auto-ajustable**: Parámetros adaptativos según volatilidad del mercado

## 🏗️ Arquitectura

```
mt5-trading-agent-base/
├── core/              # Componentes core (conexión MT5, órdenes, posiciones)
├── strategies/        # Estrategias de trading
├── risk/              # Módulos de gestión de riesgo
├── indicators/        # Indicadores técnicos
├── market_data/       # Obtención y procesamiento de datos
├── config/            # Configuración y símbolos
└── main.py            # Punto de entrada
```

## 📦 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/javiertarazon/mt5-trading-agent-base.git
cd mt5-trading-agent-base

# Instalar dependencias
pip install -r requirements.txt

# Configurar credenciales MT5
cp config/settings.example.py config/settings.py
# Editar config/settings.py con tus credenciales
```

## 🚀 Uso Rápido

```python
from core.mt5_connector import MT5Connector
from strategies.trend_following import TrendFollowingStrategy
from risk.risk_calculator import RiskCalculator

# Conectar a MT5
connector = MT5Connector()
connector.connect(login=123456, password="tu_password", server="tu_broker")

# Inicializar estrategia
strategy = TrendFollowingStrategy(symbol="EURUSD", timeframe="H1")

# Configurar risk management
risk_calc = RiskCalculator(risk_per_trade=0.02, max_drawdown=0.10)

# Ejecutar bot
connector.run_strategy(strategy, risk_calc)
```

## 🎯 Estrategias Incluidas

1. **Trend Following**: Sigue la tendencia principal del mercado
2. **Mean Reversion**: Opera reversiones a la media
3. **Breakout**: Detecta y opera rompimientos de niveles clave

## ⚠️ Advertencia

Este software es solo para fines educativos. El trading conlleva riesgos significativos de pérdida de capital. Siempre prueba en una cuenta demo antes de usar dinero real.

## 📚 Recursos

- [Documentación MetaTrader5 Python](https://www.mql5.com/en/docs/python_metatrader5)
- [Análisis de repositorios base](docs/ANALYSIS.md)

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE)

## 🙏 Créditos

Basado en análisis de los siguientes proyectos:
- [Zsunflower/Monn](https://github.com/Zsunflower/Monn) - Arquitectura modular
- [jimtin/algorithmic_trading_bot](https://github.com/jimtin/algorithmic_trading_bot) - Estrategias MACD
- [ilahuerta-IA/mt5_live_trading_bot](https://github.com/ilahuerta-IA/mt5_live_trading_bot) - Risk management
