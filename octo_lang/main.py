from ast import keyword


class octo_lang:
    def match_word(self, word): #단순히 현재 글자 포인터 기준으로 특정 문자열이 나타나는지만을 확인
        if self.chr_pointer <= (len(self.code) - len(word)) and self.code[self.chr_pointer : self.chr_pointer + len(word)] == word:
            return True
        else:
            return False

    def match_keyword(self, word): #키워드인지 확인, returna처럼 일부만 키워드인 경우를 걸러내기 위한 메소드
        if self.chr_pointer < (len(self.code) - len(word)) and self.match_word(word):
            if self.code[self.chr_pointer + len(word)] not in (self.number + self.character):
                return True
        return False

    def classify_word(self, word):
        if word not in self.keyword:
            if word[0] in self.number:
                return 'number'
            elif word[0] in self.character:
                return 'identifier'
        else:
            if word in ['if', 'else', 'elif']:
                return 'control_flow'
            elif word in ['def']:
                return 'function_definition'
            elif word in ['main']:
                return 'function_start'
            elif word in ['return']:
                return 'return'
            elif word in [':']:
                return 'colon'
            elif word in ['(', ')']:
                return 'parenthesis'
            elif word in ['[', ']']:
                return 'bracket'
            elif word in ['and', 'or', 'not']:
                return 'logical_operator'
            elif word in ['+', '-', '*', '/', '%']:
                return 'operator'
            elif word in ['=!', '==', '<', '>', '<=', '>=']:
                return 'compare_operator'

    def __init__(self, code):
        self.code = code + ' ' #chr_pointer 가산에 예외처리를 하지 않기 위해 플레이스홀더로 스페이스 추가
        self.keyword = ['def', 'main', ':', 'return', 'if', 'else', 'elif', '(', ')', '[', ']', '==', '!=', '<=', '>=', '<', '>', '+', '-', '*', '/', '%', '=', 'and', 'or', 'not']
        self.comments = {'//' : '\n', '/*' : '*/'}
        self.number = [chr(i) for i in range(48, 58)]
        self.character = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']
        #토큰화
        self.tokens = []
        self.chr_pointer = 0
        self.found_keyword = False
        self.word_tmp = ''
        self.word_type = None
        while self.chr_pointer < len(self.code):
            #주석 처리
            for com in self.comments.keys():
                if self.match_word(com):
                    while not self.match_word(self.comments[com]):
                        self.chr_pointer += 1
                    self.chr_pointer += len(self.comments[com])
            #키워드 확인
            for word in self.keyword:
                if self.match_keyword(word):
                    self.chr_pointer += (len(word) - 1)
                    self.found_keyword = True
                    self.tokens.append([word, self.classify_word(word)])
                    break
            self.chr_pointer += 1
            #키워드가 추출된 경우 이전에 추출된 식별자나 숫자를 처리
            if self.found_keyword:
                pass
            #키워드가 추출되지 않았을 경우 식별자나 숫자를 추출
            else:
                pass

with open('test.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()
    print(code)
    program = octo_lang(code)

print(program.tokens)