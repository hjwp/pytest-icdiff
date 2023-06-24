class FakeNumpyArray():

    def __init__(self, *args, **kwargs):
        pass

    def __add__(self, other):
        return self

    def __lt__(self, other):
        raise ValueError(
            'Fake for: The truth value of any array with more than one element is ambiguous.'
        )

    def __abs__(self):
        return self
