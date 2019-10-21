# Um comentário aqui!
DIGA Que alegria, menino!

nome_existe = EXISTE {nome}
SE not {nome_existe}
  nome = PERGUNTE Qual o seu nome?
  DIGA Prazer, {nome}!

como_vai = PERGUNTE Como vai seu dia?
SE {como_vai}  == 'bem'
  DIGA Legal. :)

SENÃO
  DIGA Poxa, que chato. :(


a = len('asdf')

DIGA {a}
