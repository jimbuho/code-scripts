import sys

class Currency:

    MAX_INTEGER = sys.maxsize

    def __init__(self, denominations):
        self.denominations = denominations
        self.denominations.sort(reverse=True)

    # number of ways to make change for amount
    def num_ways(self, amount):
        return self.num_ways_by_amount(amount, 0, [])

    def num_ways_by_amount(self, left_amount, i, comb, add=None):
        if add: 
            comb.append(add)
        
        if left_amount == 0 or (i+1) == len(self.denominations):
            if (i+1) == len(self.denominations) and left_amount > 0:
               if left_amount % self.denominations[i]:
                   return 0
               comb.append( (left_amount/self.denominations[i], self.denominations[i]) )
               i += 1
            while i < len(self.denominations):
                comb.append( (0, self.denominations[i]) )
                i += 1
            return 1
        
        cur = self.denominations[i]
        
        return sum(self.num_ways_by_amount(left_amount-x*cur, i+1, comb[:], (x,cur)) 
            for x in range(0, int(left_amount/cur)+1))

    # minumum number of coins required to make change for amount
    def min_change(self, amount):
        return self.min_change_by_den(amount, self.denominations)

    def min_change_by_den(self, amount, denominations):
        if amount in denominations:
            return 1

        minimal = self.MAX_INTEGER
        for i in range(0,len(denominations)):
            c = denominations[i]

            if c <= amount:
              coins_count, sum_coins = 0, 0
              while sum_coins <= amount:
                if sum_coins + c > amount:
                  break
                  
                sum_coins += c
                coins_count += 1

              if sum_coins == amount:
                  minimal = coins_count if coins_count < minimal else minimal
              elif i < len(denominations)-1:
                coins_count += self.min_change_by_den(amount - sum_coins, denominations[i+1:])
                minimal = coins_count if coins_count > 0 and coins_count < minimal else minimal

        return minimal if minimal != self.MAX_INTEGER else 0
                  

def main():

    denominations = [100, 50, 25, 10, 5, 1]

    us_cents = Currency(denominations)
    print('NUM ways:', us_cents.num_ways(100))
    print('MIN coins used:', us_cents.min_change(194))

main()  