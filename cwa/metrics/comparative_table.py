class ComparativeTable:
    def __init__(self, columns, index):
        self.columns: list[str] = columns
        self.index: list[str | int] | int = index
        self.data: dict[str, dict[str, int | float]] = {col: {idx: 0.0 for idx in index} for col in columns}
    
    def add(self, column, index, data):
        self.data[column][index] = data

    def __repr__(self):
        return repr(self._data)