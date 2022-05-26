#진행상황 : 토큰 분석 기능 완료, 브레인퍽 코드 생성 부분 구현할 것
#변수도 함수로 간주하기, 조건문 안에 들어있는 코드도 함수로 간주, 모든 것을 함수로 간주

class function:
    def __init__(self, name, parameter_names, tokens):
        self.name = name
        self.parameter_names = parameter_names
        self.tokens = tokens

    def extract_inner_functions(self):
        pass

class octo_lang_core:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.functions = {}
        self.chr_pointer = 0

        #주석 처리 키워드와 종료 키워드, 문자열 안에서는 무시되어야 함
        self.ignore_codes = {
            '//' : '\n', 
            '/*' : '*/'
        }

        self.keywords = {
            'brainfuck_input' : ['brainfuck_input', 'brainfuck'], 
            'brainfuck_output' : ['brainfuck_output', 'brainfuck'], 
            'func' : ['func', 'function'], 
            'main' : ['main', 'function'], 
            'return' : ['return', 'function'], 
            'if' : ['if', 'statement'], 
            'else' : ['else', 'statement'], 
            'not' : ['not', 'operator'], 
            'and' : ['and', 'operator'], 
            'or' : ['or', 'operator'], 
            '==' : ['==', 'operator'], 
            '!=' : ['!=', 'operator'], 
            '>=' : ['>=', 'operator'], 
            '<=' : ['<=', 'operator'], 
            '(' : ['(', 'symbol'], 
            ')' : [')', 'symbol'], 
            '[' : ['(', 'symbol'], 
            ']' : [')', 'symbol'], 
            ':' : [':', 'symbol'],
            ',' : [',', 'symbol'], 
            '\n' : ['\n', 'symbol'], 
            'pass' : ['pass', 'symbol'], 
            #부분적으로 겹치는 키워드들을 처리하기 위해 키워드를 순서를 정해 저장하였음
            '=' : ['=', 'operator'], 
            '+' : ['+', 'operator'], 
            '-' : ['-', 'operator'], 
            '/' : ['/', 'operator'], #몫의 나눗셈
            '*' : ['*', 'operator'], 
            '%' : ['%', 'operator'], 
            '>' : ['>', 'operator'], 
            '<' : ['<', 'operator'], 
            }

        self.processing_state = {
            'keyword_match' : False
        }

    def name_valid(self, name):
        if name[0].isalpha():
            for part in name.split('_'):
                if not part.isalnum():
                    return False
            return True
        else:
            return False

    def text_match(self, keyword):
        if self.space_match(len(keyword)) and self.code[self.chr_pointer : self.chr_pointer + len(keyword)] == keyword:
            return True
        else:
            return False

    def space_match(self, length):
        if self.chr_pointer < (len(self.code) - length + 1):
            return True
        else:
            return False

    #토큰 추출
    def tokenize(self):
        identifier = ''
        while self.chr_pointer < len(self.code):
            #들여쓰기 추출
            if len(self.tokens) == 0 or self.tokens[-1] == self.keywords['\n']:
                space_indent = 0
                while self.code[self.chr_pointer] == ' ':
                    space_indent += 1
                    self.chr_pointer += 1
                self.tokens.append([space_indent, 'space_indent'])

            #주석 처리
            for ignore in self.ignore_codes.keys():
                if self.text_match(ignore):
                    while self.space_match(len(self.ignore_codes[ignore])) and not self.text_match(self.ignore_codes[ignore]):
                        self.chr_pointer += 1
                    self.chr_pointer += len(self.ignore_codes[ignore])

            #키워드 추출
            for keyword in self.keywords.keys():
                if self.text_match(keyword):
                    #일부분만 키워드처럼 보이는 경우 배제
                    self.processing_state['keyword_match'] = True
                    if self.name_valid(keyword):
                        self.processing_state['keyword_match'] = not (self.space_match(len(keyword) + 1) and self.name_valid(self.code[self.chr_pointer : self.chr_pointer + len(keyword) + 1]))

                    if self.processing_state['keyword_match']:
                        #추출된 식별자를 저장
                        if len(identifier) > 0:
                            if self.name_valid(identifier):
                                self.tokens.append([identifier, 'function'])
                            elif identifier.isnumeric():
                                self.tokens.append([int(identifier), 'number'])
                            identifier = ''
                        self.tokens.append(self.keywords[keyword])
                        self.chr_pointer += len(keyword)
                    break
                    
            if self.processing_state['keyword_match']:
                self.processing_state['keyword_match'] = False

            #키워드가 추출되지 않았을 경우 식별자 추출 시도, 오류 메세지는 일단 구현을 나중으로 미룬다
            else:
                if self.code[self.chr_pointer].isalnum() or self.code[self.chr_pointer] == '_':
                    identifier += self.code[self.chr_pointer]
                self.chr_pointer += 1

    def build_function(self, info, tokens):
        pass

    #추출된 토큰에서 각 함수의 정의를 추출
    def analyze(self):
        token_pointer = 0
        while token_pointer < len(self.tokens):
            pass

with open('test.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()

octo = octo_lang_core(code)
octo.tokenize()
#octo.analyze()
for t in octo.tokens:
    if t[1] != 'space_indent':
        print(t[0], end = ' ')
    else:
        print(' ' * t[0], end = '')