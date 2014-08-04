from pagador.settings import DEBUG

CONSUMER_KEY = "6F67B3258ED44F9FB9B3A474619D93F0"
SECRET_KEY = "3CE003C1DFB047E6A027C07EB63E2411"

REQUEST_URL = "http://api.koin.{}.br/V1/TransactionService.svc/Request".format("net" if DEBUG else "com")