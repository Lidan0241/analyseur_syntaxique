in_file = 'ab_test.txt'
#in_file = 'ab_test_bad.txt'
out_file = 'ab_test_parse.log' 

all_parse_states = [ 'S', 'A0', 'A1', 'A2', 'B0', 'B1', 'LSB', 'RSB' ]
# manque les états intermédiaires dans cette liste

def main_parse( ):
     with open( in_file, 'rt') as in_fdesc:
          with open( out_file, 'wt' ) as out_fdesc:
               return S( in_fdesc, out_fdesc )
          
def next_tokn( in_f ):
     x = in_f.read( 1 )
     return x

def S( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'S'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A0( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B0( in_f, out_f, parse_state, K )
          elif next_tok == '[':
               return LSB( in_f, out_f, parse_state, K + 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
          if K == 0:
               out_f.write( 'texte accepté comme valide' )
               return True
          else:
               out_f.write( 'texte non valide [] non équilibrés' )
               return False

def A0( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'A0'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A0( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B0( in_f, out_f, parse_state, K )
          elif next_tok == '[':
               return LSB( in_f, out_f, parse_state, K + 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
           if K == 0:
               out_f.write( 'texte accepté comme valide' )
               return True
           else:
               out_f.write( 'texte non valide [] non équilibrés' )
               return False

def B0( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'B0'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A0( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B0( in_f, out_f, parse_state, K )
          elif next_tok == '[':
               return LSB( in_f, out_f, parse_state, K + 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
           if K == 0:
               out_f.write( 'texte accepté comme valide' )
               return True
           else:
               out_f.write( 'texte non valide [] non équilibrés' )
               return False   

def LSB( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'LSB'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A1( in_f, out_f, parse_state, K )
          elif next_tok == ']':
               return RSB( in_f, out_f, parse_state, K + 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
          return None     

def A1( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'A1'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A2( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B1( in_f, out_f, parse_state, K )
          elif next_tok == ']':
               return RSB( in_f, out_f, parse_state, K - 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
          return None

def B1( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'B1'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A2( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B1( in_f, out_f, parse_state, K )
          elif next_tok == ']':
               return RSB( in_f, out_f, parse_state, K - 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
          return None
     
def A2( in_f, out_f, parse_state = 'S', K = 0):
     parse_state = 'A2'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A2( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B1( in_f, out_f, parse_state, K )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
          return None

def RSB( in_f, out_f, parse_state = 'S', K = 0 ):
     parse_state = 'RSB'
     next_tok = next_tokn( in_f )
     out_f.write( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, next_tok, K ))
     if next_tok:
          if next_tok == 'a':
               return A0( in_f, out_f, parse_state, K )
          elif next_tok == 'b':
               return B0( in_f, out_f, parse_state, K )
          elif next_tok == '[':
               return LSB( in_f, out_f, parse_staten, K + 1 )
          elif next_tok == ']':
               return RSB( in_f, out_f, parse_state, K - 1 )
          else:
               print( "ERROR caractère {0} of code {1} non autorisé dans l'état {2}".format( next_tok, ord( next_tok ), parse_state ))
               print( 'aborting....')
               exit( 1 )
     else:
           if K == 0:
               out_f.write( 'texte accepté comme valide' )
               return True
           else:
               out_f.write( 'texte non valide [] non équilibrés' )
               return False
     
main_parse()
