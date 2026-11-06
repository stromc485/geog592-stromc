import sys

def say_hello(name):
    print(f"Hello, {name}!")

def main():
    name = sys.argv[1] # will return an error because the list is empty if no argument is passed
    say_hello(name)

if __name__ == "__main__":
    main()