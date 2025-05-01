import os
import graphviz

def draw_net(config, genome, view=False, filename=None):
    dot = graphviz.Digraph(format="png")
    inputs = [f"{k}" for k in range(config.genome_config.num_inputs)]
    outputs = [f"{k}" for k in range(config.genome_config.num_outputs)]

    for n in inputs:
        dot.node(n, label=f"In {n}", shape="box")

    for n in outputs:
        dot.node(n, label=f"Out {n}", shape="box")

    for node in genome.nodes:
        if str(node) not in inputs and str(node) not in outputs:
            dot.node(str(node), shape="circle")

    for cg in genome.connections.values():
        if cg.enabled:
            dot.edge(str(cg.key[0]), str(cg.key[1]), label=f"{cg.weight:.2f}")

    if filename:
        dot.render(filename, view=view)
    elif view:
        dot.view()
    return dot
