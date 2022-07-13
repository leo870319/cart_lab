import cart

catalogue = open("list.json", "r")
shoping_list = open("case2.txt", "r")
shoping_list = cart.cart(shoping_list, catalogue)
print(f"{shoping_list.sum:.2f}")
