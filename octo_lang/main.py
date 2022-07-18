class octo_lang:
    def match_word(self, word): #단순히 현재 글자 포인터 기준으로 특정 문자열이 나타나는지만을 확인
        if self.chr_pointer <= (len(self.code) - len(word)) and self.code[self.chr_pointer : self.chr_pointer + len(word)] == word:
            return True
        else:
            return False

    def match_keyword(self, word): #키워드인지 확인, returna처럼 일부만 키워드인 경우를 걸러내기 위한 메소드
        if self.chr_pointer < (len(self.code) - len(word)) and self.match_word(word):
            if self.code[self.chr_pointer + len(word)] in [' ', '\n']:
                return True
        return False

    def __init__(self, code):
        self.code = code + ' ' #chr_pointer 가산에 예외처리를 하지 않기 위해 플레이스홀더로 스페이스 추가
        self.keyword = ['def', 'return', 'if', 'else', 'elif', '(', ')', '[', ']', '+', '-', '*', '/', '%', '=', 'and', 'or', '=!', '==']
        self.number = [chr(i) for i in range(48, 58)]
        self.character = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']
        #토큰화
        self.tokens = []
        self.chr_tmp = ''
        self.chr_pointer = 0
        self.found_keyword = False
        while self.chr_pointer < len(self.code):
            #키워드 확인
            for word in self.keyword:
                if self.match_keyword(word):
                    self.chr_pointer += (len(word) - 1)
                    self.found_keyword = True
                    self.tokens.append(word)
            self.chr_pointer += 1

with open('test.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()
    print(code)
    program = octo_lang(code)

print(program.tokens)