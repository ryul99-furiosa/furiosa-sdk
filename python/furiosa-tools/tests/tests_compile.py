import os
import subprocess
import tempfile
import unittest

from tests import test_data


class CommandTests(unittest.TestCase):
    mnist_model = test_data('MNISTnet_uint8_quant_without_softmax.tflite')
    compiler_config = test_data('compiler_config.yml')
    invalid_compiler_config = test_data('invalid_compiler_config.yml')

    def assert_file_created(self, path, keep: bool = False):
        self.assertTrue(os.path.isfile(path))
        if not keep:
            os.remove(path)

    def test_compile(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = f"{tmpdir}/output.enf"
            os.chdir(tmpdir)
            result = subprocess.run(['furiosa-compile',
                                     self.mnist_model], capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assert_file_created(output_file)

    def test_compile_with_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = f"{tmpdir}/output.enf"
            result = subprocess.run(['furiosa-compile',
                                     self.mnist_model,
                                     '-o',
                                     output_file], capture_output=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assert_file_created(output_file)

    def test_compile_with_other_outputs(self):
        tmpfile = tempfile.TemporaryDirectory()
        output_file = tmpfile.name + "/output.enf"
        analyze_memory_output = tmpfile.name + "/memory_analysis.html"
        dot_graph_output = tmpfile.name + "/graph.dot"
        result = subprocess.run(['furiosa-compile',
                                 self.mnist_model,
                                 '-o', output_file,
                                 '--dot-graph', dot_graph_output,
                                 '--analyze-memory', analyze_memory_output,
                                 ], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assert_file_created(output_file)
        self.assert_file_created(dot_graph_output)
        self.assert_file_created(analyze_memory_output)

    def test_compile_with_target_npus(self):
        tmpfile = tempfile.TemporaryDirectory()
        output_file = tmpfile.name + "/output.enf"

        result = subprocess.run(['furiosa-compile',
                                 self.mnist_model,
                                 '-o', output_file,
                                 '--target-npu', 'warb'
                                 ], capture_output=True)
        self.assertTrue(result.returncode != 0, result.stderr)

        result = subprocess.run(['furiosa-compile',
                                 self.mnist_model,
                                 '-o', output_file,
                                 '--target-npu', 'warboy'
                                 ], capture_output=True)
        self.assertTrue(result.returncode == 0, result.stderr)

    def test_compile_with_optimization(self):
        tmpfile = tempfile.TemporaryDirectory()
        output_file = tmpfile.name + "/output.enf"
        result = subprocess.run(['furiosa-compile',
                                 self.mnist_model,
                                 '-o', output_file,
                                 '--batch-size', '2',
                                 '--split-after-lower',
                                 '--auto-batch-size',
                                 ], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        print(result.stdout)
        self.assert_file_created(output_file)

    def test_compile_with_genetic_optimization(self):
        tmpfile = tempfile.TemporaryDirectory()
        output_file = tmpfile.name + "/output.enf"
        result = subprocess.run(['furiosa-compile',
                                 self.mnist_model,
                                 '-o', output_file,
                                 '-ga', '2',
                                 ], capture_output=True)
        self.assertEqual(0, result.returncode, result.stderr)
        print(result.stdout)
        self.assert_file_created(output_file)