class octo_lang:
    def __init__(self, code):
        self.code = code
        self.basic_keywords = ['def', 'return', 'if', 'else', 'elif', '(', ')', '[', ']', '+', '-', '*', '/', '%', '=', 'and', 'or', '=!', '==']
        self.number = [chr(i) for i in range(48, 58)]
        self.character = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']