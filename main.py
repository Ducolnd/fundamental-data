from yahoofinancials import YahooFinancials
import pandas as pd


# Prepare yahoo finance call
tickers = input("Enter tickers to track: (seperate by comma and space) ").split(", ")
print("Loading tickers: ", tickers)

data = YahooFinancials(tickers)

income = data.get_financial_stmts('annualy', 'income')
balance = data.get_financial_stmts('annualy', 'balance')
cash = data.get_financial_stmts('annualy', 'cash')


df = pd.DataFrame()

def put_in(thing, what):
    temp = pd.DataFrame()

    for (ticker, value) in list(what.values())[0].items():
        for x in value:
            for (date, data) in x.items():
                print(date)
                temp = temp.append(pd.Series(data, name=ticker))

                # We only want most recent data so the rest we don't care about
                break
            break
    
    # Rotate
    temp = temp.T

    # For multiindex
    temp.index.name = "data"
    temp["type"] = list(what.keys())[0]

    return pd.concat([thing, temp], axis=0)
    
    
# df = put_in(df, balance)
df = put_in(df, cash)
df = put_in(df, income)

# Fix multiindex
df = df.reset_index()
df = df.set_index(["type", "data"])

# Write
outfile = input("To what file would you like to write to (path): ")
df.to_csv(outfile, index=True)

print("Loaded data successfully to ", outfile)