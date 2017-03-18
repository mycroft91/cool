/*
 *  The scanner definition for COOL.
 */

/*
 *  Stuff enclosed in %{ %} in the first section is copied verbatim to the
 *  output, so headers and global definitions are placed here to be visible
 * to the code in the file.  Don't remove anything that was here initially
 */
%{
#include <cool-parse.h>
#include <stringtab.h>
#include <utilities.h>

/* The compiler assumes these identifiers. */
#define yylval cool_yylval
#define yylex  cool_yylex

/* Max size of string constants */
#define MAX_STR_CONST 1025
#define YY_NO_UNPUT   /* keep g++ happy */

extern FILE *fin; /* we read from this file */

/* define YY_INPUT so we read from the FILE fin:
 * This change makes it possible to use this scanner in
 * the Cool compiler.
 */
#undef YY_INPUT
#define YY_INPUT(buf,result,max_size) \
	if ( (result = fread( (char*)buf, sizeof(char), max_size, fin)) < 0) \
		YY_FATAL_ERROR( "read() in flex scanner failed");
#define CHECK(lineno,limit) \
    if (lineno >= limit) {cool_yylval.error_msg = (char *)"String constant too long";BEGIN(STRERROR);return ERROR;}

char string_buf[MAX_STR_CONST]; /* to assemble string constants */
char *string_buf_ptr;

extern int curr_lineno;
extern int verbose_flag;

extern YYSTYPE cool_yylval;

/*
 *  Add Your own definitions here
 */
 int str_length;/*String token length*/
 /*I dont know whether I am using them porperly*/


%}
/* States*/
%x STRING
%x COMMENT
%x STRERROR
/*
 * Define names for regular expressions here.
 */

DARROW          =>
LE              <=
ASSIGN          <-
CLASS           [cC][lL][aA][sS][sS]
DIGIT           [0-9]
ELSE            [eE][lL][sS][eE]
FI              [fF][iI]
IF              [iI][fF]
IN              [iI][nN]
INHERITS        [iI][nN][hH][eE][rR][iI][tT][sS]
ISVOID          [iI][sS][vV][oO][iI][dD]
LET             [lL][eE][tT]
LOOP            [lL][oO][oO][pP]
POOL            [pP][oO][oO][lL]
THEN            [tT][hH][eE][nN]
WHILE           [wW][hH][iI][lL][eE]
CASE            [cC][aA][sS][eE]
ESAC            [eE][sS][aA][cC]
NEW             [nN][eE][wW]
OF              [oO][fF]
NOT             [nN][oO][tT]
INTEGER         ([0-9])+
TYPE_ID         ([A-Z])([A-Za-z_0-9]*)
OBJECT_ID       ([a-z])([A-Za-z_0-9]*)
TRUE            t[rR][uU][eE]
FALSE           f[aA][lL][sS][eE]

%%
 /*
 *  Initial state
 */
<INITIAL>{CLASS}                 { return (CLASS); }
<INITIAL>{ELSE}                  { return (ELSE); }
<INITIAL>{FI}                    { return (FI); }
<INITIAL>{IF}                    { return (IF); }
<INITIAL>{IN}                    { return (IN); }
<INITIAL>{INHERITS}              { return (INHERITS); }
<INITIAL>{ISVOID}                { return (ISVOID); }
<INITIAL>{LET}                   { return (LET); }
<INITIAL>{LOOP}                  { return (LOOP); }
<INITIAL>{POOL}                  { return (POOL); }
<INITIAL>{THEN}                  { return (THEN); }
<INITIAL>{WHILE}                 { return (WHILE); }
<INITIAL>{CASE}                  { return (CASE); }
<INITIAL>{ESAC}                  { return (ESAC); }
<INITIAL>{NEW}                   { return (NEW); }
<INITIAL>{OF}                    { return (OF); }
<INITIAL>{NOT}                   { return (NOT); }
<INITIAL>{DARROW}		          { return (DARROW); }
<INITIAL>{ASSIGN}                { return (ASSIGN); }
<INITIAL>{LE}                    { return (LE); }
<INITIAL>({TRUE})|({FALSE}) { if (!strcmp("true",yytext))
                                cool_yylval.boolean = true ;
                              else
                                cool_yylval.boolean = false;
                              return BOOL_CONST;}
<INITIAL>{INTEGER}          { cool_yylval.symbol = stringtable.add_int(atoi(yytext));
                              return INT_CONST;}
