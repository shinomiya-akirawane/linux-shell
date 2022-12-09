grammar Command;

/*
 * Lexer Rules
 */

SINGLE_QUOTED : '\'' (~[\n'])+ '\'' ;
BACKQUOTED : '`' (~[\n`])+ '`' ;
DOUBLE_QUOTED : '"' (BACKQUOTED | (~[\n`"])+)* '"';
UNQUOTED : (~[ '"`;|<>])+ ;
WS : [ \t]+;

/*
 * Parser Rules
 */

command : prefixCall partialSeq? ;
partialSeq : ';' prefixCall partialSeq? ;
prefixCall : call partialPipe? ;
partialPipe : '|' call partialPipe? ;

// command : pipe | seq | call ;
// seq : (pipe | seq | call) ';' (pipe | seq | call) ;
// pipe : call '|' call | pipe '|' call ;

call : WS* (redirection WS+)* argument WS* (WS+ atom)* WS* ;
atom : redirection | argument ;
argument : (quoted | unquoted)+ ;
redirection : '<' WS* argument | '>' WS* argument ;
quoted : SINGLE_QUOTED | BACKQUOTED | DOUBLE_QUOTED ;
unquoted : UNQUOTED;
