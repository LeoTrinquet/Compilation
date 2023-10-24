from enum import Enum
import sys

#<== GLOBAL ==>

class Token_Type(Enum):
  IDENTIFICATEUR = 1
  CONSTANTE = 2
  PLUS = 3
  MOINS = 4
  ETOILE = 5
  SLASH = 6
  POURCENT = 7
  EXCLAMATION = 8
  ESPERLUETTE = 9
  INFERIEUR = 10
  INFERIEUREGAL = 11
  SUPERIEUR = 12
  SUPERIEUREGAL = 13
  DOUBLEEGAL = 14
  EXCLAMATIONEGAL = 15
  DOUBLEESPERLUETTE = 16
  DOUBLEBARRE = 17
  PARENTHESEOUVRANTE = 18
  PARENTHESEFERMANTE = 19
  CROCHETOUVRANT = 20
  CROCHETFERMANT = 21
  ACCOLADEOUVRANTE = 22
  ACCOLADEFERMANTE = 23
  VIRGULE = 24
  POINTVIRGULE = 25
  EGAL = 26
  CLE_INT = 27
  CLE_FOR = 28
  CLE_WHILE = 29
  CLE_IF = 30
  CLE_ELSE = 31
  CLE_DO = 32
  CLE_BREAK = 33
  CLE_CONTINUE = 34
  CLE_RETURN = 35
  EOF = 36
  BARRE = 37
  CLE_DEBUG = 38
  CLE_SEND = 39

token = None  # variable globale Token actuel
last = None  # variable globale Token Précédent
PileVariable = []
nbvar = 0
nblabel = 0
label_continue = 0
label_break = 0

#<== ANALYSE LEXICALE ==>

