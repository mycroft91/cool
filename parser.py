from tree import *
from lexer import *
import ply.yacc as yacc
from ply.lex import LexToken


class CoolParser(object):
    tokens          = CoolLexer.tokens
    precedence      = (("right", "ASSIGN"),
                       ("right", "DARROW"),
                       ("right","IN"),
                       ("right", "NOT","ISVOID"),
                       ("nonassoc", '<','=',"LE"),
                       ("left", '-', '+'),
                       ("left", '*'),
                       ("left", '/'),
                       ("left", '~'),
                       ("left", '@'),
                       ("left", '.'))
    def p_program(self,p):
        """ program : class_list """
        p[0]        = Program(p[1])

    def p_classlist0(self,p):
        """ class_list : class_list class """
        p[0]        = append_Classes(p[1],p[2])

    def p_classlist1(self,p):
        """ class_list : class """
        p[0]        = single_Classes(p[1])

    def p_class0(self,p):
        """ class : CLASS TYPEID '{' feature_list '}' ';' """
        tok         = LexToken()
        tok.type    = "OBJECTID"
        tok.value   = "object"
        tok.lineno  = -1 #this is just inserted not present
        tok.lexpos  = -1
        p[0]        = class_(p[2],tok,p[4],self.filename)

    def p_class1(self,p):
        """ class : CLASS TYPEID INHERITS TYPEID '{' feature_list '}' ';' """
        p[0]        = class_(p[2],p[4],p[6],self.filename)

    def p_feature_list0(self,p):
        """ feature_list : feature_list feature ';' """
        p[0]        = append_Features(p[1],p[2])

    def p_feature_list1(self,p):
        """ feature_list : """
        p[0]        = nil_Features()

    def p_feature0(self,p):
        """ feature         : OBJECTID '(' formal_list ')' ':' TYPEID '{' expr '}'"""
        p[0]        = method(p[1],p[3],p[6],p[8])
        p[0].lineno = p.lineno(1)

    def p_feature1(self,p):
        """ feature         : OBJECTID '(' ')' ':' TYPEID '{' expr '}'"""
        p[0]        = method(p[1],nil_Formals(),p[5],p[7])
        p[0].lineno = p.lineno(1)

    def p_feature2(self,p):
        """ feature         : OBJECTID ':' TYPEID ASSIGN expr"""
        p[0]        = attr(p[1],p[3],p[5])
        p[0].lineno = p.lineno(1)

    def p_feature3(self,p):
        """ feature         : OBJECTID ':' TYPEID"""
        p[0]        = attr(p[1],p[3],no_expr())
        p[0].lineno = p.lineno(1)

    def p_feature4(self,p):
        """ feature         : error ';' """
        self.errors += 1
        self.error_msgs.append("Syntax error at %s "%str(p.lineno(1)))
        #For AST construction else the program fails here
        p[0]        = attr("","",no_expr())

    def p_formal_list0(self,p):
        """ formal_list     : formal_list ',' formal """
        p[0]        = append_Formals(p[1],p[3])

    def p_formal_list1(self,p):
        """ formal_list     : formal """
        p[0]        = single_Formals(p[1])

    def p_formal0(self,p):
        """ formal          : OBJECTID ':' TYPEID """
        p[0]        = formal(p[1],p[3])
        p[0].lineno = p.lineno(1)

    def p_formal1(self,p):
        """ formal          : error """
        self.errors += 1
        self.error_msgs.append("Syntax error at %s "%str(p.lineno(1)))
        #For AST construction else the program fails here
        p[0]        = attr(LexToken(),LexToken(),no_expr())


    def p_expr_arg_list0(self,p):
        """ expr_arg_list   : expr_arg_list ',' expr """
        p[0]        = append_Expressions(p[1],p[3])

    def p_expr_arg_list1(self,p):
        """ expr_arg_list   : expr """
        p[0]        = single_Expressions(p[1])

    def p_expr_arg_list2(self,p):
        """expr            : OBJECTID ASSIGN expr """
        p[0]        = assign(p[1],p[3])
        p[0].lineno = p.lineno(1)

    def p_expr0(self,p):
        """expr            : expr '.' OBJECTID '(' expr_arg_list ')'"""
        p[0]        = dispatch(p[1],p[3],p[5])
        p[0].lineno = p.lineno(2)

    def p_expr1(self,p):
        """ expr            : expr '.' OBJECTID '(' ')' """
        p[0]        = dispatch(p[1],p[3],nil_Expressions())
        p[0].lineno = p.lineno(2)

    def p_expr2(self,p):
        """ expr            : expr '@' TYPEID '.' OBJECTID '(' expr_arg_list ')' """
        p[0]        = static_dispatch(p[1],p[3],p[5],p[7])
        p[0].lineno = p.lineno(2)

    def p_expr3(self,p):
        """ expr            : expr '@' TYPEID '.' OBJECTID '(' ')'"""
        p[0]         = static_dispatch(p[1],p[3],p[5],nil_Expressions())
        p[0].lineno  = p.lineno(2)

    def p_expr4(self,p):
        """ expr            : OBJECTID '(' expr_arg_list ')' """
        tok          = LexToken()
        tok.type     = "OBJECTID"
        tok.value    = "self"
        tok.lineno   = -1 #this is just inserted not present
        tok.lexpos   = -1
        p[0]         = dispatch(object_(tok),p[1],p[3])
        p[0].lineno  = p.lineno(1)

    def p_expr5(self,p):
        """ expr            : OBJECTID '(' ')' """
        tok         = LexToken()
        tok.type    = "OBJECTID"
        tok.value   = "self"
        tok.lineno  = -1 #this is just inserted not present
        tok.lexpos  = -1
        p[0]        = dispatch(object_(tok),p[1],nil_Expressions())
        p.lineno    = p.lineno(1)

    def p_expr6(self,p):
        """ expr            : IF expr THEN expr ELSE expr FI """
        p[0]        = cond(p[2],p[4],p[6])
        p[0].lineno = p.lineno(1)

    def p_expr7(self,p):
        """ expr            : IF error """
        self.errors += 1
        self.error_msgs.append("Syntax error at expr = %s , after IF"%(p[2]))
        p[0]        = cond(no_expr(),no_expr(),no_expr())

    def p_expr8(self,p):
        """ expr             : IF expr THEN error """
        self.errors += 1
        self.error_msgs.append("Syntax error at expr = %s , after THEN "%(p[4]))
        p[0]        = cond(no_expr(),no_expr(),no_expr())

    def p_expr9(self,p):
        """ expr             : IF expr THEN expr ELSE error """
        self.errors += 1
        self.error_msgs.append("Syntax error at expr = %s , after ELSE "%(p[6]))
        p[0]        = cond(no_expr(),no_expr(),no_expr())

    def p_expr10(self,p):
        """ expr            : WHILE expr LOOP expr POOL """
        p[0]        = loop(p[2],p[4])
        p[0].lineno = p.lineno(1)

    def p_expr11(self,p):
        """ expr            : '{' expr_list '}' """
        p[0]        = block(p[2])
        p[0].lineno = p.lineno(1)

    def p_expr12(self,p):
        """ expr            : lets """
        p[0]        = p[1]

    def p_expr13(self,p):
        """ expr            : CASE expr OF case_list ESAC """
        p[0]        = typcase(p[2],p[4])
        p[0].lineno = p.lineno(1)

    def p_expr14(self,p):
        """ expr            :  NEW TYPEID """
        p[0]        = new_(p[2])
        p[0].lineno = p.lineno(1)

    def p_expr15(self,p):
        """ expr            : ISVOID expr """
        p[0]        = isvoid(p[2])
        p[0].lineno = p.lineno(1)

    def p_expr16(self,p):
        """ expr            : expr '+' expr """
        p[0]         = plus(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr17(self,p):
        """ expr            : expr '-' expr """
        p[0]         = sub(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr18(self,p):
        """ expr            : expr '/' expr """
        p[0]         = divide(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr19(self,p):
        """ expr            : expr '*' expr """
        p[0]         = mul(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr20(self,p):
        """ expr            : '~' expr """
        p[0]         = neg(p[2])
        p[0].lineno  = p.lineno(1)

    def p_expr21(self,p):
        """ expr            : expr '<' expr """
        p[0]         = lt(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr22(self,p):
        """ expr            : expr LE expr """
        p[0]         = leq(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr23(self,p):
        """ expr            : expr '=' expr """
        p[0]         = eq(p[1],p[3])
        p[0].lineno  = p.lineno(2)

    def p_expr24(self,p):
        """ expr            : NOT expr """
        p[0]         = comp(p[2])
        p[0].lineno  = p.lineno(1)

    def p_expr25(self,p):
        """ expr            : '(' expr ')' """
        p[0]        = p[2]

    def p_expr26(self,p):
        """ expr            : OBJECTID """
        p[0]        = object_(p[1])
        p[0].lineno = p.lineno(1)

    def p_expr27(self,p):
        """ expr            : INT_CONST """
        p[0]        = int_const(p[1])
        p[0].lineno = p.lineno(1)

    def p_expr28(self,p):
        """ expr            : STR_CONST """
        p[0]         = string_const(p[1])
        p[0].lineno  = p.lineno(1)

    def p_expr29(self,p):
        """ expr            : BOOL_CONST """
        p[0]         = bool_const(p[1])
        p[0].lineno  = p.lineno(1)

    def p_expr_list0(self,p):
        """ expr_list       : expr ';' """
        p[0]         = single_Expressions(p[1])

    def p_expr_list1(self,p):
        """ expr_list       : expr_list expr ';' """
        p[0]         = append_Expressions(p[1],p[2])

    def p_expr_list2(self,p):
        """ expr_list       : error ';' """
        self.errors  += 1
        self.error_msgs.append("Syntax error at expr = %s before %s"%(p[1],str(p[2])))
        #To make compile clean
        p[0]         = nil_Expressions()

    def p_lets0(self,p):
        """ lets    : LET OBJECTID ':' TYPEID IN expr """
        p[0]         = let(p[2], p[4], no_expr(), p[6])
        p[0].lineno  = p.lineno(1)

    def p_lets1(self,p):
        """ lets    : LET OBJECTID ':' TYPEID ASSIGN expr IN expr """
        p[0]         = let(p[2], p[4], p[6], p[8])
        p[0].lineno  = p.lineno(1)

    def p_lets2(self,p):
        """ lets    : LET OBJECTID ':' TYPEID lets """
        p[0]         = let(p[2], p[4], no_expr(), p[5])
        p[0].lineno  = p.lineno(1)

    def p_lets3(self,p):
        """lets     : LET OBJECTID ':' TYPEID ASSIGN expr lets """
        p[0]         = let(p[2], p[4], p[6], p[7])
        p[0].lineno  = p.lineno(1)

    def p_lets4(self,p):
        """lets     : LET OBJECTID ':' TYPEID ASSIGN expr let """
        p[0]         = let(p[2], p[4], p[6], p[7])
        p[0].lineno  = p.lineno(1)

    def p_lets5(self,p):
        """ lets    : LET error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[2]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_lets6(self,p):
        """ lets    : LET OBJECTID ':' error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[4]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_lets7(self,p):
        """ lets    : LET OBJECTID ':' TYPEID error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[5]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_lets8(self,p):
        """ lets    : LET OBJECTID ':' TYPEID ASSIGN error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[6]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_lets9(self,p):
        """ lets    : LET OBJECTID ':' TYPEID ASSIGN expr IN error """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s after IN "%(p[8]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_let0(self,p):
         """ let : ',' OBJECTID ':' TYPEID IN expr """
         p[0]        = let(p[2], p[4], no_expr(), p[6])
         p[0].lineno = p.lineno(1)

    def p_let1(self,p):
        """ let  : ',' OBJECTID ':' TYPEID ASSIGN expr IN expr """
        p[0]        = let(p[2], p[4], p[6], p[8])
        p[0].lineno  = p.lineno(1)

    def p_let2(self,p):
        """ let  :  ',' OBJECTID ':' TYPEID let """
    	p[0]        = let(p[2], p[4], no_expr(), p[5])
        p[0].lineno  = p.lineno(1)

    def p_let3(self,p):
        """let   : ',' OBJECTID ':' TYPEID ASSIGN expr let """
        p[0]        = let(p[2], p[4], no_expr(), p[6])
        p[0].lineno  = p.lineno(1)

    def p_let4(self,p):
        """ let  : ',' error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[2]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_let5(self,p):
        """ let : ',' OBJECTID ':' error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[4]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_let6(self,p):
        """ let  : ',' OBJECTID ':' TYPEID error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[5]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_let7(self,p):
        """ let  : ',' OBJECTID ':' TYPEID ASSIGN error IN expr """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s before IN "%(p[6]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_let8(self,p):
        """ let  : ',' OBJECTID ':' TYPEID ASSIGN expr IN error """
        self.errors += 1
        self.error_msgs.append("Syntax error in LET expr = %s after IN "%(p[8]))
        #compile clean
        p[0]        = let(no_expr(),no_expr(),no_expr(),no_expr())

    def p_case_list0(self,p):
        """ case_list       : OBJECTID ':' TYPEID DARROW expr ';' """
        p[0]        = single_Cases(branch(p[1],p[3],p[5]))

    def p_case_list1(self,p):
        """ case_list       : case_list OBJECTID ':' TYPEID DARROW expr ';' """
        p[0]        = append_Cases(p[1],branch(p[2],p[4],p[6]))

    def p_case_list2(self,p):
        """ case_list       : case_list error ESAC """
        p[0]        = nil_Cases()
        self.errors += 1
        self.error_msgs.append("Syntax error in case branch at %s before ESAC "%(p[2]))

    def p_case_list3(self,p):
        """ case_list       : error ESAC """
        p[0]        = nil_Cases()
        self.errors += 1
        self.error_msgs.append("Syntax error in case branch at %s before ESAC "%(p[1]))


    def Parse(self,filename):
        self.filename = filename
        data          = "".join(open(filename,"r").readlines())
        parser        = yacc.yacc(module=self,debug=self.debug,start="program")
        self.lexer    = CoolLexer()
        ast           = parser.parse(data,lexer=self.lexer.build())
        return ast

    def __init__(self,debug=True):
        self.debug      = debug
        self.lexer      = None
        self.error_msgs = []
        self.errors     = 0
        self.filename   = None

def main():
    filename    = "/home/mycroft/work/cool/hello_world.cl"
    parser      = CoolParser()
    print parser.Parse(filename)
    print parser.error_msgs
main()
