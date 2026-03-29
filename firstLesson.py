print("Hello, World!")
# define a function to greet the user
def greet(name):
    print(f"Hello, {name}!")
# call the function with a namegreet("Alice")
greet("Ufuk")    

# 1'den 100'e kadar asal sayıları yazdıran fonksiyon
def print_primes_1_to_100():
    for num in range(2, 101):
        is_prime = True
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            print(num)

# Fonksiyonu çağır
print_primes_1_to_100()

# haftanın gonlerini yazdıran fonksiyon
def print_weekdays():
    weekdays = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
    for day in weekdays:
        print(day)

# Çift sayıları yazdıran fonksiyon
def print_even_numbers():
    for num in range(2, 101, 2):
        print(num)

# Fonksiyonu çağır
print_even_numbers()

greeting = "good morning"

if greeting == "morning":
    print ("Good morning!")