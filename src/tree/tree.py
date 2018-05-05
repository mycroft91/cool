#This module tries to mimic the functionality of tree.h
class Tree_Node(object):
    pass

class List(object):
    def __init__(self):
        self.data = []
        self.num  = 0
    def append(self,elem):
        self.data.append(elem)
        self.num  += 1

class Program():
    def __init__(self,class_list):
        self.class_list = class_list
        self.type       = 'Program'

#class
class class_(Tree_Node):
    def __init__(self,name,parent,features,filename):
        self.name      = name
        self.parent    = parent
        self.features  = features
        self.filename  = filename
        self.type      = "Class_"

class Classes(List):
    def __init__(self):
        super(Classes,self).__init__()
        self.type      = "Classes"

def single_Classes(class_):
    if class_.type  != "Class_":
        raise TypeError("Cannot convert from "+class_.type+ " to Class_")
    temp               = Classes()
    temp.data.append(class_)
    return temp

def append_Classes(classes,class_):
    if class_.type  != "Class_":
        raise TypeError("Cannot convert from "+class_.type+ " to Class_")
    if classes.type != "Classes":
        raise TypeError("Cannot convert from "+classes.type+ " to Classes")
    classes.append(class_)
    return classes

def nil_Classes():
    return Classes()


##feature
class feature(Tree_Node):
    pass

class method(feature):
    def __init__(self,name,formals,return_type,expr):
        self.name        = name
        self.formals     = formals
        self.return_type = return_type
        self.expr        = expr
        self.type        = "Feature"
        self.subtype     = "method"

class attr(feature):
    def __init__(self,name,type_decl,init):
        self.name        = name
        self.type_decl   = type_decl
        self.init        = init
        self.type        = "Feature"
        self.subtype     = "attr"

class Features(List):
    def __init__(self):
        super(Features,self).__init__()
        self.type      = "Features"


def single_Features(feature):
    if feature.type   != "Feature":
        raise TypeError("Cannot convert from "+feature.type+ " to Feature")
    temp               = Features()
    temp.data.append(feature)
    return temp

def append_Features(features,feature):
    if feature.type   != "Feature":
        raise TypeError("Cannot convert from "+feature.type+ " to Feature")
    if features.type  != "Features":
        raise TypeError("Cannot convert from "+features.type+ " to Features")
    features.append(feature)
    return features

def nil_Features():
    return Features()

##formal
class formal(Tree_Node):
    def __init__(self,name,type_decl):
        self.name      = name
        self.type_decl = type_decl
        self.type      = "Formal"

class Formals(List):
    def __init__(self):
        super(Formals,self).__init__()
        self.type      = "Formals"


def single_Formals(formal):
    if formal.type   != "Formal":
        raise TypeError("Cannot convert from "+formal.type+ " to Formal")
    temp               = Formals()
    temp.data.append(formal)
    return temp

def append_Formals(formals,formal):
    if formal.type   != "Formal":
        raise TypeError("Cannot convert from "+formal.type+ " to Formal")
    if features.type != "Formals":
        raise TypeError("Cannot convert from "+formals.type+ " to Formals")
    formals.append(formal)
    return formals

def nil_Formals():
    return Formals()

##Case
class branch(Tree_Node):
    def __init__(self,name,type_decl,expr):
        self.name      = name
        self.type_decl = type_decl
        self.expr      = expr
        self.type      = "Case"

class Cases(List):
    def __init__(self):
        super(class_list,self).__init__()
        self.type      = "Cases"


def single_Cases(case):
    if case.type   != "Case":
        raise TypeError("Cannot convert from "+case.type+ " to Case")
    temp               = Cases()
    temp.data.append(case)
    return temp

def append_Cases(cases,case):
    if case.type   != "Case":
        raise TypeError("Cannot convert from "+case.type+ " to Case")
    if cases.type != "Cases":
        raise TypeError("Cannot convert from "+cases.type+ " to Cases")
    cases.append(case)
    return cases

def nil_Cases():
    return Cases()
