#!/usr/bin/env python3
"""gRPC server for the Digital Twin (PC2).
Starts all 4 services on port 50051.
"""

from concurrent import futures
import grpc

import state_pb2_grpc

from services.prediction_service import PredictionServiceServicer
from services.action_service import ActionServiceServicer
from services.knowledge_service import KnowledgeServiceServicer
from services.sync_service import SyncServiceServicer


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    state_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServiceServicer(), server)
    state_pb2_grpc.add_ActionServiceServicer_to_server(
        ActionServiceServicer(), server)
    state_pb2_grpc.add_KnowledgeServiceServicer_to_server(
        KnowledgeServiceServicer(), server)
    state_pb2_grpc.add_SyncServiceServicer_to_server(
        SyncServiceServicer(), server)

    server.add_insecure_port("[::]:50051")
    server.start()
    print("DT Server Running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