def Next():
  global token
  global last
  global code_source

  last = token
  value = ""
  #skip espace
  code_source = code_source.strip()
  #je verifie si on est à la fin du fichier ( dans ce cas , token EOF)
  if (len(code_source) == 0):
    token = {"type": Token_Type.EOF}
    return
  #je vérifie si le caractère actuel est un chiffre (dans ce cas , je récup tous les chiffres qui le suive et je le converti en int et je le stock dans value)
  if code_source[0].isdigit():
    value += code_source[0]
    code_source = code_source[1:]
    for i in code_source:
      if i.isdigit():
        value += i
        code_source = code_source[1:]
      else:
        break
    token = {"type": Token_Type.CONSTANTE, "value": int(value)}
    return
  #je vérifie si le caractère actuel est une lettre ou un "_"  (dans ce cas , je récup toutes les lettres ou "_" ou chiffre qui le suive
  #et ensuite je compare la valeur avec celle des mots clés, si ==, alors token CLE_XX, sinon token IDENTIFICATEUR)
  if code_source[0].isalpha() or code_source[0] == "_":
    value += code_source[0]
    code_source = code_source[1:]
    for i in code_source:
      if i.isalpha() or i == "_" or i.isdigit():
        value += i
        code_source = code_source[1:]
      else:
        break
    if value == "int":
      token = {"type": Token_Type.CLE_INT}
    elif value == "for":
      token = {"type": Token_Type.CLE_FOR}
    elif value == "while":
      token = {"type": Token_Type.CLE_WHILE}
    elif value == "if":
      token = {"type": Token_Type.CLE_IF}
    elif value == "else":
      token = {"type": Token_Type.CLE_ELSE}
    elif value == "do":  # TESTER SI ça marche
      token = {"type": Token_Type.CLE_DO}
    elif value == "break":
      token = {"type": Token_Type.CLE_BREAK}
    elif value == "continue":
      token = {"type": Token_Type.CLE_CONTINUE}
    elif value == "return":
      token = {"type": Token_Type.CLE_RETURN}
    elif value == "debug":
      token = {"type": Token_Type.CLE_DEBUG}
    elif value == "send":
      token = {"type": Token_Type.CLE_SEND}
    else:
      token = {"type": Token_Type.IDENTIFICATEUR, "value": value}
    return
  #je vérifie si le caractère est un +, (dans ce cas , token PLUS)
  if code_source[0] == "+":
    code_source = code_source[1:]
    token = {"type": Token_Type.PLUS}
    return
  #je vérifie si le caractère est un < ,(dans ce cas , si le caractère suivant est un = alors je le récup aussi et Token INFERIEUROUEGALE
  # sinon TOKEN INFERIEUR )
  if code_source[0] == "<":
    code_source = code_source[1:]
    if code_source[0] == "=":
      code_source = code_source[1:]
      token = {"type": Token_Type.INFERIEUREGAL}
    else:
      token = {"type": Token_Type.INFERIEUR}
    return
  #ETC...
  if code_source[0] == "-":
    code_source = code_source[1:]
    token = {"type": Token_Type.MOINS}
    return
  if code_source[0] == "*":
    code_source = code_source[1:]
    token = {"type": Token_Type.ETOILE}
    return
  if code_source[0] == "/":
    code_source = code_source[1:]
    token = {"type": Token_Type.SLASH}
    return
  if code_source[0] == "%":
    code_source = code_source[1:]
    token = {"type": Token_Type.POURCENT}
    return
  if code_source[0] == "!":
    code_source = code_source[1:]
    if code_source[0] == "=":
      code_source = code_source[1:]
      token = {"type": Token_Type.EXCLAMATIONEGAL}
    else:
      token = {"type": Token_Type.EXCLAMATION}
    return
  if code_source[0] == "&":
    code_source = code_source[1:]
    if code_source[0] == "&":
      code_source = code_source[1:]
      token = {"type": Token_Type.DOUBLEESPERLUETTE}
    else:
      token = {"type": Token_Type.ESPERLUETTE}
    return
  if code_source[0] == "|":
    code_source = code_source[1:]
    if code_source[0] == "|":
      code_source = code_source[1:]
      token = {"type": Token_Type.DOUBLEBARRE}
    else:
      token = {"type": Token_Type.BARRE}
    return
  if code_source[0] == "=":
    code_source = code_source[1:]
    if code_source[0] == "=":
      code_source = code_source[1:]
      token = {"type": Token_Type.DOUBLEEGAL}
    else:
      token = {"type": Token_Type.EGAL}
    return
  if code_source[0] == ">":
    code_source = code_source[1:]
    if code_source[0] == "=":
      code_source = code_source[1:]
      token = {"type": Token_Type.SUPERIEUREGAL}
    else:
      token = {"type": Token_Type.SUPERIEUR}
    return
  if code_source[0] == "(":
    code_source = code_source[1:]
    token = {"type": Token_Type.PARENTHESEOUVRANTE}
    return
  if code_source[0] == ")":
    code_source = code_source[1:]
    token = {"type": Token_Type.PARENTHESEFERMANTE}
    return
  if code_source[0] == "[":
    code_source = code_source[1:]
    token = {"type": Token_Type.CROCHETOUVRANT}
    return
  if code_source[0] == "]":
    code_source = code_source[1:]
    token = {"type": Token_Type.CROCHETFERMANT}
    return
  if code_source[0] == "{":
    code_source = code_source[1:]
    token = {"type": Token_Type.ACCOLADEOUVRANTE}
    return
  if code_source[0] == "}":
    code_source = code_source[1:]
    token = {"type": Token_Type.ACCOLADEFERMANTE}
    return
  if code_source[0] == ",":
    code_source = code_source[1:]
    token = {"type": Token_Type.VIRGULE}
    return
  if code_source[0] == ";":
    code_source = code_source[1:]
    token = {"type": Token_Type.POINTVIRGULE}
    return

def Check(T):
  if token["type"] == T:
    Next()
    return True
  return False

def Accept(T):
  if not (Check(T)):
    raise ValueError("ERROR TOKEN NOT ACCEPTED")

def InitAnalyseLexicale(nom_fichier):
  global code_source

  fichier_code = open(nom_fichier, "r")
  code_source = fichier_code.read()
  fichier_code.close()
  Next()

#<== ANALYSE SYNTAXIQUE ==>

#Atome
def A():
  if Check(Token_Type.CONSTANTE):
    return {"type": "Noeud_constante", "value": last["value"]}
  elif Check(Token_Type.IDENTIFICATEUR):
    return {"type": "Noeud_Reference", "value": last["value"], "symbole": {}}
  elif Check(Token_Type.PARENTHESEOUVRANTE):
    N = E(0)
    Accept(Token_Type.PARENTHESEFERMANTE)
    return N
  else:
    raise ValueError("ERROR ATOM")