##Expression
class assign(Tree_Node):
    def __init__(self,name,expr):
        self.name    = name
        self.expr    = expr
        self.type    = "Expression"
        self.subtype = "assign"

class static_dispatch(Tree_Node):
    def __init__(self,expr,type_name,name,actual):
        self.name       = name
        self.expr       = expr
        self.type_name  = type_name
        self.actual     = actual
        self.type       = "Expression"
        self.subtype    = "static_dispatch"

class dispatch(Tree_Node):
    def __init__(self,expr,name,actual):
        self.name       = name
        self.expr       = expr
        self.actual     = actual
        self.type       = "Expression"
        self.subtype    = "dispatch"

class cond(Tree_Node):
    def __init__(self,pred,then_exp,else_exp):
        self.pred       = pred
        self.then_exp   = then_exp
        self.else_exp   = else_exp
        self.type       = "Expression"
        self.subtype    = "cond"

class loop(Tree_Node):
    def __init__(self,pred,body):
        self.pred       = pred
        self.body       = body
        self.type       = "Expression"
        self.subtype    = "loop"

class typecase(Tree_Node):
    def __init__(self,expr,cases):
        self.expr       = expr
        self.cases      = cases
        self.type       = "Expression"
        self.subtype    = "typecase"

class block(Tree_Node):
    def __init__(self,body):
        self.body       = body
        self.type       = "Expression"
        self.subtype    = "block"

class let(Tree_Node):
    def __init__(self,identifier,type_decl,init,body):
        self.identifier = identifier
        self.type_decl  = type_decl
        self.init       = init
        self.body       = body
        self.type       = "Expression"
        self.subtype    = "let"

class plus(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "plus"

class sub(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "sub"

class mul(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "mul"

class divide(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "divide"

class neg(Tree_Node):
    def __init__(self,e1):
        self.e1         = e1
        self.type       = "Expression"
        self.subtype    = "neg"

class lt(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "lt"

class eq(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "eq"

class leq(Tree_Node):
    def __init__(self,e1,e2):
        self.e1         = e1
        self.e2         = e2
        self.type       = "Expression"
        self.subtype    = "leq"

class comp(Tree_Node):
    def __init__(self,e1):
        self.e1         = e1
        self.type       = "Expression"
        self.subtype    = "comp"

class int_const(Tree_Node):
    def __init__(self,token):
        self.token      = token
        self.type       = "Expression"
        self.subtype    = "int_const"

class string_const(Tree_Node):
    def __init__(self,token):
        self.token      = token
        self.type       = "Expression"
        self.subtype    = "string_const"

class bool_const(Tree_Node):
    def __init__(self,val):
        self.val        = val
        self.type       = "Expression"
        self.subtype    = "bool_const"

class new_(Tree_Node):
    def __init__(self,type_name):
        self.type_name  = type_name
        self.type       = "Expression"
        self.subtype    = "new_"

class isvoid(Tree_Node):
    def __init__(self,e1):
        self.e1         = e1
        self.type       = "Expression"
        self.subtype    = "isvoid"

class no_expr(Tree_Node):
    def __init__(self):
        self.type       = "Expression"
        self.subtype    = "no_expr"

class object_(Tree_Node):
    def __init__(self,name):
        self.name       = name
        self.type       = "Expression"
        self.subtype    = "object"

class Expressions(List):
    def __init__(self):
        super(Expressions,self).__init__()
        self.type      = "Expressions"


def single_Expressions(expr):
    if expr.type   != "Expression":
        raise TypeError("Cannot convert from "+expr.type+ " to Expression")
    temp               = Expressions()
    temp.data.append(expr)
    return temp

def append_Expressions(exprs,expr):
    if expr.type   != "Expression":
        raise TypeError("Cannot convert from "+expr.type+ " to Expression")
    if exprs.type != "Expressions":
        raise TypeError("Cannot convert from "+exprs.type+ " to Expressions")
    exprs.append(expr)
    return exprs

def nil_Expressions():
    return Expressions()
