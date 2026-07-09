"""Prediction Service — wraps BiLSTM model loaded from oai-cn5g/"""

import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model

import state_pb2
import state_pb2_grpc

# ── Load model once at module level ──
_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
_MODEL_PATH = os.path.join(
    _MODEL_DIR,
    "user_count_predictor_one_fewshot_sequence_oai_testbed_data_with_UPF_congestion.h5"
)
_model = load_model(_MODEL_PATH)
_scaler = MinMaxScaler(feature_range=(0, 1))
_scaler.fit(np.array([0, 1000]).reshape(-1, 1))
_SEQUENCE_LENGTH = 5


class PredictionServiceServicer(state_pb2_grpc.PredictionServiceServicer):

    def PredictState(self, request, context):
        bw_seq = list(request.bandwidth_sequence)

        if len(bw_seq) < _SEQUENCE_LENGTH:
            return state_pb2.PredictionResponse(
                predicted_state=bw_seq[-1] if bw_seq else 0,
                is_confident=False,
            )

        # Take last SEQUENCE_LENGTH values
        seq = np.array(bw_seq[-_SEQUENCE_LENGTH:]).reshape(-1, 1)
        seq_scaled = _scaler.transform(seq)
        seq_input = seq_scaled.reshape(1, _SEQUENCE_LENGTH, 1)

        pred_scaled = _model.predict(seq_input, verbose=0)
        pred = int(round(_scaler.inverse_transform(pred_scaled)[0][0]))

        return state_pb2.PredictionResponse(
            predicted_state=pred,
            is_confident=True,
        )
