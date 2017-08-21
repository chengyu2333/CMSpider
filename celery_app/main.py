from tasks import add

result = add.delay(2,5)
print("ok")
print(result.get())
