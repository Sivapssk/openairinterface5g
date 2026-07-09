"""Knowledge Service — in-memory cache (MemoryModule) for state->action pairs."""

import state_pb2
import state_pb2_grpc


class MemoryModule:
    """Clone of demotest_ADM.py's MemoryModule — at module level."""

    def __init__(self):
        self.memory = {}

    def get(self, key):
        return self.memory.get(tuple(key), None)

    def update(self, key, value):
        self.memory[tuple(key)] = value


# Singleton cache
_cache = MemoryModule()


class KnowledgeServiceServicer(state_pb2_grpc.KnowledgeServiceServicer):

    def QueryCache(self, request, context):
        key = request.state_key
        result = _cache.get((key,))
        if result is not None:
            action, bw = result
            return state_pb2.CacheResponse(found=True, action_name=action, bandwidth=bw)
        return state_pb2.CacheResponse(found=False, action_name="", bandwidth=0)

    def StoreEntry(self, request, context):
        _cache.update((request.state_key,), (request.action_name, request.bandwidth))
        return state_pb2.StoreAck(success=True)

    def SyncKnowledge(self, request_iterator, context):
        count = 0
        for update in request_iterator:
            for pair in update.pairs:
                _cache.update((str(pair.state),), (pair.action, pair.bandwidth))
                count += 1
        return state_pb2.SyncAck(updated_count=count)
