import rqdatac
rqdatac.init('13383713859', '123456')
print(rqdatac.user.get_quota())
# df = rqdatac.all_instruments(type=None, market='cn', date=None)
# df.to_csv("所有品种合约的数据.csv")
