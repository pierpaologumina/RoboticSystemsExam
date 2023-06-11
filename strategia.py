from phidias.Types import *
from phidias.Lib import *
from phidias.Main import *
from phidias.Agent import *

from utilities import *

class link(Belief): pass
class path(Procedure): pass
class select_min(Procedure): pass
class show_min(Procedure): pass
class selected(SingletonBelief): pass

# Procedura che consenta al multirotore di effettuare la scansione, blocco per blocco, 
# ed il prelevamento del blocco stesso
class scan_and_pick(Procedure) : pass

# ActiveBelief to prevent cyclic paths
class nodeNotInPath(ActiveBelief):
  def evaluate(self, P, Node):
    return (Node() not in P())



# Server beliefs
class generate_blocks(Belief): pass
class go_to_node(Belief): pass
class send_held_block(Belief): pass
class sense_color(Belief): pass

# Reactors
class target_got(Reactor): pass
class color(Reactor): pass
class releaseBlockToTower(Reactor): pass


class generate(Procedure) : pass
class generaESeguiPercorso(Procedure) : pass
class raggiungiNodo(Procedure) : pass
class inviaCatturaBlocco(Procedure) : pass
class verificaColoreBlocco(Procedure) : pass
class send_releaseBlock(Procedure) : pass


class bloccoPreso(Belief): pass
class slotDeiBlocchi(Belief): pass
class slotNonAncoraControllato(Belief): pass
class nodoPosizioneAttuale(Belief): pass
class nodoArrivoParziale(Belief): pass
class lunghezzaPercorso(Belief): pass
class coloreRilevato(Belief): pass