#Suffixe
def S():
  N = A()
  if (Check(Token_Type.PARENTHESEOUVRANTE)):
    N = {"type": "Noeud_Appel", "enfant": [N]}
    while (not Check(Token_Type.PARENTHESEFERMANTE)):
      N["enfant"].append(E(0))
      if (Check(Token_Type.PARENTHESEFERMANTE)):
        break
      Accept(Token_Type.VIRGULE)
  elif (Check(Token_Type.CROCHETOUVRANT)):
    e = E(0)
    a = N
    Accept(Token_Type.CROCHETFERMANT)
    N = {"type": "Noeud_Indirection", "enfant": []}
    N["enfant"].append({"type": "Noeud_Addition", "enfant": []})
    N["enfant"][0]["enfant"].append(a)
    N["enfant"][0]["enfant"].append(e)
  return N

#Prefixe
def P():
  if Check(Token_Type.MOINS):
    N = P()
    return {"type": "Noeud_MoinsUnaire", "enfant": [N]}
  elif Check(Token_Type.EXCLAMATION):
    N = P()
    return {"type": "Noeud_Not", "enfant": [N]}
  elif Check(Token_Type.PLUS):
    N = P()
    return N
  elif Check(Token_Type.ETOILE):
    N = P()
    return {"type": "Noeud_Indirection", "enfant": [N]}
  elif Check(Token_Type.ESPERLUETTE):
    N = P()
    return {"type": "Noeud_Adresse", "enfant": [N]}
  else:
    N = S()
    return N

Operateur = {
    Token_Type.EGAL: {
        "noeud": "Noeud_Affectation",
        "prio": 1,
        "AssocDroite": 1
    },
    Token_Type.DOUBLEBARRE: {
        "noeud": "Noeud_OR",
        "prio": 2,
        "AssocDroite": 0
    },
    Token_Type.DOUBLEESPERLUETTE: {
        "noeud": "Noeud_AND",
        "prio": 3,
        "AssocDroite": 0
    },
    Token_Type.DOUBLEEGAL: {
        "noeud": "Noeud_Egalite",
        "prio": 4,
        "AssocDroite": 0
    },
    Token_Type.EXCLAMATIONEGAL: {
        "noeud": "Noeud_Different",
        "prio": 4,
        "AssocDroite": 0
    },
    Token_Type.INFERIEUR: {
        "noeud": "Noeud_Inferieur",
        "prio": 5,
        "AssocDroite": 0
    },
    Token_Type.SUPERIEUR: {
        "noeud": "Noeud_Superieur",
        "prio": 5,
        "AssocDroite": 0
    },
    Token_Type.INFERIEUREGAL: {
        "noeud": "Noeud_InferieurEgal",
        "prio": 5,
        "AssocDroite": 0
    },
    Token_Type.SUPERIEUREGAL: {
        "noeud": "Noeud_SuperieurEgal",
        "prio": 5,
        "AssocDroite": 0
    },
    Token_Type.PLUS: {
        "noeud": "Noeud_Addition",
        "prio": 6,
        "AssocDroite": 0
    },
    Token_Type.MOINS: {
        "noeud": "Noeud_Soustraction",
        "prio": 6,
        "AssocDroite": 0
    },
    Token_Type.ETOILE: {
        "noeud": "Noeud_Multiplication",
        "prio": 7,
        "AssocDroite": 0
    },
    Token_Type.SLASH: {
        "noeud": "Noeud_Division",
        "prio": 7,
        "AssocDroite": 0
    },
    Token_Type.POURCENT: {
        "noeud": "Noeud_Modulo",
        "prio": 7,
        "AssocDroite": 0
    },
}

#Expression
def E(Priomin):
  N = P()
  while (token["type"] in Operateur):
    Op = Operateur[token["type"]]
    if Op["prio"] > Priomin:
      Next()
      M = E(Op["prio"] - Op["AssocDroite"])
      N = {"type": Op["noeud"], "enfant": [N, M]}
    else:
      break
  return N

