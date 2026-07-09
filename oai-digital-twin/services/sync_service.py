"""Sync Service — orchestrator for the Digital Twin (PC2).
Routes: check knowledge cache → if miss, call ActionService → return response.
"""

import state_pb2
import state_pb2_grpc

from services.knowledge_service import _cache as dt_cache
from services.action_service import _get_best_action


class SyncServiceServicer(state_pb2_grpc.SyncServiceServicer):

    def QueryAndSync(self, request, context):
        state_key = str(request.state)
        print(f"\n  [DT SyncService] Received query for state={state_key} (source={request.source})")

        # Step 1: Check DT's own knowledge cache first
        cached = dt_cache.get((state_key,))
        if cached is not None:
            action, bw = cached
            print(f"  [DT SyncService] Cache HIT — returning action={action} bw={bw}")
            return state_pb2.StateResponse(
                action_name=action,
                bandwidth=bw,
                is_optimal=True,
                source="dt-cache",
            )

        print(f"  [DT SyncService] Cache MISS — consulting ActionService...")
        # Step 2: Cache miss — ask ActionService (ADM CSV + nearest neighbor)
        action_name, throughput, is_optimal = _get_best_action(state_key)

        # Step 3: Only cache in DT if it was an exact (optimal) match
        if is_optimal:
            dt_cache.update((state_key,), (action_name, throughput))
            print(f"  [DT SyncService] Action is OPTIMAL — cached for next time")
        else:
            print(f"  [DT SyncService] Action is SUB-OPTIMAL — not cached")

        return state_pb2.StateResponse(
            action_name=action_name,
            bandwidth=throughput,
            is_optimal=is_optimal,
            source="dt-action" if is_optimal else "dt-nearest-neighbor",
        )
