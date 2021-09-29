# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

# FIXME(yan): This is manually modified
from . import predict_pb2 as predict__pb2


class GRPCInferenceServiceStub(object):
    """Inference Server GRPC endpoints.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ServerLive = channel.unary_unary(
                '/inference.GRPCInferenceService/ServerLive',
                request_serializer=predict__pb2.ServerLiveRequest.SerializeToString,
                response_deserializer=predict__pb2.ServerLiveResponse.FromString,
                )
        self.ServerReady = channel.unary_unary(
                '/inference.GRPCInferenceService/ServerReady',
                request_serializer=predict__pb2.ServerReadyRequest.SerializeToString,
                response_deserializer=predict__pb2.ServerReadyResponse.FromString,
                )
        self.ModelReady = channel.unary_unary(
                '/inference.GRPCInferenceService/ModelReady',
                request_serializer=predict__pb2.ModelReadyRequest.SerializeToString,
                response_deserializer=predict__pb2.ModelReadyResponse.FromString,
                )
        self.ServerMetadata = channel.unary_unary(
                '/inference.GRPCInferenceService/ServerMetadata',
                request_serializer=predict__pb2.ServerMetadataRequest.SerializeToString,
                response_deserializer=predict__pb2.ServerMetadataResponse.FromString,
                )
        self.ModelMetadata = channel.unary_unary(
                '/inference.GRPCInferenceService/ModelMetadata',
                request_serializer=predict__pb2.ModelMetadataRequest.SerializeToString,
                response_deserializer=predict__pb2.ModelMetadataResponse.FromString,
                )
        self.ModelInfer = channel.unary_unary(
                '/inference.GRPCInferenceService/ModelInfer',
                request_serializer=predict__pb2.ModelInferRequest.SerializeToString,
                response_deserializer=predict__pb2.ModelInferResponse.FromString,
                )


class GRPCInferenceServiceServicer(object):
    """Inference Server GRPC endpoints.
    """

    def ServerLive(self, request, context):
        """The ServerLive API indicates if the inference server is able to receive
        and respond to metadata and inference requests.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerReady(self, request, context):
        """The ServerReady API indicates if the server is ready for inferencing.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModelReady(self, request, context):
        """The ModelReady API indicates if a specific model is ready for inferencing.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerMetadata(self, request, context):
        """The ServerMetadata API provides information about the server. Errors are
        indicated by the google.rpc.Status returned for the request. The OK code
        indicates success and other codes indicate failure.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModelMetadata(self, request, context):
        """The per-model metadata API provides information about a model. Errors are
        indicated by the google.rpc.Status returned for the request. The OK code
        indicates success and other codes indicate failure.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModelInfer(self, request, context):
        """The ModelInfer API performs inference using the specified model. Errors are
        indicated by the google.rpc.Status returned for the request. The OK code
        indicates success and other codes indicate failure.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_GRPCInferenceServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ServerLive': grpc.unary_unary_rpc_method_handler(
                    servicer.ServerLive,
                    request_deserializer=predict__pb2.ServerLiveRequest.FromString,
                    response_serializer=predict__pb2.ServerLiveResponse.SerializeToString,
            ),
            'ServerReady': grpc.unary_unary_rpc_method_handler(
                    servicer.ServerReady,
                    request_deserializer=predict__pb2.ServerReadyRequest.FromString,
                    response_serializer=predict__pb2.ServerReadyResponse.SerializeToString,
            ),
            'ModelReady': grpc.unary_unary_rpc_method_handler(
                    servicer.ModelReady,
                    request_deserializer=predict__pb2.ModelReadyRequest.FromString,
                    response_serializer=predict__pb2.ModelReadyResponse.SerializeToString,
            ),
            'ServerMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.ServerMetadata,
                    request_deserializer=predict__pb2.ServerMetadataRequest.FromString,
                    response_serializer=predict__pb2.ServerMetadataResponse.SerializeToString,
            ),
            'ModelMetadata': grpc.unary_unary_rpc_method_handler(
                    servicer.ModelMetadata,
                    request_deserializer=predict__pb2.ModelMetadataRequest.FromString,
                    response_serializer=predict__pb2.ModelMetadataResponse.SerializeToString,
            ),
            'ModelInfer': grpc.unary_unary_rpc_method_handler(
                    servicer.ModelInfer,
                    request_deserializer=predict__pb2.ModelInferRequest.FromString,
                    response_serializer=predict__pb2.ModelInferResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'inference.GRPCInferenceService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class GRPCInferenceService(object):
    """Inference Server GRPC endpoints.
    """

    @staticmethod
    def ServerLive(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ServerLive',
            predict__pb2.ServerLiveRequest.SerializeToString,
            predict__pb2.ServerLiveResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServerReady(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ServerReady',
            predict__pb2.ServerReadyRequest.SerializeToString,
            predict__pb2.ServerReadyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModelReady(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ModelReady',
            predict__pb2.ModelReadyRequest.SerializeToString,
            predict__pb2.ModelReadyResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ServerMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ServerMetadata',
            predict__pb2.ServerMetadataRequest.SerializeToString,
            predict__pb2.ServerMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModelMetadata(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ModelMetadata',
            predict__pb2.ModelMetadataRequest.SerializeToString,
            predict__pb2.ModelMetadataResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ModelInfer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/inference.GRPCInferenceService/ModelInfer',
            predict__pb2.ModelInferRequest.SerializeToString,
            predict__pb2.ModelInferResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