#
def_vars('Src', 'Dest', 'Next', 'Cost', 'P', 'Total', 'CurrentMin', 'CurrentMinCost', 'DRONE', 'BLOCCO','NODO', 'INDICE_NODO_PARZIALE', 'NOME_NODO_PARZIALE', 'LPERCORSO', '_A', 'COLOR', 'COLORE')
class main(Agent):
    def main(self):

        ### Procedura adibita all'implementazione dell'algoritmo del cammino minimo ###
        path(Src, Dest) >> \
        [
            path([], 0, Src, Dest),
            show_min()
        ]

        path(P, Total, Dest, Dest) >> \
        [ 
            "P.append(Dest)", 
            #show_line(P, " ", Total),
            +selected(P, Total)
        ]
        path(P, Total, Src,  Dest)['all'] / (link(Src,Next,Cost) & nodeNotInPath(P,Next)) >> \
        [
            "P = P.copy()",
            "P.append(Src)",
            "Total = Total + Cost",
            select_min(P, Total, Next, Dest)
        ]

        select_min(P, Total, Next, Dest) / (selected(CurrentMin, CurrentMinCost) & gt(Total, CurrentMinCost)) >> \
        [
            #show_line(P, " ", Next, ", cost ", Total, " [CUT]")
        ]
        select_min(P, Total, Next, Dest) >> \
        [
            path(P, Total, Next, Dest)
        ]

        show_min() / selected(CurrentMin, CurrentMinCost)  >> \
        [
            show_line("Minimum Cost Path ", CurrentMin, ", cost ", CurrentMinCost),
            "LPERCORSO = len(CurrentMin)",
            +lunghezzaPercorso(LPERCORSO)
        ]
        ###---------------------------------FINE--------------------------------------###


        ### Procedura adibita alla generazione dei 10 blocchi ###
        generate() >> \
        [ 
            show_line("[ROBOT COMMUNICATION] : richiesta generazione 10 blocchi"),
            +generate_blocks()[{'to': 'robot@127.0.0.1:6566'}] #,
            #restoreSlots()
        ]
        ### -----------------------FINE---------------------------###

        ### Procedura che consenta al multirotore di effettuare la scansione, blocco per blocco, 
        ### ed il prelevamento del blocco stesso
        scan_and_pick() >> \
        [
            generaESeguiPercorso()
        ]


        generaESeguiPercorso() / (lunghezzaPercorso(LPERCORSO) & selected(CurrentMin, CurrentMinCost) & nodoArrivoParziale(INDICE_NODO_PARZIALE) & bloccoPreso(BLOCCO) & slotNonAncoraControllato(NODO) & slotDeiBlocchi(NODO) & nodoPosizioneAttuale(DRONE) & eq(BLOCCO,0)) >> \
        [
            show_line("--------BLOCCO NON IN POSSESSO-------", BLOCCO),
            -lunghezzaPercorso(LPERCORSO),
            -selected(CurrentMin, CurrentMinCost),
            -nodoArrivoParziale(INDICE_NODO_PARZIALE),
            path(DRONE,NODO),
            +nodoArrivoParziale(0),
            raggiungiNodo()
            
        ]

        generaESeguiPercorso() / (lunghezzaPercorso(LPERCORSO) & selected(CurrentMin, CurrentMinCost) & nodoArrivoParziale(INDICE_NODO_PARZIALE) & bloccoPreso(BLOCCO) & nodoPosizioneAttuale(DRONE) & eq(BLOCCO,1)) >> \
        [
            show_line("--------BLOCCO IN POSSESSO-------", BLOCCO),
            -selected(CurrentMin, CurrentMinCost),
            -nodoArrivoParziale(INDICE_NODO_PARZIALE),
            -lunghezzaPercorso(LPERCORSO),
            path(DRONE,'nodo_target'),
            +nodoArrivoParziale(0),
            raggiungiNodo()
        ]

        raggiungiNodo() / (nodoPosizioneAttuale(DRONE) & nodoArrivoParziale(INDICE_NODO_PARZIALE) & lunghezzaPercorso(LPERCORSO) & selected(CurrentMin, CurrentMinCost) & lt(INDICE_NODO_PARZIALE,LPERCORSO)) >> \
        [   
            -nodoPosizioneAttuale(DRONE),
            'NOME_NODO_PARZIALE = CurrentMin[INDICE_NODO_PARZIALE]',
            +nodoPosizioneAttuale(NOME_NODO_PARZIALE),
            +go_to_node(NOME_NODO_PARZIALE)[{'to': 'robot@127.0.0.1:6566'}]
        ]
        
        raggiungiNodo() / (nodoPosizioneAttuale(DRONE) & nodoArrivoParziale(INDICE_NODO_PARZIALE) & lunghezzaPercorso(LPERCORSO) & eq(INDICE_NODO_PARZIALE,LPERCORSO) & neq(DRONE,'nodo_target')) >> \
        [   
            verificaColoreBlocco(),
            show_line("--------verificaColoreBlocco-------", DRONE)
            
            #generaESeguiPercorso()
        ]

        raggiungiNodo() / (selected(CurrentMin, CurrentMinCost) & nodoPosizioneAttuale(DRONE) & eq(DRONE,'nodo_target')) >> \
        [  
            show_line("--------RILASCIO BLOCCO-------", DRONE),
            'Src = CurrentMin[0]',
            show_line("--------Src-------", Src),
            send_releaseBlock(),
            -slotNonAncoraControllato(Src),
            -bloccoPreso(1),
            +bloccoPreso(0),
            generaESeguiPercorso()
        ]

        ### ricezione della risposta 
        +target_got()[{'from': _A}] / ( nodoArrivoParziale(INDICE_NODO_PARZIALE)) >> \
        [   
            -nodoArrivoParziale(INDICE_NODO_PARZIALE),
            'INDICE_NODO_PARZIALE=INDICE_NODO_PARZIALE+1',
            +nodoArrivoParziale(INDICE_NODO_PARZIALE),
            raggiungiNodo()
        ]

        verificaColoreBlocco() >> \
        [
            +sense_color()[{'to': 'robot@127.0.0.1:6566'}] 
        ]

        +color(COLOR)[{'from':_A}] / (coloreRilevato(COLORE) & nodoPosizioneAttuale(DRONE) & selected(CurrentMin, CurrentMinCost)) >> \
        [ 
            show_line("[ROBOT] : Color ", COLOR, " sampled in slot "),
            -coloreRilevato(COLORE),
            +coloreRilevato(COLOR),
            inviaCatturaBlocco(DRONE)
        ]

        inviaCatturaBlocco(DRONE) / (coloreRilevato(COLORE) & neq(COLORE,'blue')) >> \
        [
            -bloccoPreso(0),
            +bloccoPreso(1),
            +send_held_block(DRONE)[{'to': 'robot@127.0.0.1:6566'}],
            generaESeguiPercorso()
        ]
        inviaCatturaBlocco(DRONE) / (nodoPosizioneAttuale(DRONE) & coloreRilevato(COLORE) & eq(COLORE,'blue')) >> \
        [
            -slotNonAncoraControllato(DRONE),
            generaESeguiPercorso()
        ]

        send_releaseBlock() >> [ +releaseBlockToTower()[{'to': 'robot@127.0.0.1:6566'}] ]






       
        

