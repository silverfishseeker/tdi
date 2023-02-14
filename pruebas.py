def a():
    def b():
        print("b")
    print("a")
    b()
a()