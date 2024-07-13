import sys
from typing import Union, List
from enum import Enum

class JsonTokenInfo:
    def __init__(self, symbol: str, action: str, next_token: Union['JsonTokens', List['JsonTokens'], None]):
        self.symbol = symbol
        self.action = action
        self.next_token = next_token

class JsonTokens(Enum):
    OPEN_BRACE = JsonTokenInfo('{', 'disolve', ['KEY_OPENER', 'CLOSED_BRACE'])
    KEY_OPENER = JsonTokenInfo('"', 'find', 'KEY_CLOSER')
    KEY_CLOSER = JsonTokenInfo('"', 'expect', 'COLON')
    COLON = JsonTokenInfo(':', 'disolve', ['VAL_OPENER', 'BOOLEAN_TRUE','BOOLEAN_FALSE', 'NULL', 'NUMBER', 'OPEN_BRACE'])
    VAL_OPENER = JsonTokenInfo('"', 'find', 'VAL_CLOSER')
    VAL_CLOSER = JsonTokenInfo('"', 'disolve', ['COMMA', 'CLOSED_BRACE'])
    COMMA = JsonTokenInfo(',', 'expect', 'KEY_OPENER')
    CLOSED_BRACE = JsonTokenInfo('}', 'finish', ['COMMA', 'CLOSED_BRACE'])
    BOOLEAN_TRUE = JsonTokenInfo('t', 'parse_bool', ['COMMA', 'CLOSED_BRACE'])
    BOOLEAN_FALSE = JsonTokenInfo('f', 'parse_bool', ['COMMA', 'CLOSED_BRACE'])
    NULL = JsonTokenInfo('n', 'parse_null', ['COMMA', 'CLOSED_BRACE'])
    NUMBER = JsonTokenInfo("0123456789", 'parse_number', ['COMMA', 'CLOSED_BRACE'])


class JsonParser():



    def __init__(self, content):
        self.content = content.strip()
        self.content = self.content.replace('\n', '')
        self.content+= ' '
        self.depth = 0
        self.cursor = 0
        self.cursorLimit = len(self.content)
        self.funcMap = {
            'expect': self.expect_token,
            'find': self.find_token,
            'disolve': self.disolve_token,
            'finish': self.finish,
            'parse_bool': self.parse_bool,
            'parse_null': self.parse_null,
            'parse_number': self.parse_number
        }
    
    def parse(self):
        self.expect_token('OPEN_BRACE')
    
    def parse_number(self, token_list):
        self.backward_cursor()
        while self.content[self.cursor].isdigit():
            self.forward_cursor()
        self.disolve_token(token_list)
        

    def parse_bool(self, token_list):
        self.backward_cursor()
        try:
            if self.content[self.cursor:self.cursor+4] == 'true':
                self.forward_cursor(4)
            elif self.content[self.cursor:self.cursor+5] == 'false':
                self.forward_cursor(5)
            else:
                raise Exception("Invalid Json")
            self.disolve_token(token_list)
        except Exception as e:
            raise e
        
    def parse_null(self, token_list):
        self.backward_cursor()
        try:
            if self.content[self.cursor:self.cursor+4] == 'null':
                self.forward_cursor(4)
            else:
                raise Exception("Invalid Json")
            self.disolve_token(token_list)
        except Exception as e:
            raise e
        
    
    def skip_space(self):
        try:
            while self.content[self.cursor]==' ':
                self.forward_cursor()
        except Exception:
            raise Exception("Invalid Json")
    
    def forward_cursor(self, step = None):
        if not step:
            self.cursor += 1
        else:
            self.cursor += step
        if self.cursor >= self.cursorLimit:
            raise Exception("Invalid Json")
    
    def backward_cursor(self, unstep = None):
        if not unstep:
            self.cursor -= 1
        else:
            self.cursor -= unstep
        if self.cursor < 0:
            raise Exception("Invalid Json")
    
    def find_token(self, token):
        print(f"Finding {token} cursor at {self.cursor}")
        token = JsonTokens[token]
        try:
            while self.content[self.cursor] not in token.value.symbol:
                self.forward_cursor()
            self.forward_cursor()
            self.funcMap[token.value.action](token.value.next_token)
        except Exception as e:
            raise e
    
    def expect_token(self, token):
        print(f"EXPECTING {token} cursor at {self.cursor}")
        token = JsonTokens[token]
        try:
            self.skip_space()
            if self.content[self.cursor] in token.value.symbol:
                if token.value.symbol == '{':
                    self.depth+=1
                self.forward_cursor()
                self.funcMap[token.value.action](token.value.next_token)
            else:
                raise Exception("Invalid Json")
        except Exception as e:
            raise e
    
    def disolve_token(self, token_list):
        print(f"Disolving {token_list} cursor at {self.cursor}")
        try:
            self.skip_space()
            found = False
            for TOKEN in token_list:
                TOKEN_ = TOKEN
                TOKEN = JsonTokens[TOKEN]
                if self.content[self.cursor] in TOKEN.value.symbol:
                    self.funcMap['expect'](TOKEN_)
                    found = True
                    break
            if not found:
                raise Exception("Invalid Json")
        except Exception as e:
            raise e
    
    def finish(self, token):
        self.depth -= 1
        if self.depth != 0:
            self.disolve_token(['COMMA', 'CLOSED_BRACE'])
        else:
            if self.cursor != self.cursorLimit-1:
                raise Exception("Invalid Json")
            print("Valid Json")

def parse(content):
    # import ipdb;ipdb.set_trace()
    content = content.strip()
    print(content)
    try:
        JsonParser(content).parse()
    except Exception:
        print("Invalid Json")



def execute():
    file = None
    input = None
    if len(sys.argv) == 2:
        file = sys.argv[1]
    elif len(sys.argv) == 1:
        input = sys.stdin.read()
    else:
        print("Invalid Arguments")
    
    if file:
        with open(file, 'r') as f:
            content = f.read()
    else:
        content = input
    
    return parse(content)
    

if __name__ == "__main__":
    execute()