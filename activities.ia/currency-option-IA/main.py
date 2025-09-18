import pathlib
import sys

from value_importer import ValueImporter
from price_plotter import PricePlotter
from agent_cambio import AgentCambio
from average_calculator import mediaMovelCumulativa, funcaoAgenteCompraDolar
from finance_environment import FinanceEnvironment

ROOT = pathlib.Path(__file__).parent

if __name__ == "__main__":
    csv_path = ROOT / "assets" / "bcdata.sgs.10813.csv"
    if not csv_path.exists():
        print(f"Arquivo CSV não encontrado em: {csv_path}")
        sys.exit(1)

    importer = ValueImporter(str(csv_path))
    prices = importer.load_prices()
    if not prices:
        print("Nenhum preço carregado do CSV. Verifique o conteúdo do arquivo.")
        sys.exit(1)

    medias = mediaMovelCumulativa(prices)
    plotter = PricePlotter("Valor do Dólar (BRL)")
    plotter.plot_prices_with_ma(prices, ma=medias, reverse=True)

    price_series = list(reversed(prices))
    agent = AgentCambio(estadoInicial=[], funcaoAgent=funcaoAgenteCompraDolar)
    
    environment = FinanceEnvironment(estado=price_series)
    environment.adicionaAgente(agent)
    environment.executaAmbiente()
    
    desempenhos = environment.desempenhoAgentes()
    print("\nDesempenho dos agentes:")
    total = 0.0
    for idx, perf in desempenhos:
        if perf is None:
            print(f"Agente {idx}: desempenho desconhecido")
        else:
            print(f"Agente {idx}: {perf:.2f} BRL")
            total += perf
    print(f"\nDesempenho total do sistema: {total:.2f} BRL")

    performances = []
    labels = []
    for idx, agent in enumerate(environment.agents):
        series = getattr(agent, "evolucaoReal", None)
        if series is None:
            series = []
        performances.append(series)
        labels.append(f"Agente {idx}")

    plotter.plot_performance(performances, labels=labels, title="Desempenho dos Agentes (BRL)")
