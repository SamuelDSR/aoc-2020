#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import deque


class Node:
    def __init__(self, data, next=None, prev=None):
        self.data = data
        self.next = next
        self.prev = prev

    def __repr__(self):
        return "data:{}".format(self.data)

    def __str__(self):
        return repr(self)

    def __hash__(self):
        return hash(self.data)


class CircularLinkedList:
    """Circular Double Linked List
    """
    def __init__(self, seq):
        self.head = Node(seq[0])
        current = self.head
        self.nodes = [self.head]

        # node value => node mapping
        self._inner_dictionary = {}
        self._inner_dictionary[current.data] = current

        for item in seq[1:]:
            current.next = Node(item, None, current)
            current = current.next
            self.nodes.append(current)
            self._inner_dictionary[current.data] = current
        current.next = self.head
        self.head.prev = current

    def traverse(self, current=None, stop_func=None, include_last=False):
        """Traverse until the condition of stop_func satisfies
        Signature of stop_func: lambda current_node, init_node: boolean
        """
        current = current if current is not None else self.head
        if stop_func is None:
            stop_func = lambda x, y: x == y
        node = current
        while True:
            yield node
            node = node.next
            if stop_func is not None and stop_func(node, current):
                if include_last:
                    yield node
                break

    def take(self, current, count):
        node, subslice = current, [current]
        for i in range(count - 1):
            node = node.next
            subslice.append(node)
        # chain original circular list
        current.prev.next = node.next
        node.next.prev = current.prev
        current.prev, node.next = None, None
        return subslice

    def insert_after(self, current, subslices):
        n = current.next
        current.next = subslices[0]
        subslices[0].prev = current

        subslices[-1].next = n
        n.prev = subslices[-1]

    def find_node_by_data(self, data):
        return self._inner_dictionary[data]

    def __repr__(self):
        datas = [n.data for n in self.traverse(self.head)]
        return "->".join([str(d) for d in datas])

    def __str__(self):
        return repr(self)


def crab_game(seq, moves):
    circular_list = CircularLinkedList(seq)
    current = circular_list.head
    current_label = current.data

    max_values = set([len(seq), len(seq) - 1, len(seq) - 2, len(seq) - 3])

    for i in range(moves):
        pick_up_node = circular_list.take(current.next, 3)
        pick_up_data = [n.data for n in pick_up_node]

        # chose next target cup
        target_label = current_label - 1
        while target_label in pick_up_data:
            target_label -= 1
        if target_label <= 0:
            # chose the largest remain value
            target_label = max(max_values - set(pick_up_data))

        # find destination node
        destination_node = circular_list.find_node_by_data(target_label)

        # insert pick up after destination
        circular_list.insert_after(destination_node, pick_up_node)
        current = current.next
        current_label = current.data

    return circular_list


if __name__ == '__main__':
    seq = [9, 4, 2, 3, 8, 7, 6, 1, 5]
    c = CircularLinkedList(seq)

    # test CircularLinkedList
    traverse = [n.data for n in c.traverse(c.head.next, lambda x, y: x == y)]
    assert traverse == [4, 2, 3, 8, 7, 6, 1, 5, 9], "Wrong traverse"

    sub = c.take(c.head.next, 3)
    assert [n.data for n in sub] == [4, 2, 3]
    assert sub[0].prev == None
    assert sub[0].next.data == 2
    assert sub[-1].next == None

    traverse = [n.data for n in c.traverse(c.head.next, lambda x, y: x == y)]
    assert traverse == [8, 7, 6, 1, 5, 9], "Wrong traverse"

    # part 1
    c = crab_game(seq, 100)
    node_of_1 = c.find_node_by_data(1)
    answers = [
        str(n.data) for n in c.traverse(node_of_1.next, lambda x, y: x.data == 1)
    ]
    print("Answer to part 1:{}".format("".join(answers)))

    #  seq = [3, 8, 9, 1, 2, 5, 4, 6, 7]
    seq = seq + list(range(len(seq) + 1, 1000001))
    c = crab_game(seq, 10000000)
    node = c.find_node_by_data(1)
    print("Answer to part 2: {}".format(node.next.data*node.next.next.data))
