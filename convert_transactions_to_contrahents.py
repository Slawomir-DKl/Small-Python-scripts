""" Script converts CSV file with transactions exported from iPKO Biznes account to CSV file for contractor import
Input data structure (unfortunately, with many errors:
"Data realizacji","Data utworzenia","Dane transakcji","Typ","Status","Kwota","Waluta","Biała lista VAT","Data weryfikacji","Sposób realizacji"
Output data structure acc. to:
https://www.pkobp.pl/media_files/1bc6443e-c38b-4282-92ab-aa1618ea1095.pdf
"""

import pandas as pd

df = pd.read_csv('transactions.csv')

STREET = [' ul', ' al', ' pl', ' UL', ' Pl', ' Wilkowice ', ' Milejowice ']

contractors = []
accounts = []
contractors_list = []

nr = -1
print("Unable to process the following entries:")
for i in range(df["Dane transakcji"].count()):
    transaction_data = df["Dane transakcji"][i].replace("  ", " ")
    account = transaction_data.split("|")[1].split(":")[1].replace(" ", "")
    if account not in accounts:
        contractor = transaction_data.split("|")[0].split(":")[1]
        cnt = 0
        for the_street in STREET:
            if the_street in contractor:

                contractor_name = contractor.split(the_street)[0].strip()
                short_name = contractor_name.title()
                while len(short_name) > 20:
                    short_name = short_name.rsplit(" ", 1)[0]
                name1 = contractor_name
                while len(name1) > 35:
                    name1 = name1.rsplit(" ", 1)[0]
                name2 = contractor_name[len(name1):].strip()

                contractor_address = the_street + contractor.split(the_street)[1].strip().replace("- ", "-").replace(" -", "-")
                hyphen = contractor_address.rfind('-')
                if contractor_address[hyphen + 1].isdigit() and contractor_address[hyphen + 2].isdigit():
                    postal_code = contractor_address[hyphen - 3: hyphen + 5].replace(" ", "")
                    city = contractor_address[hyphen + 5:].replace(" ", "").title()
                    street = contractor_address[:hyphen - 3].strip().title()
                    street = street.replace(street[0], street[0].lower(), 1)
                    cnt = 1
                break
        if cnt == 0:
            print(transaction_data)
        else:
            accounts.append(account)
            nr += 1
            contractors.append(["", "", "", "", "", "", ""])
            contractors[nr][0] = short_name
            contractors[nr][1] = account
            contractors[nr][2] = account[2:10]
            contractors[nr][3] = name1
            contractors[nr][4] = name2
            contractors[nr][5] = street
            contractors[nr][6] = postal_code + " " + city

csv = ""

for i in contractors:
    for j in range(7):
        csv += i[j] + ";"
    csv = csv[:-1].replace("_", " ") + "\n"

with open('contractors.csv', mode="x") as f:
    f.write(csv)

print("\nGenerated " + str(len(contractors)) + " contractors")
