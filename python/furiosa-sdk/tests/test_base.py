import os
import random

import numpy as np
import tensorflow as tf

from furiosa.extras.runtime import session
from . import test_data


def model_path(name: str) -> str:
    return os.path.dirname(__file__) + "/../npu-models/" + name


MNIST_MOBINENET_V2 = test_data("MNISTnet_uint8_quant_without_softmax.tflite")
#COCO_SSD_MOBILENET_V1 = model_path("tflite/mscoco_300x300_ssd_mobilenet_v1_uint8_quantization-aware-trained.tflite")


def assert_tensors_equal(expected, result):
    assert np.array_equal(expected, result), "{} was expected, but the result was {}".format(expected, result)


class SessionTester:
    def __init__(self, model_path):
        self.session = session.create(model=model_path)


class AsyncSessionTester:
    def __init__(self, model_path):
        (self.session, self.queue) = session.create_async(model=model_path)


class PredictionTester:
    def __init__(self, model_path):
        self.tf_sess = tf.lite.Interpreter(model_path=model_path)

    def _run_nux(self, inputs: np.ndarray):
        pass

    def _run_tf(self, inputs: np.ndarray):
        self.tf_sess.allocate_tensors()
        tf_inputs = self.tf_sess.get_input_details()
        tf_outputs = self.tf_sess.get_output_details()

        self.tf_sess.set_tensor(tf_inputs[0]['index'], inputs)
        self.tf_sess.invoke()
        return self.tf_sess.get_tensor(tf_outputs[0]['index'])

    def assert_equals(self, inputs: np.ndarray):
        tf_results = self._run_tf(inputs)
        nux_results = self._run_nux(inputs)

        assert_tensors_equal(tf_results, nux_results)


class BlockingPredictionTester(PredictionTester):
    def __init__(self, model_path):
        self.nux_sess = session.create(model=model_path)
        super().__init__(model_path)

    def _run_nux(self, inputs: np.ndarray):
        return self.nux_sess.run(inputs)[0].numpy()


class AsyncPredictionTester(PredictionTester):
    def __init__(self, model_path):
        (nux_sess, nux_queue) = nux.session.create_async(model=model_path)
        self.nux_sess = nux_sess
        self.nux_queue = nux_queue
        super().__init__(model_path)

    def _run_nux(self, inputs: np.ndarray) -> np.ndarray:
        key = random.randint(0, 100)
        self.nux_sess.submit(inputs, context={'key': key})
        _, outputs = self.nux_queue.recv()
        return outputs[0].numpy()
