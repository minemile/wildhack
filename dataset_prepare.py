import logging


class Filter:
    def log_before_and_after(self, was_size, after_size):
        print(f"{self.__class__.__name__}: dataset size {was_size} -> {after_size}")


class ToStrLower(Filter):
    def __init__(self, column):
        super().__init__()
        self.column = column

    def apply(self, df):
        df[self.column] = df[self.column].astype(str).str.lower()
        return df


class DropDuplicates(Filter):
    def __init__(self, subset):
        super().__init__()
        self.subset = subset

    def apply(self, df):
        before_size = df.shape[0]
        df = df.drop_duplicates(subset=self.subset)
        self.log_before_and_after(before_size, df.shape[0])
        return df


class FilterByQuantile(Filter):
    def __init__(self, column, upper_quantile, lower_quantile=0):
        super().__init__()
        self.column = column
        self.upper_quantile = upper_quantile
        self.lower_quantile = lower_quantile

    def apply(self, df):
        before_size = df.shape[0]
        upper_quantile_value = df[self.column].quantile(self.upper_quantile)
        if self.lower_quantile > 0:
            lower_quantile_value = df[self.column].quantile(self.quantile)
        else:
            lower_quantile_value = 0
        df = df[
            (df[self.column] >= lower_quantile_value)
            & (df[self.column] <= upper_quantile_value)
        ]
        print(
            f"Lower quantile: {lower_quantile_value}. Upper quantile: {upper_quantile_value}"
        )
        self.log_before_and_after(before_size, df.shape[0])
        return df