ag = main()
ag.start()

block_slots =	{
  #sotto
  "nodo_slot_A": (70,660),
  "nodo_slot_B": (170,690),
  "nodo_slot_C": (270,690),
  "nodo_slot_D": (370,690),
  "nodo_slot_E": (470,690),
  #sopra
  "nodo_slot_F": (70,180),
  "nodo_slot_G": (170,180),
  "nodo_slot_H": (270,180),
  "nodo_slot_I": (370,180),
  "nodo_slot_J": (470,180)
}

nodi =	{
  #sotto
  "nodo_slot_A": (470,600),
  "nodo_slot_B": (370,630),
  "nodo_slot_C": (270,630),
  "nodo_slot_D": (170,630),
  "nodo_slot_E": (70,630),
  #sopra
  "nodo_slot_F": (470,120),
  "nodo_slot_G": (370,120),
  "nodo_slot_H": (270,120),
  "nodo_slot_I": (170,120),
  "nodo_slot_J": (70,120),
  #altri
  "nodo_A": (580,70),
  "nodo_B": (730,120),
  "nodo_C": (700,330),
  "nodo_D": (900,330),
  "nodo_E": (470,500),
  "nodo_F": (600,530),
  "nodo_G": (900,600),
  "nodo_H": (1145,330),
  "nodo_target": (1145,450),
  "nodo_start": (640,655)
}

