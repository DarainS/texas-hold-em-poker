#!/usr/bin/env python3
# -*- coding=utf-8 -*-

import copy


class SevenCard(object):

    LEVEL_TABLE = {0: '非高牌', 1: '高牌', 2: '一对', 3: '两对', 4: '三条', 5: '顺子', 6: '同花', 7: '葫芦', 8: '四条', 9: '同花顺'}

    def __init__(self, arr=None):
        if arr is None:
            arr = []
        self.arr = copy.deepcopy(arr)
        self.max_value = 0
        self.value = 0
        self.level_text = self.LEVEL_TABLE[1]
        self.level = 0
        self.win = False
        self.hands_list = []

    def get_card_level_text(self):
        assert self.value > 0
        self.level = int(str(self.value)[0])
        self.level_text = self.LEVEL_TABLE[self.level]
        return self.level_text

    def __str__(self):
        res = ''
        for card in self.arr:
            res += card.__str__() + ' '
        return res

    @staticmethod
    def from_cards(hands):
        ls = hands.hands.copy()
        assert 5 <= len(ls) <= 7
        res = SevenCard()
        for card in ls:
            card.isActive = False
        res.arr = ls
        res.arr.sort(key=lambda card: card.num)
        return res

    def add_show_card_and_calculate(self, card):
        assert len(self.arr) <= 6
        self.arr.append(card)
        self.calculate_all()

    @staticmethod
    def _generate_num_num(cards):
        nums = {x: 0 for x in range(1, 15)}
        for card in cards:
            nums[card.num] += 1
            if card.num == 14:
                nums[1] += 1
        return nums

    @staticmethod
    def _generate_tag_num(cards):
        tags = {'h': 0, 'd': 0, 'c': 0, 's': 0}
        for card in cards:
            tags[card.tag] += 1
        return tags

    # 同花顺-9 同花-6
    @staticmethod
    def _try_resolve_straight_flush_and_flush(cards, num_num, tag_num):
        tag = None
        for t in tag_num:
            if tag_num[t] >= 5:
                tag = t
                break
        if tag == None:
            return False
        ls = cards.copy()
        for card in ls:
            if card.tag != tag:
                ls.remove(card)

        r = SevenCard._test_straight(ls, SevenCard._generate_num_num(ls), [])
        if r:
            lev, m_value = r
            return 9, m_value
        for card in ls[-5:]:
            card.isActive = True
        return 6, ls[-1].num, ls[-2].num, ls[-3].num, ls[-4].num, ls[-5].num

    # 顺子-5
    @staticmethod
    def _test_straight(self, cards, numNum, tagNum):
        nums = {x: 0 for x in range(1, 15)}
        for card in cards:
            nums[card.num] += 1
            if card.num == 14:
                nums[1] += 1

        for i in range(14, 5 - 1, -1):
            muNum = 0
            for j in range(0, 5):
                if nums[i - j] >= 1:
                    muNum += 1
            if muNum == 5:
                for n in range(i, i - 5, -1):
                    for card in cards:
                        if card.num == n:
                            card.isActive = True
                            break
                        if n == 1 and card.num == 14:
                            card.isActive = True
                            break
                return (5, i)
        return False

    @staticmethod
    def _try_resolve_straight(self, cards, num_num, tag_num):
        r = self._test_straight(cards, num_num, tag_num)
        return r

    @staticmethod
    def _try_resolve_quads(self, cards, num_num, tag_num):
        f = 0
        for num in range(14, 1, -1):
            if num_num[num] >= 4:
                f = num
                break
        if f == 0:
            return False
        for card in cards:
            if card.num == f:
                card.isActive = True
        for num in range(14, 1, -1):
            if num_num[num] >= 1 and num != f:
                for card in cards:
                    if card.num == num:
                        card.isActive = True
                        break
                return (8, f, num)

    # 7
    @staticmethod
    def _try_resolve_full_house(self, cards, numNum, tagNum):
        f, h = 0, 0
        for num in range(14, 1, -1):
            if numNum[num] >= 3:
                if f == 0:
                    f = num
                else:
                    h = num
            if numNum[num] >= 2:
                if num != f and num > h:
                    h = num

        if f > 0 and h > 0:
            t = 5
            for card in cards:
                if card.num == f:
                    t -= 1
                    card.isActive = True
            for card in cards:
                if card.num == h and t > 0:
                    t -= 1
                    card.isActive = True
            return (7, f, h)
        return False

    # 4
    @staticmethod
    def _try_resolve_set(self, cards, numNum, tagNum):
        f, h1, h2 = 0, 0, 0
        for num in range(14, 1, -1):
            if numNum[num] >= 3:
                f = num
                break
        if f == 0:
            return False
        for num in range(14, 1, -1):
            if numNum[num] >= 1:
                if num != f:
                    if h1 == 0:
                        h1 = num
                    else:
                        h2 = num
                        break
        for card in cards:
            if card.num == f or card.num == h1 or card.num == h2:
                card.isActive = True
        return (4, f, h1, h2)

    # 2
    @staticmethod
    def _try_resolve_pair(self, cards, numNum, tagNum):
        p1, p2, t = 0, 0, 0
        ticker = []
        for num in range(14, 1, -1):
            if numNum[num] == 2:
                if p1 == 0:
                    p1 = num
                else:
                    p2 = num
                    break
        if p1 == 0:
            return False

        if p1 != 0 and p2 == 0:
            for num in range(14, 1, -1):
                if len(ticker) == 3:
                    break
                if numNum[num] == 1:
                    ticker.append(num)
            for card in cards:
                if card.num == p1 or card.num == ticker[0] or card.num == ticker[1] or card.num == ticker[2]:
                    card.isActive = True

            tup = (2, p1, ticker[0], ticker[1], ticker[2])
            return tup

        if p1 != 0 and p2 != 0:
            for num in range(14, 1, -1):
                if numNum[num] == 1:
                    t = num
                    break
            mt = True
            for card in cards:
                if card.num == p1 or card.num == p2:
                    card.isActive = True
                if mt and card.num == t:
                    card.isActive = True
                    mt = False
            tup = (3, p1, p2, t)
            return tup

    @staticmethod
    def _try_resolve_high(cards, numNum, tagNum):
        t = (1, cards[-1].num, cards[-2].num, cards[-3].num, cards[-4].num, cards[-5].num)
        for card in cards[-5:]:
            card.isActive = True
        return t

    @staticmethod
    def _calculate_value_from_iterator(iterator):
        v = []
        v.extend(iterator)
        toApend = 6 - len(v)
        v.extend([0 for i in range(0, toApend)])
        s = '%02d%02d%02d%02d%02d%02d' % (v[0], v[1], v[2], v[3], v[4], v[5])
        val = int(s)
        return val

    resolveMethodList = [_try_resolve_straight_flush_and_flush, _try_resolve_quads, _try_resolve_full_house,
                         _try_resolve_straight,
                         _try_resolve_set, _try_resolve_pair, _try_resolve_high]

    def _resolve_max_value(self):
        cards = self.arr
        numNum = self._generate_num_num(cards)
        tagNum = self._generate_tag_num(cards)

        for resolve in self.resolveMethodList:
            t = resolve(self, cards, numNum, tagNum)
            if t:
                sum = 0
                for card in cards:
                    if card.isActive:
                        sum += 1
                if sum != 5:
                    print(sum, t, cards)
                return self._calculate_value_from_iterator(t)

    def calculate_all(self):
        self.value = self._resolve_max_value()
        self.level_text = self.get_card_level_text()
        return self


def test_all_level_cards():
    from model.deck import Deck
    fs = []
    level_set = set([i for i in range(1, 10)])
    while len(level_set) > 0:
        deck = Deck()
        cards = []
        for i in range(0, 7):
            cards.append(deck.dealOne())
        seven = SevenCard.from_cards(cards)
        seven.calculate_all()
        if seven.level in level_set:
            fs.append(seven)
            level_set.remove(seven.level)

    ls2 = sorted(fs, key=lambda seven: seven.value)
    for s in ls2:
        print(s, s.level_text, s.value)


def main():
    test_all_level_cards()


if __name__ == '__main__':
    main()
