from main import *

kebapbois = []


def get_kebapbois_titlecase():
    kebapbois_titlecase = []
    for kebapboi in kebapbois:
        kebapbois_titlecase.append(kebapboi["name"].title())
    return kebapbois_titlecase


def print_kebapbois_titlecase():
    kebapbois_titlecase = get_kebapbois_titlecase()
    print(kebapbois_titlecase)


def add_kebapboi(name, kebaps=0):
    kebapboi = {"name": name, "kebaps": kebaps}
    kebapbois.append(kebapboi)


def save_file(kebapboi):
    try:
        f = open("kebapstats.txt", "a")
        f.write(kebapboi + "\n")
        f.close()
    except Exception:
        print("Could not save file")


def read_file():
    try:
        f = open("kebapstats.txt", "r")
        for kebapboi in f.readlines():
            add_kebapboi(kebapboi)
        f.close()
    except Exception:
        print("Could not read file")


read_file()
print_kebapbois_titlecase()

kebapboi_name = input("Enter a Kebapboi: ")
kebapboi_kebaps = input("How many Kebaps did you eat so far: ")

add_kebapboi(kebapboi_name, kebapboi_kebaps)
save_file("\n" + kebapboi_name + "           | " + kebapboi_kebaps + "                 |")
