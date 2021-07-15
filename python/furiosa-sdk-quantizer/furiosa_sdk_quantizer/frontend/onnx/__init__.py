from typing import Callable, Dict, IO, List, Text, Tuple

import numpy as np
import onnx

__DOMAIN__ = ''
__OPSET_VERSION__ = 12

from furiosa_sdk_quantizer.frontend.onnx import calibrate, spec
from furiosa_sdk_quantizer.frontend.onnx.quantizer import quantizer
from furiosa_sdk_quantizer.frontend.onnx.transformer.polish_model import PolishModel
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_bn_into_conv import FuseBnIntoConv
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_lp_normalization import FuseLpNormalization
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_conv import FuseConv
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_depth_to_space import FuseDepthToSpace
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_gelu import FuseGELU
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_layer_normalization import FuseLayerNormalization
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_redundant_reshape_pattern import FuseRedundantReshapePattern
from furiosa_sdk_quantizer.frontend.onnx.transformer.fuse_pad import FusePad
from furiosa_sdk_quantizer.frontend.onnx.transformer.eliminate_redundant_reshape_pattern import \
    EliminateRedundantReshapePattern
from furiosa_sdk_quantizer.frontend.onnx.transformer.convert_conv1d_to_conv2d import ConvertConv1dToConv2d
from furiosa_sdk_quantizer.frontend.onnx.utils.inference_shape import InferenceShape
from furiosa_sdk_quantizer.frontend.onnx.utils.version_checker import CheckVersion


def _transform(transformers: List[Callable[[onnx.ModelProto], onnx.ModelProto]],
               model: onnx.ModelProto) -> onnx.ModelProto:
    for transform in transformers:
        model = transform(model)
    return model


def _polish_model(model: onnx.ModelProto) -> onnx.ModelProto:
    return _transform([
        PolishModel().transform,
    ], model)


def _inference_shape(model: onnx.ModelProto) -> onnx.ModelProto:
    return InferenceShape(model).inference_shape()


def _reify(model: onnx.ModelProto) -> onnx.ModelProto:
    transformers = [
        ConvertConv1dToConv2d().transform,
        FuseConv().transform,
        FusePad().transform,
        FuseBnIntoConv().transform,
        FuseDepthToSpace().transform,
        FuseGELU().transform,
        FuseLayerNormalization().transform,
        FuseLpNormalization().transform,
        FuseRedundantReshapePattern().transform,
        EliminateRedundantReshapePattern().transform,
    ]
    return _transform(transformers, model)


def export_spec(model: onnx.ModelProto, output: IO[Text]):
    model = _transform([_inference_shape, _reify], model)
    spec.export_spec.OnnxExportSpec(model).dump(output)


def optimize_model(model: onnx.ModelProto) -> onnx.ModelProto:
    model = _transform([CheckVersion().transform], model)
    model = _transform([_polish_model], model)

    # Apply _inference_shape if there exists 1) a node output whose value
    # information is not stored in model.graph.value_info or
    # model.graph.output or 2) a value_info in model.graph.value_info whose
    # shape information is empty.
    value_names = set(value_info.name for value_info in model.graph.value_info)
    value_names.update(value_info.name for value_info in model.graph.output)

    if (any(value_name not in value_names
            for node in model.graph.node
            for value_name in node.output) or
            any(not value_info.type.tensor_type.shape.dim
                for value_info in model.graph.value_info)):
        model = _transform([_inference_shape], model)

    # TODO check if graph_transform should apply.
    model = _transform([_reify], model)

    return model


def quantize(model: onnx.ModelProto,
             per_channel: bool,
             static: bool,
             mode: quantizer.QuantizationMode,
             dynamic_ranges: Dict[str, Tuple[float, float]]) -> onnx.ModelProto:
    return quantizer.FuriosaONNXQuantizer(model,
                                          per_channel,
                                          static,
                                          mode,
                                          dynamic_ranges).quantize()


def post_training_quantize(
    model: onnx.ModelProto,
    dataset: List[Dict[str, np.ndarray]],
    per_channel: bool = True,
) -> onnx.ModelProto:
    """Post-training-quantizes an ONNX model with a calibration dataset.

    Args:
        model: An ONNX model to quantize.
        dataset: A calibration dataset.
        per_channel: If per_channel is True, Conv's filters are
          per-channel quantized. Otherwise, they are per-tensor
          quantized.
    Returns:
        An ONNX model post-training-quantized with the calibration
        dataset.
    """
    model = optimize_model(model)
    ranges = calibrate.calibrate(model, dataset)
    return quantize(model, per_channel, True, quantizer.QuantizationMode.dfg, ranges)


def post_training_quantization_with_random_calibration(
    model: onnx.ModelProto,
    per_channel: bool,
    static: bool,
    mode: quantizer.QuantizationMode,
    num_data: int = 8,
) -> onnx.ModelProto:
    if not static:
        raise Exception("Currently only supports static quantization.")
    if mode not in [quantizer.QuantizationMode.dfg, quantizer.QuantizationMode.fake]:
        raise Exception("Currently only supports QuantizationMode dfg or fake.")

    model = optimize_model(model)
    dynamic_ranges = calibrate.calibrate_with_random_data(model, num_data)
    return quantize(model, per_channel, static, mode, dynamic_ranges)
