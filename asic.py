# using [] to be able to analyze multiple
# only deals with one diff atm
# no delay used yet

Thashrate = [78,84,78,110] # Thash
miner_price = [9800,12848,9800,17000]# $
wattage = [3400,3150,3400,3250] # watts
elec_cost = [0.063,0.067,0.00000000,0.045] # $ per kwh
delay = [0] # months before online

difficulty_increase = [1.05,1.10,1.15] # %/100 a year + 1

btc_price = 68000 # $
difficulty = 21659344833264
uptime = .995 # %/100


hashrate = []
miner_price_btc = []
for i in range(0,len(miner_price)):
    hashrate.append(Thashrate[i] * 1000000000000)
    miner_price_btc.append(miner_price[i]/btc_price)

difficulty_increase_month = [] # seperate loop as can have as many/little diff increases
for i in range(0,len(difficulty_increase)):
    difficulty_increase_month.append(difficulty_increase[i] ** (1 / 12))  # **(1/12) to make it increase per month


def elec_btc(wattage,elec_cost,btc_price,uptime):
    return wattage/1000*24*elec_cost*30.41/btc_price*uptime

def btc_pm (difficulty,hashrate,wattage,elec_cost,btc_price,uptime):
    btc_reward = 6.3
    month_sec = 24*60*60*30.41
    elec_cost_btc = elec_btc(wattage,elec_cost,btc_price,uptime)
    revenue = btc_reward/(difficulty*2**32)*hashrate*month_sec
    profit = revenue*uptime - elec_cost_btc*uptime
    return profit

def roi(difficulty,difficulty_increase_month,miner_price_btc,hashrate,wattage,elec_cost,btc_price,uptime):


    for i in range(0,len(miner_price)):
        print("Thash=",hashrate[i]/1000000000000," price=",round(miner_price_btc[i],3))
        incdifficulty = difficulty
        for j in range(0,len(difficulty_increase_month)):
            btc_mined = 0 # reset btc mined
            months_to_roi = 0 # reset months to roi
            while (btc_mined < miner_price_btc[i] and months_to_roi < 24):
                btc_mined = btc_mined + btc_pm(incdifficulty, hashrate[i], wattage[i], elec_cost[i], btc_price, uptime)

                months_to_roi = months_to_roi +1
                incdifficulty = incdifficulty*difficulty_increase_month[j]
            print("month=",months_to_roi," BTC=",round(btc_mined,5)," diff% = ", round((difficulty_increase_month[j]**12-1)*100),"%" )




print(btc_pm(difficulty,hashrate[0],wattage[0],elec_cost[0],btc_price,uptime))
roi(difficulty,difficulty_increase_month,miner_price_btc,hashrate,wattage,elec_cost,btc_price,uptime)
