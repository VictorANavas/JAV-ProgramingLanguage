import basicMath

#Basic loop to give me the output I need
while True:
    text = input('basicMath > ')
    result, error = basicMath.run('<stdin>', text)

    if error: print(error.as_string())
    else: print(result)
