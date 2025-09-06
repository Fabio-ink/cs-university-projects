import matplotlib.pyplot as plt
from typing import Optional, List
import importlib.util
import pathlib
import math

class PricePlotter:
    def __init__(self, title: Optional[str] = None):
        self.title = title or "Preço"

    def plot_prices(self, prices: List[float], reverse: bool = True) -> None:
        if reverse:
            y = list(reversed(prices))
        else:
            y = prices[:]
        x = list(range(len(y)))
        plt.plot(x, y, label="Preço", color="tab:blue")
        plt.xlabel("Periodo(Dias)")
        plt.ylabel("Valor do dolar em reais")
        if self.title:
            plt.title(self.title)
        plt.grid(True)
        plt.show()

    def plot_prices_with_ma(self, prices: List[float], ma: Optional[List[float]] = None, reverse: bool = True) -> None:
        if reverse:
            y = list(reversed(prices))
            ma_series = list(reversed(ma)) if ma is not None else None
        else:
            y = prices[:]
            ma_series = ma[:] if ma is not None else None

        x = list(range(len(y)))
        plt.plot(x, y, label="Preço", color="tab:blue", linewidth=1.5, zorder=1)

        if ma_series is not None:
            # Pad à esquerda com NaN para manter alinhamento temporal
            if len(ma_series) != len(y):
                if len(ma_series) < len(y):
                    pad_len = len(y) - len(ma_series)
                    ma_series = [math.nan] * pad_len + ma_series
                else:
                    ma_series = ma_series[-len(y):]
            # plotar média com destaque
            plt.plot(x, ma_series, label="Média Móvel", color="tab:orange", linewidth=2.5, alpha=0.9, zorder=2)

        plt.xlabel("Periodo(Dias)")
        plt.ylabel("Valor do dolar em reais")
        if self.title:
            plt.title(self.title)
        plt.legend()
        plt.grid(True)
        plt.show()

    # plota desempenho (evolução do valor em BRL) de um ou mais agentes
    def plot_performance(self, performances: List[List[float]], labels: Optional[List[str]] = None, title: Optional[str] = None) -> None:
        title = title or (self.title + " - Desempenho")
        plt.figure()
        for idx, series in enumerate(performances):
            if not series:
                continue
            x = list(range(len(series)))
            label = labels[idx] if labels and idx < len(labels) else f"Agente {idx}"
            plt.plot(x, series, label=label, linewidth=1.5)
        plt.xlabel("Passos (percepções)")
        plt.ylabel("Valor do portfólio (BRL)")
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location(
        "value_importer",
        str(pathlib.Path(__file__).parent / "value_importer.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ValueImporter = module.ValueImporter

    csv_path = pathlib.Path(__file__).parent / "assets" / "bcdata.sgs.10813.csv"

    importer = ValueImporter(str(csv_path))
    prices = importer.load_prices()
    plotter = PricePlotter("Valor do Dólar (BRL)")
    
    # Calcular média móvel (exemplo: média móvel de 5 períodos)
    ma_period = 5
    moving_averages = [sum(prices[i-ma_period:i])/ma_period for i in range(ma_period, len(prices)+1)]

    plotter.plot_prices_with_ma(prices, ma=moving_averages, reverse=True)
