import re

class TokenCompiler(object):

    def __init__(self, input):
        self.source = input # Tokenized input
        self.variables = []
        self.read_variables()
        print('Args',self.variables, 'Src', self.source)

    def read_variables(self):
        # Get the variables or arguments of: '[', 'x', 'y', 'z', ']'
        self.next_token()
        arg = self.next_token()

        while len(self.source) > 0 and arg != ']':
            self.variables.append(arg)
            arg = self.next_token()

    def next_token(self):
        # Do a pop(0) of tokens
        founded = self.source[0] if len(self.source) > 0 else None
        if founded:
            self.source = self.source[1:]
        return founded

    def expresion(self):
        """
        Read the expresion from pop token with + or -
        """
        a_part = self.term()        
        t0 = self.source[0] if len(self.source) > 0 else None
        now = None

        if t0 is None or (t0 != '+' and t0 != '-'):
            return a_part

        while t0 and (t0 == '+' or t0 == '-'):
            curop = self.next_token()
            b_part = self.term()

            if now:
                now = {'op':curop, 'a':now, 'b':b_part}
            else:
                now = {'op':curop, 'a':a_part, 'b':b_part}

            t0 = self.source[0] if len(self.source) > 0 else None

        return now

    def term(self):
        """
        Read the term from token with * or /
        """
        a_part = self.factor()
        t0 = self.source[0] if len(self.source) > 0 else None
        now = None

        if t0 is None or (t0 != '*' and t0 != '/'):
            return a_part

        while t0 and (t0 == '*' or t0 == '/'):
            curop = self.next_token()
            b_part = self.factor()

            if now:
                now = {'op':curop, 'a':now, 'b':b_part}
            else:
                now = {'op':curop, 'a':a_part, 'b':b_part}

            t0 = self.source[0] if len(self.source) > 0 else None

        return now

    def factor(self):
        """
        Read the factor
        """
        tok = self.next_token()

        if isinstance(tok, int):
            return {'op':'imm', 'n':tok}

        if isinstance(tok, str) and tok.isalpha():
            return {'op':'arg', 'n':self.variables.index(tok)}

        ret = self.expresion()
        self.next_token() # Remove )

        return ret

    def simplify(self, expr):
        """
        Simplify the givven expresion
        """
        this_op = expr['op']

        if this_op == 'imm' or this_op == 'arg':
            return expr

        left = self.simplify( expr['a'] )
        right = self.simplify( expr['b'] )

        if left['op'] == 'imm' and right['op'] == 'imm':
            lval = left['n']
            rval = right['n']

            value = None

            if this_op == '+':
                value = lval + rval
            elif this_op == '-':
                value = lval - rval
            elif this_op == '*':
                value = lval * rval
            elif this_op == '/':
                value = lval / rval

            return { 'op': 'imm', 'n': value }

        return { 'op': this_op, 'a': left, 'b': right }

    def generate(self, node):
        """
        Generate a new language
        """
        mc_ins = []

        if node['op'] == 'imm' or node['op'] == 'arg':
            if node['op'] == 'imm':
                mc_ins.append('IM %d' % node['n'])
            else:
                mc_ins.append('AR %s' % str(node['n']))
        else:
            mc_ins = self.generate( node['a'] )
            mc_ins = mc_ins + self.generate(node['b'])
            mc_ins = mc_ins + ['PO','SW','PO']

            if node['op'] == '+':
                mc_ins.append('AD')
            elif node['op'] == '-':
                mc_ins.append('SU')
            elif node['op'] == '*':
                mc_ins.append('MU')
            elif node['op'] == '/':
                mc_ins.append('DI')

        return mc_ins + ['PU']

class Compiler(object):
    
    def compile(self, program):
        return self.pass3(self.pass2(self.pass1(program)))
        
    def tokenize(self, program):
        """Turn a program string into an array of tokens.  Each token
           is either '[', ']', '(', ')', '+', '-', '*', '/', a variable
           name or a number (as a string)"""
        token_iter = (m.group(0) for m in re.finditer(r'[-+*/()[\]]|[A-Za-z]+|\d+', program))
        return [int(tok) if tok.isdigit() else tok for tok in token_iter]

    def pass1(self, program):
        """Returns an un-optimized AST"""
        tokens = self.tokenize(program)
        self.lexer = TokenCompiler(tokens)
        return self.lexer.expresion()
            
    def pass2(self, ast):
        """Returns an AST with constant expressions reduced"""
        return self.lexer.simplify(ast)

    def pass3(self, ast):
        """Returns assembly instructions"""
        return self.lexer.generate(ast)

def main():
    prog = '[ x y z ] ( 2*3*x + 5*y - 3*z ) / (1 + 3 + 2*2)'
    #prog = '[ x y ] ( x + y ) / 2'
    c = Compiler()
    p1 = c.compile(prog)

    print('RESPUESTA=',p1)


main()