class Bag:
    def __init__(self, bag = None):
        if bag == None:
            self._items = list()
        else: 
            self._items = list(bag)
    
    def __contains__(self, item):
        return item in self._items

    def __len__(self):
        return len(self._items)

    def add(self, item):
        return self._items.append(item)
    
    def remove(self, item):
        if self._items.__contains__(item):
            self._items.remove(item)
        else:
            raise Exception('item doesn\'t exist in this bag')

    def __iter__(self):
        return _BagIterator(self._items)


class _BagIterator:
    def __init__(self, seq):
        self._bag_items = seq
        self._cur_item = 0

    def __next__(self):
        if self._cur_item >= len(self._bag_items):
            raise StopIteration
        else:
            item = self._bag_items[self._cur_item]
            self._cur_item += 1
            return item

    def __iter__(self):
        return self

    

bag = Bag()
bag.add(1)
bag.add(2)
for i in bag:
    print(i)

# print(type(_BagIterator(list())))