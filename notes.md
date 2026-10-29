# Notes

## Tokens

| Type                    | Token       | Regex                              |
|-------------------------|-------------|------------------------------------|
| `class`                 | CLASS       |`class`                             |
| `public`                | PUBLIC      |`public`                            |
| `static`                | STATIC      |`static`                            |
| `void`                  | VOID        |`void`                              |
| `int`                   | INT         |`int`                               |
| `float`                 | FLOAT       |`float`                             |
| `boolean`               | BOOLEAN     |`boolean`                           |
| `char`                  | CHAR        |`char`                              |
| `String`                | STRING_TYPE |`String`                            |
| `if`                    | IF          |`if`                                |
| `else`                  | ELSE        |`else`                              |
| `while`                 | WHILE       |`while`                             |
| `for`                   | FOR         |`for`                               |
| `return`                | RETURN      |`return`                            |
| Identifier              | ID          | `[a-zA-Z_][a-zA-Z0-9_]*`           |
| Number                  | NUMBER      | `[1-9][0-9]*(\.[0-9]+)?`           |
| String                  | STRING      | `\"(.*)\" \| \'(.*)\'`             |
| Boolean                 | BOOLEAN     | `true \| false`                    |
| Assignment              | ASSIGN      | `=`                                |
| Logical operator        | LOGOP       | `== \| != \| > \| < \| >= \| <=` |
| Left parenthesis        | LPAR        | `\(`                               |
| Right parenthesis       | RPAR        | `\)`                               |
| Left curly Bracket      | LCUR        | `\{`                               |
| Right curly Bracket     | RCUR        | `\}`                               |
| Left square Bracket     | LSQU        | `\[`                               |
| Right square bracket    | RSQU        | `\]`                               |
| Semicolon               | SEMICOLON   | `;`                                |
| Comma                   | COMMA       | `,`                                |
| Dot                     | DOT         | `\.`                               |
| Comment (ignored)       | COMMENT     | `(//.*) \| (/\*.*\*/)`             |
| Spaces (ignored)        | SPACE       | `[\s\n\t]+`                        |
| Addition operator       | ADDOP       | `\+ \| \-`                         |
| Multiplication operator | MULOP       | `\* \| % \| /`                     |
| Logical AND             | ANDOP       | `&&`                               |
| Logical OR              | OROP        | `\|\|`                             |
| Logical NOT             | NOTOP       | `!`                                |
| Bitwise AND             | BITANDOP    | `&`                                |
| Bitwise OR              | BITOROP     | `\|`                               |
| Bitwise NOT             | BITNOTOP    | `\~`                               |
| Bitwise XOR             | BITXOROP    | `\^`                               |

## Transition Table
