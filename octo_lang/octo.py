#octo language

import sys

'''
진행상황 : 토큰 추출 구현 완료

*토큰 분석 단계에서 indent 오류를 잡아주는 기능 구현할 것
*문자열 안에서는 주석처리 되지 않도록 할 것.
*빈 줄에 대해서는 indent가 맞지 않더라도 오류로 처리하지 않는 예외 처리 넣어줄 것
*실제 처리 과정에서 변수와 함수를 구분하지 말 것(변수는 사실상 상수함수와 다르지 않으므로)
'''

class octo_lang:
    def __init__(self, code):
        self.code = code

        #주석 처리 규칙 
        self.ignore_keyword = {
            '//' : '\n', 
            '/*' : '*/'
        }
        #키워드
        self.keyword = [
            {
                '+' : ['operator', '+'], 
                '-' : ['operator', '-'], 
                '*' : ['operator', '*'], 
                '/' : ['operator', '/'], 
                '%' : ['operator', '%'], 
                '^' : ['operator', '^'], 
                '(' : ['indicator', '('],  
                ')' : ['indicator', ')'], 
                ':' : ['indicator', ':'], 
                ',' : ['indicator', ','], 
                '\n' : ['indicator', '\n'], 
                '\\n' : ['newline_indicator', '\\n'], 
                '\'' : ['indicator', '\''], 
                'int' : ['type_indicator', 'int'], 
                '==' : ['comparison_operator', '=='], 
                '!=' : ['comparison_operator', '!='], 
                '>' : ['comparison_operator', '>'], 
                '<' : ['comparison_operator', '<'], 
                '>=' : ['comparison_operator', '>='], 
                '<=' : ['comparison_operator', '<=']
            }, 
            {
                'if' : ['control_statement', 'if'], 
                'elif' : ['control_statement', 'elif'], 
                'else' : ['control_statement', 'else'], 
                'func' : ['function_definition', 'func'], 
                'main' : ['main_function', 'main'], 
                'return' : ['function_return', 'return'], 
                'int' : ['builtin_function', 'int'], 
                'gets' : ['builtin_function', 'gets'], 
                'puts' : ['builtinfunction', 'puts'], 
                'and' : ['logical_operator', 'and'], 
                'or' : ['logical_operator', 'or'], 
                'not' : ['logical_operator', 'not'], 
                '=' : ['constant_definition', '=']
            }
        ]
        #변수명 및 함수명 작명 규칙, 인덱스 0는 머리글자, 인덱스 1은 이후 글자의 규칙이다(알파벳과 언더바로 시작, 뒤로는 숫자까지 이어질 수 있음)
        self.identifier_naming_rules = [
                list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))) + ['_'],
            list(map(chr, range(48, 58))) + list(map(chr, range(65, 91))) + list(map(chr, range(97, 123))) + ['_']
            ]

        #상수 규칙, 0~9로 시작, 이후에는 0~9가 이어질 수 있음, -의 경우는 토큰 분석 단계에서 처리, 0만 있는 경우는 밑에서 예외처리 해주었음
        self.constant_rules = [list(map(chr, range(49, 58))), list(map(chr, range(48, 58)))]

        #토큰 저장
        self.token = []

    def disassemble(self): #현재까지는 주석 처리 및 키워드 추출만 구현됨, 식별자 추출은 곧 구현 예정
        chr_pointer = 0 #코드 포인터
        line_split = self.code.split('\n')
        line_split_len = [(len(line) + 1) for line in line_split] #코드 각 줄의 글자수, 개행 문자를 계산에 포함하기 위해 1을 더함
        line_counter = 0 #몇 번째 줄인지 기록
        keyword_match = False #키워드가 인식되었을 경우 True로 설정
        string_start = False #작은따옴표가 시작되었을 경우 True로 설정
        word = '' #식별자 및 값 저장
        word_type = None #word에 저장된 문자열의 의미(식별자, 상수, 문자열)를 저장
        while chr_pointer < len(self.code):
            for i in range(0, len(line_split)):
                if chr_pointer < sum(line_split_len[:i + 1]):
                    line_counter = i + 1
                    break
            #주석 처리
            if not string_start:
                for k in self.ignore_keyword.keys(): #주석 처리 규칙에서 주석 처리 시작 문자열을 가지고 옴
                    if chr_pointer < len(self.code) - (len(k) - 1):
                        if self.code[chr_pointer : chr_pointer + len(k)] == k:
                            while chr_pointer < len(self.code):
                                #현재 코드 포인터가 가리키는 위치에서 앞쪽으로 주석 처리 종료 문자열이 등장하는지 검사
                                if chr_pointer >= len(self.ignore_keyword[k]) - 1:
                                    #주석 처리 종료 문자열을 만났을 경우
                                    if self.code[chr_pointer - (len(self.ignore_keyword[k]) - 1) : chr_pointer + 1] == self.ignore_keyword[k]:
                                        chr_pointer += 1
                                        break
                                chr_pointer += 1

            indent_check = False #들여쓰기 검사 여부
            if len(self.token) == 0:
                indent_check = True
            elif self.token[-1] == self.keyword[0]['\n']:
                indent_check = True
            #들여쓰기 추출(일단 스페이스만 구현)
            if indent_check:
                space_counter = 0
                if self.code[chr_pointer] == ' ':
                    while chr_pointer < len(self.code):
                        if self.code[chr_pointer] == ' ':
                            space_counter += 1
                            chr_pointer += 1
                        else:
                            break
                self.token.append(['space_indent', space_counter])
                        
            #부분적으로 글자가 겹치는 키워드들이 있어 처리 순서를 나눔
            for process_level in range(0, len(self.keyword)):
                for k in self.keyword[process_level].keys():
                    if chr_pointer < len(self.code) - (len(k) - 1):
                        if self.code[chr_pointer : chr_pointer + len(k)] == k:
                            #인식된 키워드가 식별자(변수명 및 함수명) 작명 규칙을 만족하는지 확인하고 그렇다면 키워드를 추출하지 않음
                            #변수명으로 쓴 'funcl'에서 키워드 'func'를 추출해 버리는 오류 방지 
                            #키워드 끝 바로 다음의 글자를 검사하기 위해 키워드의 끝이 소스코드의 끝이 아닌지 확인
                            if chr_pointer < len(self.code) - (len(k) - 1) - 1:
                                #머리글자부터 규칙에 해당될 경우
                                if k[0] not in self.identifier_naming_rules[0]:
                                    keyword_match = True

                                #이후 글자가 규칙에 해당될 경우
                                else:
                                    if self.code[chr_pointer + len(k)] not in self.identifier_naming_rules[1]:
                                        keyword_match = True
                            else:
                                keyword_match = True
                            
                            #작은따옴표가 시작되었을 경우 키워드로 인식하지 않음
                            if string_start:
                                keyword_match = False

                            #키워드로 인식 되었을 경우
                            if keyword_match:
                                #이전에 추출된 식별자를 토큰에 추가
                                if word != '':
                                    self.token.append([word_type, word])
                                    word = ''
                                chr_pointer += (len(k) - 1) #코드 포인터를 키워드 끝 글자로 이동
                                if self.token[-1] == self.keyword[0]['\'']: #작은따옴표가 시작되고 끝남에 따라 string_start를 관리
                                    if string_start:
                                        #추출된 문자열을 토큰에 추가
                                        self.token.append([word_type, word])
                                        word = ''
                                        string_start = False
                                    else:
                                        string_start = True
                                self.token.append(self.keyword[process_level][k]) #키워드 추가
                                break
                if keyword_match:
                    break
            
            #식별자 및 값 추출
            if keyword_match:
                keyword_match = False

            #키워드가 아닐 경우
            else:
                if string_start:
                    word_type = 'string'
                    word += self.code[chr_pointer]
                else:
                    if word == '':
                        if self.code[chr_pointer] in self.identifier_naming_rules[0]:
                            word_type = 'identifier'
                            word += self.code[chr_pointer]
                        elif self.code[chr_pointer] == '0':
                            word_type = 'zero' #'07', '0058'과 같은 오류를 걸러내기 위해 'zero'로 구분해 저장
                            word += self.code[chr_pointer]
                        elif self.code[chr_pointer] in self.constant_rules[0]:
                            word_type = 'integer' #추후에 부동소수점이 추가될 때를 대비해 일단 'interger'로 저장
                            word += self.code[chr_pointer]
                        elif self.code[chr_pointer] not in ['\n', ' ']:
                            self.alert_error(line_counter, 'systax error : {0}'.format(self.code[chr_pointer]))
                    else:
                        if word_type == 'identifier':
                            if self.code[chr_pointer] in self.identifier_naming_rules[1]:
                                word += self.code[chr_pointer]
                            elif self.code[chr_pointer] not in ['\n', ' ']:
                                self.alert_error(line_counter, 'systax error : {0}'.format(self.code[chr_pointer]))
                            else:
                                #추출된 문자열을 토큰에 추가
                                self.token.append([word_type, word])
                                word = ''
                        elif word_type == 'integer':
                            if self.code[chr_pointer] in self.constant_rules[1]:
                                word += self.code[chr_pointer]
                            elif self.code[chr_pointer] not in ['\n', ' ']:
                                self.alert_error(line_counter, 'systax error : {0}'.format(self.code[chr_pointer]))
                            else:
                                #추출된 문자열을 토큰에 추가
                                self.token.append([word_type, word])
                                word = ''
                        elif word_type == 'zero':
                            if self.code[chr_pointer] not in ['\n', ' ']: #추후에 부동소수점을 추가한다면 이 부분에서 '.'에 관한 처리 추가할 것
                                self.alert_error(line_counter, 'systax error : {0}'.format(self.code[chr_pointer]))
                            else:
                                #추출된 문자열을 토큰에 추가
                                self.token.append([word_type, word])
                                word = ''

            chr_pointer += 1 #코드 포인터를 다음 글자로 이동

    #추출된 토큰을 분석
    def parse(self):
        pass

    #오류 보고
    def alert_error(self, line_number, reason):
        print('Error occurred in line {0} : {1}'.format(line_number, reason))
        sys.exit()

with open('octo_lang\\test_code.octo', 'r', encoding = 'utf-8') as f:
    code = f.read()

octo = octo_lang(code)
octo.disassemble()
for t in octo.token:
    if t[0] != 'space_indent':
        print(t[1] + ' ', end = '')