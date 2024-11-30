import re
in_file = 'annule_arg.TS'
#out_file = 'annule_arg_parse.log'
out_file = 'annule_arg_parse.csv'
all_parse_states = [ 'P0' ]
terminals_re = { '#'      : '^[ \n]*#[ \n]*' ,
                 '}'      : '^[ \n]*}[ \n]*' ,
                 'I'      : '^[ \n]*I[ \n]*' ,
                 'P'      : '^[ \n]*P[ \n]*' ,
                 'G'      : '^[ \n]*G[ \n]*' ,
                 'D'      : '^[ \n]*D[ \n]*' ,
                 '0'      : '^[ \n]*0[ \n]*' ,
                 '1'      : '^[ \n]*1[ \n]*' ,
                 'fin'    : '^[ \n]*fin[ \n]*' ,
                 'boucle' : '^[ \n]*boucle[ \n]*' ,
                 'si(0)'  : '^[ \n]*si[ \n]*\([ \n]*0[ \n]*\)[ \n]*' ,
                 'si(1)'  : '^[ \n]*si[ \n]*\([ \n]*1[ \n]*\)[ \n]*' }

terminals_automata = { x : re.compile( terminals_re[ x ] ) for x in terminals_re.keys() }

def tokenize( in_f, terms_autom = {} ):
     txt = in_f.read()
     txt_sz = len( txt )
     tokens = []
     match = True
     while match and (len( txt ) != 0):
          for tok_nm in terms_autom.keys():
               match = terms_autom[ tok_nm ].search( txt )
               if match:
                    (b, e ) = match.span( 0 )
                    if b == 0:
                         tokens.append( tok_nm )
                         txt = txt[ e: ]
                         break
     if match or len( txt ) == 0:
          return tokens
     else:
          print( 'ERROR unknow token encountered in the input at position {0}'.format( txt_sz - len( txt ) ) )
          print( 'aborting' )
          exit( 1 )

def next_tok( tokens ):
     if tokens == []:
          print( 'ERROR offset in next_tok() out of range (i.e. >= {0})'.format( len( tokens )))
          return ''
     else:
          return tokens[ 0 ]

def main_parse( terms_autom ):
     with open( in_file, 'rt') as in_fdesc:
          with open( out_file, 'wt' ) as out_fdesc:
               tokens = tokenize( in_fdesc, terms_autom )
               return P0( tokens, out_fdesc )

def print_opdb( out_f, opdb, level_db ):
     out_f.write( '#tokID\ttok\tlevel\tmatchtok\tmatchtokID\n' )
     for (k, v ) in opdb.items():
          if v is None:
                    out_f.write( '{0}\t"{1}"\t{2}\t"{3}"\t"{4}"\n'.format( k[1], k[0], level_db[k], None, None) )
          else:
               print( 'v is ' , v )
               print( 'v[ 0 ] ' , v[ 0 ] , ' v[1] ' , v[ 1 ] )
               out_f.write( '{0}\t"{1}"\t{2}\t"{3}"\t{4}\n'.format( k[1], k[0], level_db[k], v[0], v[1]) )   

def P0( tokens, out_f, parse_state = 'P0', K = 0, tokid = 0, stack = [], opdb = {}, level_db = {} ):
     assert( stack is not None )
     print( '==> beg P0() stack == ', stack )
     print( '==> beg P0() opdb == ', opdb )
     tok = next_tok( tokens )
     tokid += 1
     print( 'in state {0} with new input token {1} and K == {2}\n'.format( parse_state, tok, K ))
     if ( tok == '#') and (K == 0):
          opdb[ (tok, tokid) ] = None ; level_db[ (tok, tokid) ] = K
          print_opdb( out_f, opdb, level_db )
          return True  #===== stop recursion here
     elif tok in [ 'I', 'P', 'G', 'D', '0', '1' ]:
          opdb[ (tok, tokid) ] = None ; level_db[ (tok, tokid) ] = K
          return P0( tokens[ 1: ], out_f, 'P0', K, tokid, stack, opdb )    #============= P0()
     elif tok in [ 'fin' ]:
          opdb[ (tok, tokid) ] = None ; level_db[ (tok, tokid) ] = K
          return P0( tokens[ 1: ], out_f, 'P0', K, tokid, stack, opdb )  #=============  P0()
     elif tok in [ 'boucle', 'si(0)', 'si(1)' ]:
          #out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
          opdb[ (tok, tokid) ] = None
          level_db[ (tok, tokid) ] = K
          return P0( tokens[ 1: ], out_f, 'P0', K + 1, tokid, stack + [ (tok, tokid) ], opdb ) #=============  P0()
     elif tok == '}':
          if K < 1:
               print( 'ERROR unbalanced closing code block token "}"' )
               return False #===== stop recursion here
          else:
               level_db[ (tok, tokid) ] = K
               opdb[ stack[ -1 ] ] = (tok, tokid)
               opdb[ (tok, tokid) ] =  None
               if stack[ -1 ][ 0 ] == 'boucle':
                    # on remonte dans les tokens, du dernier token au token boucle qui est en sommet de pile (dernière instruction boucle vue).
                    # (notez que depuis cette dernière instruction boucle, le programme a pu voir passer beaucoup de blocs "si(0)" ou "si(1)"
                    # qui depuis on été ensuite dépilées, mais dont les instructions"fin" qu'ils pouvaient contenir ne sont pas associés au numéro du
                    # dernier token "boucle" car nous n'avions pas encore rencontré sa fin (le token courrant "}").
                    for i in range( tokid, stack[ -1 ][ -1 ], -1 ):
                         # l'assert exprime le fait que nous avons déjà vus passer tous les tokens
                         # entre le début du bloc et sa fin (le token courant '}')
                         assert( i in [ k[1] for k in opdb.keys()] )
                         if ('fin', i) in opdb.keys():
                              opdb[ ('fin', i) ] = stack[ -1 ]
               return P0( tokens[ 1: ], out_f, 'P0', K - 1, tokid, stack[ 0:-1], opdb  ) #=============  P0()
     else:
          print( 'ERROR unexpected end of input' )
          return False #===== stop recursion here
     
main_parse( terminals_automata )
