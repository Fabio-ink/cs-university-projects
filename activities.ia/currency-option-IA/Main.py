import importlib.util
import pathlib
import sys
import types

ROOT = pathlib.Path(__file__).parent

def load_module_from_path(name: str, path: pathlib.Path):
    path = pathlib.Path(path)
    if not path.exists() or path.is_dir():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or getattr(spec, "loader", None) is None:
        module = types.ModuleType(name)
        module.__file__ = str(path)
        source = path.read_text(encoding='utf-8')
        exec(compile(source, str(path), 'exec'), module.__dict__)
        return module
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

if __name__ == "__main__":
    import matplotlib

    csv_path = ROOT / "assets" / "bcdata.sgs.10813.csv"
    if not csv_path.exists():
        print(f"Arquivo CSV não encontrado em: {csv_path}")
        sys.exit(1)

    vi_mod = load_module_from_path("ValueImporter", ROOT / "ValueImporter.py")
    ValueImporter = vi_mod.ValueImporter

    pp_path = ROOT / "PricePlotter"
    if not pp_path.exists():
        pp_path = ROOT / "PricePlotter.py"
    pp_mod = load_module_from_path("PricePlotter", pp_path)
    PricePlotter = pp_mod.PricePlotter

    importer = ValueImporter(str(csv_path))
    prices = importer.load_prices()
    if not prices:
        print("Nenhum preço carregado do CSV. Verifique o conteúdo do arquivo.")
        sys.exit(1)

    plotter = PricePlotter("Valor do Dólar (BRL)")
    plotter.plot_prices(prices, reverse=True)
