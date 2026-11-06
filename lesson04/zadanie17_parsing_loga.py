# Lekcja 04 - Zadanie 17: Parsing loga treningowego

log = "Epoch 23/100 - loss: 0.3421 - accuracy: 0.8934 - val_loss: 0.4102 - val_accuracy: 0.8712"

# Podział loga na poszczególne fragmenty
fragmenty = log.split(" - ")

# Wyodrębnienie numeru epoki i liczby epok
epoki = fragmenty[0].strip().split(" ")[1].split("/")

numer_epoki = int(epoki[0])
total_epok = int(epoki[1])

# Wyodrębnienie metryk
loss = float(fragmenty[1].split(":")[1].strip())
accuracy = float(fragmenty[2].split(":")[1].strip())
val_loss = float(fragmenty[3].split(":")[1].strip())
val_accuracy = float(fragmenty[4].split(":")[1].strip())

# Obliczenie różnicy dokładności
roznica_accuracy = accuracy - val_accuracy

# Budowanie raportu
print("=" * 50)
print(f"{'RAPORT TRENINGU MODELU':^50}")
print("=" * 50)

print(f"{'Epoka:':<25} {numer_epoki}/{total_epok}")

print("-" * 50)

print(f"{'Train loss:':<25} {loss:.4f}")
print(f"{'Train accuracy:':<25} {accuracy:.2%}")

print(f"{'Validation loss:':<25} {val_loss:.4f}")
print(f"{'Validation accuracy:':<25} {val_accuracy:.2%}")

print("-" * 50)

print(f"{'Różnica accuracy:':<25} {roznica_accuracy:.2%}")

if roznica_accuracy > 0:
    print("Train accuracy jest wyższe od validation accuracy.")
    print("Możliwy sygnał overfittingu.")
elif roznica_accuracy < 0:
    print("Validation accuracy jest wyższe od train accuracy.")
else:
    print("Train i validation accuracy są identyczne.")

print("=" * 50)
