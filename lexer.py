## Basic lex file for cool language from the assignment 1
import ply.lex as lex
from ply.lex import TOKEN

MAX_STR_CONST    = 1024 #Compatibility with the assignment

class CoolLexer (object):
    reserved     = {'class':'CLASS',
                    'if':'IF',
                    'fi':"FI",
                    'then':"THEN",
                    'else':"ELSE",
                    'while':"WHILE",
                    'inherits':"INHERITS",
                    'isvoid':"ISVOID",
                    'let':"LET",
                    'loop':"LOOP",
                    'pool':"POOL",
                    'case':"CASE",
                    'esac':"ESAC",
                    'not':"NOT",
                    'new':"NEW",
                    'of':"OF",
                    'in' : "IN"}
    bool_consts  = ['true','false']
    #reserved_TY  = ['Int','Bool']
    states       = (("STR","exclusive"),
                    ("COMMENT","exclusive"),
                    ('STRERROR',"exclusive"))
    tokens       = ('TYPEID','OBJECTID','INT_CONST','BOOL_CONST','STR_CONST','ERROR','DARROW','LE','ASSIGN')\
                    +tuple(reserved.values())
    literals     = ";<(),.@=~*+-/{}:"

    t_INT_CONST  = "[0-9]+"
    #t_WHITESPACE = "[\n\t\f\r\v]"
    @TOKEN(r'<=')
    def t_INITIAL_LE(self,t):
        t.type   = "LE"
        return t
    @TOKEN(r'<-')
    def t_INITIAL_ASSIGN(self,t):
        t.type   = "ASSIGN"
        return t
    @TOKEN(r"=>")
    def t_INITIAL_DARROW(self,t):
        t.type   = "DARROW"
        return t

    @TOKEN(r'[\n\t\f\r\v ]')
    def t_INITIAL_WHITESPACE(self,t):
        t.lexer.lineno += t.value.count('\n')

    @TOKEN(r"[A-Z][A-Za-z_0-9]*")
    def t_INITIAL_TYPEID(self,t):
        t.type     = self.reserved.get(t.value.lower(),"TYPEID")
        if self.debug:
            print "[*]Token: "+t.value+"Type:"+t.type
        return t

    @TOKEN(r"(t[rR][uU][eE])|(f[aA][lL][sS][eE])")
    def t_INITIAL_BOOL(self,t):
        t.type       = "BOOL_CONST"
        if len(t.value) == 4:
            t.value  = True
        else:
            t.value  = False
        return t

    @TOKEN(r"[a-z][A-Za-z_0-9]*")
    def t_INITIAL_OBJECTID  (self,t):
        t.type     = self.reserved.get(t.value.lower(),"OBJECTID")
        if self.debug:
            print "[*]Token: "+t.value+"Type:"+t.type
        return t

    @TOKEN(r"[*][)]")
    def t_INITIAL_ERROR(self,t):
        t.type     = "ERROR"
        t.value    = "Unmatched *)"
        return t

    @TOKEN(r'"')
    def t_INITIAL_begin_str(self,t):
        t.lexer.begin('STR')
        self.string_tok        = ""
        self.string_tok_length = 0

    @TOKEN(r"(\n)|(\t)|(\v)|(\r)|(\f)")
    def t_INITIAL_whitespace(self,t):
        t.lexer.lineno        += t.value.count('\n')

    @TOKEN(r"--(.)*[^\n]")
    def t_INITIAL_inline(self,t):
        #ignore inline comment
        pass

    @TOKEN(r'[(][*]')
    def t_INITIAL_begin_comment(self,t):
        t.lexer.begin('COMMENT')

    @TOKEN(r"\\\"")
    def t_STR_escquote(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "\""
    @TOKEN(r'\"')
    def t_STR_quote(self,t):
        t.value                = self.string_tok
        t.type                 = "STR_CONST"
        t.lexer.begin('INITIAL')
        self.string_tok_length = 0
        self.string_tok        = ""
        return t
    @TOKEN(r'\\0')
    def t_STR_escnull(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "0"
    @TOKEN(r'\0')
    def t_STR_null(self,t):
        t.type                 = "ERROR"
        t.value                = "Null character in string"
        t.begin('STRERROR')
        #t.lexer.begin('INITIAL')
        return t
    @TOKEN(r'(\\t)')
    def t_STR_tab(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "\t"
    @TOKEN(r'(\\v)')
    def t_STR_vert(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "\v"
    @TOKEN(r'(\\r)')
    def t_STR_r(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "\r"
    @TOKEN(r'([\\][n])|([\\][\n])')
    def t_STR_nline(self,t):
        #print "new line proper:\""+self.string_tok+"\""
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += "\n"
    @TOKEN(r'\n')
    def t_STR_nline_err(self,t):
        t.type                 = "ERROR"
        t.value                = "Unterminated string constant"
        t.lexer.lineno        += 1
        t.lexer.begin('INITIAL')
        return t
    def t_STR_eof(self,t):
        t.value                = "EOF in string const"
        t.type                 = "ERROR"
        t.lexer.begin("INITIAL")
        return t
    @TOKEN(r'[^\"\n]')
    def t_STR_any(self,t):
        self.string_tok_length+=1
        if (self.string_tok_length > MAX_STR_CONST ):
            t.type             = "ERROR"
            t.value            = "String constant too long"
            t.begin('STRERROR')
            return t
        self.string_tok       += t.value

    @TOKEN(r'\\n')
    def t_STRERROR_nline(self,t):
        pass
    def t_STRERROR_eof(self,t):
        t.value                = "EOF in string"
        t.type                 = "ERROR"
        t.lexer.begin('INITIAL')
        return t
    @TOKEN(r'\n')
    def t_STRERROR_goinit(self,t):
        t.lexer.begin('INITIAL')
    @TOKEN(r'\"')
    def t_STRERROR_goinit2(self,t):
        t.lexer.begin('INITIAL')
    @TOKEN(r'.')
    def t_STRERROR_any(self,t):
        #ignore any other character in this mode
        pass
    @TOKEN(r'[\n]+')
    def t_COMMENT_nline (self,t):
        t.lexer.lineno += t.value.count('\n')
    def t_COMMENT_eof(self,t):
        t.value         = "EOF in comment"
        t.type          = "ERROR"
        t.lexer.begin('INITIAL')
        return t
    @TOKEN(r'[*][)]')
    def t_COMMENT_end(self,t):
        self.lexer.begin('INITIAL')
    @TOKEN(r'.')
    def t_COMMENT_any (self,t):
        pass

    #Maintanence Functions
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
        self.debug      = debug
        if self.debug:
            self.logger = Printer()
        self.errors     = []
        self.last_token = None

if __name__ == "__main__":
    t = CoolLexer()
    t.build()
    test = open("hello_world.cl",'r').readlines()
    s = ""
    for line in test:
        s=s+line
    t.test(s)
