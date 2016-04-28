## Basic lex file for cool language from the assignment 1
import ply.lex as lex

class CoolLexer (object):
    reserved     = ['class','if','fi','then','else','while','inherits','isvoid','let','loop','pool','case','esac','true','not','new','of']
    states       = (("str","exclusive"))
    tokens       = ('WHITESPACE','TYPE','ID','INTEGER','STRING')+tuple(reserved)
    literals     = ";[](),.'@<>/=~*+-\{\}:"

    t_INTEGER    = "[0-9]+"
    t_WHITESPACE = "[\n\t\f\r\v]"

    def t_TYPE(self,t):
        "[A-Z][A-Za-z_0-9]*"
        ##THis function should be remodelled to appropriately reconginize true nad false
        t.type   = reserved.get(t.value.lower(),"TYPE")
        if self.debug:
            print "[*]Token: "+t.value+"Type:"+t.type
        return t

    def t_ID  (self,t):
        "[a-z][A-Za-z_0-9]*"
        t.type   = reserved.get(t.value.lower(),"ID")
        if self.debug:
            print "[*]Token: "+t.value+"Type:"+t.type
        return t
    def t_begin(self,t):
        r'"'
        self.lexer.begin('str')

    def t_ignore_COMMENT(self,t):
        pass

    #Lex builder
    def build(self,**kwargs):
        self.lexer=lex.lex(object=self,**kwargs)
        return self.lexer

    #Other Interface for calling calling the lexer
    def input(self, text):
        self.lexer.input(text)

    def token(self):
        self.last_token = self.lexer.token()
        return self.last_token

    def find_tok_column(self, token):
        """ Find the column of the token in its line.
        """
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        if last_cr <0: last_cr = 0
        return token.lexpos - last_cr

    def test(self,data):
        self.lexer.input(data)
        for tok in self.lexer:
            print (tok)

    def make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))

    def __init__(self,debug=False):
        #self.logger = logging.getlogger('Main_Lexer.log')
        #if error_func == None:
        #    error_func == self._error_func
        #self.error_func = error_func
        self.debug      = debug
        if self.debug:
            self.logger = Printer()
        self.errors     = []
        #self.last_token = None
