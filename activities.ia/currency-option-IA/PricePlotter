import matplotlib.pyplot as plt
from typing import Optional, List
import importlib.util
import pathlib

class PricePlotter:
    def __init__(self, title: Optional[str] = None):
        self.title = title or "Preço"

    def plot_prices(self, prices: List[float], reverse: bool = True) -> None:
        if reverse:
            y = list(reversed(prices))
        else:
            y = prices[:]
        x = list(range(len(y)))
        plt.plot(x, y)
        plt.xlabel("Periodo(Dias)")
        plt.ylabel("Valor do dolar em reais")
        if self.title:
            plt.title(self.title)
        plt.grid(True)
        plt.show()

if __name__ == "__main__":
    spec = importlib.util.spec_from_file_location(
        "ValueImporter",
        str(pathlib.Path(__file__).parent / "ValueImporter.py")
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    ValueImporter = module.ValueImporter

    csv_path = pathlib.Path(__file__).parent / "assets" / "bcdata.sgs.10813.csv"

    importer = ValueImporter(str(csv_path))
    prices = importer.load_prices()
    plotter = PricePlotter("Valor do Dólar (BRL)")
    plotter.plot_prices(prices, reverse=True)