#Instruction
def I():
  if (Check(Token_Type.POINTVIRGULE)):
    return {"type": "Noeud_Vide"}
  elif (Check(Token_Type.CLE_INT)):
    N = {"type": "Noeud_Sequence", "enfant": []}
    while (True):
      Accept(Token_Type.IDENTIFICATEUR)
      N["enfant"].append({"type": "Noeud_Declaration", "value": last["value"]})
      if (not Check(Token_Type.VIRGULE)):
        break
    Accept(Token_Type.POINTVIRGULE)
    return N
  elif (Check(Token_Type.ACCOLADEOUVRANTE)):
    N = {"type": "Noeud_Block", "enfant": []}
    while (not Check(Token_Type.ACCOLADEFERMANTE)):
      N["enfant"].append(I())
    return N
  elif (Check(Token_Type.CLE_DEBUG)):
    N = E(0)
    Accept(Token_Type.POINTVIRGULE)
    return {"type": "Noeud_Debug", "enfant": [N]}
  elif (Check(Token_Type.CLE_SEND)):
    N = E(0)
    Accept(Token_Type.POINTVIRGULE)
    return {"type": "Noeud_Send", "enfant": [N]}
  elif (Check(Token_Type.CLE_RETURN)):
    N = E(0)
    Accept(Token_Type.POINTVIRGULE)
    return {"type": "Noeud_Return", "enfant": [N]}
  elif (Check(Token_Type.CLE_IF)):
    Accept(Token_Type.PARENTHESEOUVRANTE)
    e = E(0)
    Accept(Token_Type.PARENTHESEFERMANTE)
    i1 = I()
    N = {"type": "Noeud_Condition", "enfant": [e, i1]}
    if (Check(Token_Type.CLE_ELSE)):
      i2 = I()
      N["enfant"].append(i2)
    return N
  elif (Check(Token_Type.CLE_WHILE)):
    Accept(Token_Type.PARENTHESEOUVRANTE)
    e = E(0)
    Accept(Token_Type.PARENTHESEFERMANTE)
    i = I()
    l = {"type": "Noeud_Loop", "enfant": []}
    t = {"type": "Noeud_Target"}
    c = {"type": "Noeud_Condition", "enfant": []}
    b = {"type": "Noeud_Break"}
    l["enfant"].append(t)
    l["enfant"].append(c)
    c["enfant"].append(e)
    c["enfant"].append(i)
    c["enfant"].append(b)
    return l
  elif (Check(Token_Type.CLE_FOR)):
    Accept(Token_Type.PARENTHESEOUVRANTE)
    E1 = E(0)
    Accept(Token_Type.POINTVIRGULE)
    E2 = E(0)
    Accept(Token_Type.POINTVIRGULE)
    E3 = E(0)
    Accept(Token_Type.PARENTHESEFERMANTE)
    i = I()

    s1 = {"type": "Noeud_Sequence", "enfant": []}
    d1 = {"type": "Noeud_Drop", "enfant": []}
    l = {"type": "Noeud_Loop", "enfant": []}
    c = {"type": "Noeud_Condition", "enfant": []}
    b = {"type": "Noeud_Break"}
    t = {"type": "Noeud_Target"}
    d2 = {"type": "Noeud_Drop", "enfant": []}
    s2 = {"type": "Noeud_Sequence", "enfant": []}

    d1["enfant"].append(E1)
    c["enfant"].append(E2)
    s2["enfant"].append(i)
    s2["enfant"].append(t)
    d2["enfant"].append(E3)
    s2["enfant"].append(d2)
    c["enfant"].append(s2)
    c["enfant"].append(b)
    l["enfant"].append(c)
    s1["enfant"].append(d1)
    s1["enfant"].append(l)

    return s1

  elif (Check(Token_Type.CLE_BREAK)):
    Accept(Token_Type.POINTVIRGULE)
    N = {"type": "Noeud_Break"}
    return N
  elif (Check(Token_Type.CLE_CONTINUE)):
    Accept(Token_Type.POINTVIRGULE)
    N = {"type": "Noeud_Continue"}
    return N

  else:
    N = E(0)
    Accept(Token_Type.POINTVIRGULE)
    return {"type": "Noeud_Drop", "enfant": [N]}

def AnalyseSyntaxique():
  Accept(Token_Type.CLE_INT)
  Accept(Token_Type.IDENTIFICATEUR)
  N = {"type": "Noeud_Fonction", "value": last["value"], "enfant": []}
  Accept(Token_Type.PARENTHESEOUVRANTE)
  while (Check(Token_Type.CLE_INT)):
    Accept(Token_Type.IDENTIFICATEUR)
    N["enfant"].append({"type": "Noeud_Declaration", "value": last["value"]})
    if (Check(Token_Type.VIRGULE)):
      continue
    break
  Accept(Token_Type.PARENTHESEFERMANTE)
  N["enfant"].append(I())
  return N

