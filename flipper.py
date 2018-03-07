cards = [5, -2, 1, -4, -3]

class Solver(object):
    best_start = None
    start_points = []
    steps = None
    current_highest = 0
    end_point = None

    def __init__(self, cards):
        self.cards = cards

    def __call__(self, *args, **kwargs):
        return self.flip_solver()

    def compute_sum(self, index=0, end=1, sum=0):
        sum += -index
        next = index+1
        if end <= self.end_point:
            return self.compute_sum(index=index, end=next, sum=sum)

        return sum

    def flip_solver(self):
        for key, value in enumerate(self.cards):
            if value < 0:
                self.start_points.append(key)

        if not self.start_points:
            return cards
        self.end_point = self.start_points[-1]

        for key in self.start_points:
            self.compute_sum(key)
            sum = -cards[key]
            index= key
            if index < self.end_point:
                print('still going')
            if sum > self.current_highest:
                best_start = key
                steps = 1
                current_highest = sum

            print(key)
        for key, value in enumerate(self.cards):
            if key in range(self.best_start, self.best_start+steps):
                self.cards[key] = -value

        return self.cards

