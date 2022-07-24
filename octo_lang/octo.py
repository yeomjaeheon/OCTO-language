from inspect import Parameter
import sys
from textwrap import indent

class octo_lang:

    def __init__(self, code): #lexing이 이루어짐
        self.code = code + ' ' #chr_pointer 가산에 예외처리를 하지 않기 위해 플레이스홀더로 스페이스 추가
        self.keyword = {
                    'output_integer' : 'NAME', #아스키 출력을 위한 빌트인 함수
                    'input_interger' : 'NAME', #아스키 입력을 위한 빌트인 함수
                    'def' : 'DEFINE', 
                    'return' : 'RETURN', 
                    'main' : 'NAME', #특수 함수, 없으면 오류
                    ':' : 'COLON', 
                    ',' : 'COMMA', 
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
        self.built_in_functions = ['output_integer', 'input_interger']
        self.comments = {'//' : '\n', '/*' : '*/'}
        self.number = [chr(i) for i in range(48, 58)]
        self.character = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)] + ['_']
        self.errors = []
        #토큰화

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
        self.line_tmp = 1
        while self.chr_pointer < len(self.code):
            #주석 처리
            recheck = False
            for com in self.comments.keys():
                if match_word(com):
                    while not match_word(self.comments[com]):
                        if self.code[self.chr_pointer] == '\n': #개행 수 세기
                            self.line_tmp += 1
                        self.chr_pointer += 1
                    if self.comments[com] == '*/':
                        self.chr_pointer += len(self.comments[com])
                    recheck = True
                    break
            #주석 처리가 일어났다면 while 루프 처음으로 복귀
            if recheck:
                continue

            #들여쓰기 처리
            if self.found_newline:
                self.line_tmp += 1
                self.found_newline = False
                space_tmp = 0
                while match_word(' '):
                    space_tmp += 1
                    self.chr_pointer += 1
                self.tokens.append(['INDENT', space_tmp, self.line_tmp])
            if self.code[self.chr_pointer] == '\n':
                self.found_newline = True
            #워드 처리를 위한 내부 함수
            def append_word():
                if self.word_tmp != '':
                    #self.word_type = classify_word(self.word_tmp)
                    if self.word_type == 'INTEGER':
                        try:
                            self.word_tmp = int(self.word_tmp)
                        except:
                            print('{0}번째 줄> 오류 : 잘못된 정수 {1}'.format(self.line_tmp, self.word_tmp))
                            sys.exit()
                    if self.word_type == 'WEIRD_NAME':
                        print('{0}번째 줄> 오류 : 잘못된 이름 {1}'.format(self.line_tmp, self.word_tmp))
                        sys.exit()
                    self.tokens.append([self.word_type, self.word_tmp, self.line_tmp])
                    self.word_type = None
                    self.word_tmp = ''

            #키워드 확인
            for word in self.keyword.keys():
                if match_keyword(word):
                    self.chr_pointer += (len(word) - 1)
                    self.found_keyword = True
                    #키워드가 추출된 경우 이전에 추출된 식별자나 숫자를 처리
                    append_word()
                    self.tokens.append([self.keyword[word], word, self.line_tmp])
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
                    elif self.word_type == 'INTEGER':
                        pass
                elif self.code[self.chr_pointer] in self.number:
                    self.word_tmp += self.code[self.chr_pointer]
                    if self.word_type == None:
                        self.word_type = 'INTEGER'
                else:
                    self.word_tmp += self.code[self.chr_pointer]
                    self.word_type = 'WEIRD_NAME'

            self.chr_pointer += 1
        self.tokens.append(['END', 'END', self.line_tmp])

    def parse(self):
        #현재 라인 수는 각 토큰의 index 2에 있음
        self.parse_tree = {}
        self.indent_data = [] #들여쓰기 칸 수 기록
        self.parent_data = [] #부모 함수 파싱 트리 주소 기록
        self.parent_name_data = [] #부모 함수 이름 기록

        self.parent_data.append(self.parse_tree)
        self.parent_name_data.append('')

        self.in_block = False
        self.token_pointer = 0
        for b in self.built_in_functions:
            self.parse_tree[b] = {'parameters' : 1, 'block' : [], 'nested_functions' : [], 'variables' : [{'name' : 'n', 'type' : 'INTEGER', 'value' : None}]}

        def get_token():
            self.token_pointer += 1
            return self.tokens[self.token_pointer - 1]

        def process_function(nested = False): #내부 함수용 처리는 따로 만들어야 함
            if self.token[0] == 'NAME':
                if self.token[1] not in self.parent_data[-1].keys():
                    if nested:
                        self.parent_data[-1]['nested_functions'].append({'parameters' : 0, 'block' : [], 'nested_functions' : [], 'variables' : []})
                        self.parent_data.append(self.parent_data[-1]['nested_functions'][-1])
                        self.parent_name_data.append(self.token[1])
                    else:
                        self.parse_tree[self.token[1]] = {'parameters' : 0, 'block' : [], 'nested_functions' : [], 'variables' : []} #변수 중 처음 ['parameters']개의 변수가 매개변수
                        self.parent_data.append(self.parse_tree[self.token[1]])
                        self.parent_name_data.append(self.token[1])
                    self.token = get_token()
                    if self.token[0] == 'L_PAREN':
                        self.token = get_token()
                        process_function_parameter() #닫는 소괄호를 찾을 때까지
                        self.token = get_token()
                        if self.token[0] == 'COLON':
                            self.token = get_token()
                            self.in_block = True
                            process_function_block()
                            #함수 파싱 마치는 처리 필요
                            '''
                            if self.token[0] == 'INDENT': #아마 이 부분도 블럭에서 알아서 처리 하게 해야될 듯
                                print(self.token[1])
                                if self.token[1] > self.indent_data[-1]:
                                    self.indent_data.append(self.token[1])
                                    self.in_block = True
                                    self.token = get_token()
                                    process_function_block()
                                    #함수 파싱 마치는 처리 필요
                                    sys.exit()
                            elif self.token[0] == 'END':
                                print('{0}번째 줄> 오류 : 완전하게 정의되지 않은 함수 {1}'.format(self.token[2], self.parent_name_data[-1]))
                                sys.exit()
                            else:
                                print('{0}번째 줄> 오류 : {1}'.format(self.token[2], self.token[1]))
                                sys.exit()
                            '''
                        else:
                            print('{0}번째 줄> 오류 : 세미콜론이 없음'.format(self.token[2]))
                            sys.exit()
                    else:
                        print('{0}번째 줄> 오류 : 여는 소괄호가 없음'.format(self.token[2]))
                        sys.exit()
                else:
                    print('{0}번째 줄> 오류 : 중복 정의된 함수 {1}'.format(self.token[2], self.token[1]))
                    sys.exit()
            else:
                print('{0}번째 줄> 오류 : 함수명을 찾을 수 없음'.format(self.token[2]))
                sys.exit()

        def process_function_parameter():
            while self.token[0] != 'R_PAREN':
                if self.token[0] == 'NAME':
                    if self.token[1] not in self.parent_data[-1]['variables']:
                        self.parent_data[-1]['parameters'] += 1
                        self.parent_data[-1]['variables'].append({'name' : self.token[1], 'type' : 'unknown', 'value' : None})
                    else:
                        print('{0}번째 줄> 오류 : 중복된 매개변수 {1}'.format(self.token[2], self.token[1]))
                        sys.exit()
                elif self.token[0] in ['INDENT', 'END', 'COLON']:
                    print('{0}번째 줄> 오류 : 소괄호가 닫히지 않음'.format(self.token[2]))
                    sys.exit()
                else:
                    print('{0}번째 줄> 오류 : {1}'.format(self.token[2], self.token[1]))
                    sys.exit()
                self.token = get_token()
                if self.token[0] == 'COMMA':
                    self.token = get_token()
                elif self.token[0] == 'R_PAREN':
                    pass
                elif self.token[0] in ['INDENT', 'END', 'COLON']:
                    print('{0}번째 줄> 오류 : 소괄호가 닫히지 않음'.format(self.token[2]))
                    sys.exit()
                else:
                    print('{0}번째 줄> 오류 : {1}'.format(self.token[2], self.token[1]))
                    sys.exit()

        def process_function_block(): #이제 이거 구현하면 됨
            while True:
                if self.token[0] == 'INDENT':
                    print('P')
                if self.token[0] == 'DEFINE':
                    self.token = get_token()
                    process_function(nested = True)
                    #함수 인식 후처리
                if self.token[0] == 'RETURN':
                    self.token = get_token()
                    process_return()
                    #리턴 후 처리
                elif self.token[0] == 'NAME':
                    pass
                self.token = get_token()

        def process_expression():
            pass

        def process_call():
            pass

        def process_return():
            pass

        '''
        이름 중복 관련 대응 방안 : 
        내부 함수는 바깥 함수의 변수에 함부로 접근할 수 없음(매개변수로 입력 받아야만 함)
        기본 함수의 경우 내부 함수와 다른 함수의 이름이 같다면 내부 함수를 호출
        '''

        while True:
            self.token = get_token()
            if self.token[0] == 'DEFINE':
                self.token = get_token()
                process_function()
                self.parent_data.pop()
                self.parent_name_data.pop()
                #indent 관련한 처리
            elif self.token[0] == 'INDENT':
                self.indent_data.append(self.token[1])
            elif self.token[0] == 'END':
                break
            else:
                print('{0}번째 줄> 오류 : {1}'.format(self.token[2], self.token[1]))
                sys.exit()
            print(self.parse_tree)

with open('test.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()
    print(code)

program = octo_lang(code)
print(program.tokens)
program.parse()