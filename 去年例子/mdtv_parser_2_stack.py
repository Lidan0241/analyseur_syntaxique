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
               else:
                    pass
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
               out_fdesc.write( '#tokID\ttok\tlevel\n' )
               tokens = tokenize( in_fdesc, terms_autom )
               return P0( tokens, out_fdesc )    

def P0( tokens, out_f, parse_state = 'P0', K = 0, tokid = 0, stack = [], opdb = {} ):
     assert( stack is not None )
     tok = next_tok( tokens )
     tokid += 1
     if ( tok == '#') and (K == 0):
          out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
          opdb[ (tok, tokid) ] = None
          return True  #===== stop recursion here
     elif tok in [ 'I', 'P', 'G', 'D', '0', '1' ]:
          out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
          opdb[ (tok, tokid) ] = None
          return P0( tokens[ 1: ], out_f, 'P0', K, tokid, stack, opdb )    #============= P0()
     elif tok in [ 'fin' ]:
          out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
          opdb[ (tok, tokid) ] = None
          return P0( tokens[ 1: ], out_f, 'P0', K, tokid, stack, opdb )  #=============  P0()
     elif tok in [ 'boucle', 'si(0)', 'si(1)' ]:
          out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
          opdb[ (tok, tokid) ] = None
          return P0( tokens[ 1: ], out_f, 'P0', K + 1, tokid, stack + [ (tok, tokid) ], opdb ) #=============  P0()
     elif tok == '}':
          if K < 1:
               print( 'ERROR unbalanced closing code block token "}"' )
               return False #===== stop recursion here
          else:
               out_f.write( '{0}\t"{1}"\t{2}\n'.format( tokid, tok, K ))
               opdb[ (tok, tokid) ] = None
               opdb[ stack[ -1 ] ] = (tok, tokid)
               for i in range( len( stack )-1, 0, -1 ):
                    if stack[ i ][ 0 ] == 'boucle':  # on s'arrête au premier boucle rencontré en remontant dans la pile
                         break
                    else:
                         if stack[ i ][ 0 ] == 'fin':  # il peut y avoir plusieurs "fin" dans le bloc d'une boucle
                              opdb[ stack[ i ] ] =  (tok, tokid)
               return P0( tokens[ 1: ], out_f, 'P0', K - 1, tokid, stack[ 0:-1], opdb  ) #=============  P0()
     else:
          print( 'ERROR unexpected end of input' )
          return False #===== stop recursion here

main_parse( terminals_automata )
