#!/usr/bin/env python

# Token types
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'

class Token:
    def __init__(self, type, value):
        # token type
        self.type = type
        # token value
        self.value = value

    def __str__(self):
        return 'Token({}, {})'.format(self.type, repr(self.value))

    def __repr__(self):
        return self.__str__()

class Interpreter:
    def __init__(self, text):
        self.text = text.strip()
        self.pos = 0
        self.current_token = None

    def error(self):
        raise Exception("Error parsing input")

    def get_next_token(self):
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        current_char = text[self.pos]

        # ignore whitespaces
        while current_char == ' ':
            self.pos += 1
            current_char = text[self.pos]

        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        self.error()

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def list_to_int(self, l):
        return int(''.join([str(x.value) for x in l]))

    def expr(self):
        self.current_token = self.get_next_token()

        left_digits = [self.current_token]
        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            left_digits.append(self.current_token)
            self.eat(INTEGER)

        op = self.current_token
        self.eat(PLUS)

        right_digits = [self.current_token]
        self.eat(INTEGER)

        while self.current_token.type == INTEGER:
            right_digits.append(self.current_token)
            self.eat(INTEGER)

        left = self.list_to_int(left_digits)
        right = self.list_to_int(right_digits)
        
        result = left + right
        return result


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)

if __name__ == '__main__':
    main()
