from economy import Economy

eco = Economy()
eco.open()

text = """
Choose an Action
1) Add Money to User
2) Remove Money From User
3) See money of User
4) Set Money of User
5) Delete User
"""

while True:
    print(text)
    act = int(input(">>"))
    id = int(input("User ID >>"))
    if act == 1:
        amt = int(input("Amount >>"))
        eco.add_money(id, amt)
    elif act == 2:
        amt = int(input("Amount >>"))
        eco.remove_money(id, amt)
    elif act == 4:
        amt = int(input("Amount >>"))
        eco.set_money(id, amt)
    elif act == 5:
        eco.remove_entry(id)
    print("\n" + str(eco.get_entry(id)[1]))