#<== ANALYSE SEMANTIQUE ==>

def Begin():
  PileVariable.append({"nom": ""})
  return

def End():
  if (len(PileVariable) > 0):
    while (PileVariable[len(PileVariable) - 1]["nom"] != ""):
      PileVariable.pop()
    PileVariable.pop()
  return

def Cherche(nom):
  for i in reversed(PileVariable):
    if i["nom"] == nom:
      return i["symbole"]
  raise ValueError("variable non déclarée")

def Declare(nom):
  for i in reversed(PileVariable):
    if i["nom"] == nom:
      raise ValueError("variable déjà déclarée")
    if i["nom"] == "":
      break
  S = {}  #NouveauSymbole
  PileVariable.append({"nom": nom, "symbole": S})
  return S

def AnalyseSemantique(N):
  global nbvar
  typeNoeud = N["type"]
  if typeNoeud == "Noeud_Block":
    Begin()
    for enfant in N["enfant"]:
      AnalyseSemantique(enfant)
    End()
  elif typeNoeud == "Noeud_Declaration":
    S = Declare(N["value"])
    S["position"] = nbvar
    nbvar += 1
    S["type"] = "variable_locale"
  elif typeNoeud == "Noeud_Reference":
    S = Cherche(N["value"])
    N["symbole"] = S
  elif typeNoeud == "Noeud_Fonction":
    nbvar = 0
    S = Declare(N["value"])
    Begin()
    for enfant in N["enfant"]:
      AnalyseSemantique(enfant)
    End()
    S["type"] = "symbole_fonction"
    S["nbvar"] = nbvar - (len(N["enfant"]) - 1)
    N["symbole"] = S
  else:
    if "enfant" in N:
      for enfant in N["enfant"]:
        AnalyseSemantique(enfant)

#<== GENERATION DE CODE ==>

