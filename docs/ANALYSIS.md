# Análisis de Repositorios MT5

Documento generado automáticamente el 2026-02-27

## 🎯 Objetivo

Analizar repositorios existentes de bots de trading para MT5 en Python y crear una base de código modular y funcional.

## 📊 Repositorios Analizados

### 1. **jimtin/how_to_build_a_metatrader5_trading_bot_expert_advisor** ⭐ 163
- **URL**: https://github.com/jimtin/how_to_build_a_metatrader5_trading_bot_expert_advisor
- **Última actualización**: 2026-01-25
- **Descripción**: Tutorial educativo con integración de MT5 y Python
- **Puntos fuertes**:
  - Excelente documentación para principiantes
  - Videos tutoriales incluidos
  - Código limpio y bien comentado
- **Uso en este proyecto**: Inspiración para la estructura de documentación

---

### 2. **jimtin/algorithmic_trading_bot** ⭐ 142
- **URL**: https://github.com/jimtin/algorithmic_trading_bot
- **Última actualización**: 2026-02-26
- **Descripción**: Bot algorítmico para MT5 y Binance con estrategias MACD
- **Puntos fuertes**:
  - Múltiples estrategias (MACD Crossover, Zero Cross)
  - Estructura modular clara
  - Indicadores técnicos bien implementados
- **Archivos clave analizados**:
  - `mt5_lib.py`: Gestión de conexión MT5
  - `make_trade.py`: Ejecución de órdenes
  - `indicator_lib.py`: Librería de indicadores
- **Uso en este proyecto**: Base para el módulo de indicadores técnicos

---

### 3. **Zsunflower/Monn** ⭐ 76 ✅ **PRINCIPAL FUENTE**
- **URL**: https://github.com/Zsunflower/Monn
- **Última actualización**: 2026-02-27 (muy activo)
- **Descripción**: Bot de trading con múltiples estrategias y análisis multi-timeframe
- **Arquitectura**:
  ```
  Monn/
  ├── main.py
  ├── trader.py
  ├── order.py
  ├── exchange/
  │   ├── mt5_api.py
  │   └── mt5_oms.py
  ├── strategies/
  │   ├── base_strategy.py
  │   ├── ma_cross_strategy.py
  │   └── break_strategy.py
  └── configs/
  ```
- **Puntos fuertes**:
  - Sistema de estrategias plug-and-play
  - Multi-timeframe simultáneo
  - Order Management System robusto
- **Uso en este proyecto**: **Base arquitectural principal**

---

### 4. **ilahuerta-IA/mt5_live_trading_bot** ⭐ 22
- **URL**: https://github.com/ilahuerta-IA/mt5_live_trading_bot
- **Descripción**: Monitor profesional con GUI y risk management avanzado
- **Puntos fuertes**:
  - Risk management comprehensivo
  - Monitoreo en tiempo real
- **Uso en este proyecto**: Inspiración para risk management

---

## 🏗️ Arquitectura Final

```
mt5-trading-agent-base/
├── core/              # Conexión MT5 y órdenes
├── strategies/        # Estrategias modulares
├── risk/              # Risk management avanzado
├── indicators/        # Indicadores técnicos
├── market_data/       # Datos históricos y en vivo
├── config/            # Configuración
└── main.py
```

## 🛡️ Características

### Conexión MT5
- Autenticación
- Info de cuenta y símbolos
- Gestión de posiciones

### Gestión de Órdenes
- Market orders (BUY/SELL)
- Pending orders (LIMIT/STOP)
- Modificación SL/TP

### Risk Management
- **Cálculo dinámico de lotes**
- **Stop Loss adaptativo con ATR**
- **Take Profit multinivel**
- **Límites de pérdida diaria**

### Símbolos Soportados
- **Forex**: EURUSD, GBPUSD, USDJPY, etc.
- **Crypto**: BTCUSD, ETHUSD, etc.
- **Índices sintéticos**: Volatility, Boom, Crash

## 🚀 Próximos Pasos

1. Implementar estrategias concretas
2. Añadir más indicadores técnicos
3. Sistema de backtesting
4. Dashboard web
5. Alertas por Telegram

---

**Repositorio**: https://github.com/javiertarazon/mt5-trading-agent-base