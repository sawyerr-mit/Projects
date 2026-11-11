"""
Rocko Graziano, University of Maine at Augusta, 2026

This package implements an Indexed minimum priority queue
Based on implementation in Algorithms, 4th Edition

"""

class IndexMinPQ:
    def __init__(self, maxN: int):
        self.__n = 0
        self.__maxN = maxN+1
        self.__pq = [None for i in range(maxN+1)]    # our heap of the keys sorted by min value - index into qp & keys
        self.__qp = [ -1 for i in range(maxN+1)]     # for each possible key, pointer to its value in __pq[]
        self.__keyValues = [None for i in range(maxN+1)]  # the value associated with a key

    def isEmpty(self) ->bool:
        return self.__n == 0

    def contains(self, key: int) ->bool:
        return not self.__qp[key] == -1

    def valueOf(self, key: int) -> int | float:
        return self.__keyValues[key]

    def minKey(self) -> int | float:
        return (self.__pq[1], self.__keyValues[self.__pq[1]])

    def size(self) -> int:
        return self.__n

    def push(self, key: int, value: int | float) -> None:
        if key >= self.__maxN:
            print(f'Error: Key {key} outside acceptable range')
            return
        self.__n += 1
        self.__qp[key] = self.__n
        self.__keyValues[key] = value
        self.__pq[self.__n] = key
        self.swim(self.__n)

    def pop(self) -> tuple[int, int | float]:
        if self.__n == 0:
            return None
        key, value = self.__pq[1], self.__keyValues[self.__pq[1]]   # grab the top of the queue
        self.exchange(1, self.__n) # swap the first & last value
        self.__qp[key] = -1
        self.__pq[self.__n] = None
        self.__keyValues[key] = None
        self.__n -= 1
        self.sink(1)

        return (key, value)

    def swim(self, k: int) -> None:
        while k > 1 and self.less( k, k // 2):
            self.exchange( k // 2 , k)
            k = k // 2

    def sink(self, k: int) -> None:
        while 2*k <= self.size():
            j = 2*k
            if j < self.size() and self.less(j+1, j):
                j += 1
            if not self.less(j, k): break
            self.exchange(j, k)
            k = j

    def exchange(self, i: int, j: int) -> None:
        self.__pq[i], self.__pq[j] = self.__pq[j], self.__pq[i]
        self.__qp[self.__pq[i]], self.__qp[self.__pq[j]] = i, j

    def less(self, i: int, j: int) -> bool:
        return self.__keyValues[self.__pq[i]] < self.__keyValues[self.__pq[j]]

    def update(self, key: int, value: int | float) -> None:
        if self.__qp[key]:
            self.__keyValues[key] = value
            self.swim(self.__qp[key])
            self.sink(self.__qp[key])

    def dump(self)-> None:
        print("QP:        ", self.__qp[1:])
        print("PQ:        ", self.__pq[1:])
        print("KeyValues: ", self.__keyValues[1:])

        for i in range(1,self.__n+1):
            print(f'Position {i} held by Key {self.__pq[i]} with Value {self.__keyValues[self.__pq[i]]}')

def main():
    # simple smoke test

    myPQ = IndexMinPQ(15)

    myPQ.push(1,5)
    myPQ.push(2,3)
    myPQ.push(3,10)
    myPQ.push(4,1)
    #myPQ.dump()
    #print()
    myPQ.push(6,4)
    myPQ.push(9,4)
    myPQ.push(10,7)
    myPQ.push(11,8)

    myPQ.dump()

    print(f'Key 11: has value {myPQ.valueOf(11)}')
    print(myPQ.minKey())

    print()

    myPQ.update(6, 2)

    myPQ.dump()

    for _ in range(myPQ.size()):
        k,v = myPQ.pop()
        print(f'Key: {k} Value: {v}')

if __name__ == '__main__':  main()