<INITIAL>{OBJECT_ID}        {  /*Compare with keywords*/
                              //printf("Token ObjID");
                              cool_yylval.symbol = stringtable.add_string(yytext,yyleng);
                              return OBJECTID;}
<INITIAL>{TYPE_ID}          { cool_yylval.symbol = stringtable.add_string(yytext,yyleng);
                              return TYPEID;}
<INITIAL>\"                 { /*start STRING state, reset the buf pointer and reset string length*/
                              BEGIN(STRING);
                              string_buf_ptr = string_buf;
                              str_length =0;}
<INITIAL>\n                 { /*increment the lineno and dont return anything */
                              curr_lineno += 1;}
<INITIAL>--(.)*[^\n]        {/*Ignore inline comment*/ }
<INITIAL>\t                 {/*Do nothing*/}
<INITIAL>\r                 {/*Do nothing*/}
<INITIAL>\v                 {/*Do nothing*/}
<INITIAL>[ ]                {/*Do nothing*/}
<INITIAL>\*\)               {cool_yylval.error_msg = (char *)"Unmatched *)";
                             return ERROR;}
<INITIAL>\(\*               {BEGIN(COMMENT);}
<INITIAL>";"                { return int(';'); }
<INITIAL>","                { return int(','); }
<INITIAL>":"                { return int(':'); }
<INITIAL>"{"                { return int('{'); }
<INITIAL>"}"                { return int('}'); }
<INITIAL>"+"                { return int('+'); }
<INITIAL>"-"                { return int('-'); }
<INITIAL>"*"                { return int('*'); }
<INITIAL>"/"                { return int('/'); }
<INITIAL>"<"                { return int('<'); }
<INITIAL>"="                { return int('='); }
<INITIAL>"~"                { return int('~'); }
<INITIAL>"."                { return int('.'); }
<INITIAL>"@"                { return int('@'); }
<INITIAL>"("                { return int('('); }
<INITIAL>")"                { return int(')'); }
<INITIAL>.                  { yylval.error_msg = yytext; return (ERROR); }


 /*
  *  Nested comments
  */
<COMMENT>\n         {curr_lineno += 1;}
<COMMENT>\*\)       {BEGIN(INITIAL);}
<COMMENT><<EOF>>    {cool_yylval.error_msg = (char *)"EOF in comment";BEGIN(INITIAL);return ERROR;}
<COMMENT>.          {/*Do Nothing*/}



 /*
  * Keywords are case-insensitive except for the values true and false,
  * which must begin with a lower-case letter.
  */


 /*
  *  String constants (C syntax)
  *  Escape sequence \c is accepted for all characters c. Except for
  *  \n \t \b \f, the result is c.
  *
  */
<STRING>\\\n  {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\n';}
<STRING>\\n   {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\n';}
<STRING>\n    {cool_yylval.error_msg = (char *)"Unterminated string constant";curr_lineno +=1; BEGIN(INITIAL);return ERROR;}
<STRING>\0    {cool_yylval.error_msg = (char *)"Null character found in string"; return ERROR;}
<STRING>\\0   {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '0'  ;}
<STRING>\\t   {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\t' ;}
<STRING>\\b   {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\b' ;}
<STRING>\\f   {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\f' ;}
<STRING>\\\"  {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\"' ;}
<STRING>\"    {CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = '\0' ;
                BEGIN(INITIAL);
                /*Here string entry doesnt take yytext or yyleng instead give our saved values as args*/
                cool_yylval.symbol = stringtable.add_string(string_buf,str_length);
                //printf("String found \"%s\"",string_buf);
                return STR_CONST;}
<STRING><<EOF>> {cool_yylval.error_msg = (char *)"EOF in string const";BEGIN(INITIAL);return ERROR;}
<STRING>.       {str_length +=1; CHECK(str_length,MAX_STR_CONST);*string_buf_ptr++ = yytext[0];}

<STRERROR>\\n     {/*Do nothing*/}
<STRERROR>\n      {BEGIN(INITIAL);}
<STRERROR>\\\"    {/*Do nothing*/}
<STRERROR>\"      {BEGIN(INITIAL);}
<STRERROR><<EOF>> {cool_yylval.error_msg = (char *)"EOF in string const";BEGIN(INITIAL);return ERROR;}
<STRERROR>.       {/*Do nothing*/}

%%
