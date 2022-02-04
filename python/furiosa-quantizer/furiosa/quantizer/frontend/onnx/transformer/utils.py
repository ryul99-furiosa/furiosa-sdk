from collections import Counter, OrderedDict
import logging

import onnx
from onnx import numpy_helper
from onnx.helper import make_model, make_opsetid, make_tensor_value_info

from furiosa.quantizer.frontend.onnx import __DOMAIN__, __OPSET_VERSION__
from furiosa.quantizer.frontend.onnx.quantizer.utils import __PRODUCER__

logger = logging.getLogger('Furiosa-Quantizer')
logging.basicConfig(level=logging.INFO)


def name_nodes(model):
    for idx, node in enumerate(model.graph.node):
        node.name = '%s_%d' % (node.op_type, idx)

    return model


def eliminate_unused_initializer(model):
    node_input_names = [node_input for node in model.graph.node for node_input in node.input]

    unused_initializer = list()
    for init in model.graph.initializer:
        if init.name not in node_input_names:
            unused_initializer.append(init)

    for unused in unused_initializer:
        model.graph.initializer.remove(unused)

    return model


def eliminate_unused_input(model):
    node_input_names = [node_input for node in model.graph.node for node_input in node.input]

    unused_input = list()
    for input in model.graph.input:
        if input.name not in node_input_names:
            unused_input.append(input)

    for unused in unused_input:
        model.graph.input.remove(unused)

    return model


def eliminate_unused_output(model):
    node_output_names = [node_output for node in model.graph.node for node_output in node.output]

    unused_output = list()
    for output in model.graph.output:
        if output.name not in node_output_names:
            unused_output.append(output)

    for unused in unused_output:
        model.graph.output.remove(unused)

    return model


def eliminate_unused_value_info(model):
    node_output_names = [node_output for node in model.graph.node for node_output in node.output]
    graph_output_names = [vi.name for vi in model.graph.output]
    unused_value_info = list()
    for value_info in model.graph.value_info:
        if value_info.name not in node_output_names:
            unused_value_info.append(value_info)
        if value_info.name in graph_output_names:
            unused_value_info.append(value_info)

    for unused in unused_value_info:
        model.graph.value_info.remove(unused)

    return model


def eliminate_unused_protos(model):
    funcs = [
        eliminate_unused_initializer,
        eliminate_unused_input,
        eliminate_unused_output,
        eliminate_unused_value_info,
    ]

    for func in funcs:
        model = func(model)

    return model


def include_initializer_to_graph_input(model):
    input_value_names = [inp.name for inp in model.graph.input]
    for init in model.graph.initializer:
        if init.name not in input_value_names:
            dims = numpy_helper.to_array(init).shape
            value_info = make_tensor_value_info(init.name, init.data_type, dims)
            model.graph.input.append(value_info)

            # do not append duplicated initializer to graph input
            input_value_names.append(init.name)

    return model


def rebuild_model(model, new_nodes, eliminate=True, renaming=True):
    # remove all nodes and re-make model.graph based on newly given nodes.
    model.graph.ClearField('node')
    model.graph.node.extend(new_nodes)
    default_opset = make_opsetid(__DOMAIN__, __OPSET_VERSION__)
    model = make_model(model.graph, opset_imports=[default_opset])

    # eliminate all unused protos such as initializer, input, output, and value_info.
    if eliminate:
        model = eliminate_unused_protos(model)

    # include initializer to graph input
    model = include_initializer_to_graph_input(model)

    # rename node.name
    if renaming:
        model = name_nodes(model)
    model.producer_name = __PRODUCER__
    return model


def remove_unused_operators(model):
    operators_in_use = set()
    producer_map = {node_output: node for node in model.graph.node for node_output in node.output}
    name_to_node = OrderedDict({node.name: node for node in model.graph.node})
    nodes_to_search = []
    for output in model.graph.output:
        if output.name in producer_map:
            nodes_to_search.append(producer_map[output.name].name)

    while len(nodes_to_search) > 0:
        current_node = nodes_to_search[-1]
        nodes_to_search.pop()
        operators_in_use.add(current_node)
        for input_tensor in name_to_node[current_node].input:
            if input_tensor in producer_map:
                if producer_map[input_tensor].name not in operators_in_use:
                    nodes_to_search.append(producer_map[input_tensor].name)

    for node in list(name_to_node):
        if node not in operators_in_use:
            del name_to_node[node]
    model.graph.ClearField('node')
    model.graph.node.extend(list(name_to_node.values()))
    eliminate_unused_protos(model)
    return model


def fix_batch_size_as_one(model):
    """
    fix batch_size = 1 if dim_param is given.
    """
    for input in model.graph.input:
        try:
            batch_dim = input.type.tensor_type.shape.dim[0]
        except IndexError:
            continue

        if batch_dim.dim_param:
            logger.info(
                "Dynamic batch size is detected at input_name: {}. "
                "Fix batch_size=1 for valid shape inference.".format(input.name)
            )
            input.type.tensor_type.shape.dim[0].dim_value = 1

    return model


def make_initializer_name_unique(model):
    # Renames Operators' initializers, if necessary, to make their names unique
    initializer = {init.name: init for init in model.graph.initializer}
    seen = set()
    for node in model.graph.node:
        for idx, node_input in enumerate(node.input):
            if node_input not in initializer:
                continue

            if node_input not in seen:
                seen.add(node_input)
                continue
            tensor = onnx.TensorProto()
            tensor.CopyFrom(initializer[node_input])
            # HACK: This attempts to give the initializer a new unique name.
            # Although it is unlikely, there is a possibility that the new
            # name is already occupied by a tensor in the model.
            tensor.name = f"{node_input}_{node.output[0]}"
            node.input[idx] = tensor.name
            model.graph.initializer.append(tensor)

    return model