edge =	[]
#archi del nodo "nodo_slot_A"
edge.append(("nodo_slot_A","nodo_slot_B",int(math.ceil(distanceCouple(nodi["nodo_slot_A"],nodi["nodo_slot_B"])))))
edge.append(("nodo_slot_A","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_slot_A"],nodi["nodo_E"])))))
#archi del nodo "nodo_slot_B"
edge.append(("nodo_slot_B","nodo_slot_A",int(math.ceil(distanceCouple(nodi["nodo_slot_B"],nodi["nodo_slot_A"])))))
edge.append(("nodo_slot_B","nodo_slot_C",int(math.ceil(distanceCouple(nodi["nodo_slot_B"],nodi["nodo_slot_C"])))))
edge.append(("nodo_slot_B","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_slot_B"],nodi["nodo_E"])))))
#archi del nodo "nodo_slot_C"
edge.append(("nodo_slot_C","nodo_slot_B",int(math.ceil(distanceCouple(nodi["nodo_slot_C"],nodi["nodo_slot_B"])))))
edge.append(("nodo_slot_C","nodo_slot_D",int(math.ceil(distanceCouple(nodi["nodo_slot_C"],nodi["nodo_slot_D"])))))
edge.append(("nodo_slot_C","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_slot_C"],nodi["nodo_E"])))))
#archi del nodo "nodo_slot_D"
edge.append(("nodo_slot_D","nodo_slot_C",int(math.ceil(distanceCouple(nodi["nodo_slot_D"],nodi["nodo_slot_C"])))))
edge.append(("nodo_slot_D","nodo_slot_E",int(math.ceil(distanceCouple(nodi["nodo_slot_D"],nodi["nodo_slot_E"])))))
edge.append(("nodo_slot_D","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_slot_D"],nodi["nodo_E"])))))
#archi del nodo "nodo_slot_E"
edge.append(("nodo_slot_E","nodo_slot_D",int(math.ceil(distanceCouple(nodi["nodo_slot_E"],nodi["nodo_slot_D"])))))
edge.append(("nodo_slot_E","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_slot_E"],nodi["nodo_E"])))))
#archi del nodo "nodo_slot_F"
edge.append(("nodo_slot_F","nodo_slot_G",int(math.ceil(distanceCouple(nodi["nodo_slot_F"],nodi["nodo_slot_G"])))))
edge.append(("nodo_slot_F","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_slot_F"],nodi["nodo_A"])))))
#archi del nodo "nodo_slot_G"
edge.append(("nodo_slot_G","nodo_slot_F",int(math.ceil(distanceCouple(nodi["nodo_slot_G"],nodi["nodo_slot_F"])))))
edge.append(("nodo_slot_G","nodo_slot_H",int(math.ceil(distanceCouple(nodi["nodo_slot_G"],nodi["nodo_slot_H"])))))
edge.append(("nodo_slot_G","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_slot_G"],nodi["nodo_A"])))))
#archi del nodo "nodo_slot_H"
edge.append(("nodo_slot_H","nodo_slot_G",int(math.ceil(distanceCouple(nodi["nodo_slot_H"],nodi["nodo_slot_G"])))))
edge.append(("nodo_slot_H","nodo_slot_I",int(math.ceil(distanceCouple(nodi["nodo_slot_H"],nodi["nodo_slot_I"])))))
edge.append(("nodo_slot_H","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_slot_H"],nodi["nodo_A"])))))
#archi del nodo "nodo_slot_I"
edge.append(("nodo_slot_I","nodo_slot_H",int(math.ceil(distanceCouple(nodi["nodo_slot_I"],nodi["nodo_slot_H"])))))
edge.append(("nodo_slot_I","nodo_slot_J",int(math.ceil(distanceCouple(nodi["nodo_slot_I"],nodi["nodo_slot_J"])))))
edge.append(("nodo_slot_I","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_slot_I"],nodi["nodo_A"])))))
#archi del nodo "nodo_slot_J"
edge.append(("nodo_slot_J","nodo_slot_I",int(math.ceil(distanceCouple(nodi["nodo_slot_J"],nodi["nodo_slot_I"])))))
edge.append(("nodo_slot_J","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_slot_J"],nodi["nodo_A"])))))


