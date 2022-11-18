from math import floor


class OneBitPredictor:
    def __init__(self, predict):
        self.predict = predict
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def taken(self):
        self.total += 1
        if self.predict == 'NT':
            self.predict = 'T'
            self.incorrect += 1
        else:
            self.predict = 'T'
            self.correct += 1
    
    def not_taken(self):
        self.total += 1
        if self.predict == 'NT':
            self.predict = 'NT'
            self.correct += 1
        else:
            self.predict = 'NT'
            self.incorrect += 1

class SaturatedCounter:
    def __init__(self, low, high):
        self.high = high
        self.low = low
        self.count = floor(high-low/2)

    def inc(self):
        if(self.count < self.high):
            self.count += 1
    
    def dec(self):
        if(self.count > self.low):
            self.count -= 1

class TwoBitPredictor:
    def __init__(self, predict):
        self.predict = predict
        self.state = SaturatedCounter(0,3)
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def taken(self):
        self.total += 1
        if self.predict == 'T':
            self.correct += 1
        else:
            self.incorrect += 1

        self.state.inc()
        self.predict = 'NT' if self.state.count < 2 else 'T'

    def not_taken(self):
        self.total += 1
        if self.predict == 'NT':
            self.correct += 1
        else:
            self.incorrect += 1

        self.state.dec()
        self.predict = 'NT' if self.state.count < 2 else 'T'

class ThreeBitPredictor:
    def __init__(self, predict):
        self.predict = predict
        self.state = SaturatedCounter(0,7)
        self.correct = 0
        self.incorrect = 0
        self.total = 0

    def taken(self):
        self.total += 1
        if self.predict == 'T':
            self.correct += 1
        else:
            self.incorrect += 1

        self.state.inc()
        self.predict = 'NT' if self.state.count < 4 else 'T'

    def not_taken(self):
        self.total += 1
        if self.predict == 'NT':
            self.correct += 1
        else:
            self.incorrect += 1

        self.state.dec()
        self.predict = 'NT' if self.state.count < 4 else 'T'
