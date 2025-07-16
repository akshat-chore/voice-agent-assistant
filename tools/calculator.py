def solve_math(query):
    try:
        result = eval(query)
        return f"The result is {result}"
    except:
        return "Sorry, I couldn’t calculate that."
