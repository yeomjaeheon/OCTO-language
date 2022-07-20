class octo_lang:

    def __init__(self, code): #lexing이 이루어짐
        self.code = code + ' ' #chr_pointer 가산에 예외처리를 하지 않기 위해 플레이스홀더로 스페이스 추가
        self.keyword = ['def', 'main', ':', ',', 'return', 'if', 'else', 'elif', '(', ')', '[', ']', '==', '!=', '<=', '>=', '<', '>', '+', '-', '*', '/', '%', '=', 'and', 'or', 'not']
        self.comments = {'//' : '\n', '/*' : '*/'}
        self.number = [chr(i) for i in range(48, 58)]
        self.character = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']
        self.errors = []
        #토큰화
        def classify_word(word):
            if word not in self.keyword:
                if word[0] in self.number:
                    return 'NUMBER'
                elif word[0] in self.character:
                    return 'NAME'
            else:
                classification = {
                    'def' : 'DEFINE', 
                    'return' : 'RETURN', 
                    'main' : 'FUNC_MAIN', 
                    ':' : 'COLON', 
                    ',' : 'COMMA', 
                    'if' : 'IF', 
                    'else' : 'ELSE', 
                    'elif' : 'ELIF', 
                    '(' : 'L_PAREN', 
                    ')' : 'R_PAREN', 
                    '[' : 'L_BRACK', 
                    ']' : 'R_BRACK', 
                    '==' : 'EQUAL', 
                    '!=' : 'NOT_EQUAL', 
                    '<=' : 'LESS_EQUAL', 
                    '>=' : 'GREATER_EQUAL', 
                    '<' : 'LESS', 
                    '>' : 'GREATER', 
                    '+' : 'PLUS', 
                    '-' : 'MINUS', 
                    '*' : 'MULT', 
                    '/' : 'DIV', 
                    '%' : 'MOD', 
                    '=' : 'IS', 
                    'and' : 'AND', 
                    'or' : 'OR', 
                    'not' : 'NOT'
                }

                return classification[word]


        def match_word(word): #단순히 현재 글자 포인터 기준으로 특정 문자열이 나타나는지만을 확인
            if self.chr_pointer <= (len(self.code) - len(word)) and self.code[self.chr_pointer : self.chr_pointer + len(word)] == word:
                return True
            else:
                return False

        def match_keyword(word): #키워드인지 확인, 알파벳으로 이루어졌을 경우 returna처럼 일부만 키워드인 경우를 걸러내기 위한 메소드
            if self.chr_pointer < (len(self.code) - len(word)) and match_word(word):
                if self.code[self.chr_pointer] not in self.character or self.code[self.chr_pointer + len(word)] not in (self.number + self.character):
                    return True
            return False

        self.tokens = []
        self.chr_pointer = 0
        self.found_keyword = False
        self.word_tmp = ''
        self.word_type = None
        self.found_newline = False
        line_tmp = 1
        while self.chr_pointer < len(self.code):
            #주석 처리
            recheck = False
            for com in self.comments.keys():
                if match_word(com):
                    while not match_word(self.comments[com]):
                        self.chr_pointer += 1
                    if self.comments[com] == '\n': #개행 수 세기
                        line_tmp += 1
                    self.chr_pointer += len(self.comments[com])
                    recheck = True
                    break
            #주석 처리가 일어났다면 while 루프 처음으로 복귀
            if recheck:
                continue

            #들여쓰기 처리
            if self.found_newline:
                line_tmp += 1
                self.found_newline = False
                space_tmp = 0
                while match_word(' '):
                    space_tmp += 1
                    self.chr_pointer += 1
                self.tokens.append([space_tmp, 'INDENT'])
            if self.code[self.chr_pointer] == '\n':
                self.found_newline = True
            #워드 처리를 위한 내부 함수
            def append_word():
                if self.word_tmp != '':
                    self.word_type = classify_word(self.word_tmp)
                    self.tokens.append([self.word_tmp, self.word_type])
                    self.word_type = None
                    self.word_tmp = ''

            #키워드 확인
            for word in self.keyword:
                if match_keyword(word):
                    self.chr_pointer += (len(word) - 1)
                    self.found_keyword = True
                    #키워드가 추출된 경우 이전에 추출된 식별자나 숫자를 처리
                    append_word()
                    self.tokens.append([word, classify_word(word)])
                    break

            if self.found_keyword:
                self.found_keyword = False
            #키워드가 나타나지 않았을 경우
            else:
                if self.code[self.chr_pointer] in [' ', '\n']: #공백이나 개행이 나타났을 경우
                    append_word()
                elif self.code[self.chr_pointer] in self.character:
                    self.word_tmp += self.code[self.chr_pointer]
                    if self.word_type == None:
                        self.word_type = 'NAME'
                    elif self.word_type == 'NAME':
                        pass
                    elif self.word_type == 'NUMBER':
                        self.errors.append({'line' : line_tmp, 'index' : len(self.tokens), 'error' : '잘못된 식별자명 : '})
                elif self.code[self.chr_pointer] in self.number:
                    self.word_tmp += self.code[self.chr_pointer]
                    if self.word_type == None:
                        self.word_type = 'NUMBER'

            self.chr_pointer += 1

    def parse(self):
        pass

    def notice_errors(self):
        for e in self.errors:
            print('{0}번째 줄> {1}{2}'.format(e['line'], e['error'], self.tokens[e['index']][0]))

with open('test.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()
    print(code)
    program = octo_lang(code)

print(program.tokens)
program.notice_errors()