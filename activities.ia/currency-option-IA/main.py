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

    # carregar ValueImporter
    vi_mod = load_module_from_path("ValueImporter", ROOT / "value_importer.py")
    ValueImporter = vi_mod.ValueImporter

    # carregar price_plotter
    pp_path = ROOT / "price_plotter"
    if not pp_path.exists():
        pp_path = ROOT / "price_plotter.py"
    pp_mod = load_module_from_path("price_plotter", pp_path)
    PricePlotter = pp_mod.PricePlotter

    # carregar agente e função de decisão
    ac_mod = load_module_from_path("agent_cambio", ROOT / "agent_cambio.py")
    AgentCambio = ac_mod.AgentCambio

    avg_mod = load_module_from_path("average_calculator", ROOT / "average_calculator.py")
    funcaoAgenteCompraDolar = avg_mod.funcaoAgenteCompraDolar

    # carregar ambiente financeiro
    fe_mod = load_module_from_path("finance_environment", ROOT / "finance_environment.py")
    FinanceEnvironment = fe_mod.FinanceEnvironment

    # executar fluxo principal
    importer = ValueImporter(str(csv_path))
    prices = importer.load_prices()
    if not prices:
        print("Nenhum preço carregado do CSV. Verifique o conteúdo do arquivo.")
        sys.exit(1)

    # calcula média móvel e plota preço + média móvel
    medias = avg_mod.mediaMovel(prices)  # lista de médias com mesmo comprimento de prices
    plotter = PricePlotter("Valor do Dólar (BRL)")
    plotter.plot_prices_with_ma(prices, ma=medias, reverse=True)

    # preparar série invertida (y) e agente
    y = list(reversed(prices))
    ac = AgentCambio(estadoInicial=[], funcaoAgent=funcaoAgenteCompraDolar)

    for i in y[:10]:
        ac.percepcao(i)
        print(ac.saida(), end=" ")
        
    ag = AgentCambio(estadoInicial=[], funcaoAgent=funcaoAgenteCompraDolar)
    
    amb = FinanceEnvironment(estado=y)
    
    amb.adicionaAgente(ag)
    amb.executaAmbiente()
    desempenhos = amb.desempenhoAgentes()
    # imprime desempenho individual e total do sistema
    print("\nDesempenho dos agentes:")
    total = 0.0
    for idx, perf in desempenhos:
        if perf is None:
            print(f"Agente {idx}: desempenho desconhecido")
        else:
            print(f"Agente {idx}: {perf:.2f} BRL")
            total += perf
    print(f"\nDesempenho total do sistema: {total:.2f} BRL")

    # plota desempenho temporal dos agentes (evolucaoReal)
    performances = []
    labels = []
    for idx, agent in enumerate(amb.agents):
        # garantir que exista evolucaoReal
        series = getattr(agent, "evolucaoReal", None)
        if series is None:
            series = []
        performances.append(series)
        labels.append(f"Agente {idx}")

    # usa o mesmo plotter para mostrar desempenho do usuário/teste
    plotter.plot_performance(performances, labels=labels, title="Desempenho dos Agentes (BRL)")
