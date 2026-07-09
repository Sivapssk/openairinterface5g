"""Action Service for Digital Twin (PC2).
Reads best_actions_output_ADM.csv from ~/openairinterface5g/.
If state not found, finds nearest neighbor and returns sub-optimal.
"""

import os
import csv

import state_pb2
import state_pb2_grpc

CSV_PATH = os.path.expanduser("~/openairinterface5g/best_actions_output_ADM.csv")


def _load_adm_csv():
    """Load the ADM CSV. Returns list of (state_int, action, throughput_int) sorted by state."""
    rows = []
    if not os.path.exists(CSV_PATH):
        print(f"[WARN] ADM CSV not found at {CSV_PATH}")
        return rows
    with open(CSV_PATH, newline="") as f:
        reader = csv.reader(f)
        next(reader, None)  # skip header
        for row in reader:
            if len(row) >= 3:
                state = int(row[0].strip())
                action = row[1].strip()
                throughput = int(row[2].strip())
                rows.append((state, action, throughput))
    rows.sort(key=lambda r: r[0])  # sort by state
    return rows


def _nearest_neighbor(state: int, rows: list) -> tuple[int, str, int]:
    """Find the nearest state by absolute distance.
    If two states are equally close, pick the one whose throughput
    is closest to the requested state's value.
    Returns (best_state, best_action, best_throughput).
    """
    if not rows:
        return None

    # find minimum distance
    min_dist = min(abs(r[0] - state) for r in rows)

    # get all candidates at this distance
    candidates = [r for r in rows if abs(r[0] - state) == min_dist]

    if len(candidates) == 1:
        return candidates[0]

    # tie-break: pick whose throughput is closest to the requested state
    best = min(candidates, key=lambda r: abs(r[2] - state))
    return best


def _get_best_action(state_key: str) -> tuple[str, int, bool]:
    """Return (action_name, expected_throughput, is_optimal) for a given state.
    Optimal only if the state is literally in the ADM CSV.
    Otherwise returns nearest neighbor as sub-optimal.
    """
    state = int(state_key)
    rows = _load_adm_csv()

    # Check for exact match first
    for s, a, t in rows:
        if s == state:
            print(f"  [DT ActionService] Found exact match: state={s} -> action={a} bw={t} (OPTIMAL)")
            return a, t, True

    # Not found — nearest neighbor as sub-optimal
    nearest = _nearest_neighbor(state, rows)
    if nearest is None:
        print(f"  [DT ActionService] ADM CSV is empty or unreadable — returning fallback")
        return "$a_1$", 50, False

    print(f"  [DT ActionService] state={state} not in ADM, nearest={nearest[0]} -> action={nearest[1]} bw={nearest[2]} (SUB-OPTIMAL)")
    return nearest[1], nearest[2], False


class ActionServiceServicer(state_pb2_grpc.ActionServiceServicer):

    def GetBestAction(self, request, context):
        action_name, throughput, optimal = _get_best_action(str(request.state))
        return state_pb2.ActionResponse(
            action_name=action_name,
            expected_throughput=throughput,
            is_optimal=optimal,
        )