def GenCode(N):
  global nblabel
  global label_continue
  global label_break
  typeNoeud = N["type"]
  if typeNoeud == "Noeud_constante":
    print("push", N["value"])
  elif typeNoeud == "Noeud_Not":
    GenCode(N["enfant"][0])
    print("not")
  elif typeNoeud == "Noeud_MoinsUnaire":
    print("push 0")
    GenCode(N["enfant"][0])
    print("sub")
  elif typeNoeud == "Noeud_Indirection":
    GenCode(N["enfant"][0])
    print("read")
  elif typeNoeud == "Noeud_Adresse":
    if (N["enfant"][0]["type"] != "Noeud_Reference") and (
        N["enfant"][0]["symbole"]["type"] == "variable_locale"):
      raise ValueError("ERROR ADRESS")
    print("prep start")
    print("swap")
    print("drop 1")
    print("push", N["enfant"][0]["symbole"]["position"] + 1)
    print("sub")
  elif typeNoeud == "Noeud_OR":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("or")
  elif typeNoeud == "Noeud_AND":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("and")
  elif typeNoeud == "Noeud_Egalite":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmpeq")
  elif typeNoeud == "Noeud_Different":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmpne")
  elif typeNoeud == "Noeud_Inferieur":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmplt")
  elif typeNoeud == "Noeud_Superieur":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmpgt")
  elif typeNoeud == "Noeud_InferieurEgal":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmple")
  elif typeNoeud == "Noeud_SuperieurEgal":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("cmpge")
  elif typeNoeud == "Noeud_Addition":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("add")
  elif typeNoeud == "Noeud_Soustraction":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("sub")
  elif typeNoeud == "Noeud_Multiplication":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("mul")
  elif typeNoeud == "Noeud_Division":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("div")
  elif typeNoeud == "Noeud_Modulo":
    GenCode(N["enfant"][0])
    GenCode(N["enfant"][1])
    print("mod")
  elif typeNoeud == "Noeud_Block" or typeNoeud == "Noeud_Sequence":
    for item in N["enfant"]:
      GenCode(item)
  elif typeNoeud == "Noeud_Affectation":
    GenCode(N["enfant"][1])
    print("dup")
    if (N["enfant"][0]["type"]
        == "Noeud_Reference") and (N["enfant"][0]["symbole"]["type"]
                                   == "variable_locale"):
      print("set ", N["enfant"][0]["symbole"]["position"])
    elif (N["enfant"][0]["type"] == "Noeud_Indirection"):
      GenCode(N["enfant"][0]["enfant"][0])
      print("write")
    else:
      raise ValueError("ERROR ASSIGNMENT")
  elif typeNoeud == "Noeud_Debug":
    GenCode(N["enfant"][0])
    print("dbg")
  elif typeNoeud == "Noeud_Send":
    GenCode(N["enfant"][0])
    print("send")
  elif typeNoeud == "Noeud_Return":
    GenCode(N["enfant"][0])
    print("ret")
  elif typeNoeud == "Noeud_Drop":
    GenCode(N["enfant"][0])
    print("drop 1")
  elif typeNoeud == "Noeud_Reference":
    if (N["symbole"]["type"] == "variable_locale"):
      print("get ", N["symbole"]["position"])
  elif typeNoeud == "Noeud_Condition":
    if (len(N["enfant"]) == 2):
      nblabel += 1
      l1 = nblabel
      GenCode(N["enfant"][0])
      print(f"jumpf l{l1}")
      GenCode(N["enfant"][1])
      print(f".l{l1}")
    else:
      nblabel += 1
      l1 = nblabel
      nblabel += 1
      l2 = nblabel
      GenCode(N["enfant"][0])
      print(f"jumpf l{l1}")
      GenCode(N["enfant"][1])
      print(f"jump l{l2}")
      print(f".l{l1}")
      GenCode(N["enfant"][2])
      print(f".l{l2}")
  elif typeNoeud == "Noeud_Target":
    print(f".l{label_continue}")
  elif typeNoeud == "Noeud_Break":
    print(f"jump l{label_break}")
  elif typeNoeud == "Noeud_Continue":
    print(f"jump l{label_continue}")
  elif typeNoeud == "Noeud_Loop":
    save_continue = label_continue
    save_break = label_break
    nblabel += 1
    label_debut = nblabel
    nblabel += 1
    label_continue = nblabel
    nblabel += 1
    label_break = nblabel
    print(f".l{label_debut}")
    for enfant in N["enfant"]:
      GenCode(enfant)
    print(f"jump l{label_debut}")
    print(f".l{label_break}")
    label_continue = save_continue
    label_break = save_break
  elif typeNoeud == "Noeud_Fonction":
    print(f".{N['value']}")
    print("resn", N["symbole"]["nbvar"])
    GenCode(N["enfant"][-1])
    print("push 0")
    print("ret")
  elif typeNoeud == "Noeud_Appel":
    if N["enfant"][0]["type"] != "Noeud_Reference":
      raise ValueError("ERROR CALL")
    if N["enfant"][0]["symbole"]["type"] != "symbole_fonction":
      raise ValueError("ERROR CALL")
    print("prep", N["enfant"][0]["value"])
    for enfant in N["enfant"][1:]:
      GenCode(enfant)
    print("call", len(N["enfant"]) - 1)
  elif typeNoeud == "Noeud_Declaration" or typeNoeud == "Noeud_Vide":
    pass
  else:
    raise ValueError("ERROR GENCODE")

#<== COMPILATION ==>

def Compile_Fichier(nom_fichier):
  InitAnalyseLexicale(nom_fichier)
  while (token["type"] != Token_Type.EOF):
    N = AnalyseSyntaxique()
    #optimiseurSyntaxique = Optimiseur(N)
    AnalyseSemantique(N)
    GenCode(N)

def Compile():
  Compile_Fichier("lib.c")
  Compile_Fichier("test.c")
  print(".start")
  print("prep init")
  print("call 0")
  print("prep main")
  print("call 0")
  print("halt")

#def Optimiseur(N):
#    typeNoeud = N["type"]
#    if typeNoeud == "Noeud_Addition":
#        if N["enfant"][0]["type"] == "Noeud_constante" and N["enfant"][1]["type"] == "Noeud_constante":
#            return {"type":"Noeud_constante", "value":N["enfant"][0]["value"] + N["enfant"][1]["value"]}
#        else:
#            Optimiseur(N["enfant"][0])
#            Optimiseur(N["enfant"][1])
#    return N

#<== MAIN ==>
if __name__ == "__main__":

  path = 'code_compile.txt'
  sys.stdout = open(path, 'w')
  Compile()
