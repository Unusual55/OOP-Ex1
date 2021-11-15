import pandas as pd
from Call import Call


class Controller:
    __columns_headers = ['elevator-call', 'time', 'source',
                         'destination', 'status', 'allocated-elevator']

    def __init__(self, calls_log: pd.DataFrame):
        self.calls_log = calls_log
        self.calls_data = self.calls_log[[
            'time', 'source', 'destination', 'allocated-elevator']]
        self.calls = [Call(row["time"], row["source"], row["destination"])
                      for _, row in self.calls_data.iterrows()]
        self.opened_calls = self.calls
        self.closed_calls = []
        pass

    @classmethod
    def from_csv(cls, file_name: str):
        return cls(pd.read_csv(file_name, names=cls.__columns_headers))

    def allocate_calls(self):
        for call in reversed(self.calls):
            # call.allocated_elevator = 1
            call.allocate_elevator(self.opened_calls)
            pass
            