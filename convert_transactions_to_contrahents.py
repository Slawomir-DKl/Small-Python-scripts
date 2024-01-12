''' Script converts CSV file with transactions exported from iPKO Biznes account to CSV file for contrahent import
Input data structure (unfortunately, with many errors:
"Data realizacji","Data utworzenia","Dane transakcji","Typ","Status","Kwota","Waluta","Biała lista VAT","Data weryfikacji","Sposób realizacji"
Output data structure acc. to:
https://www.pkobp.pl/media_files/1bc6443e-c38b-4282-92ab-aa1618ea1095.pdf
'''

import pandas as pd

df = pd.read_csv('transactions.csv')

STREET = [' ul', ' al', ' pl', ' UL', ' Pl', ' Wilkowice ', ' Milejowice ']

contrahents = []
accounts = []

contrahents_list = []

nr = -1

for i in range(df["Dane transakcji"].count()):
    transaction_data = df["Dane transakcji"][i].replace("  ", " ")
    account = transaction_data.split("|")[1].split(":")[1].replace(" ", "")
    if account not in accounts:
        contrahent = transaction_data.split("|")[0].split(":")[1]
        cnt = 0
        for ul in STREET:
            if ul in contrahent:
                contrahent_name = contrahent.split(ul)[0].strip()
                short_name = contrahent_name.title()
                while len(short_name) > 20:
                    short_name = short_name.rsplit(" ", 1)[0]
                name1 = contrahent_name
                while len(name1) > 35:
                    name1 = name1.rsplit(" ", 1)[0]
                name2 = contrahent_name[len(name1):].strip()
                contrahent_address = ul + contrahent.split(ul)[1].strip().replace("- ", "-").replace(" -", "-")
                hyphen = contrahent_address.rfind('-')
                if contrahent_address[hyphen + 1].isdigit() and contrahent_address[hyphen + 2].isdigit():
                    postal_code = contrahent_address[hyphen - 3: hyphen + 5].replace(" ", "")
                    city = contrahent_address[hyphen + 5:].replace(" ", "").title()
                    street = contrahent_address[:hyphen - 3].strip().title()
                    street = street.replace(street[0], street[0].lower(), 1)
                    cnt = 1
                break
        if cnt == 0:
            print(transaction_data)
        else:
            accounts.append(account)
            nr += 1
            contrahents.append(["", "", "", "", "", "", ""])
            contrahents[nr][0] = short_name
            contrahents[nr][1] = account
            contrahents[nr][2] = account[2:10]
            contrahents[nr][3] = name1
            contrahents[nr][4] = name2
            contrahents[nr][5] = street
            contrahents[nr][6] = postal_code + " " + city
csv = ""
for i in contrahents:
    for j in range(7):
        csv += i[j] + ";"
    csv = csv[:-1].replace("_", " ") + "\n"
with open('contrahents.csv', mode="x") as f:
    f.write(csv)