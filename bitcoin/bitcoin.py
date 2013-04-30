from sys import stdin


class FluxCapacitor():
    def __init__(self, initial_euros, exchange_rates):
        self.initial_euros = int(initial_euros)
        self.exchange_rates = \
            [int(x) for x in exchange_rates.rstrip().split(' ')]
        self.maximum_of_euros = 0
        self.actual_euros = self.initial_euros
        self.actual_bitcoins = 0

    def getMaximumOfEuros(self):
        self.processExchangeRates()

        return self.maximum_of_euros

    def processExchangeRates(self):
        for i in xrange(0, len(self.exchange_rates)):
            if self.shouldIBuyAtMoment(i):
                self.buyBitcoinsWithRate(self.exchange_rates[i])
            elif self.shouldISellAtMoment(i):
                self.sellBitcoinsWithRate(self.exchange_rates[i])

    def shouldIBuyAtMoment(self, moment):
        return self.actual_euros \
            and moment + 1 < len(self.exchange_rates) \
            and self.exchange_rates[moment] <= self.exchange_rates[moment + 1]

    def shouldISellAtMoment(self, moment):
        if self.actual_bitcoins:
            if moment + 1 < len(self.exchange_rates):
                return self.exchange_rates[moment] > \
                    self.exchange_rates[moment + 1]
            else:
                return True

    def buyBitcoinsWithRate(self, rate):
        if self.actual_euros > rate and self.actual_euros % rate == 0:
            self.actual_bitcoins = self.actual_euros / rate
            self.actual_euros = 0
        # print 'Comprados', self.actual_bitcoins

    def sellBitcoinsWithRate(self, rate):
        self.actual_euros = self.actual_bitcoins * rate
        self.actual_bitcoins = 0
        self.maximum_of_euros = max(self.actual_euros, self.maximum_of_euros)
        # print 'Vendidos', self.actual_euros


if __name__ == '__main__':
    t = 0
    case = 0
    initial_euros = ''
    exchange_rates = ''
    for line in stdin.readlines():
        if t != 0:
            if t >= case:
                if not initial_euros:
                    initial_euros = line
                elif not exchange_rates:
                    exchange_rates = line
                    fluxCapacitor = FluxCapacitor(
                        initial_euros,
                        exchange_rates
                    )
                    print fluxCapacitor.getMaximumOfEuros()
                    initial_euros = ''
                    exchange_rates = ''
                    case += 1
        else:
            t = int(line)