#archi del nodo "nodo_A"
edge.append(("nodo_A","nodo_slot_F",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_slot_F"])))))
edge.append(("nodo_A","nodo_slot_G",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_slot_G"])))))
edge.append(("nodo_A","nodo_slot_H",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_slot_H"])))))
edge.append(("nodo_A","nodo_slot_I",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_slot_I"])))))
edge.append(("nodo_A","nodo_slot_J",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_slot_J"])))))
edge.append(("nodo_A","nodo_B",int(math.ceil(distanceCouple(nodi["nodo_A"],nodi["nodo_B"])))))
#archi del nodo "nodo_B"
edge.append(("nodo_B","nodo_A",int(math.ceil(distanceCouple(nodi["nodo_B"],nodi["nodo_A"])))))
edge.append(("nodo_B","nodo_C",int(math.ceil(distanceCouple(nodi["nodo_B"],nodi["nodo_C"])))))
#archi del nodo "nodo_C"
edge.append(("nodo_C","nodo_B",int(math.ceil(distanceCouple(nodi["nodo_C"],nodi["nodo_B"])))))
edge.append(("nodo_C","nodo_D",int(math.ceil(distanceCouple(nodi["nodo_C"],nodi["nodo_D"])))))
edge.append(("nodo_C","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_C"],nodi["nodo_E"])))))
edge.append(("nodo_C","nodo_F",int(math.ceil(distanceCouple(nodi["nodo_C"],nodi["nodo_F"])))))
#archi del nodo "nodo_D"
edge.append(("nodo_D","nodo_C",int(math.ceil(distanceCouple(nodi["nodo_D"],nodi["nodo_C"])))))
edge.append(("nodo_D","nodo_G",int(math.ceil(distanceCouple(nodi["nodo_D"],nodi["nodo_G"])))))
edge.append(("nodo_D","nodo_H",int(math.ceil(distanceCouple(nodi["nodo_D"],nodi["nodo_H"])))))
#archi del nodo "nodo_E"
edge.append(("nodo_E","nodo_slot_A",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_slot_A"])))))
edge.append(("nodo_E","nodo_slot_B",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_slot_B"])))))
edge.append(("nodo_E","nodo_slot_C",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_slot_C"])))))
edge.append(("nodo_E","nodo_slot_D",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_slot_D"])))))
edge.append(("nodo_E","nodo_slot_E",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_slot_E"])))))
edge.append(("nodo_E","nodo_F",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_F"])))))
edge.append(("nodo_E","nodo_C",int(math.ceil(distanceCouple(nodi["nodo_E"],nodi["nodo_C"])))))
#archi del nodo "nodo_F"
edge.append(("nodo_F","nodo_start",int(math.ceil(distanceCouple(nodi["nodo_F"],nodi["nodo_start"])))))
edge.append(("nodo_F","nodo_E",int(math.ceil(distanceCouple(nodi["nodo_F"],nodi["nodo_E"])))))
edge.append(("nodo_F","nodo_C",int(math.ceil(distanceCouple(nodi["nodo_F"],nodi["nodo_C"])))))
#archi del nodo "nodo_G"
edge.append(("nodo_G","nodo_start",int(math.ceil(distanceCouple(nodi["nodo_G"],nodi["nodo_start"])))))
edge.append(("nodo_G","nodo_D",int(math.ceil(distanceCouple(nodi["nodo_G"],nodi["nodo_D"])))))
#archi del nodo "nodo_H"
edge.append(("nodo_H","nodo_target",int(math.ceil(distanceCouple(nodi["nodo_H"],nodi["nodo_target"])))))
edge.append(("nodo_H","nodo_D",int(math.ceil(distanceCouple(nodi["nodo_H"],nodi["nodo_D"])))))
#archi del nodo "nodo_start"
edge.append(("nodo_start","nodo_G",int(math.ceil(distanceCouple(nodi["nodo_start"],nodi["nodo_G"])))))
edge.append(("nodo_start","nodo_F",int(math.ceil(distanceCouple(nodi["nodo_start"],nodi["nodo_F"])))))
#archi del nodo "nodo_target"
edge.append(("nodo_target","nodo_H",int(math.ceil(distanceCouple(nodi["nodo_target"],nodi["nodo_H"])))))  




for ed in edge:
  ag.assert_belief(link(ed[0],ed[1],ed[2]))


for block_slot in block_slots:
  ag.assert_belief(slotDeiBlocchi(block_slot))
  ag.assert_belief(slotNonAncoraControllato(block_slot))

ag.assert_belief(nodoPosizioneAttuale("nodo_start"))
ag.assert_belief(bloccoPreso(0))
ag.assert_belief(lunghezzaPercorso(999))
ag.assert_belief(selected([], 999))
ag.assert_belief(nodoArrivoParziale(0))
ag.assert_belief(coloreRilevato('None')),
  
PHIDIAS.run_net(globals(), 'http')
PHIDIAS.shell(globals())