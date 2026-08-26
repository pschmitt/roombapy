"""Fault texts as iRobot's own applications word them.

## Provenance

These strings are **iRobot's**, not ours. They were extracted from the
localisation bundles shipped inside the vendor's own mobile application
(``com.irobot.home.prime`` 3.0.0) — the same text a user sees in the app
when their robot reports a fault. They are reproduced here so that a
consumer can show a person something actionable rather than a terse label.

Two things follow from that, and neither should be quietly forgotten.

**They carry iRobot's copyright.** roombapy is MIT-licensed; these strings
are not ours to relicense. They are included on the view that showing a user
their own robot's error message is reasonable use, and on the understanding
that this can be revisited if iRobot would rather it were not.

**The source is the newer application.** Whether every code means exactly
the same thing on the older, locally-controlled robots this library talks to
is *unverified*. The 48 codes that also appear in
``ROOMBA_ERROR_MESSAGES`` are listed in :data:`UNVERIFIED_OVERLAP` — for
those, our own label and the vendor's text disagree in wording, and
occasionally in emphasis, and we do not know which is right for a given
firmware. Callers that need certainty should prefer
``ROOMBA_ERROR_MESSAGES``, which has been in use against these robots for
years.

## Shape

``VENDOR_ERROR_TEXTS[code][language]`` gives ``{"title", "content"}``.
Languages: de, en, es, fr, it, nl, pl, pt.

Use :func:`vendor_error_text` rather than indexing directly; it falls back
to English and then to ``None`` instead of raising.
"""

# The strings below are verbatim vendor text and must not be reflowed:
# breaking them would change quoted content.

from __future__ import annotations

from typing import Final, TypedDict


class VendorErrorText(TypedDict):
    """One fault, in one language."""

    title: str
    content: str


#: Codes that also appear in ``ROOMBA_ERROR_MESSAGES``. The vendor wording
#: for these has **not** been verified against older robots; see the module
#: docstring.
UNVERIFIED_OVERLAP: Final[frozenset[int]] = frozenset(
    {
        1,
        2,
        4,
        5,
        6,
        7,
        9,
        10,
        12,
        14,
        16,
        18,
        19,
        22,
        24,
        26,
        29,
        30,
        32,
        33,
        35,
        36,
        42,
        44,
        46,
        47,
        48,
        66,
        68,
        69,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        109,
        110,
        111,
        114,
        115,
        119,
        120,
        121,
        1000,
        1001,
        1008,
    }
)


VENDOR_ERROR_TEXTS: Final[dict[int, dict[str, VendorErrorText]]] = {
    1: {
        "de": {
            "title": "@val wurde bewegt oder befindet sich auf einem unebenen Untergrund",
            "content": "Bewegen Sie @val auf einen neuen, ebenen Untergrund. Wenn er sich bereits auf einem ebenen Untergrund befindet, müssen Sie ihn möglicherweise neu starten. (1)",
        },
        "en": {
            "title": "@val\xa0moved or on an uneven surface",
            "content": "Move\xa0@val\xa0to a new, flat surface. If it is already on a flat surface, you may need to reboot it. (1)",
        },
        "es": {
            "title": "@val se ha movido o está en una superficie irregular",
            "content": "Mueve @val a otra superficie que sea plana. Si ya está en una superficie plana, es posible que debas reiniciarlo. (1)",
        },
        "fr": {
            "title": "@val a été déplacé ou se trouve sur une surface irrégulière",
            "content": "Déplacez @val sur une nouvelle surface plane. S’il est déjà sur une surface plane, vous devrez peut-être le redémarrer. (1)",
        },
        "it": {
            "title": "@val è stato spostato o si trova su una superficie irregolare",
            "content": "Spostare @val su una nuova superficie piana. Se è già su una superficie piana, potrebbe essere necessario riavviarlo. (1)",
        },
        "nl": {
            "title": "@val is verplaatst of staat op een oneffen oppervlak",
            "content": "Verplaats @val naar een nieuw, vlak oppervlak. Als deze al op een vlak oppervlak staat, moet u deze mogelijk opnieuw opstarten. (1)",
        },
        "pl": {
            "title": "Robot @val został przeniesiony lub znajduje się na nierównej powierzchni",
            "content": "Przenieś robota @val na nową, płaską powierzchnię. Jeśli znajduje się już na płaskiej powierzchni, może być konieczne ponowne jego uruchomienie. (1)",
        },
        "pt": {
            "title": "@val foi movido ou está numa superfície irregular",
            "content": "Mova @val para uma nova superfície plana. Se já estiver numa superfície plana, poderá ser necessário reiniciá-lo. (1)",
        },
    },
    2: {
        "de": {
            "title": "Hauptbürste klemmt",
            "content": "Entfernen Sie Hindernisse oder verwickelte Fasern von der Bürste, sodass sie sich frei drehen kann. (2)",
        },
        "en": {
            "title": "Main Brush stuck",
            "content": "Clear obstacles or tangled fibers from the brush so it can spin freely. (2)",
        },
        "es": {
            "title": "Cepillo multisuperficie atascado",
            "content": "Retira los obstáculos o las fibras enredadas del cepillo para que pueda girar libremente. (2)",
        },
        "fr": {
            "title": "La brosse principale est bloquée",
            "content": "Retirez les blocages ou les fibres emmêlées de la brosse afin qu’elle puisse tourner librement. (2)",
        },
        "it": {
            "title": "Spazzola multiuso bloccata",
            "content": "Rimuovere gli ostacoli o le fibre aggrovigliate dalla spazzola in modo che possa ruotare liberamente. (2)",
        },
        "nl": {
            "title": "Hoofdborstel zit vast",
            "content": "Verwijder obstakels of verwarde vezels uit de borstel, zodat deze vrij kan draaien. (2)",
        },
        "pl": {
            "title": "Szczotka główna jest zablokowana",
            "content": "Usuń przeszkody lub splątane włókna ze szczotki, aby mogła swobodnie się obracać. (2)",
        },
        "pt": {
            "title": "Escova principal bloqueada",
            "content": "Remova obstáculos ou fibras emaranhadas da escova para que possa rodar livremente. (2)",
        },
    },
    4: {
        "de": {
            "title": "Linkes Rad klemmt",
            "content": "Drücken Sie das Rad einige Male nach oben und unten und drehen Sie es dann, um eingeklemmten Schmutz zu lösen. Es sollte sich frei drehen lassen. (4)",
        },
        "en": {
            "title": "Left Wheel stuck",
            "content": "Push Left/Right Wheel up and down a few times, then spin it to loosen trapped debris. It should spin freely. (4)",
        },
        "es": {
            "title": "Rueda izquierda atascada",
            "content": "Empuja la rueda hacia arriba y hacia abajo unas cuantas veces, y luego gírala para soltar los residuos atrapados. Debería girar libremente. (4)",
        },
        "fr": {
            "title": "La roue gauche est bloquée",
            "content": "Actionnez la roue de haut en bas à plusieurs reprises, puis faites-la tourner pour déloger les débris coincés. Elle doit tourner librement. (4)",
        },
        "it": {
            "title": "Ruota sinistra bloccata",
            "content": "Spingere la ruota su e giù un paio di volte, quindi farla girare per estrarre i detriti incastrati. Dovrebbe girare liberamente. (4)",
        },
        "nl": {
            "title": "Linkerwiel zit vast",
            "content": "Duw het wiel een paar keer op en neer en draai het vervolgens rond om vastzittend vuil los te maken. Het moet vrij kunnen draaien. (4)",
        },
        "pl": {
            "title": "Lewe kółko jest zablokowane",
            "content": "Popchnij kółko w górę i w dół kilka razy, a następnie obróć nim, aby poluzować uwięzione zanieczyszczenia. Powinno swobodnie się obracać. (4)",
        },
        "pt": {
            "title": "Roda esquerda bloqueada",
            "content": "Empurre a roda para cima e para baixo algumas vezes e depois rode-a para soltar os resíduos presos. Deve rodar livremente. (4)",
        },
    },
    5: {
        "de": {
            "title": "Rechtes Rad klemmt",
            "content": "Drücken Sie das Rad einige Male nach oben und unten und drehen Sie es dann, um eingeklemmten Schmutz zu lösen. Es sollte sich frei drehen lassen. (5)",
        },
        "en": {
            "title": "Right Wheel stuck",
            "content": "Push Left/Right Wheel up and down a few times, then spin it to loosen trapped debris. It should spin freely. (5)",
        },
        "es": {
            "title": "Rueda derecha atascada",
            "content": "Empuja la rueda hacia arriba y hacia abajo unas cuantas veces, y luego gírala para soltar los residuos atrapados. Debería girar libremente. (5)",
        },
        "fr": {
            "title": "La roue droite est bloquée",
            "content": "Actionnez la roue de haut en bas à plusieurs reprises, puis faites-la tourner pour déloger les débris coincés. Elle doit tourner librement. (5)",
        },
        "it": {
            "title": "La ruota destra è bloccata",
            "content": "Spingere la ruota su e giù un paio di volte, quindi farla girare per estrarre i detriti incastrati. Dovrebbe girare liberamente. (5)",
        },
        "nl": {
            "title": "Rechterwiel zit vast",
            "content": "Duw het wiel een paar keer op en neer en draai het vervolgens rond om vastzittend vuil los te maken. Het moet vrij kunnen draaien. (5)",
        },
        "pl": {
            "title": "Prawe koło jest zablokowane",
            "content": "Popchnij kółko w górę i w dół kilka razy, a następnie obróć nim, aby poluzować uwięzione zanieczyszczenia. Powinno swobodnie się obracać. (5)",
        },
        "pt": {
            "title": "Roda direita bloqueada",
            "content": "Empurre a roda para cima e para baixo algumas vezes e depois rode-a para soltar os resíduos presos. Deve rodar livremente. Deve rodar livremente. (5)",
        },
    },
    6: {
        "de": {
            "title": "Abgrundsensoren müssen gereinigt werden",
            "content": "Reinigen Sie die unteren Absturzsensoren mit einem weichen, trockenen Tuch, damit Treppen korrekt erkannt werden können. Stellen Sie @val auf den Boden und drücken Sie die Starttaste, um die Reinigung fortzusetzen. (6)",
        },
        "en": {
            "title": "Clean Cliff Sensors",
            "content": "Clean the bottom Cliff Sensors with a soft, dry cloth so stairs can be accurately detected. Place\xa0@val\xa0on the floor and press the start button to resume cleaning. (6)",
        },
        "es": {
            "title": "Es necesario limpiar los sensores anticaída",
            "content": "Limpia los sensores de desnivel inferiores con un paño suave y seco para que las escaleras se detecten con precisión. Coloca @val en el suelo y pulsa el botón de inicio para reanudar la limpieza. (6)",
        },
        "fr": {
            "title": "Les capteurs de vide ont besoin d’être nettoyés",
            "content": "Nettoyez les capteurs de vide situés sous le robot avec un chiffon doux et sec afin que les escaliers puissent être détectés avec précision. Placez @val sur le sol et appuyez sur le bouton Démarrer pour reprendre le nettoyage. (6)",
        },
        "it": {
            "title": "I sensori di caduta sono sporchi",
            "content": "Pulisci i sensori di dislivello inferiori con un panno morbido e asciutto affinché le scale vengano rilevate con precisione. Posiziona @val sul pavimento e premi il pulsante di avvio per riprendere la pulizia. (6)",
        },
        "nl": {
            "title": "Afgrondsensoren moeten worden schoongemaakt",
            "content": "Maak de onderste afgrondsensoren schoon met een zachte, droge doek zodat trappen nauwkeurig kunnen worden gedetecteerd. Plaats @val op de vloer en druk op de startknop om het schoonmaken te hervatten. (6)",
        },
        "pl": {
            "title": "Czujniki spadku wymagają wyczyszczenia",
            "content": "Wyczyść dolne czujniki uskoku miękką, suchą ściereczką, aby schody były dokładnie wykrywane. Umieść robota @val na podłodze i naciśnij przycisk start, aby wznowić sprzątanie. (6)",
        },
        "pt": {
            "title": "Sensores de desnível precisam de limpeza",
            "content": "Limpe os sensores de desnível inferiores com um pano macio e seco para que as escadas possam ser detetadas com precisão. Coloque @val no chão e prima o botão Iniciar para retomar a limpeza. (6)",
        },
    },
    7: {
        "de": {
            "title": "Problem mit linkem Radsensor",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Nehmen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (7)",
        },
        "en": {
            "title": "Left wheel sensor issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (7)",
        },
        "es": {
            "title": "Problema con el sensor de la rueda izquierda",
            "content": "Reinicia @val para solucionarlo. Retíralo de la base y, a continuación, mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (7)",
        },
        "fr": {
            "title": "Problème de capteur de la roue gauche",
            "content": "Redémarrez @val pour effacer. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (7)",
        },
        "it": {
            "title": "Problema con il sensore della ruota sinistra",
            "content": "Riavviare @val per risolverlo. Rimuoverlo dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (7)",
        },
        "nl": {
            "title": "Probleem met linker wielsensor",
            "content": "Start @val opnieuw op om te wissen. Haal het apparaat van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (7)",
        },
        "pl": {
            "title": "Wystąpił problem z czujnikiem lewego kółka",
            "content": "Uruchom ponownie robota @val w celu usunięcia problemu. Wyjmij go ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (7)",
        },
        "pt": {
            "title": "Problema no sensor da roda esquerda",
            "content": "Reinicie @val para corrigir. Retire-o da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (7)",
        },
    },
    9: {
        "de": {
            "title": "Stoßfänger steckt fest",
            "content": "Entfernen Sie alle Objekte, die möglicherweise hinter dem vorderen Stoßfänger von @val verkantet sind. (9)",
        },
        "en": {
            "title": "Bumper is stuck",
            "content": "Clear any objects that may be wedged behind\xa0@val’s front bumper. (9)",
        },
        "es": {
            "title": "El parachoques está atascado",
            "content": "Retira cualquier objeto que pueda estar encajado detrás del parachoques frontal de @val. (9)",
        },
        "fr": {
            "title": "Le pare-chocs est bloqué",
            "content": "Retirez tout objet qui pourrait être coincé derrière le pare-chocs avant de @val. (9)",
        },
        "it": {
            "title": "Paraurti incastrato",
            "content": "Rimuovere eventuali oggetti incastrati dietro il paraurti anteriore di @val. (9)",
        },
        "nl": {
            "title": "Bumper zit vast",
            "content": "Verwijder alle voorwerpen die mogelijk achter de voorbumper van @val vastzitten. (9)",
        },
        "pl": {
            "title": "Zderzak jest zablokowany",
            "content": "Usuń wszelkie przedmioty, które mogły utknąć za przednim zderzakiem robota @val. (9)",
        },
        "pt": {
            "title": "Para-choques bloqueado",
            "content": "Remova quaisquer objetos que possam estar presos atrás do para-choques frontal de @val. (9)",
        },
    },
    10: {
        "de": {
            "title": "Problem mit rechtem Radsensor",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Nehmen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (10)",
        },
        "en": {
            "title": "Right wheel sensor issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (10)",
        },
        "es": {
            "title": "Problema con el sensor de la rueda derecha",
            "content": "Reinicia @val para solucionarlo. Retíralo de la base y, a continuación, mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (10)",
        },
        "fr": {
            "title": "Problème de capteur de la roue droite",
            "content": "Redémarrez @val pour effacer. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (10)",
        },
        "it": {
            "title": "Problema con il sensore della ruota destra",
            "content": "Riavviare @val per risolverlo. Rimuoverlo dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (10)",
        },
        "nl": {
            "title": "Probleem met rechterwielsensor",
            "content": "Start @val opnieuw op om te wissen. Haal het apparaat van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (10)",
        },
        "pl": {
            "title": "Problem z czujnikiem prawego kółka",
            "content": "Uruchom ponownie robota @val w celu usunięcia problemu. Wyjmij go ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (10)",
        },
        "pt": {
            "title": "Problema no sensor da roda direita",
            "content": "Reinicie @val para corrigir. Retire-o da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (10)",
        },
    },
    12: {
        "de": {
            "title": "Abgrundsensor blockiert",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Entfernen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (12)",
        },
        "en": {
            "title": "Cliff sensor stall",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (12)",
        },
        "es": {
            "title": "Bloqueo del sensor anticaída",
            "content": "Reinicia @val para solucionarlo. Retíralo de la base y mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (12)",
        },
        "fr": {
            "title": "Capteur de vide bloqué",
            "content": "Redémarrez @val pour effacer. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (12)",
        },
        "it": {
            "title": "Sensore di caduta bloccato",
            "content": "Riavviare @val per risolverlo. Rimuovere dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (12)",
        },
        "nl": {
            "title": "Storing afgrondsensor",
            "content": "Start @val opnieuw op om te wissen. Haal het van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (12)",
        },
        "pl": {
            "title": "Zatrzymanie spowodowane zadziałaniem czujnika spadku",
            "content": "Uruchom ponownie robota @val w celu usunięcia problemu. Wyjmij ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (12)",
        },
        "pt": {
            "title": "Bloqueio dos sensores de precipício",
            "content": "Reinicie @val para corrigir. Retire da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (12)",
        },
    },
    14: {
        "de": {
            "title": "Der Behälter von @val fehlt",
            "content": "Bitte stellen Sie sicher, dass der Behälter von @val eingesetzt ist und die Sensoren sauber sind. Verwenden Sie zur Reinigung ein weiches, trockenes Tuch.(14)",
        },
        "en": {
            "title": "@val’s bin is missing",
            "content": "Please make sure\xa0@val’s bin is installed and the sensors are clean. Use a soft, dry cloth to clean.(14)",
        },
        "es": {
            "title": "Falta el depósito de @val",
            "content": "Asegúrate de que el depósito de @val esté instalado y de que los sensores estén limpios. Usa un paño suave y seco para limpiarlos.(14)",
        },
        "fr": {
            "title": "Le bac de @val est manquant",
            "content": "Veuillez vous assurer que le bac de @val est installé et que les capteurs sont propres. Utilisez un chiffon doux et sec pour nettoyer.(14)",
        },
        "it": {
            "title": "Il cestino di @val è mancante",
            "content": "Assicurati che il cestino di @val sia installato e che i sensori siano puliti. Utilizzare un panno morbido e asciutto per pulire.(14)",
        },
        "nl": {
            "title": "De opvangbak van @val ontbreekt",
            "content": "Zorg ervoor dat de opvangbak van @val is geïnstalleerd en dat de sensoren schoon zijn. Gebruik een zachte, droge doek om schoon te maken.(14)",
        },
        "pl": {
            "title": "Brak pojemnika robota @val",
            "content": "Upewnij się, że pojemnik robota @val jest zamontowany, a czujniki czyste. Do czyszczenia użyj miękkiej, suchej ściereczki.(14)",
        },
        "pt": {
            "title": "O depósito de @val está em falta",
            "content": "Certifique-se de que o depósito de @val está instalado e que os sensores estão limpos. Utilize um pano macio e seco para limpar. (14)",
        },
    },
    16: {
        "de": {
            "title": "@val wurde bewegt oder befindet sich auf einem unebenen Untergrund",
            "content": "Bewegen Sie @val auf einen neuen, ebenen Untergrund. Wenn er sich bereits auf einem ebenen Untergrund befindet, müssen Sie ihn möglicherweise neu starten. (16)",
        },
        "en": {
            "title": "@val\xa0was moved or is on an uneven surface",
            "content": "Move\xa0@val\xa0to a new, flat surface. If it is already on a flat surface, you may need to reboot it. (16)",
        },
        "es": {
            "title": "@val se ha movido o está en una superficie irregular",
            "content": "Mueve @val a otra superficie que sea plana. Si ya está en una superficie plana, es posible que debas reiniciarlo. (16)",
        },
        "fr": {
            "title": "@val a été déplacé ou se trouve sur une surface irrégulière",
            "content": "Déplacez @val sur une nouvelle surface plane. S’il est déjà sur une surface plane, vous devrez peut-être le redémarrer. (16)",
        },
        "it": {
            "title": "@val è stato spostato o si trova su una superficie irregolare",
            "content": "Spostare @val su una nuova superficie piana. Se è già su una superficie piana, potrebbe essere necessario riavviarlo. (16)",
        },
        "nl": {
            "title": "@val is verplaatst of staat op een oneffen oppervlak",
            "content": "Verplaats @val naar een nieuw, vlak oppervlak. Als deze al op een vlak oppervlak staat, moet u het mogelijk opnieuw opstarten. (16)",
        },
        "pl": {
            "title": "Robot @val został przeniesiony lub znajduje się na nierównej powierzchni",
            "content": "Przenieś robota @val na nową, płaską powierzchnię. Jeśli znajduje się już na płaskiej powierzchni, może być konieczne ponowne jego uruchomienie. (16)",
        },
        "pt": {
            "title": "@val foi movido ou está numa superfície irregular",
            "content": "Mova @val para uma nova superfície plana. Se já estiver numa superfície plana, poderá ser necessário reiniciá-lo. (16)",
        },
    },
    18: {
        "de": {
            "title": "@val konnte nicht zur Dockingstation zurückkehren. Bewegen Sie ihn und stellen Sie ihn zum Laden auf die Dockingstation.",
            "content": "Stellen Sie sicher, dass der Pfad frei ist, damit @val zu seiner Dockingstation zurückkehren kann. Überprüfen Sie, ob die Dockingstation eingesteckt ist und sich an ihrem ursprünglichen Standort befindet. (18)",
        },
        "en": {
            "title": "@val\xa0couldn't return to Dock. Move and place it on the Dock for charging.",
            "content": "Make sure the path is clear for\xa0@val\xa0to return to its dock. Check that the dock is plugged in and in its original location. (18)",
        },
        "es": {
            "title": "@val no ha podido volver a la base. Muévelo y colócalo en la base para cargarlo.",
            "content": "Asegúrate de que no haya obstáculos en el camino de vuelta a la base de @val. Comprueba que la base esté enchufada y en su ubicación original. (18)",
        },
        "fr": {
            "title": "@val n’a pas pu retourner à la station d’accueil. Déplacez-le et placez-le sur la station d’accueil pour le charger.",
            "content": "Assurez-vous que le chemin est dégagé pour que @val puisse retourner à sa station d’accueil. Vérifiez que la station d’accueil est branchée et qu’elle se trouve à son emplacement d’origine. (18)",
        },
        "it": {
            "title": "@val non è riuscito a tornare alla base. Spostalo e posizionalo sulla base per la ricarica.",
            "content": "Assicurarsi che il percorso sia libero affinché @val possa tornare alla sua base. Controllare che la base sia collegata e si trovi nella posizione originale. (18)",
        },
        "nl": {
            "title": "@val kon niet terugkeren naar het basisstation. Verplaats hem en plaats hem op het basisstation om op te laden.",
            "content": "Zorg ervoor dat het pad vrij is zodat @val kan terugkeren naar zijn dock. Controleer of het dock is aangesloten en op de oorspronkelijke locatie staat. (18)",
        },
        "pl": {
            "title": "Robot @val nie mógł wrócić do stacji dokującej. Przesuń go i umieść na stacji dokującej w celu ładowania.",
            "content": "Upewnij się, że droga jest wolna, aby robot @val mógł wrócić do stacji dokującej. Sprawdź, czy stacja dokująca jest podłączona do zasilania i znajduje się w swoim pierwotnym miejscu. (18)",
        },
        "pt": {
            "title": "@val não conseguiu regressar à base. Mova-o e coloque-o na base para carregar.",
            "content": "Certifique-se de que o caminho está livre para @val regressar à base. Verifique se a base está ligada e na sua localização original. (18)",
        },
    },
    19: {
        "de": {
            "title": "Verlassen der Dockingstation nicht möglich: Hindernis im Weg",
            "content": "@val konnte seine Dockingstation nicht verlassen. Räumen Sie Hindernisse um die Dockingstation herum aus dem Weg, damit der Roboter genug Platz zum An- und Abdocken hat. (19)",
        },
        "en": {
            "title": "Unable to leave dock: obstacle in the way",
            "content": "@val\xa0was unable to leave its dock. Clear obstacles around the dock so it has enough room to come and go. (19)",
        },
        "es": {
            "title": "No se puede salir de la base: hay un obstáculo en el camino",
            "content": "@val no ha podido salir de su base. Despeja los obstáculos en torno a la base dejando espacio suficiente para entrar y salir. (19)",
        },
        "fr": {
            "title": "Impossible de quitter la station d’accueil : obstacle sur le chemin",
            "content": "@val n’a pas pu quitter sa station d’accueil. Dégagez les obstacles autour de la station d’accueil pour qu’il ait suffisamment d’espace pour circuler. (19)",
        },
        "it": {
            "title": "Impossibile lasciare la base: un ostacolo blocca il passaggio",
            "content": "@val non è riuscito a lasciare la base. Rimuovere gli ostacoli intorno alla base in modo che il robot abbia spazio a sufficienza per eseguire le manovre di ingresso/uscita. (19)",
        },
        "nl": {
            "title": "Kan het dock niet verlaten: er bevindt zich een obstakel in de weg",
            "content": "@val kon zijn dock niet verlaten. Verwijder obstakels rondom het basisstation zodat het voldoende ruimte heeft om in en uit te rijden. (19)",
        },
        "pl": {
            "title": "Nie może opuścić stacji dokującej: przeszkoda na drodze",
            "content": "Robot @val nie mógł opuścić stacji dokującej. Usuń przeszkody wokół stacji dokującej, aby zapewnić robotowi wystarczającą ilość miejsca do wyjazdu i powrotu. (19)",
        },
        "pt": {
            "title": "Não é possível sair da base: obstáculo no caminho",
            "content": "@val não conseguiu sair da base. Remova obstáculos à volta da base para que tenha espaço suficiente para entrar e sair. (19)",
        },
    },
    22: {
        "de": {
            "title": "@val steckt fest",
            "content": "Bewegen Sie ihn in einen freien Bereich und drücken Sie die Ein-/Aus-Taste, um fortzufahren. Entfernen Sie Hindernisse und öffnen Sie Türen. (22)",
        },
        "en": {
            "title": "@val\xa0is stuck",
            "content": "Move it to an open area and press the Power button to resume. Clear obstacles and open doors. (22)",
        },
        "es": {
            "title": "@val está atascado",
            "content": "Muévelo a un área despejada y pulsa el botón de encendido para reanudar su actividad. Retira los obstáculos y abre las puertas. (22)",
        },
        "fr": {
            "title": "@val est bloqué",
            "content": "Déplacez-le vers une zone dégagée et appuyez sur le bouton d’alimentation pour reprendre. Dégagez les obstacles et ouvrez les portes. (22)",
        },
        "it": {
            "title": "@val è bloccato",
            "content": "Spostarlo in un'area aperta e premere il pulsante di accensione per riprendere il funzionamento. Rimuovere gli ostacoli e aprire le porte. (22)",
        },
        "nl": {
            "title": "@val zit vast",
            "content": "Verplaats het naar een open ruimte en druk op de aan-uitknop om door te gaan. Verwijder obstakels en open deuren. (22)",
        },
        "pl": {
            "title": "Robot @val jest zablokowany",
            "content": "Przenieś na otwartą przestrzeń i naciśnij przycisk zasilania, aby wznowić. Usuń przeszkody i otwórz drzwi. (22)",
        },
        "pt": {
            "title": "@val está preso",
            "content": "Mova-o para uma área aberta e prima o botão de alimentação para retomar. Remova os obstáculos e abra as portas. (22)",
        },
    },
    24: {
        "de": {
            "title": "Navigationsproblem",
            "content": "Stellen Sie @val auf einen ebenen Untergrund und drücken Sie die Ein-/Aus-Taste, um fortzufahren. (24)",
        },
        "en": {
            "title": "Navigation Issue",
            "content": "Move\xa0@val\xa0to a flat surface and press the Power button to resume. (24)",
        },
        "es": {
            "title": "Problema de navegación",
            "content": "Mueve @val a una superficie plana y pulsa el botón de encendido para reanudar su actividad. (24)",
        },
        "fr": {
            "title": "Problème de navigation",
            "content": "Déplacez @val sur une surface plane et appuyez sur le bouton d’alimentation pour reprendre. (24)",
        },
        "it": {
            "title": "Problema di navigazione",
            "content": "Spostare @val su una superficie piana e premere il pulsante di accensione per riprendere il funzionamento. (24)",
        },
        "nl": {
            "title": "Navigatieprobleem",
            "content": "Plaats @val op een vlakke ondergrond en druk op de aan/uit-knop om door te gaan. (24)",
        },
        "pl": {
            "title": "Problem z nawigacją",
            "content": "Przenieś robota @val na płaską powierzchnię i naciśnij przycisk zasilania, aby wznowić. (24)",
        },
        "pt": {
            "title": "Problema de navegação",
            "content": "Mova @val para uma superfície plana e prima o botão de alimentação para retomar. (24)",
        },
    },
    26: {
        "de": {
            "title": "Saugmotor blockiert",
            "content": "Der Filter von @val ist möglicherweise verstopft. Entfernen Sie den Filter aus dem Staubbehälter und klopfen Sie ihn über einem Mülleimer aus, um angesammelten Schmutz zu entfernen. (26)",
        },
        "en": {
            "title": "Vacuum motor is stalled",
            "content": "@val’s filter may be clogged. Remove filter from dust bin and tap it out over a trash bin to clear built-up debris. (26)",
        },
        "es": {
            "title": "El motor de aspiración está atascado",
            "content": "Es posible que el filtro de @val esté obstruido. Retira el filtro del depósito de polvo y golpéalo suavemente sobre un cubo de basura para eliminar la suciedad acumulada. (26)",
        },
        "fr": {
            "title": "Le moteur d’aspiration est bloqué",
            "content": "Le filtre de @val est peut-être obstrué. Retirez le filtre du bac à poussière et tapotez-le au-dessus d’une poubelle pour éliminer les débris accumulés. (26)",
        },
        "it": {
            "title": "Il motore di aspirazione è bloccato",
            "content": "Il filtro di @val potrebbe essere ostruito. Rimuovere il filtro dal contenitore della polvere e sbatterlo su un cestino dei rifiuti per rimuovere i detriti accumulati. (26)",
        },
        "nl": {
            "title": "Zuigmotor is vastgelopen",
            "content": "Het filter van @val is mogelijk verstopt. Verwijder het filter uit de stofbak en klop het uit boven een vuilnisbak om opgehoopt vuil te verwijderen. (26)",
        },
        "pl": {
            "title": "Silnik odkurzacza jest zablokowany",
            "content": "Filtr robota @val może być zatkany. Wyjmij filtr z pojemnika na kurz i wytrzep go nad koszem na śmieci, aby usunąć nagromadzony brud. (26)",
        },
        "pt": {
            "title": "Motor de aspiração bloqueado",
            "content": "O filtro de @val pode estar obstruído. Retire o filtro do depósito de pó e bata-o ligeiramente sobre o caixote do lixo para remover os resíduos acumulados. (26)",
        },
    },
    29: {
        "de": {
            "title": "Roboter-Software wird aktualisiert",
            "content": "Dies kann bis zu 20 Minuten dauern. Wenn es länger als 20 Minuten dauert, starten Sie @val neu. (29)",
        },
        "en": {
            "title": "Robot software is updating",
            "content": "This can take up to 20 minutes. If it takes longer than 20 minutes, reboot\xa0@val. (29)",
        },
        "es": {
            "title": "El software del robot se está actualizando",
            "content": "Este proceso puede tardar hasta 20\xa0minutos. Si tarda más de 20\xa0minutos, reinicia @val. (29)",
        },
        "fr": {
            "title": "Mise à jour du logiciel du robot en cours",
            "content": "Cela peut prendre jusqu’à 20 minutes. Si cela prend plus de 20 minutes, redémarrez @val. (29)",
        },
        "it": {
            "title": "Aggiornamento del software del robot in corso",
            "content": "Potrebbe richiedere fino a 20 minuti. Se impiega più di 20 minuti, riavviare @val. (29)",
        },
        "nl": {
            "title": "Robotsoftware wordt bijgewerkt",
            "content": "Dit kan tot 20 minuten duren. Als het langer dan 20 minuten duurt, start je @val opnieuw op. (29)",
        },
        "pl": {
            "title": "Trwa aktualizacja oprogramowania robota",
            "content": "Może to potrwać maksymalnie 20\xa0minut. Jeśli potrwa to dłużej niż 20\xa0minut, uruchom ponownie @val. (29)",
        },
        "pt": {
            "title": "O software do robô está a ser atualizado",
            "content": "Isto pode demorar até 20 minutos. Se demorar mais de 20 minutos, reinicie @val. (29)",
        },
    },
    30: {
        "de": {
            "title": "Saugmotor-Problem",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Nehmen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (30)",
        },
        "en": {
            "title": "Vacuum motor issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (30)",
        },
        "es": {
            "title": "Problema del motor de aspiración",
            "content": "Reinicia @val para solucionarlo. Retíralo de la base y, a continuación, mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (30)",
        },
        "fr": {
            "title": "Problème du moteur d’aspiration",
            "content": "Redémarrez @val pour effacer. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (30)",
        },
        "it": {
            "title": "Problema al motore di aspirazione",
            "content": "Riavviare @val per risolverlo. Rimuoverlo dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (30)",
        },
        "nl": {
            "title": "Probleem met vacuümmotor",
            "content": "Start @val opnieuw op om te wissen. Haal het apparaat van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (30)",
        },
        "pl": {
            "title": "Problem z silnikiem odkurzacza",
            "content": "Uruchom ponownie robota @val w celu usunięcia problemu. Wyjmij go ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (30)",
        },
        "pt": {
            "title": "Problema no motor de aspiração",
            "content": "Reinicie @val para corrigir. Retire-o da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (30)",
        },
    },
    32: {
        "de": {
            "title": "@val konnte die angeforderten Kartenbereiche nicht erreichen",
            "content": "Stellen Sie sicher, dass @val die für diese Routine verwendeten Bereiche auf der Karte erreichen kann. Dieses Problem kann bei mehreren Karten auftreten, die nicht miteinander verbunden sind. (32)",
        },
        "en": {
            "title": "@val\xa0couldn’t get to the requested map areas",
            "content": "Make sure\xa0@val\xa0can reach the areas on the map used for this routine. This issue can happen with multiple maps that don’t connect. (32)",
        },
        "es": {
            "title": "@val no ha podido llegar a las áreas del mapa solicitadas",
            "content": "Asegúrate de que @val pueda llegar a las áreas del mapa utilizadas para esta rutina. Este problema puede producirse cuando hay varios mapas que no se conectan. (32)",
        },
        "fr": {
            "title": "@val n’a pas pu accéder aux zones de la carte demandées",
            "content": "Vérifiez que @val peut atteindre les zones de la carte utilisée pour cette routine. Ce problème peut se produire si plusieurs cartes ne sont pas connectées. (32)",
        },
        "it": {
            "title": "@val non ha potuto raggiungere le aree della mappa richieste",
            "content": "Assicurarsi che @val possa raggiungere le aree sulla mappa utilizzate per questa routine. Questo problema può verificarsi con più mappe che non si connettono. (32)",
        },
        "nl": {
            "title": "@val kon de gevraagde kaartgebieden niet bereiken",
            "content": "Zorg ervoor dat @val de gebieden op de kaart die voor deze routine worden gebruikt, kan bereiken. Dit probleem kan optreden bij meerdere kaarten die niet met elkaar verbonden zijn. (32)",
        },
        "pl": {
            "title": "Robot @val nie mógł dotrzeć do żądanych obszarów na mapie",
            "content": "Upewnij się, że robot @val może dotrzeć do obszarów na mapie używanych w tej rutynie. Ten problem może wystąpić w przypadku wielu map, które się nie łączą. (32)",
        },
        "pt": {
            "title": "@val não conseguiu aceder às áreas do mapa solicitadas",
            "content": "Certifique-se de que o @val consegue chegar às áreas do mapa utilizadas para esta rotina. Este problema pode ocorrer com vários mapas que não estão ligados. (32)",
        },
    },
    33: {
        "de": {
            "title": "@val wurde an Möbeln oder einer Tür eingeklemmt",
            "content": "Stellen Sie sicher, dass die Türen vollständig geöffnet sind und um Möbel herum genug Platz für @val vorhanden ist, um Fahrmanöver auszuführen. (33)",
        },
        "en": {
            "title": "@val\xa0got trapped by furniture or a door",
            "content": "Make sure doors are open all the way and there is enough space around furniture for\xa0@val\xa0to maneuver around. (33)",
        },
        "es": {
            "title": "@val se ha quedado atrapado con un mueble o una puerta",
            "content": "Asegúrate de que las puertas estén completamente abiertas y de que haya suficiente espacio alrededor de los muebles para que @val pueda maniobrar. (33)",
        },
        "fr": {
            "title": "@val est resté coincé par un meuble ou une porte",
            "content": "Assurez-vous que les portes sont complètement ouvertes et qu’il y a suffisamment d’espace autour des meubles pour que @val puisse se déplacer. (33)",
        },
        "it": {
            "title": "@val si è incastrato in un mobile o una porta",
            "content": "Assicurarsi che le porte siano completamente aperte e che ci sia spazio sufficiente intorno ai mobili per consentire a @val di muoversi. (33)",
        },
        "nl": {
            "title": "@val zat klem door meubels of een deur",
            "content": "Zorg ervoor dat deuren helemaal openstaan en dat er genoeg ruimte rond de meubels is voor @val om te manoeuvreren. (33)",
        },
        "pl": {
            "title": "Robot @val utknął pod meblem lub drzwiami",
            "content": "Sprawdź, czy drzwi są całkowicie otwarte, a wokół mebli jest wystarczająco dużo miejsca, aby robot @val mógł się przemieszczać. (33)",
        },
        "pt": {
            "title": "@val ficou preso em mobiliário ou numa porta",
            "content": "Certifique-se de que as portas estão totalmente abertas e que existe espaço suficiente à volta dos móveis para @val se movimentar. (33)",
        },
    },
    35: {
        "de": {
            "title": "Kein Mopp angebracht",
            "content": "Bringen Sie den Mopp von @val an, um das Wischen zu aktivieren. (35)",
        },
        "en": {
            "title": "No mop attached",
            "content": "Attach\xa0@val's mop to enable mopping. (35)",
        },
        "es": {
            "title": "Mopa no instalada",
            "content": "Coloca la mopa de @val para poder fregar. (35)",
        },
        "fr": {
            "title": "Aucune serpillière fixée",
            "content": "Fixez la serpillière de @val pour activer le nettoyage à la serpillière. (35)",
        },
        "it": {
            "title": "Nessun panno di lavaggio inserito",
            "content": "Inserire il panno di lavaggio di @val per abilitare il lavaggio. (35)",
        },
        "nl": {
            "title": "Geen dweil bevestigd",
            "content": "Bevestig de dweil van @val om te dweilen. (35)",
        },
        "pl": {
            "title": "Nie podłączono mopa",
            "content": "Podłącz mopa do robota @val, aby umożliwić mycie mopem. (35)",
        },
        "pt": {
            "title": "Sem mopa instalada",
            "content": "Instale a mopa de @val para ativar a lavagem. (35)",
        },
    },
    36: {
        "de": {
            "title": "Behälter möglicherweise voll oder Schmutz blockiert den Kanal",
            "content": "Entleeren Sie den Behälter von @val und entfernen Sie mögliche Blockaden am Staubverdichter und Kanal. (36)",
        },
        "en": {
            "title": "Dustbin may be full or Air Duct is blocked. Clean it",
            "content": "Empty\xa0@val’s Dustbin and clear any possible obstructions to the Dust Compactor and Air Duct. (36)",
        },
        "es": {
            "title": "Es posible que el depósito esté lleno o haya residuos bloqueando la cámara",
            "content": "Vacía el depósito de @val y retira cualquier posible obstrucción en el compactador de polvo y la cámara. (36)",
        },
        "fr": {
            "title": "Le bac est peut-être plein ou des débris bloquent le conduit d’aspiration",
            "content": "Videz le bac de @val et éliminez toute obstruction possible du compacteur de poussière et du conduit d’aspiration. (36)",
        },
        "it": {
            "title": "Il cestino potrebbe essere pieno o della sporcizia potrebbe bloccare il condotto",
            "content": "Svuotare il cestino di @val e rimuovere eventuali ostruzioni dal compattatore della polvere e dal condotto. (36)",
        },
        "nl": {
            "title": "Opvangbak kan vol zijn of vuil kan het plenum blokkeren",
            "content": "Leeg de opvangbak van @val en verwijder eventuele verstoppingen uit de stofpers en het plenum. (36)",
        },
        "pl": {
            "title": "Pojemnik może być pełny, a zanieczyszczenia mogą blokować kanał powietrzny",
            "content": "Opróżnij pojemnik robota @val i usuń wszelkie możliwe blokady w zgniatarce kurzu oraz kanale powietrznym. (36)",
        },
        "pt": {
            "title": "O depósito pode estar cheio ou ter resíduos a bloquear o conduto",
            "content": "Esvazie o depósito de @val e remova quaisquer obstruções do compactador de pó e do conduto. (36)",
        },
    },
    42: {
        "de": {
            "title": "@val konnte einen Ihrer Räume nicht erreichen",
            "content": "Öffnen Sie Türen und entfernen Sie Hindernisse, die den Weg blockieren könnten, und versuchen Sie es erneut. (42)",
        },
        "en": {
            "title": "@val\xa0couldn’t reach one of your rooms",
            "content": "Open doors and clear obstacles that could be blocking its path and try again. (42)",
        },
        "es": {
            "title": "@val no ha podido llegar a una de las habitaciones",
            "content": "Abre las puertas, retira los obstáculos que puedan estar bloqueando su camino e inténtalo de nuevo. (42)",
        },
        "fr": {
            "title": "@val n’a pas pu atteindre l’une de vos pièces",
            "content": "Ouvrez les portes, dégagez les obstacles qui pourraient bloquer son chemin et réessayez. (42)",
        },
        "it": {
            "title": "@val non è riuscito a raggiungere una delle stanze",
            "content": "Aprire le porte, rimuovere gli ostacoli che potrebbero bloccare il percorso e riprovare. (42)",
        },
        "nl": {
            "title": "@val kon een van uw kamers niet bereiken",
            "content": "Open deuren en verwijder obstakels die het pad kunnen blokkeren en probeer het opnieuw. (42)",
        },
        "pl": {
            "title": "Robot @val nie mógł dotrzeć do jednego z pomieszczeń",
            "content": "Otwórz drzwi i usuń przeszkody, które mogą blokować drogę, a następnie spróbuj ponownie. (42)",
        },
        "pt": {
            "title": "@val não conseguiu chegar a uma das divisões",
            "content": "Abra portas e remova obstáculos que possam estar a bloquear o caminho e tente novamente. (42)",
        },
    },
    44: {
        "de": {
            "title": "Pumpe im Wasserbehälter des Roboters ist möglicherweise blockiert",
            "content": "Bitte lesen Sie unseren Hilfeartikel für Schritte zur Behebung dieses Problems durch. (44)",
        },
        "en": {
            "title": "Robot water bin pump may be blocked",
            "content": "Please view our help article for steps to troubleshoot this issue. (44)",
        },
        "es": {
            "title": "Es posible que la bomba del depósito de agua del robot esté bloqueada",
            "content": "Consulta nuestro artículo de ayuda para conocer los pasos para solucionar este problema. (44)",
        },
        "fr": {
            "title": "La pompe du bac d’eau du robot est peut-être bloquée",
            "content": "Veuillez consulter notre article d’aide pour connaître les étapes de dépannage de ce problème. (44)",
        },
        "it": {
            "title": "La pompa del serbatoio dell'acqua del robot potrebbe essere bloccata",
            "content": "Consultare il nostro articolo della guida per i passaggi su come risolvere questo problema. (44)",
        },
        "nl": {
            "title": "De pomp van de watertank van de robot is mogelijk verstopt",
            "content": "Raadpleeg ons help-artikel voor stappen om dit probleem op te lossen. (44)",
        },
        "pl": {
            "title": "Pompa zbiornika na wodę robota może być zablokowana",
            "content": "Zapoznaj się z artykułem pomocy, by dowiedzieć się, jak rozwiązać ten problem. (44)",
        },
        "pt": {
            "title": "A bomba do depósito de água do robô pode estar bloqueada",
            "content": "Consulte o nosso artigo de ajuda para ver os passos de resolução deste problema. (44)",
        },
    },
    46: {
        "de": {
            "title": "Akkustand zu niedrig für die Reinigung",
            "content": 'Stellen Sie @val auf seine Dockingstation und lassen Sie ihn ausreichend aufladen. Sie können den Akkustatus hier auf der Registerkarte "Roboter" überprüfen. (46)',
        },
        "en": {
            "title": "Battery too low to clean",
            "content": "Place\xa0@val\xa0on its dock and allow it to charge sufficiently. You can check battery status here in the Robots tab. (46)",
        },
        "es": {
            "title": "Batería demasiado baja para limpiar",
            "content": "Coloca @val en su base y deja que cargue lo suficiente. Puedes comprobar el estado de la batería aquí, en la pestaña Robots. (46)",
        },
        "fr": {
            "title": "Batterie trop faible pour nettoyer",
            "content": "Placez @val sur sa station d’accueil et laissez-le se recharger suffisamment. Vous pouvez vérifier l’état de la batterie ici, dans l’onglet Robots. (46)",
        },
        "it": {
            "title": "Batteria troppo scarica per la pulizia",
            "content": "Posizionare @val sulla sua base e lasciarlo caricare a un livello sufficiente. È possibile controllare lo stato della batteria qui, nella scheda Robot. (46)",
        },
        "nl": {
            "title": "Batterij is te zwak om te reinigen",
            "content": "Plaats @val op het dock en laat het voldoende opladen. Je kunt de batterijstatus hier controleren op het tabblad Robots. (46)",
        },
        "pl": {
            "title": "Zbyt niski poziom akumulatora, aby sprzątać",
            "content": "Umieść robota @val na stacji dokującej i pozwól mu się wystarczająco naładować. Stan naładowania akumulatora możesz sprawdzić tutaj, na zakładce Roboty. (46)",
        },
        "pt": {
            "title": "Bateria demasiado fraca para limpar",
            "content": "Coloque @val na base e permita que carregue suficientemente. Pode verificar o estado da bateria aqui no separador Robôs. (46)",
        },
    },
    47: {
        "de": {
            "title": "Wichtiges Update verfügbar – wir unterstützen Sie dabei",
            "content": 'Gehen Sie im unteren App-Menü zur Registerkarte "Support" und wenden Sie sich an unser Team, damit wir Ihren Roboter per Fernzugriff aktualisieren können.\nDadurch wird ein Sensor aktualisiert, der zur ordnungsgemäßen Funktion von @val beiträgt. (47)',
        },
        "en": {
            "title": "Important update available – we’re here to help",
            "content": "Go to the Support tab from the bottom app menu and contact our team so we can remotely update your robot.\nThis will update a sensor that helps\xa0@val\xa0work properly. (47)",
        },
        "es": {
            "title": "Actualización importante disponible: estamos aquí para ayudarte",
            "content": "Ve a la pestaña Atención al cliente en el menú inferior de la app y contacta con nuestro equipo para que podamos actualizar tu robot de forma remota.\nSe actualizará un sensor que contribuye a que @val funcione correctamente. (47)",
        },
        "fr": {
            "title": "Mise à jour importante disponible ; nous sommes là pour vous aider",
            "content": "Accédez à l’onglet Assistance dans le menu inférieur de l’application et contactez notre équipe pour que nous puissions mettre à jour votre robot à distance.\nCela mettra à jour un capteur qui aide @val à fonctionner correctement. (47)",
        },
        "it": {
            "title": "Aggiornamento importante disponibile – siamo qui per aiutarti",
            "content": "Accedere alla scheda Assistenza dal menu in basso dell'app e contattare il nostro team, in modo da poter aggiornare da remoto il robot.\nQuesto aggiornerà un sensore che aiuta @val a funzionare correttamente. (47)",
        },
        "nl": {
            "title": "Er is een belangrijke update beschikbaar – we helpen je graag",
            "content": "Ga naar de tab Ondersteuning in het onderste menu van de app en neem contact op met ons team, zodat we je robot op afstand kunnen updaten.\nHiermee wordt een sensor bijgewerkt die ervoor zorgt dat @val correct werkt. (47)",
        },
        "pl": {
            "title": "Dostępna jest ważna aktualizacja — chętnie pomożemy",
            "content": "Przejdź do karty Wsparcie w dolnym menu aplikacji i skontaktuj się z naszym zespołem, abyśmy mogli zdalnie zaktualizować robota.\nZaktualizuje to czujnik, który umożliwia robotowi @val prawidłowe działanie. (47)",
        },
        "pt": {
            "title": "Atualização importante disponível – estamos aqui para ajudar",
            "content": "Vá ao separador Suporte no menu inferior da aplicação e contacte a nossa equipa para que possamos atualizar remotamente o seu robô.\nIsto irá atualizar um sensor que ajuda @val a funcionar corretamente. (47)",
        },
    },
    48: {
        "de": {
            "title": "Ein Hindernis blockierte den Eingang zu einem Raum",
            "content": "Stellen Sie sicher, dass Türen offen und frei von Hindernissen sind. Es sollte auch überprüft werden, ob Ihre Karte Ihren Raum präzise abbildet. (48)",
        },
        "en": {
            "title": "An obstacle blocked the entrance to a room",
            "content": "Make sure doors are open and free from obstacles. It’s also a good idea to check that your map accurately represents your space. (48)",
        },
        "es": {
            "title": "Un obstáculo bloqueaba la entrada a una habitación",
            "content": "Asegúrate de que las puertas estén abiertas y libres de obstáculos. También es recomendable comprobar que el mapa represente el espacio con exactitud. (48)",
        },
        "fr": {
            "title": "Un obstacle a bloqué l’entrée d’une pièce",
            "content": "Assurez-vous que les portes sont ouvertes et dégagées de tout obstacle. Il est également recommandé de vérifier que votre carte représente fidèlement votre espace. (48)",
        },
        "it": {
            "title": "Un ostacolo bloccava l'ingresso a una stanza",
            "content": "Assicurarsi che le porte siano aperte e libere da ostacoli. È anche una buona idea verificare che la mappa rappresenti accuratamente lo spazio. (48)",
        },
        "nl": {
            "title": "Een obstakel blokkeerde de ingang van een kamer",
            "content": "Zorg ervoor dat deuren open zijn en vrij van obstakels. Het is ook een goed idee om te controleren of je kaart je ruimte accuraat weergeeft. (48)",
        },
        "pl": {
            "title": "Przeszkoda zablokowała wejście do pomieszczenia",
            "content": "Upewnij się, że drzwi są otwarte i wolne od przeszkód. Warto również sprawdzić, czy mapa dokładnie odzwierciedla przestrzeń. (48)",
        },
        "pt": {
            "title": "Um obstáculo bloqueou a entrada de uma divisão",
            "content": "Certifique-se de que as portas estão abertas e sem obstáculos. Também é recomendável verificar se o mapa representa corretamente o seu espaço. (48)",
        },
    },
    66: {
        "de": {
            "title": "Für den Speicher ist ein kurzer Neustart erforderlich",
            "content": "Nehmen Sie für einen Neustart den Roboter von der Dockingstation, halten Sie die Ein-/Aus-Taste zum Ausschalten 10 Sekunden lang gedrückt und halten Sie sie dann zum Einschalten erneut 3 Sekunden lang gedrückt. (66)",
        },
        "en": {
            "title": "Memory storage needs a quick reboot",
            "content": "To reboot, remove from dock, press and hold Power button for 10 seconds to Power off, press and hold again for 3 seconds to Power back on. (66）",
        },
        "es": {
            "title": "Es necesario un reinicio rápido del almacenamiento en memoria",
            "content": "Para reiniciar, retira el robot de la base, mantén pulsado el botón de encendido durante 10\xa0segundos para apagarlo y vuelve a mantenerlo pulsado durante 3\xa0segundos para encenderlo de nuevo. (66)",
        },
        "fr": {
            "title": "Le stockage en mémoire nécessite un redémarrage rapide",
            "content": "Pour redémarrer, retirez de la station d’accueil, maintenez le bouton d’alimentation enfoncé pendant 10 secondes pour éteindre, puis appuyez de nouveau et maintenez-le enfoncé pendant 3 secondes pour rallumer. (66)",
        },
        "it": {
            "title": "La memoria richiede un riavvio rapido",
            "content": "Per riavviare, rimuovere il robot dalla base, tenere premuto il pulsante di accensione per 10 secondi per spegnere, quindi tenere premuto di nuovo per 3 secondi per riaccendere. (66)",
        },
        "nl": {
            "title": "Geheugenopslag heeft een snelle herstart nodig",
            "content": "Om opnieuw op te starten, haal het apparaat van het dock, houd de aan-/uitknop 10 seconden ingedrukt om uit te schakelen en houd deze opnieuw 3 seconden ingedrukt om weer in te schakelen. (66)",
        },
        "pl": {
            "title": "Pamięć wymaga szybkiego ponownego uruchomienia",
            "content": "Aby ponownie uruchomić robota, zdejmij go ze stacji dokującej, naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund, aby go wyłączyć, a następnie ponownie naciśnij i przytrzymaj przez 3\xa0sekundy, aby go włączyć. (66)",
        },
        "pt": {
            "title": "A memória precisa de um reinício rápido",
            "content": "Para reiniciar, retire da base, prima sem soltar o botão de alimentação durante 10 segundos para desligar, prima novamente durante 3 segundos para ligar. (66)",
        },
    },
    68: {
        "de": {
            "title": "Kamera kann Objekte und Hindernisse nicht erkennen",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Entfernen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (68)",
        },
        "en": {
            "title": "Camera unable to detect objects and obstacles",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (68)",
        },
        "es": {
            "title": "La cámara no puede detectar objetos ni obstáculos",
            "content": "Reinicia @val para solucionar el error. Retíralo de la base y mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (68)",
        },
        "fr": {
            "title": "La caméra ne parvient pas à détecter les objets et les obstacles",
            "content": "Redémarrez @val pour effacer l’erreur. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (68)",
        },
        "it": {
            "title": "Fotocamera non in grado di rilevare oggetti e ostacoli",
            "content": "Riavviare @val per risolvere l'errore. Rimuovere dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (68)",
        },
        "nl": {
            "title": "Camera kan geen objecten en obstakels detecteren",
            "content": "Start @val opnieuw op om de fout te wissen. Verwijder het van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (68)",
        },
        "pl": {
            "title": "Kamera nie może wykryć obiektów i przeszkód",
            "content": "Uruchom ponownie robota @val w celu usunięcia błędu. Wyjmij ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (68)",
        },
        "pt": {
            "title": "A câmara não consegue detetar objetos e obstáculos",
            "content": "Reinicie @val para corrigir o erro. Retire da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (68)",
        },
    },
    69: {
        "de": {
            "title": "@val konnte den Weg zurück nicht finden",
            "content": "Achten Sie darauf, dass Türen geöffnet sind und der Pfad zur Dockingstation nicht blockiert ist. Stellen Sie @val auf die Dockingstation, wenn der Akku leer ist. (69)",
        },
        "en": {
            "title": "@val\xa0was unable to find its way home",
            "content": "Make sure doors are open and that nothing is blocking the path to the dock. Place\xa0@val\xa0on dock if its battery has run out. (69)",
        },
        "es": {
            "title": "@val no ha podido encontrar el camino de vuelta a la base",
            "content": "Asegúrate de que las puertas estén abiertas y de que no haya nada bloqueando el camino a la base. Si @val se ha quedado sin batería, colócalo en la base. (69)",
        },
        "fr": {
            "title": "@val n’a pas pu retrouver son chemin vers la station d’accueil",
            "content": "Assurez-vous que les portes sont ouvertes et que rien ne bloque le passage vers la station d’accueil. Placez @val sur la station d’accueil si sa batterie est épuisée. (69)",
        },
        "it": {
            "title": "@val non è riuscito a tornare alla base",
            "content": "Assicurarsi che le porte siano aperte e che non ci siano ostacoli lungo il percorso verso la base. Posizionare @val sulla base se la batteria è esaurita. (69)",
        },
        "nl": {
            "title": "@val kon de weg naar huis niet vinden",
            "content": "Zorg ervoor dat de deuren open zijn en dat niets het pad naar het dock blokkeert. Plaats @val op het dock als de accu leeg is. (69)",
        },
        "pl": {
            "title": "Robot @val nie mógł znaleźć drogi powrotnej",
            "content": "Upewnij się, że drzwi są otwarte i nic nie blokuje drogi do stacji dokującej. Umieść robota @val w stacji dokującej, jeśli jego akumulator się wyczerpał. (69)",
        },
        "pt": {
            "title": "@val não conseguiu encontrar o caminho de regresso à base",
            "content": "Certifique-se de que as portas estão abertas e que nada bloqueia o caminho até à base. Coloque @val na base se a bateria tiver acabado. (69)",
        },
    },
    101: {
        "de": {
            "title": "Ladeproblem: Akku nicht erkannt",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku und setzen Sie ihn wieder ein, um den Fehler zu beheben. (101)",
        },
        "en": {
            "title": "Charging Issue: battery not detected",
            "content": "@val\xa0is having trouble detecting its battery. Remove and reinstall battery to clear. (101)",
        },
        "es": {
            "title": "Problema de carga: batería no detectada",
            "content": "@val tiene problemas para detectar la batería. Retira y vuelve a instalar la batería para solucionarlo. (101)",
        },
        "fr": {
            "title": "Problème de chargement : batterie non détectée",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez puis réinstallez la batterie pour effacer l’erreur. (101)",
        },
        "it": {
            "title": "Problema di ricarica: batteria non rilevata",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere e reinstallare la batteria per risolvere il problema. (101)",
        },
        "nl": {
            "title": "Oplaadprobleem: batterij niet gedetecteerd",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu en plaats deze opnieuw om de fout te wissen. (101)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie wykryto akumulatora",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij i włóż ponownie akumulator, aby usunąć błąd. (101)",
        },
        "pt": {
            "title": "Problema de carregamento: bateria não detetada",
            "content": "@val está com dificuldade em detetar a bateria. Remova e volte a instalar a bateria para corrigir. (101)",
        },
    },
    102: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku und setzen Sie ihn wieder ein, um den Fehler zu beheben. (102)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove and reinstall battery to clear. (102)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira y vuelve a instalar la batería para solucionarlo. (102)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez puis réinstallez la batterie pour effacer l’erreur. (102)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere e reinstallare la batteria per risolvere il problema. (102)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu en plaats deze opnieuw om te wissen. (102)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij i włóż ponownie akumulator, aby usunąć błąd. (102)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova e volte a instalar a bateria para corrigir. (102)",
        },
    },
    103: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku und setzen Sie ihn wieder ein, um den Fehler zu beheben. (103)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove and reinstall battery to clear. (103)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira y vuelve a instalar la batería para solucionarlo. (103)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez puis réinstallez la batterie pour effacer l’erreur. (103)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere e reinstallare la batteria per risolvere il problema. (103)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu en plaats deze opnieuw om te wissen. (103)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij i włóż ponownie akumulator, aby usunąć błąd. (103)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova e volte a instalar a bateria para corrigir. (103)",
        },
    },
    104: {
        "de": {
            "title": "Ladeproblem: Kontakte müssen gereinigt werden",
            "content": "Trennen Sie die Dockingstation vom Strom und wischen Sie die Ladekontakte am Roboter und an der Dockingstation mit einem leicht feuchten Tuch ab. (104)",
        },
        "en": {
            "title": "Charging Issue: contacts need to be cleaned",
            "content": "Unplug the Dock Power, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (104)",
        },
        "es": {
            "title": "Problema de carga: es necesario limpiar los contactos",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un paño ligeramente húmedo. (104)",
        },
        "fr": {
            "title": "Problème de chargement : les contacts doivent être nettoyés",
            "content": "Débranchez l’alimentation de la station d’accueil, puis essuyez les contacts de charge du robot et de la station avec un chiffon légèrement humide. (104)",
        },
        "it": {
            "title": "Problema di ricarica: è necessario ripulire i contatti",
            "content": "Scollega la base dall’alimentazione e pulisci i contatti di ricarica del robot e della base con un panno leggermente umido. (104)",
        },
        "nl": {
            "title": "Oplaadprobleem: contacten moeten gereinigd worden",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de laadcontacten van de robot en het basisstation schoon met een licht vochtige doek. (104)",
        },
        "pl": {
            "title": "Problem z ładowaniem: styki wymagają wyczyszczenia",
            "content": "Odłącz zasilanie stacji dokującej, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (104)",
        },
        "pt": {
            "title": "Problema de carregamento: contactos precisam de limpeza",
            "content": "Desligue a base da alimentação e limpe os contactos de carregamento do robô e da base com um pano ligeiramente húmido. (104)",
        },
    },
    105: {
        "de": {
            "title": "Ladeproblem: Kontakte müssen gereinigt werden",
            "content": "Trennen Sie die Dockingstation vom Strom und wischen Sie die Ladekontakte am Roboter und an der Dockingstation mit einem leicht feuchten Tuch ab. (105)",
        },
        "en": {
            "title": "Charging Issue: contacts need to be cleaned",
            "content": "Unplug the Dock Power, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (105)",
        },
        "es": {
            "title": "Problema de carga: es necesario limpiar los contactos",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un paño ligeramente húmedo. (105)",
        },
        "fr": {
            "title": "Problème de chargement : les contacts doivent être nettoyés",
            "content": "Débranchez l’alimentation de la station d’accueil, puis essuyez les contacts de charge du robot et de la station avec un chiffon légèrement humide. (105)",
        },
        "it": {
            "title": "Problema di ricarica: è necessario ripulire i contatti",
            "content": "Scollega la base dall’alimentazione e pulisci i contatti di ricarica del robot e della base con un panno leggermente umido. (105)",
        },
        "nl": {
            "title": "Oplaadprobleem: contacten moeten gereinigd worden",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de laadcontacten van de robot en het basisstation schoon met een licht vochtige doek. (105)",
        },
        "pl": {
            "title": "Problem z ładowaniem: styki wymagają wyczyszczenia",
            "content": "Odłącz zasilanie stacji dokującej, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (105)",
        },
        "pt": {
            "title": "Problema de carregamento: contactos precisam de limpeza",
            "content": "Desligue a base da alimentação e limpe os contactos de carregamento do robô e da base com um pano ligeiramente húmido. (105)",
        },
    },
    106: {
        "de": {
            "title": "Ladeproblem: Warten Sie, bis der Akku abgekühlt ist, und versuchen Sie es erneut",
            "content": "Stellen Sie sicher, dass @val und Dockingstation bei Raumtemperatur aufbewahrt werden. Entfernen Sie sie von jeglichen Wärmequellen. (106)",
        },
        "en": {
            "title": "Charging Issue: Wait for the battery to cool down and try again",
            "content": "Make sure\xa0@val\xa0and dock are stored in a room temperature location. Move away from heat source. (106)",
        },
        "es": {
            "title": "Problema de carga: espera a que la batería se enfríe e inténtalo de nuevo",
            "content": "Asegúrate de que @val y la base se encuentren a temperatura ambiente. Aléjalos de fuentes de calor. (106)",
        },
        "fr": {
            "title": "Problème de charge : attendez que la batterie refroidisse",
            "content": "Assurez-vous que @val et la station d’accueil se trouvent dans un endroit à température ambiante. Éloigner de toute source de chaleur. (106)",
        },
        "it": {
            "title": "Problema di ricarica: attendi che la batteria si raffreddi e riprova",
            "content": "Assicurarsi che @val e la base si trovino a temperatura ambiente. Allontanare da fonti di calore. (106)",
        },
        "nl": {
            "title": "Oplaadprobleem: wacht tot de accu is afgekoeld en probeer het opnieuw",
            "content": "Zorg ervoor dat de @val en het dock zich in een ruimte op kamertemperatuur bevinden. Plaats uit de buurt van een warmtebron. (106)",
        },
        "pl": {
            "title": "Problem z ładowaniem: Poczekaj, aż akumulator ostygnie, i spróbuj ponownie",
            "content": "Upewnij się, że robot @val i stacja dokująca są przechowywane w temperaturze pokojowej. Odsuń od źródła ciepła. (106)",
        },
        "pt": {
            "title": "Problema de carregamento: aguarde que a bateria arrefeça e tente novamente",
            "content": "Certifique-se de que @val e a base estão num local à temperatura ambiente. Afaste-os de fontes de calor. (106)",
        },
    },
    107: {
        "de": {
            "title": "Ladeproblem: Warten Sie, bis der Akku abgekühlt ist, und versuchen Sie es erneut",
            "content": "Stellen Sie sicher, dass @val und Dockingstation bei Raumtemperatur aufbewahrt werden. Entfernen Sie sie von jeglichen Wärmequellen. (107)",
        },
        "en": {
            "title": "Charging Issue: Wait for the battery to cool down and try again",
            "content": "Make sure\xa0@val\xa0and Dock are stored in a room temperature location. Move away from heat source. (107)",
        },
        "es": {
            "title": "Problema de carga: espera a que la batería se enfríe e inténtalo de nuevo",
            "content": "Asegúrate de que @val y la base se encuentren a temperatura ambiente. Aléjalos de fuentes de calor. (107)",
        },
        "fr": {
            "title": "Problème de charge : attendez que la batterie refroidisse",
            "content": "Assurez-vous que @val et la station d’accueil se trouvent dans un endroit à température ambiante. Éloignez de toute source de chaleur. (107)",
        },
        "it": {
            "title": "Problema di ricarica: attendi che la batteria si raffreddi e riprova",
            "content": "Assicurarsi che @val e la base si trovino a temperatura ambiente. Allontanare da fonti di calore. (107)",
        },
        "nl": {
            "title": "Oplaadprobleem: wacht tot de accu is afgekoeld en probeer het opnieuw",
            "content": "Zorg ervoor dat de @val en het basisstation zich in een ruimte op kamertemperatuur bevinden. Verplaats het weg van warmtebronnen. (107)",
        },
        "pl": {
            "title": "Problem z ładowaniem: Poczekaj, aż akumulator ostygnie, i spróbuj ponownie",
            "content": "Upewnij się, że robot @val i stacja dokująca są przechowywane w temperaturze pokojowej. Odsuń od źródła ciepła. (107)",
        },
        "pt": {
            "title": "Problema de carregamento: aguarde que a bateria arrefeça e tente novamente",
            "content": "Certifique-se de que @val e a base estão num local à temperatura ambiente. Afaste-os de fontes de calor. (107)",
        },
    },
    109: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku, warten Sie 15 Minuten und setzen Sie ihn zur Fehlerbehebung wieder ein. (109)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove battery, wait 15 minutes, and reinstall to clear. (109)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira la batería, espera 15\xa0minutos y vuelve a instalarla para solucionarlo. (109)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez la batterie, patientez 15 minutes, puis réinstallez-la pour effacer l’erreur. (109)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere la batteria, attendere 15 minuti e reinstallarla per ripristinare. (109)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu, wacht 15 minuten en plaats deze opnieuw om de fout te wissen. (109)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij akumulator, odczekaj 15\xa0minut i włóż go ponownie, aby usunąć błąd. (109)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova a bateria, aguarde 15 minutos e volte a instalar para corrigir. (109)",
        },
    },
    110: {
        "de": {
            "title": "Ladeproblem: Wenden Sie sich zum Austausch des Akkus an den Kundenservice",
            "content": "Bitte ersetzen Sie den Akku von @val. Stellen Sie sicher, dass Sie einen originalen Akku von iRobot für Ihr Robotermodell verwenden. (110)",
        },
        "en": {
            "title": "Charging Issue: Contact customer service to replace the battery",
            "content": "Please replace\xa0@val’s battery. Make sure you use an authentic iRobot battery for your robot model. (110)",
        },
        "es": {
            "title": "Problema de carga: contacta con atención al cliente para sustituir la batería",
            "content": "Sustituye la batería de @val. Asegúrate de usar una batería iRobot auténtica adecuada para tu modelo de robot. (110)",
        },
        "fr": {
            "title": "Problème de charge : contactez le service client pour remplacer la batterie",
            "content": "Veuillez remplacer la batterie de @val. Assurez-vous d’utiliser une batterie iRobot authentique pour votre modèle de robot. (110)",
        },
        "it": {
            "title": "Problema di ricarica: contatta il servizio clienti per sostituire la batteria",
            "content": "Sostituire la batteria di @val. Assicurarsi di utilizzare una batteria iRobot originale per il proprio modello di robot. (110)",
        },
        "nl": {
            "title": "Oplaadprobleem: neem contact op met de klantenservice om de accu te vervangen",
            "content": "Vervang de batterij van @val. Zorg ervoor dat u een originele iRobot-accu voor uw robotmodel gebruikt. (110)",
        },
        "pl": {
            "title": "Problem z ładowaniem: Skontaktuj się z obsługą klienta w celu wymiany akumulatora",
            "content": "Wymień akumulator robota @val. Upewnij się, że używasz oryginalnego akumulatora iRobot odpowiedniego dla modelu robota. (110)",
        },
        "pt": {
            "title": "Problema de carregamento: contacte o apoio ao cliente para substituir a bateria",
            "content": "Substitua a bateria de @val. Certifique-se de que utiliza uma bateria iRobot original para o seu modelo de robô. (110)",
        },
    },
    111: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku, warten Sie 15 Minuten und setzen Sie ihn zur Fehlerbehebung wieder ein. (111)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove battery, wait 15 minutes, and reinstall to clear. (111)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira la batería, espera 15\xa0minutos y vuelve a instalarla para solucionarlo. (111)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez la batterie, patientez 15 minutes, puis réinstallez-la pour effacer l’erreur. (111)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere la batteria, attendere 15 minuti e reinstallarla per ripristinare. (111)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu, wacht 15 minuten en plaats deze opnieuw om te wissen. (111)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij akumulator, odczekaj 15\xa0minut i włóż go ponownie, aby usunąć błąd. (111)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova a bateria, aguarde 15 minutos e volte a instalar para corrigir. (111)",
        },
    },
    114: {
        "de": {
            "title": "Ladeproblem",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Entfernen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (114)",
        },
        "en": {
            "title": "Charging Issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (114)",
        },
        "es": {
            "title": "Problema de carga",
            "content": "Reinicia @val para solucionar el error. Retíralo de la base y mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (114)",
        },
        "fr": {
            "title": "Problème de charge",
            "content": "Redémarrez @val pour effacer l’erreur. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (114)",
        },
        "it": {
            "title": "Problema di ricarica",
            "content": "Riavviare @val per risolvere l'errore. Rimuovere dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (114)",
        },
        "nl": {
            "title": "Oplaadprobleem",
            "content": "Start @val opnieuw op om de fout te wissen. Verwijder het van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (114)",
        },
        "pl": {
            "title": "Błąd ładowania",
            "content": "Uruchom ponownie robota @val w celu usunięcia błędu. Wyjmij ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (114)",
        },
        "pt": {
            "title": "Problema de carregamento",
            "content": "Reinicie @val para corrigir o erro. Retire da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (114)",
        },
    },
    115: {
        "de": {
            "title": "Ladeproblem: Wenden Sie sich zum Austausch des Akkus an den Kundenservice",
            "content": "Bitte ersetzen Sie den Akku von @val. Stellen Sie sicher, dass Sie einen originalen Akku von iRobot für Ihr Robotermodell verwenden. (115)",
        },
        "en": {
            "title": "Charging Issue: Contact customer service to replace the battery",
            "content": "Please replace\xa0@val’s battery. Make sure you use an authentic iRobot battery for your robot model. (115)",
        },
        "es": {
            "title": "Problema de carga: contacta con atención al cliente para sustituir la batería",
            "content": "Sustituye la batería de @val. Asegúrate de usar una batería iRobot auténtica adecuada para tu modelo de robot. (115)",
        },
        "fr": {
            "title": "Problème de charge : contactez le service client pour remplacer la batterie",
            "content": "Veuillez remplacer la batterie de @val. Assurez-vous d’utiliser une batterie iRobot authentique pour votre modèle de robot. (115)",
        },
        "it": {
            "title": "Problema di ricarica: contatta il servizio clienti per sostituire la batteria",
            "content": "Sostituire la batteria di @val. Assicurarsi di utilizzare una batteria iRobot originale per il proprio modello di robot. (115)",
        },
        "nl": {
            "title": "Oplaadprobleem: neem contact op met de klantenservice om de accu te vervangen",
            "content": "Vervang de batterij van @val. Zorg ervoor dat u een originele iRobot-accu voor uw robotmodel gebruikt. (115)",
        },
        "pl": {
            "title": "Problem z ładowaniem: Skontaktuj się z obsługą klienta w celu wymiany akumulatora",
            "content": "Wymień akumulator robota @val. Upewnij się, że używasz oryginalnego akumulatora iRobot odpowiedniego dla modelu robota. (115)",
        },
        "pt": {
            "title": "Problema de carregamento: contacte o apoio ao cliente para substituir a bateria",
            "content": "Substitua a bateria de @val. Certifique-se de que utiliza uma bateria iRobot original para o seu modelo de robô. (115)",
        },
    },
    117: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku, warten Sie 15 Minuten und setzen Sie ihn zur Fehlerbehebung wieder ein. (117)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove battery, wait 15 minutes, and reinstall to clear. (117)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira la batería, espera 15\xa0minutos y vuelve a instalarla para solucionarlo. (117)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez la batterie, patientez 15 minutes, puis réinstallez-la pour effacer l’erreur. (117)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere la batteria, attendere 15 minuti e reinstallarla per ripristinare. (117)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu, wacht 15 minuten en plaats deze opnieuw om te wissen. (117)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij akumulator, odczekaj 15\xa0minut i włóż go ponownie, aby usunąć błąd. (117)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova a bateria, aguarde 15 minutos e volte a instalar para corrigir. (117)",
        },
    },
    119: {
        "de": {
            "title": "Ladeproblem: Kontakte müssen gereinigt werden",
            "content": "Stecken Sie die Dockingstation vom Stromnetz aus und reinigen Sie die Ladekontakte an Roboter und Dockingstation mit einem feuchten Schmutzradierer. (119)",
        },
        "en": {
            "title": "Charging Issue: contacts need to be cleaned",
            "content": "Unplug the Dock, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (119)",
        },
        "es": {
            "title": "Problema de carga: es necesario limpiar los contactos",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un pañuelo ligeramente húmedo. (119)",
        },
        "fr": {
            "title": "Problème de chargement : les contacts doivent être nettoyés",
            "content": "Débranchez la station d’accueil, puis essuyez les contacts de chargement du robot et de la station d’accueil avec un mouchoir légèrement humide. (119)",
        },
        "it": {
            "title": "Problema di ricarica: è necessario ripulire i contatti",
            "content": "Scollegare la base, quindi pulire i contatti di ricarica sul robot e sulla base con un fazzoletto leggermente umido. (119)",
        },
        "nl": {
            "title": "Oplaadprobleem: contacten moeten gereinigd worden",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de oplaadcontacten op de robot en het basisstation schoon met een licht vochtig doekje. (119)",
        },
        "pl": {
            "title": "Problem z ładowaniem: styki wymagają wyczyszczenia",
            "content": "Odłącz stację dokującą, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (119)",
        },
        "pt": {
            "title": "Problema de carregamento: contactos precisam de limpeza",
            "content": "Desligue a base e limpe os contactos de carregamento no robô e na base com um lenço ligeiramente húmido. (119)",
        },
    },
    120: {
        "de": {
            "title": "Ladeproblem: Aufladen nicht möglich",
            "content": "@val hat Probleme, seinen Akku zu erkennen. Entfernen Sie den Akku, warten Sie 15 Minuten und setzen Sie ihn zur Fehlerbehebung wieder ein. (120)",
        },
        "en": {
            "title": "Charging Issue: unable to charge",
            "content": "@val\xa0is having trouble detecting its battery. Remove battery, wait 15 minutes, and reinstall to clear. (120)",
        },
        "es": {
            "title": "Problema de carga: no se puede cargar",
            "content": "@val tiene problemas para detectar la batería. Retira la batería, espera 15\xa0minutos y vuelve a instalarla para solucionarlo. (120)",
        },
        "fr": {
            "title": "Problème de chargement : impossible de recharger",
            "content": "@val n’arrive pas à détecter sa batterie. Retirez la batterie, patientez 15 minutes, puis réinstallez-la pour effacer l’erreur. (120)",
        },
        "it": {
            "title": "Problema di ricarica: impossibile ricaricare",
            "content": "@val ha problemi a rilevare la batteria. Rimuovere la batteria, attendere 15 minuti e reinstallarla per ripristinare. (120)",
        },
        "nl": {
            "title": "Oplaadprobleem: kan niet worden opgeladen",
            "content": "@val heeft problemen met het detecteren van de accu. Verwijder de accu, wacht 15 minuten en plaats deze opnieuw om te wissen. (120)",
        },
        "pl": {
            "title": "Problem z ładowaniem: nie można naładować",
            "content": "Robot @val ma problem z wykryciem akumulatora. Wyjmij akumulator, odczekaj 15\xa0minut i włóż go ponownie, aby usunąć błąd. (120)",
        },
        "pt": {
            "title": "Problema de carregamento: não é possível carregar",
            "content": "@val está com dificuldade em detetar a bateria. Remova a bateria, aguarde 15 minutos e volte a instalar para corrigir. (120)",
        },
    },
    121: {
        "de": {
            "title": "Ladeproblem: Kontakte müssen gereinigt werden",
            "content": "Stecken Sie die Dockingstation vom Stromnetz aus und reinigen Sie die Ladekontakte an Roboter und Dockingstation mit einem feuchten Schmutzradierer. (121)",
        },
        "en": {
            "title": "Charging Issue: contacts need to be cleaned",
            "content": "Unplug the Dock, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (121)",
        },
        "es": {
            "title": "Problema de carga: es necesario limpiar los contactos",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un pañuelo ligeramente húmedo. (121)",
        },
        "fr": {
            "title": "Problème de chargement : les contacts doivent être nettoyés",
            "content": "Débranchez la station d’accueil, puis essuyez les contacts de chargement du robot et de la station d’accueil avec un mouchoir légèrement humide. (121)",
        },
        "it": {
            "title": "Problema di ricarica: è necessario ripulire i contatti",
            "content": "Scollegare la base, quindi pulire i contatti di ricarica sul robot e sulla base con un fazzoletto leggermente umido. (121)",
        },
        "nl": {
            "title": "Oplaadprobleem: contacten moeten gereinigd worden",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de oplaadcontacten op de robot en het basisstation schoon met een licht vochtig doekje. (121)",
        },
        "pl": {
            "title": "Problem z ładowaniem: styki wymagają wyczyszczenia",
            "content": "Odłącz stację dokującą, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (121)",
        },
        "pt": {
            "title": "Problema de carregamento: contactos precisam de limpeza",
            "content": "Desligue a base e limpe os contactos de carregamento no robô e na base com um lenço ligeiramente húmido. (121)",
        },
    },
    201: {
        "de": {
            "title": "Start nicht möglich: Treppe oder Absturzstelle erkannt",
            "content": "Bewegen Sie @val an einen anderen Ort und versuchen Sie es erneut. (201)",
        },
        "en": {
            "title": "Unable to start: stairs or drop-off detected",
            "content": "Please move\xa0@val\xa0to a new location and try again. (201)",
        },
        "es": {
            "title": "No se puede iniciar: se han detectado escalones o un desnivel",
            "content": "Mueve @val a una nueva ubicación e inténtalo de nuevo. (201)",
        },
        "fr": {
            "title": "Impossible de démarrer : escaliers ou vide détectés",
            "content": "Veuillez déplacer @val vers un nouvel emplacement et réessayer. (201)",
        },
        "it": {
            "title": "Impossibile avviare: scale o dislivelli rilevati",
            "content": "Spostare @val in una nuova posizione e riprovare. (201)",
        },
        "nl": {
            "title": "Kan niet starten: trappen of afstapje gedetecteerd",
            "content": "Verplaats @val naar een nieuwe locatie en probeer het opnieuw. (201)",
        },
        "pl": {
            "title": "Nie można rozpocząć: wykryto schody lub spadek",
            "content": "Przenieś robota @val w nowe miejsce i spróbuj ponownie. (201)",
        },
        "pt": {
            "title": "Não é possível iniciar: escadas ou queda detetada",
            "content": "Mova @val para outro local e tente novamente. (201)",
        },
    },
    202: {
        "de": {
            "title": "Roboter schwebt in der Luft",
            "content": "Der Roboter hat erkannt, dass er in der Luft schwebt. Bitte bringen Sie ihn an einen neuen Ort und starten Sie ihn erneut.",
        },
        "en": {
            "title": "Robot is suspended",
            "content": "The Robot has detected that it is suspended in mid-air. Please move it to a new location and start again.",
        },
        "es": {
            "title": "Robot suspendido",
            "content": "El robot ha detectado que está suspendido en el aire. Muévelo a una nueva ubicación e inícialo de nuevo.",
        },
        "fr": {
            "title": "Robot en suspension",
            "content": "Le robot a détecté qu’il est en suspension dans les airs. Veuillez le déplacer vers un nouvel emplacement et le redémarrer.",
        },
        "it": {
            "title": "Robot sospeso in aria",
            "content": "Il robot ha rilevato di essere sospeso in aria. Spostalo in una nuova posizione e riavvialo.",
        },
        "nl": {
            "title": "Robot zweeft in de lucht",
            "content": "De robot heeft gedetecteerd dat hij in de lucht zweeft. Verplaats hem naar een nieuwe locatie en start opnieuw.",
        },
        "pl": {
            "title": "Robot jest zawieszony",
            "content": "Robot wykrył, że jest zawieszony w powietrzu. Przenieś go w nowe miejsce i uruchom ponownie.",
        },
        "pt": {
            "title": "Robô suspenso no ar",
            "content": "O robô detetou que está suspenso no ar. Mova-o para um novo local e inicie novamente.",
        },
    },
    207: {
        "de": {
            "title": "Start nicht möglich: Behälter nicht installiert",
            "content": "Bitte setzen Sie den Behälter von @val ein und versuchen Sie es erneut. (207)",
        },
        "en": {
            "title": "Unable to start: bin not installed",
            "content": "Please install\xa0@val’s bin and try again. (207)",
        },
        "es": {
            "title": "No se puede iniciar: depósito de polvo no instalado",
            "content": "Instala el depósito de @val e inténtalo de nuevo. (207)",
        },
        "fr": {
            "title": "Impossible de démarrer : bac non installé",
            "content": "Veuillez installer le bac de @val et réessayer. (207)",
        },
        "it": {
            "title": "Impossibile avviare: cestino non installato",
            "content": "Installare il cestino di @val e riprovare. (207)",
        },
        "nl": {
            "title": "Kan niet starten: opvangbak niet geïnstalleerd",
            "content": "Installeer de opvangbak van @val en probeer het opnieuw. (207)",
        },
        "pl": {
            "title": "Nie można rozpocząć: pojemnik nie jest zamontowany",
            "content": "Zamontuj pojemnik robota @val i spróbuj ponownie. (207)",
        },
        "pt": {
            "title": "Não é possível iniciar: depósito não instalado",
            "content": "Instale o depósito de @val e tente novamente. (207)",
        },
    },
    210: {
        "de": {
            "title": "Start nicht möglich: hängt in einer nicht zu befahrenden Zone fest",
            "content": "Bewegen Sie @val aus der nicht zu befahrenden Zone heraus, damit der Roboter seine neue Routine starten kann. (210)",
        },
        "en": {
            "title": "Unable to start: stuck in a Keep Out Zone",
            "content": "Move\xa0@val\xa0out of the Keep Out Zone so it can start its new routine. (210)",
        },
        "es": {
            "title": "No se puede iniciar: robot atascado en una zona de exclusión",
            "content": "Mueve @val fuera de la zona de exclusión para que pueda iniciar la nueva rutina. (210)",
        },
        "fr": {
            "title": "Impossible de démarrer : bloqué dans une zone à ignorer",
            "content": "Déplacez @val en dehors de la zone à ignorer pour qu’il puisse démarrer sa nouvelle routine. (210)",
        },
        "it": {
            "title": "Impossibile avviare: bloccato in una zona da escludere",
            "content": "Spostare @val fuori dalla zona da escludere per poter avviare la nuova routine. (210)",
        },
        "nl": {
            "title": "Kan niet starten: vast in een verbodszone",
            "content": "Verplaats @val uit de verbodszone zodat deze de nieuwe routine kan starten. (210)",
        },
        "pl": {
            "title": "Nie można rozpocząć: utknął w strefie bez dostępu",
            "content": "Przenieś robota @val poza strefę bez dostępu, aby mógł rozpocząć nową rutynę. (210)",
        },
        "pt": {
            "title": "Não é possível iniciar: preso numa Zona de Exclusão",
            "content": "Retire @val da Zona de Exclusão para que possa iniciar a nova rotina. (210)",
        },
    },
    215: {
        "de": {
            "title": "Start nicht möglich: Akkustand niedrig",
            "content": "Bitte lassen Sie @val den Akku ausreichend aufladen und versuchen Sie es erneut. (215)",
        },
        "en": {
            "title": "Unable to start: battery low, recharge it",
            "content": "Please allow\xa0@val\xa0to charge its battery sufficiently and try again. (215)",
        },
        "es": {
            "title": "No se puede iniciar: batería baja",
            "content": "Deja que @val cargue la batería lo suficiente e inténtalo de nuevo. (215)",
        },
        "fr": {
            "title": "Impossible de démarrer : batterie faible",
            "content": "Veuillez laisser @val recharger suffisamment sa batterie et réessayer. (215)",
        },
        "it": {
            "title": "Impossibile avviare: batteria scarica",
            "content": "Lasciare che @val carichi sufficientemente la batteria e riprovare. (215)",
        },
        "nl": {
            "title": "Kan niet starten: accu bijna leeg",
            "content": "Laat @val voldoende opladen en probeer het opnieuw. (215)",
        },
        "pl": {
            "title": "Nie można rozpocząć: niski poziom akumulatora, naładuj go",
            "content": "Poczekaj, aż robot @val naładuje się wystarczająco i spróbuj ponownie. (215)",
        },
        "pt": {
            "title": "Não é possível iniciar: bateria fraca",
            "content": "Permita que @val carregue suficientemente a bateria e tente novamente. (215)",
        },
    },
    216: {
        "de": {
            "title": "Start nicht möglich: Behälter voll oder verstopft",
            "content": "Leeren Sie den Behälter von @val und entfernen Sie mögliche Hindernisse, damit Staubverdichter und Kanal frei sind. (216)",
        },
        "en": {
            "title": "Unable to start: bin full or clogged",
            "content": "Empty\xa0@val’s bin and clear any possible obstructions to the dust compactor and plenum is clear. (216)",
        },
        "es": {
            "title": "No se puede iniciar: depósito lleno u obstruido",
            "content": "Vacía el depósito de @val y retira cualquier posible obstrucción asegurándote de que el compactador de polvo y la cámara estén despejados. (216)",
        },
        "fr": {
            "title": "Impossible de démarrer : bac plein ou bouché",
            "content": "Videz le bac de @val et éliminez toute obstruction possible du compacteur de poussière et du conduit d’aspiration. (216)",
        },
        "it": {
            "title": "Impossibile avviare: cestino pieno o ostruito",
            "content": "Svuotare il cestino di @val e rimuovere eventuali ostruzioni dal compattatore della polvere e assicurarsi che il condotto sia libero. (216)",
        },
        "nl": {
            "title": "Kan niet starten: opvangbak vol of verstopt",
            "content": "Leeg de opvangbak van @val en verwijder eventuele verstoppingen, zodat de stofverdichter en het plenum vrij zijn. (216)",
        },
        "pl": {
            "title": "Nie można rozpocząć: pojemnik jest pełny lub zatkany",
            "content": "Opróżnij pojemnik robota @val i wyczyść wszelkie możliwe blokady w zgniatarce kurzu oraz kanale powietrznym. (216)",
        },
        "pt": {
            "title": "Não é possível iniciar: depósito cheio ou obstruído",
            "content": "Esvazie o depósito de @val e remova quaisquer obstruções do compactador de pó e do conduto. (216)",
        },
    },
    218: {
        "de": {
            "title": "Start nicht möglich: Roboter-Update läuft",
            "content": "Lassen Sie @val auf seiner Dockingstation, bis das Update abgeschlossen ist. Reinigung wird in Kürze verfügbar sein. (218)",
        },
        "en": {
            "title": "Unable to start: robot update in progress",
            "content": "Leave\xa0@val\xa0on its Dock until update is complete. Cleaning will be available shortly. (218)",
        },
        "es": {
            "title": "No se puede iniciar: actualización del robot en curso",
            "content": "Deja @val en su base hasta que se complete la actualización. La limpieza estará disponible en breve. (218)",
        },
        "fr": {
            "title": "Impossible de démarrer : mise à jour du robot en cours",
            "content": "Laissez @val sur sa station d’accueil jusqu’à ce que la mise à jour soit terminée. Le nettoyage sera bientôt disponible. (218)",
        },
        "it": {
            "title": "Impossibile avviare: aggiornamento del robot in corso",
            "content": "Lasciare @val sulla base fino al completamento dell'aggiornamento. La pulizia sarà di nuovo disponibile a breve. (218)",
        },
        "nl": {
            "title": "Kan niet starten: robotupdate wordt uitgevoerd",
            "content": "Laat @val op het dock staan tot de update is voltooid. Schoonmaken is binnenkort beschikbaar. (218)",
        },
        "pl": {
            "title": "Nie można rozpocząć: trwa aktualizacja robota",
            "content": "Pozostaw robota @val w stacji dokującej do zakończenia aktualizacji. Sprzątanie będzie wkrótce dostępne. (218)",
        },
        "pt": {
            "title": "Não é possível iniciar: atualização do robô em curso",
            "content": "Deixe @val na base até a atualização estar concluída. A limpeza estará disponível em breve. (218)",
        },
    },
    222: {
        "de": {
            "title": "Start nicht möglich: Problem mit dem Navigationsmodul",
            "content": "Bewegen Sie @val an einen anderen Ort und versuchen Sie es erneut. (222)",
        },
        "en": {
            "title": "Unable to start: Navigation Module issue, restart the Robot",
            "content": "Move\xa0@val\xa0to a new location and try again. (222)",
        },
        "es": {
            "title": "No se puede iniciar: problema del módulo de navegación",
            "content": "Mueve @val a una nueva ubicación e inténtalo de nuevo. (222)",
        },
        "fr": {
            "title": "Impossible de démarrer : problème du module de navigation",
            "content": "Déplacez @val vers un nouvel emplacement et réessayez. (222)",
        },
        "it": {
            "title": "Impossibile avviare: problema del modulo di navigazione",
            "content": "Spostare @val in una nuova posizione e riprovare. (222)",
        },
        "nl": {
            "title": "Kan niet starten: probleem met navigatiemodule",
            "content": "Verplaats @val naar een nieuwe locatie en probeer het opnieuw. (222)",
        },
        "pl": {
            "title": "Nie można rozpocząć: problem z modułem nawigacji, uruchom ponownie robota",
            "content": "Przenieś robota @val w nowe miejsce i spróbuj ponownie. (222)",
        },
        "pt": {
            "title": "Não é possível iniciar: problema no módulo de navegação",
            "content": "Mova @val para outro local e tente novamente. (222)",
        },
    },
    224: {
        "de": {
            "title": "Start nicht möglich: Kartenproblem",
            "content": "Überprüfen Sie, ob die Karte von @val präzise ist, und versuchen Sie es erneut. (224)",
        },
        "en": {
            "title": "Unable to start: Map issue, please remap",
            "content": "Check that\xa0@val's map is accurate and try again. (224)",
        },
        "es": {
            "title": "No se puede iniciar: problema con el mapa",
            "content": "Comprueba que el mapa de @val sea correcto e inténtalo de nuevo. (224)",
        },
        "fr": {
            "title": "Impossible de démarrer : problème de carte",
            "content": "Vérifiez que la carte de @val est correcte et réessayez. (224)",
        },
        "it": {
            "title": "Impossibile avviare: problema della mappa",
            "content": "Verificare che la mappa di @val sia accurata e riprovare. (224)",
        },
        "nl": {
            "title": "Kan niet starten: kaartprobleem",
            "content": "Controleer of de kaart van @val nauwkeurig is en probeer het opnieuw. (224)",
        },
        "pl": {
            "title": "Nie można rozpocząć: problem z mapą, wykonaj mapowanie ponownie",
            "content": "Sprawdź, czy mapa robota @val jest dokładna i spróbuj ponownie. (224)",
        },
        "pt": {
            "title": "Não é possível iniciar: problema no mapa",
            "content": "Verifique se o mapa de @val está correto e tente novamente. (224)",
        },
    },
    228: {
        "de": {
            "title": "Start nicht möglich: Wichtiges Update verfügbar",
            "content": 'Gehen Sie im unteren App-Menü zur Registerkarte "Support" und wenden Sie sich an unser Team, damit wir Ihren Roboter per Fernzugriff aktualisieren können.\nDadurch wird ein Sensor aktualisiert, der zur ordnungsgemäßen Funktion von @val beiträgt. (228)',
        },
        "en": {
            "title": "Unable to start: Update to the latest version",
            "content": "Go to the Support tab from the bottom app menu and contact our team so we can remotely update your robot.\nThis will update a sensor that helps\xa0@val\xa0work properly. (228)",
        },
        "es": {
            "title": "No se puede iniciar: Actualización importante disponible",
            "content": "Ve a la pestaña Atención al cliente en el menú inferior de la app y contacta con nuestro equipo para que podamos actualizar tu robot de forma remota.\nSe actualizará un sensor que contribuye a que @val funcione correctamente. (228)",
        },
        "fr": {
            "title": "Impossible de démarrer : Mise à jour importante disponible",
            "content": "Accédez à l’onglet Assistance dans le menu inférieur de l’application et contactez notre équipe pour que nous puissions mettre à jour votre robot à distance.\nCela mettra à jour un capteur qui aide @val à fonctionner correctement. (228)",
        },
        "it": {
            "title": "Impossibile avviare: Importante aggiornamento disponibile",
            "content": "Accedere alla scheda Assistenza dal menu in basso dell'app e contattare il nostro team, in modo da poter aggiornare da remoto il robot.\nQuesto aggiornerà un sensore che aiuta @val a funzionare correttamente. (228)",
        },
        "nl": {
            "title": "Kan niet starten: Belangrijke update beschikbaar",
            "content": "Ga naar de tab ondersteuning in het onderste menu van de app en neem contact op met ons team, zodat we je robot op afstand kunnen updaten.\nHiermee wordt een sensor bijgewerkt die ervoor zorgt dat @val correct werkt. (228)",
        },
        "pl": {
            "title": "Nie można rozpocząć: Dostępna jest ważna aktualizacja",
            "content": "Przejdź do karty Wsparcie w dolnym menu aplikacji i skontaktuj się z naszym zespołem, abyśmy mogli zdalnie zaktualizować robota.\nZaktualizuje to czujnik, który umożliwia robotowi @val prawidłowe działanie. (228)",
        },
        "pt": {
            "title": "Não é possível iniciar: Atualização importante disponível",
            "content": "Vá ao separador Suporte no menu inferior da aplicação e contacte a nossa equipa para que possamos atualizar remotamente o seu robô.\nIsto irá atualizar um sensor que ajuda @val a funcionar corretamente. (228)",
        },
    },
    231: {
        "de": {
            "title": "Start nicht möglich: Frischwassertankstand niedrig",
            "content": "Bitte füllen Sie den Dockingstation-Tank vollständig auf und versuchen Sie es erneut. (231)",
        },
        "en": {
            "title": "Unable to start: Clean Water Tank level low",
            "content": "Fill up the Clean Water Tank and try again. (231)",
        },
        "es": {
            "title": "No se puede iniciar: nivel bajo del depósito de agua limpia",
            "content": "Llena el tanque de la base por completo e inténtalo de nuevo. (231)",
        },
        "fr": {
            "title": "Impossible de démarrer : niveau bas du réservoir d’eau propre",
            "content": "Veuillez remplir complètement le réservoir de la station d’accueil et réessayer. (231)",
        },
        "it": {
            "title": "Impossibile avviare: livello basso del serbatoio dell’acqua pulita",
            "content": "Riempire completamente il serbatoio della base e riprovare. (231)",
        },
        "nl": {
            "title": "Kan niet starten: schoonwatertank bijna leeg",
            "content": "Vul de tank van het basisstation volledig bij en probeer het opnieuw. (231)",
        },
        "pl": {
            "title": "Nie można rozpocząć: niski poziom w zbiorniku na czystą wodę",
            "content": "Całkowicie napełnij zbiornik na czystą wodę i spróbuj ponownie. (231)",
        },
        "pt": {
            "title": "Não é possível iniciar: nível baixo do depósito de água limpa",
            "content": "Encha completamente o depósito da base e tente novamente. (231)",
        },
    },
    234: {
        "de": {
            "title": "Start nicht möglich: kein Mopp angebracht",
            "content": "Bitte befestigen Sie einen Mopp und versuchen Sie es erneut. (234)",
        },
        "en": {
            "title": "Unable to start: no mop attached",
            "content": "Please attach a mop and try again. (234)",
        },
        "es": {
            "title": "No se puede iniciar: mopa no instalada",
            "content": "Instala una mopa e inténtalo de nuevo. (234)",
        },
        "fr": {
            "title": "Impossible de démarrer : aucune serpillière fixée",
            "content": "Veuillez fixer une serpillière et réessayer. (234)",
        },
        "it": {
            "title": "Impossibile avviare: panno di lavaggio non installato",
            "content": "Installare un panno di lavaggio e riprovare. (234)",
        },
        "nl": {
            "title": "Kan niet starten: geen dweil bevestigd",
            "content": "Bevestig een dweil en probeer het opnieuw. (234)",
        },
        "pl": {
            "title": "Nie można rozpocząć: nie zamontowano mopa",
            "content": "Załóż nakładkę mopującą i spróbuj ponownie. (234)",
        },
        "pt": {
            "title": "Não é possível iniciar: mopa não instalada",
            "content": "Instale uma mopa e tente novamente. (234)",
        },
    },
    237: {
        "de": {
            "title": "Start nicht möglich: kein Akku erkannt",
            "content": "Bitte setzen Sie den Akku von @val ein und versuchen Sie es erneut. (237)",
        },
        "en": {
            "title": "Unable to start: no battery detected",
            "content": "Please install\xa0@val's battery and try again. (237)",
        },
        "es": {
            "title": "No se puede iniciar: no se ha detectado la batería",
            "content": "Instala la batería de @val e inténtalo de nuevo. (237)",
        },
        "fr": {
            "title": "Impossible de démarrer : aucune batterie détectée",
            "content": "Veuillez installer la batterie de @val et réessayer. (237)",
        },
        "it": {
            "title": "Impossibile avviare: nessuna batteria rilevata",
            "content": "Installare la batteria di @val e riprovare. (237)",
        },
        "nl": {
            "title": "Kan niet starten: geen batterij gedetecteerd",
            "content": "Installeer de batterij van @val en probeer het opnieuw. (237)",
        },
        "pl": {
            "title": "Nie można rozpocząć: nie wykryto akumulatora",
            "content": "Zamontuj akumulator robota @val i spróbuj ponownie. (237)",
        },
        "pt": {
            "title": "Não é possível iniciar: bateria não detetada",
            "content": "Instale a bateria de @val e tente novamente. (237)",
        },
    },
    238: {
        "de": {
            "title": "Start nicht möglich: kein Akku erkannt",
            "content": "Bitte setzen Sie den Akku von @val ein und versuchen Sie es erneut. (238)",
        },
        "en": {
            "title": "Unable to start: no battery detected",
            "content": "Please install\xa0@val's battery and try again. (238)",
        },
        "es": {
            "title": "No se puede iniciar: no se ha detectado la batería",
            "content": "Instala la batería de @val e inténtalo de nuevo. (238)",
        },
        "fr": {
            "title": "Impossible de démarrer : aucune batterie détectée",
            "content": "Veuillez installer la batterie de @val et réessayer. (238)",
        },
        "it": {
            "title": "Impossibile avviare: nessuna batteria rilevata",
            "content": "Installare la batteria di @val e riprovare. (238)",
        },
        "nl": {
            "title": "Kan niet starten: geen batterij gedetecteerd",
            "content": "Installeer de batterij van @val en probeer het opnieuw. (238)",
        },
        "pl": {
            "title": "Nie można rozpocząć: nie wykryto akumulatora",
            "content": "Zamontuj akumulator robota @val i spróbuj ponownie. (238)",
        },
        "pt": {
            "title": "Não é possível iniciar: bateria não detetada",
            "content": "Instale a bateria de @val e tente novamente. (238)",
        },
    },
    239: {
        "de": {
            "title": "Start nicht möglich: Karte wird gespeichert",
            "content": "Reinigung wird in Kürze verfügbar sein. (239)",
        },
        "en": {
            "title": "Unable to start: saving map",
            "content": "Cleaning will be available shortly. (239)",
        },
        "es": {
            "title": "No se puede iniciar: guardando mapa",
            "content": "La limpieza estará disponible en breve. (239)",
        },
        "fr": {
            "title": "Impossible de démarrer : sauvegarde de la carte",
            "content": "Le nettoyage sera bientôt disponible. (239)",
        },
        "it": {
            "title": "Impossibile avviare: salvataggio mappa",
            "content": "La pulizia sarà di nuovo disponibile a breve. (239)",
        },
        "nl": {
            "title": "Kan niet starten: kaart opslaan",
            "content": "Schoonmaken is binnenkort beschikbaar. (239)",
        },
        "pl": {
            "title": "Nie można rozpocząć: zapisywanie mapy",
            "content": "Sprzątanie będzie wkrótce dostępne. (239)",
        },
        "pt": {
            "title": "Não é possível iniciar: guardar mapa",
            "content": "A limpeza estará disponível em breve. (239)",
        },
    },
    251: {
        "de": {
            "title": "Start nicht möglich: Kameraproblem",
            "content": "@val kann aufgrund eines Kameraproblems nicht navigieren. Halten Sie die Reinigungstaste 10 Sekunden lang gedrückt, um den Fehler zu beheben. (Fehler 251)",
        },
        "en": {
            "title": "Unable to start: camera issue",
            "content": "%robotName can’t navigate because of a camera issue. To clear error, press and hold clean button for 10 seconds. (Error 251)",
        },
        "es": {
            "title": "No se puede iniciar: problema con la cámara",
            "content": "@val no puede navegar debido a un problema con la cámara. Para solucionar el error, mantén pulsado el botón CLEAN durante 10\xa0segundos. (Error\xa0251)",
        },
        "fr": {
            "title": "Impossible de démarrer : problème de caméra",
            "content": "@val ne peut pas naviguer en raison d’un problème de caméra. Pour effacer l’erreur, maintenez le bouton de nettoyage enfoncé pendant 10 secondes. (Erreur 251)",
        },
        "it": {
            "title": "Impossibile avviare: problema alla fotocamera",
            "content": "@val non riesce a spostarsi a causa di un problema alla fotocamera. Per risolvere l'errore, tenere premuto il pulsante Pulisci per 10 secondi. (Errore 251)",
        },
        "nl": {
            "title": "Kan niet starten: cameraprobleem",
            "content": "@val kan niet navigeren vanwege een cameraprobleem. Houd de CLEAN-knop 10 seconden ingedrukt om de fout te wissen. (Fout 251)",
        },
        "pl": {
            "title": "Nie można rozpocząć: problem z kamerą",
            "content": "Robot @val nie może nawigować z powodu problemu z kamerą. Aby usunąć błąd, naciśnij i przytrzymaj przycisk czyszczenia przez 10\xa0sekund. (Błąd 251)",
        },
        "pt": {
            "title": "Não é possível iniciar: problema na câmara",
            "content": "@val não consegue navegar devido a um problema na câmara. Para corrigir o erro, prima sem soltar o botão Clean durante 10 segundos. (Erro 251)",
        },
    },
    266: {
        "de": {
            "title": "Start nicht möglich: Problem mit dem iRobot Select-Abonnement",
            "content": "Bitte besuchen Sie Ihr Mitgliedschaftsportal, um die Zahlungsmethode zu aktualisieren und den Abonnementstatus zu überprüfen. Tippen Sie unten, um sich beim Portal anzumelden. (266)",
        },
        "en": {
            "title": "Unable to start: issue with iRobot Select subscription",
            "content": "Please visit your Membership Portal to update payment method and check on subscription status. Tap below to login to the portal. (266)",
        },
        "es": {
            "title": "No se puede iniciar: problema con la suscripción a iRobot\xa0Select",
            "content": "Visita el portal de suscriptores para actualizar el método de pago y comprobar el estado de la suscripción. Toca a continuación para iniciar sesión en el portal. (266)",
        },
        "fr": {
            "title": "Impossible de démarrer : problème avec l’abonnement iRobot Select",
            "content": "Veuillez consulter votre portail d’abonnement pour mettre à jour votre mode de paiement et vérifier l’état de votre abonnement. Appuyez ci-dessous pour vous connecter au portail. (266)",
        },
        "it": {
            "title": "Impossibile avviare: problema con l'abbonamento iRobot Select",
            "content": "Visitare il Portale di abbonamento per aggiornare il metodo di pagamento e controllare lo stato dell'abbonamento. Toccare qui sotto per accedere al portale. (266)",
        },
        "nl": {
            "title": "Kan niet starten: probleem met iRobot Select-abonnement",
            "content": "Bezoek je ledenportaal om de betaalmethode bij te werken en de abonnementsstatus te controleren. Tik hieronder om in te loggen op het portaal. (266)",
        },
        "pl": {
            "title": "Nie można uruchomić: problem z subskrypcją iRobot Select",
            "content": "Odwiedź portal dla członków, aby zaktualizować metodę płatności i sprawdzić stan subskrypcji. Kliknij poniżej, aby zalogować się do portalu. (266)",
        },
        "pt": {
            "title": "Não é possível iniciar: problema com a subscrição iRobot Select",
            "content": "Visite o seu Portal de Membros para atualizar o método de pagamento e verificar o estado da subscrição. Toque abaixo para iniciar sessão no portal. (266)",
        },
    },
    268: {
        "de": {
            "title": "Start nicht möglich: Karte wird gespeichert",
            "content": "Reinigung wird in Kürze verfügbar sein. (268)",
        },
        "en": {
            "title": "Unable to start: saving map",
            "content": "Cleaning will be available shortly. (268)",
        },
        "es": {
            "title": "No se puede iniciar: guardando mapa",
            "content": "La limpieza estará disponible en breve. (268)",
        },
        "fr": {
            "title": "Impossible de démarrer : sauvegarde de la carte",
            "content": "Le nettoyage sera bientôt disponible. (268)",
        },
        "it": {
            "title": "Impossibile avviare: salvataggio mappa",
            "content": "La pulizia sarà di nuovo disponibile a breve. (268)",
        },
        "nl": {
            "title": "Kan niet starten: kaart opslaan",
            "content": "Schoonmaken is binnenkort beschikbaar. (268)",
        },
        "pl": {
            "title": "Nie można rozpocząć: zapisywanie mapy",
            "content": "Sprzątanie będzie wkrótce dostępne. (268)",
        },
        "pt": {
            "title": "Não é possível iniciar: guardar mapa",
            "content": "A limpeza estará disponível em breve. (268)",
        },
    },
    283: {
        "de": {
            "title": "Lasersensor-Problem",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Entfernen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (283)",
        },
        "en": {
            "title": "Laser sensor issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (283)",
        },
        "es": {
            "title": "Problema del sensor láser",
            "content": "Reinicia @val para solucionar el error. Retíralo de la base y mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (283)",
        },
        "fr": {
            "title": "Problème de capteur laser",
            "content": "Redémarrez @val pour effacer l’erreur. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. Puis maintenez-le enfoncé pendant 3s. (283)",
        },
        "it": {
            "title": "Problema al sensore laser",
            "content": "Riavviare @val per risolvere l'errore. Rimuovere dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3s. (283)",
        },
        "nl": {
            "title": "Probleem met lasersensor",
            "content": "Start @val opnieuw op om de fout te wissen. Verwijder het van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3s ingedrukt. (283)",
        },
        "pl": {
            "title": "Problem z czujnikiem laserowym",
            "content": "Uruchom ponownie robota @val w celu usunięcia błędu. Wyjmij ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3s. (283)",
        },
        "pt": {
            "title": "Problema no sensor laser",
            "content": "Reinicie @val para corrigir o erro. Retire da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3s. (283)",
        },
    },
    284: {
        "de": {
            "title": "Inkompatible Karte",
            "content": 'Bitte löschen Sie die aktuelle Karte von @val und senden Sie den Roboter los, um über die Registerkarte "Mein Zuhause" eine neue Karte zu erstellen. (284)',
        },
        "en": {
            "title": "Map Incompatible",
            "content": "Please delete\xa0@val's current map and send it to create a new map from the My Home tab. (284)",
        },
        "es": {
            "title": "Mapa incompatible",
            "content": "Elimina el mapa actual de @val y envíalo a crear uno nuevo desde la pestaña Mi casa. (284)",
        },
        "fr": {
            "title": "Carte incompatible",
            "content": "Veuillez supprimer la carte actuelle de @val et ordonnez-lui de créer une nouvelle carte à partir de l’onglet Mon domicile. (284)",
        },
        "it": {
            "title": "Mappa incompatibile",
            "content": "Eliminare la mappa attuale di @val e avviarlo per creare una nuova mappa dalla scheda La mia casa. (284)",
        },
        "nl": {
            "title": "Incompatibele kaart",
            "content": "Verwijder de huidige kaart van @val en stuur hem opnieuw in om een nieuwe kaart te maken vanaf het tabblad My Home. (284)",
        },
        "pl": {
            "title": "Niekompatybilna mapa",
            "content": "Usuń obecną mapę robota @val i wyślij go, aby utworzył nową mapę w zakładce Mój dom. (284)",
        },
        "pt": {
            "title": "Mapa incompatível",
            "content": "Elimine o mapa atual de @val e envie-o para criar um novo mapa a partir do separador A minha casa. (284)",
        },
    },
    285: {
        "de": {
            "title": "Start nicht möglich: Wassertank des Roboters wird gerade entleert",
            "content": "Bitte warten Sie, bis @val die Entleerung des Wassertanks abgeschlossen hat, bevor Sie eine neue Routine starten. (285)",
        },
        "en": {
            "title": "Unable to start: robot water tank is currently draining",
            "content": "Please wait until\xa0@val\xa0finishes draining its water tank before beginning a new routine. (285)",
        },
        "es": {
            "title": "No se puede iniciar: el tanque de agua del robot se está vaciando",
            "content": "Espera a que @val termine de vaciar el tanque de agua antes de empezar una rutina nueva. (285)",
        },
        "fr": {
            "title": "Impossible de démarrer : le réservoir d’eau du robot est en cours de vidange",
            "content": "Veuillez attendre que @val termine de vidanger son réservoir d’eau avant de commencer une nouvelle routine. (285)",
        },
        "it": {
            "title": "Impossibile avviare: il serbatoio dell'acqua del robot si sta svuotando",
            "content": "Attendere che @val finisca di svuotare il serbatoio dell'acqua prima di iniziare una nuova routine. (285)",
        },
        "nl": {
            "title": "Kan niet starten: het watertankje van de robot wordt momenteel geleegd",
            "content": "Wacht tot @val klaar is met het legen van het waterreservoir voordat u een nieuwe routine begint. (285)",
        },
        "pl": {
            "title": "Nie można rozpocząć: obecnie trwa opróżnianie zbiornika na wodę robota",
            "content": "Zanim włączysz nową rutynę, poczekaj, aż robot @val zakończy opróżnianie zbiornika na wodę. (285)",
        },
        "pt": {
            "title": "Não é possível iniciar: o depósito de água do robô está a drenar",
            "content": "Aguarde até @val terminar de drenar o depósito de água antes de iniciar uma nova rotina. (285)",
        },
    },
    286: {
        "de": {
            "title": "Bereit zum Reinigen? Stellen Sie sicher, dass sich @val auf dem Boden befindet und einsatzbereit ist",
            "content": "",
        },
        "en": {
            "title": "Ready to clean? Make sure\xa0@val\xa0is on the floor and ready to roll",
            "content": "",
        },
        "es": {
            "title": "¿Listo para limpiar? Asegúrate de que @val esté en el suelo y listo para empezar",
            "content": "",
        },
        "fr": {
            "title": "Prêt à nettoyer ? Assurez-vous que @val est sur le sol et prêt à l’emploi",
            "content": "",
        },
        "it": {
            "title": "Pronto per la pulizia? Assicurarsi che @val sia sul pavimento e pronto per l'uso",
            "content": "",
        },
        "nl": {
            "title": "Klaar om schoon te maken? Zorg ervoor dat @val op de vloer staat en klaar is voor gebruik",
            "content": "",
        },
        "pl": {
            "title": "Gotowy do sprzątania? Upewnij się, że robot @val znajduje się na podłodze i jest gotowy do pracy",
            "content": "",
        },
        "pt": {
            "title": "Pronto para limpar? Certifique-se de que @val está no chão e pronto para funcionar",
            "content": "",
        },
    },
    287: {
        "de": {
            "title": "Saugen nicht möglich: Wischtuchplatte entfernen",
            "content": "Entfernen Sie die Wischtuchplatte von @val, damit der Roboter mit seiner Saugroutine beginnen kann. (287)",
        },
        "en": {
            "title": "Unable to vacuum: remove Pad Plate",
            "content": "Remove\xa0@val’s Pad Plate so it can begin its vacuuming routine. (287)",
        },
        "es": {
            "title": "No se puede aspirar: retira el soporte de la mopa",
            "content": "Retira el soporte de la mopa de @val para que pueda empezar su rutina de aspirado. (287)",
        },
        "fr": {
            "title": "Impossible d’aspirer : retirez le support de lingette",
            "content": "Retirez le support de lingette de @val pour qu’il puisse commencer sa routine d’aspiration. (287)",
        },
        "it": {
            "title": "Impossibile aspirare: rimuovere la piastra del panno",
            "content": "Rimuovere la piastra del panno di @val in modo che possa iniziare la sua routine di aspirazione. (287)",
        },
        "nl": {
            "title": "Kan niet stofzuigen: verwijder de Pad Plate",
            "content": "Verwijder de padplaat van @val zodat de stofzuigroutine kan beginnen. (287)",
        },
        "pl": {
            "title": "Nie można odkurzać: zdejmij płytkę nakładki",
            "content": "Zdejmij płytkę nakładki robota @val, aby mógł on zacząć zaplanowane odkurzanie. (287)",
        },
        "pt": {
            "title": "Não é possível aspirar: remova a placa da mopa",
            "content": "Remova a placa da mopa de @val para que possa iniciar a rotina de aspiração. (287)",
        },
    },
    290: {
        "de": {
            "title": "Wischen kann nicht gestartet werden: Wischtuchplatte anbringen",
            "content": "Befestigen Sie ein Wischtuch an der Wischtuchplatte und bringen Sie die Wischtuchplatte an @val an, damit der Roboter zum Wischen bereit ist. (290)",
        },
        "en": {
            "title": "Unable to start mopping: attach Pad Plate",
            "content": "Attach a Mop Pad to the Pad Plate, and install the Pad Plate onto\xa0@val\xa0so it's ready to mop. (290)",
        },
        "es": {
            "title": "No se ha podido iniciar el fregado: coloca el soporte de la mopa",
            "content": "Para fregar, coloca una mopa en su soporte e instálalo en @val. (290)",
        },
        "fr": {
            "title": "Impossible de commencer le nettoyage à la serpillière : fixez le support de lingette",
            "content": "Fixez une lingette de lavage au support de lingette, puis installez celui-ci sur @val pour qu’il soit prêt à nettoyer à la serpillière. (290)",
        },
        "it": {
            "title": "Impossibile avviare il lavaggio: installare la piastra del panno",
            "content": "Fissare un panno per lavaggio alla piastra del panno e installare la piastra del panno su @val in modo che sia pronto per il lavaggio. (290)",
        },
        "nl": {
            "title": "Kan niet beginnen met dweilen: bevestig de padplaat",
            "content": "Bevestig een dweilpad aan de padplaat en plaats de padplaat op @val zodat deze klaar is om te dweilen. (290)",
        },
        "pl": {
            "title": "Nie można rozpocząć mycia mopem: zamocuj płytkę nakładki",
            "content": "Przymocuj nakładkę mopującą do płytki nakładki i zamontuj płytkę nakładki w robocie @val, aby był gotowy do mycia mopem. (290)",
        },
        "pt": {
            "title": "Não é possível iniciar a lavagem: coloque a placa da mopa",
            "content": "Coloque uma mopa na placa da mopa e instale a placa em @val para que esteja pronto para lavar. (290)",
        },
    },
    350: {
        "de": {
            "title": "Entleerung des Behälters nicht verfügbar: Beutel fehlt",
            "content": "Öffnen Sie den Deckel der Dockingstation und setzen Sie einen neuen Beutel ein, indem Sie die Karte in die Führungsschienen schieben. Setzen Sie den Deckel wieder auf die Dockingstation auf. (350)",
        },
        "en": {
            "title": "Bin empty unavailable: bag missing",
            "content": "Lift Dock Lid and install a new Dust Bag by sliding along the Guide Rails. Place Lid back on Dock. (350)",
        },
        "es": {
            "title": "Vaciado del depósito no disponible: falta la bolsa",
            "content": "Levanta la tapa de la base e instala una bolsa nueva deslizando el cartón por las guías. Vuelve a colocar la tapa en la base. (350)",
        },
        "fr": {
            "title": "Vidage du bac indisponible : sac manquant",
            "content": "Soulevez le couvercle de la station d’accueil et installez un nouveau sac en faisant glisser le carton dans les rails de guidage. Replacez le couvercle sur la station d’accueil. (350)",
        },
        "it": {
            "title": "Svuotamento cestino non disponibile: sacchetto mancante",
            "content": "Sollevare il coperchio della base e installare un nuovo sacchetto facendo scorrere la scheda nelle guide. Riposizionare il coperchio sulla base. (350)",
        },
        "nl": {
            "title": "Opvangbak legen niet beschikbaar: zak ontbreekt",
            "content": "Til het deksel van het basisstation op en installeer een nieuwe zak door de kaart in de geleiderails te schuiven. Plaats het deksel terug op het basisstation. (350)",
        },
        "pl": {
            "title": "Opróżnianie pojemnika niedostępne: brak worka",
            "content": "Podnieś pokrywę stacji dokującej i zainstaluj nowy worek, wsuwając kartę w prowadnice. Umieść pokrywę z powrotem na stacji dokującej. (350)",
        },
        "pt": {
            "title": "Esvaziamento do depósito indisponível: saco em falta",
            "content": "Levante a tampa da base e instale um novo saco deslizando o cartão nas calhas. Volte a colocar a tampa na base. (350)",
        },
    },
    353: {
        "de": {
            "title": "Entleerung des Behälters nicht verfügbar: Beutel voll",
            "content": "Öffnen Sie den Deckel der Dockingstation und entnehmen Sie den vollen Beutel. Setzen Sie einen neuen Beutel ein, indem Sie die Karte in die Führungsschienen schieben. Setzen Sie den Deckel wieder auf die Dockingstation auf. (353)",
        },
        "en": {
            "title": "Bin empty unavailable: bag full",
            "content": "Lift dock lid and remove the full bag. Install a new bag by sliding the card into the guide rails. Place lid back on dock. (353)",
        },
        "es": {
            "title": "Vaciado del depósito no disponible: bolsa llena",
            "content": "Levanta la tapa de la base y retira la bolsa llena. Instala una bolsa nueva deslizando el cartón por las guías. Vuelve a colocar la tapa en la base. (353)",
        },
        "fr": {
            "title": "Vidage du bac indisponible : sac plein",
            "content": "Soulevez le couvercle de la station d’accueil et retirez le sac plein. Installez un nouveau sac en faisant glisser le carton dans les rails de guidage. Replacez le couvercle sur la station d’accueil. (353)",
        },
        "it": {
            "title": "Svuotamento cestino non disponibile: sacchetto pieno",
            "content": "Sollevare il coperchio della base e rimuovere il sacchetto pieno. Installare un nuovo sacchetto facendo scorrere la scheda nelle guide. Riposizionare il coperchio sulla base. (353)",
        },
        "nl": {
            "title": "Opvangbak legen niet beschikbaar: zak vol",
            "content": "Til het deksel van het dock op en verwijder de volle zak. Installeer een nieuwe zak door de kaart in de geleiderails te schuiven. Plaats het deksel terug op het dock. (353)",
        },
        "pl": {
            "title": "Opróżnianie pojemnika niedostępne: pełny worek",
            "content": "Podnieś pokrywę stacji dokującej i wyjmij pełny worek. Zainstaluj nowy worek, wsuwając kartę w prowadnice. Umieść pokrywę z powrotem na stacji dokującej. (353)",
        },
        "pt": {
            "title": "Esvaziamento do depósito indisponível: saco cheio",
            "content": "Levante a tampa da base e remova o saco cheio. Instale um novo saco deslizando o cartão nas calhas. Volte a colocar a tampa na base. (353)",
        },
    },
    360: {
        "de": {
            "title": "@val kann nicht mit der Dockingstation kommunizieren",
            "content": "Zeigen Sie die Schritte zur Fehlerbehebung an, um die Kommunikation wiederherzustellen. (360)",
        },
        "en": {
            "title": "@val\xa0can't communicate with its Dock",
            "content": "View troubleshooting steps to reestablish communication. (360)",
        },
        "es": {
            "title": "@val no puede comunicarse con la base",
            "content": "Consulta los pasos de resolución de problemas para restablecer la comunicación. (360)",
        },
        "fr": {
            "title": "@val ne peut pas communiquer avec sa station d’accueil",
            "content": "Consultez les étapes de dépannage pour rétablir la communication. (360)",
        },
        "it": {
            "title": "@val non riesce a comunicare con la sua base",
            "content": "Visualizzare i passaggi per la risoluzione dei problemi per ripristinare la comunicazione. (360)",
        },
        "nl": {
            "title": "@val kan niet communiceren met het basisstation",
            "content": "Bekijk de stappen voor probleemoplossing om de communicatie te herstellen. (360)",
        },
        "pl": {
            "title": "Robot @val nie może nawiązać połączenia ze stacją dokującą",
            "content": "Wyświetl kroki rozwiązywania problemów, aby przywrócić komunikację. (360)",
        },
        "pt": {
            "title": "@val não consegue comunicar com a base",
            "content": "Consulte os passos de resolução para restabelecer a comunicação. (360)",
        },
    },
    365: {
        "de": {
            "title": "Entleerung des Behälters nicht verfügbar: Bitte warten Sie 10 Minuten",
            "content": "Es ist am besten, den Behälter nicht öfter als einmal innerhalb von 10 Minuten über die App zu entleeren. Dadurch wird der Motor vor Überhitzung geschützt. (365)",
        },
        "en": {
            "title": "Bin empty unavailable: please wait 10 minutes",
            "content": "It’s best not to empty the bin from the app more than once in a 10 minute period. This protects the motor from overheating. (365)",
        },
        "es": {
            "title": "Vaciado del depósito no disponible: espera 10\xa0minutos",
            "content": "Es recomendable no vaciar el depósito desde la app más de una vez en un periodo de 10 minutos. Esto protege el motor frente a sobrecalentamientos. (365)",
        },
        "fr": {
            "title": "Vidage du bac indisponible : veuillez patienter 10 minutes",
            "content": "Il est préférable de ne pas vider le bac depuis l’application plus d’une fois au cours d’une période de 10 minutes. Cela protège le moteur d’une surchauffe. (365)",
        },
        "it": {
            "title": "Svuotamento cestino non disponibile: attendere 10 minuti",
            "content": "Si consiglia di non svuotare il cestino dall'app più di una volta entro un periodo di 10 minuti. Ciò protegge il motore dal surriscaldamento. (365)",
        },
        "nl": {
            "title": "Opvangbak legen niet beschikbaar: wacht 10 minuten",
            "content": "Het is beter om de bak via de app niet vaker dan één keer in een periode van 10 minuten te legen. Dit beschermt de motor tegen oververhitting. (365)",
        },
        "pl": {
            "title": "Opróżnianie pojemnika niedostępne: odczekaj 10\xa0minut",
            "content": "Najlepiej nie opróżniać pojemnika z poziomu aplikacji częściej niż raz na 10\xa0minut. Chroni to silnik przed przegrzaniem. (365)",
        },
        "pt": {
            "title": "Esvaziamento do depósito indisponível: aguarde 10 minutos",
            "content": "Evite esvaziar o depósito a partir da aplicação mais do que uma vez num período de 10 minutos. Isto protege o motor de sobreaquecimento. (365)",
        },
    },
    450: {
        "de": {
            "title": "Dockingstation-Tank fehlt",
            "content": "Installieren Sie den Tank in der Dockingstation, um Wischen und Moppwäsche zu ermöglichen. (450)",
        },
        "en": {
            "title": "Dock tank missing",
            "content": "Install the tank into the dock to enable mopping and mop wash. (450)",
        },
        "es": {
            "title": "Falta el tanque de la base",
            "content": "Instala el tanque en la base para permitir el fregado y el lavado de la mopa. (450)",
        },
        "fr": {
            "title": "Réservoir de la station d’accueil manquant",
            "content": "Installez le réservoir dans la station d’accueil pour activer le nettoyage à la serpillière et le lavage de serpillière. (450)",
        },
        "it": {
            "title": "Serbatoio della base mancante",
            "content": "Installare il serbatoio nella base per abilitare il lavaggio dei pavimenti e del panno. (450)",
        },
        "nl": {
            "title": "Docktank ontbreekt",
            "content": "Installeer de tank in het dock om te kunnen dweilen en de dweil te wassen. (450)",
        },
        "pl": {
            "title": "Brak zbiornika w stacji dokującej",
            "content": "Zainstaluj zbiornik w stacji dokującej, aby umożliwić mycie mopem i mycie mopa. (450)",
        },
        "pt": {
            "title": "Depósito da base em falta",
            "content": "Instale o depósito na base para ativar a lavagem e a limpeza da mopa. (450)",
        },
    },
    451: {
        "de": {
            "title": "Frischwassertankstand niedrig",
            "content": "Füllen Sie den Dockingstation-Tank auf, damit @val mit dem Wischen fortfahren kann. Wenn der Fehler weiterhin besteht, starten Sie @val neu. (451)",
        },
        "en": {
            "title": "Clean Water Tank level low",
            "content": "Refill Clean Water Tank so\xa0@val\xa0can continue mopping. If the error persists, restart\xa0@val. (451)",
        },
        "es": {
            "title": "Nivel bajo del depósito de agua limpia",
            "content": "Llena el tanque de la base para que @val pueda seguir fregando. Si el error persiste, reinicia @val. (451)",
        },
        "fr": {
            "title": "Niveau bas du réservoir d’eau propre",
            "content": "Remplissez le réservoir de la station d’accueil pour que @val puisse continuer à nettoyer à la serpillière. Si l’erreur persiste, redémarrez @val. (451)",
        },
        "it": {
            "title": "Livello basso del serbatoio dell’acqua pulita",
            "content": "Riempire il serbatoio della base in modo che @val possa continuare il lavaggio. Se l'errore persiste, riavviare @val. (451)",
        },
        "nl": {
            "title": "Schoonwatertank bijna leeg",
            "content": "Vul de tank van het basisstation zodat @val verder kan dweilen. Als de fout aanhoudt, start @val dan opnieuw op. (451)",
        },
        "pl": {
            "title": "Niski poziom w zbiorniku na czystą wodę",
            "content": "Napełnij zbiornik na czystą wodę, aby robot @val mógł kontynuować mycie mopem. Jeśli błąd będzie się powtarzał, uruchom ponownie robota @val. (451)",
        },
        "pt": {
            "title": "Nível baixo do depósito de água limpa",
            "content": "Encha o depósito da base para que @val possa continuar a lavagem. Se o erro persistir, reinicie @val. (451)",
        },
    },
    455: {
        "de": {
            "title": "Hardwareproblem mit Dockingstation-Pumpe",
            "content": "Nachfüllen von @val nicht möglich. Saugen ist weiterhin verfügbar, aber die Pumpenhardware muss möglicherweise ausgetauscht werden (Fehler 455)",
        },
        "en": {
            "title": "Dock pump hardware issue",
            "content": "Unable to refill\xa0@val. Vacuuming is still available but your pump hardware may need to be replaced (Error 455)",
        },
        "es": {
            "title": "Problema mecánico en la bomba de la base",
            "content": "No se puede rellenar @val. El aspirado sigue estando disponible, pero es posible que se deba reemplazar la maquinaria de la bomba (Error 455)",
        },
        "fr": {
            "title": "Problème matériel de la pompe de la station d’accueil",
            "content": "Impossible de remplir @val. L’aspiration est toujours disponible, mais le matériel de votre pompe doit peut-être être remplacé (Erreur 455)",
        },
        "it": {
            "title": "Problema hardware della pompa della base",
            "content": "Impossibile riempire @val. L'aspirazione è ancora disponibile ma potrebbe essere necessario sostituire l'hardware della pompa (Errore 455)",
        },
        "nl": {
            "title": "Hardwareprobleem met de dockpomp",
            "content": "Kan @val niet bijvullen. Stofzuigen is nog steeds beschikbaar, maar uw pomphardware moet mogelijk worden vervangen (fout 455)",
        },
        "pl": {
            "title": "Problem sprzętowy z pompą stacji dokującej",
            "content": "Nie można napełnić robota @val. Odkurzanie jest nadal dostępne, ale pompa może wymagać wymiany (błąd 455)",
        },
        "pt": {
            "title": "Problema de hardware da bomba da base",
            "content": "Não é possível reabastecer @val. A aspiração continua disponível, mas o hardware da bomba pode precisar de ser substituído (Erro 455)",
        },
    },
    457: {
        "de": {
            "title": "Kommunikationsproblem mit der Dockingstation",
            "content": "Nachfüllen von @val nicht möglich. Stecken Sie die Dockingstation vom Stromnetz aus und reinigen Sie die Ladekontakte an Roboter und Dockingstation mit einem feuchten Schmutzradierer. (457)",
        },
        "en": {
            "title": "Dock communication issue",
            "content": "Unable to refill\xa0@val. Unplug dock and use a damp melamine sponge to scrub charging contacts on robot and dock. (457)",
        },
        "es": {
            "title": "Problema de comunicación con la base",
            "content": "No se puede rellenar @val. Desenchufa la base y utiliza una esponja de melamina húmeda para limpiar los contactos de carga del robot y de la base. (457)",
        },
        "fr": {
            "title": "Problème de communication avec la station d’accueil",
            "content": "Impossible de remplir @val. Débranchez la station d’accueil et utilisez une éponge en mélamine légèrement humide pour essuyer les contacts de chargement du robot et de la station d’accueil. (457)",
        },
        "it": {
            "title": "Problema di comunicazione della base",
            "content": "Impossibile riempire @val. Scollegare la base e usare una spugna melaminica inumidita per strofinare i contatti di ricarica sul robot e sulla base. (457)",
        },
        "nl": {
            "title": "Communicatieprobleem met dock",
            "content": "Kan @val niet bijvullen. Haal de stekker van het dock uit het stopcontact en gebruik een vochtige melaminespons om de oplaadcontacten op de robot en het dock schoon te schrobben. (457)",
        },
        "pl": {
            "title": "Problem z komunikacją ze stacją dokującą",
            "content": "Nie można napełnić robota @val. Odłącz stację dokującą i użyj wilgotnej gąbki z melaminy, aby wyczyścić styki ładowania na robocie i stacji dokującej. (457)",
        },
        "pt": {
            "title": "Problema de comunicação da base",
            "content": "Não é possível reabastecer @val. Desligue a base e utilize uma esponja de melamina húmida para limpar os contactos de carregamento no robô e na base. (457)",
        },
    },
    464: {
        "de": {
            "title": "Reinigungsmitteltank der Dockingstation leer",
            "content": "Befüllen Sie den Reinigungsmitteltank mit dem StayClean™ Wischkonzentrat, damit es beim Wischen automatisch dosiert werden kann. Oder schalten Sie die Funktion in den Robotereinstellungen aus. (464)",
        },
        "en": {
            "title": "Dock Detergent tank empty",
            "content": "Fill detergent tank with StayClean™ Mopping Concentrate so it can auto-dispense during mopping. Or turn off feature in Robot Settings. (464)",
        },
        "es": {
            "title": "Tanque de detergente de la base vacío",
            "content": "Llena el tanque de detergente con el concentrado para fregar StayClean™ para que pueda dispensarse automáticamente durante el fregado. También puedes desactivar la función en Configuración del robot. (464)",
        },
        "fr": {
            "title": "Réservoir de détergent de la station d’accueil vide",
            "content": "Remplissez le réservoir de détergent avec le concentré de nettoyage à la serpillière StayClean™ afin qu’il soit distribué automatiquement pendant le nettoyage à la serpillière. Ou désactivez la fonctionnalité dans les paramètres du robot. (464)",
        },
        "it": {
            "title": "Il serbatoio del detergente della base è vuoto",
            "content": "Riempire il serbatoio del detergente con StayClean™ Mopping Concentrate per consentirne l'erogazione automatica durante il lavaggio. Oppure disattiva la funzione in Impostazioni robot. (464)",
        },
        "nl": {
            "title": "Reinigingsmiddeltank dock leeg",
            "content": "Vul de reinigingsmiddeltank met StayClean™ Mopping Concentrate zodat deze automatisch kan worden toegediend tijdens het dweilen. Of schakel de functie uit in de robotinstellingen. (464)",
        },
        "pl": {
            "title": "Zbiornik na detergent w stacji dokującej jest pusty",
            "content": "Napełnij zbiornik na detergent koncentratem do mycia mopem StayClean™, aby mógł być automatycznie dozowany podczas mycia mopem. Można też wyłączyć tę funkcję w Ustawieniach robota. (464)",
        },
        "pt": {
            "title": "Depósito de detergente da base vazio",
            "content": "Encha o depósito de detergente com StayClean™ Mopping Concentrate para distribuição automática durante a lavagem. Ou desative a funcionalidade nas Definições do Robô. (464)",
        },
    },
    510: {
        "de": {
            "title": "Dockingstation-Update läuft",
            "content": "Bitte warten Sie vor der Reinigung, bis das Update abgeschlossen ist. Dies sollte weniger als 20 Minuten dauern. (510)",
        },
        "en": {
            "title": "Dock update in progress",
            "content": "Please wait for update to complete before cleaning. This should take under 20 minutes. (510)",
        },
        "es": {
            "title": "Actualización de la base en curso",
            "content": "Espera a que se complete la actualización antes de limpiar. Debería tardar menos de 20\xa0minutos. (510)",
        },
        "fr": {
            "title": "Mise à jour de la station d’accueil en cours",
            "content": "Veuillez patienter jusqu’à la fin de la mise à jour avant de procéder au nettoyage. Cela devrait prendre moins de 20 minutes. (510)",
        },
        "it": {
            "title": "Aggiornamento della base in corso",
            "content": "Attendere il completamento dell'aggiornamento prima di eseguire la pulizia. Dovrebbe richiedere meno di 20 minuti. (510)",
        },
        "nl": {
            "title": "Dock-update in uitvoering",
            "content": "Wacht tot de update is voltooid voordat u gaat schoonmaken. Dit zou minder dan 20 minuten moeten duren. (510)",
        },
        "pl": {
            "title": "Trwa aktualizacja stacji dokującej",
            "content": "Przed rozpoczęciem sprzątania poczekaj na zakończenie aktualizacji. Powinno to potrwać mniej niż 20\xa0minut. (510)",
        },
        "pt": {
            "title": "Atualização da base em curso",
            "content": "Aguarde que a atualização termine antes de iniciar a limpeza. Isto deve demorar menos de 20 minutos. (510)",
        },
    },
    513: {
        "de": {
            "title": "Wischen und Moppwäsche nicht verfügbar: Pumpenproblem",
            "content": "Schließen Sie die Dockingstation erneut an",
        },
        "en": {
            "title": "Mopping and mop wash unavailable: pump issue",
            "content": "Replug Dock to restart and enable Mopping and Mop Wash. (513)",
        },
        "es": {
            "title": "Fregado y lavado de mopa no disponibles: problema con la bomba",
            "content": "Vuelve a enchufar la base para reiniciarla y activar el fregado y el lavado de la mopa. (513)",
        },
        "fr": {
            "title": "Nettoyage à la serpillière et lavage de serpillière indisponibles : problème de pompe",
            "content": "Rebranchez la station d’accueil pour la redémarrer et activer le nettoyage à la serpillière et le lavage de la serpillière. (513)",
        },
        "it": {
            "title": "Lavaggio pavimento e lavaggio panno non disponibili: problema alla pompa",
            "content": "Ricollega la base per riavviarla e abilitare il lavaggio e il lavaggio del mop. (513)",
        },
        "nl": {
            "title": "Dweilen en dweilwassen niet beschikbaar: pompprobleem",
            "content": "Sluit het basisstation opnieuw aan om opnieuw te starten en dweilen en mop wassen in te schakelen. (513)",
        },
        "pl": {
            "title": "Mycie mopem i mycie mopa niedostępne: problem z pompą",
            "content": "Podłącz ponownie stację dokującą, aby ją zrestartować i włączyć mopowanie oraz mycie mopa. (513)",
        },
        "pt": {
            "title": "Lavagem e limpeza da mopa indisponíveis: problema na bomba",
            "content": "Volte a ligar a base para reiniciar e ativar a lavagem do chão e a lavagem da esfregona. (513)",
        },
    },
    517: {
        "de": {
            "title": "Problem mit Moppwäsche: Schmutzwasserbehälter und Dockingstation reinigen",
            "content": "Reinigen Sie den Schmutzwasserbehälter von @val mit milder Seife und prüfen Sie ihn auf Verstopfungen. Wischen Sie das Mopp-Reinigungsbecken und die Kanalbelüftung der Dockingstation mit einem sauberen, trockenen Tuch ab (517)",
        },
        "en": {
            "title": "Mop wash issue: Clean dirty water tank and dock",
            "content": "Clean\xa0@val's Dirty Water Tank with mild soap and check for clogs. Wipe the Dock's Mop Wash Tray and Air Duct Vent with a clean, dry cloth (517)",
        },
        "es": {
            "title": "Problema de lavado de mopa: Limpia el depósito de agua sucia y la base",
            "content": "Limpia el depósito de agua sucia de @val con un jabón suave y comprueba que no haya obstrucciones. Limpia la cubeta de lavado de la mopa y el conducto de ventilación de la base con un paño limpio y seco (517)",
        },
        "fr": {
            "title": "Problème de lavage de serpillière : Nettoyez le bac d’eau sale et la station d’accueil",
            "content": "Nettoyez le bac d’eau sale de @val avec un savon doux et vérifiez s’il y a des obstructions. Essuyez le bac de lavage de serpillière de la station d’accueil et l’ouverture du conduit d’aspiration avec un chiffon propre et sec (517)",
        },
        "it": {
            "title": "Problema con il lavaggio del panno: Pulire il serbatoio dell'acqua sporca e la base",
            "content": "Pulire il serbatoio dell'acqua sporca di @val con un sapone neutro e controllare se ci sono ostruzioni. Pulire la vaschetta per il lavaggio del panno della base e la presa d'aria con un panno pulito e asciutto (517)",
        },
        "nl": {
            "title": "Probleem met dweilwassen: Reinig de opvangbak voor vuil water en het basisstation",
            "content": "Maak de opvangbak voor vuil water van @val schoon met milde zeep en controleer op verstoppingen. Veeg de dweilwaskom en het luchtkanaal van het basisstation schoon met een schone, droge doek (517)",
        },
        "pl": {
            "title": "Problem z myciem mopa: Wyczyść zbiornik na brudną wodę i stację dokującą",
            "content": "Wyczyść zbiornik na brudną wodę robota @val łagodnym mydłem i sprawdź, czy brak zatorów. Przetrzyj czystą, suchą szmatką nieckę mycia mopa w stacji dokującej oraz otwór wentylacyjny (517)",
        },
        "pt": {
            "title": "Problema de lavagem da mopa: Limpe o depósito de água suja e a base",
            "content": "Lave o depósito de água suja de @val com sabão neutro e verifique se existem obstruções. Limpe o recipiente de lavagem da mopa da base e a ventilação com um pano limpo e seco (517)",
        },
    },
    520: {
        "de": {
            "title": "@val kann nicht mit der Dockingstation kommunizieren",
            "content": "Reinigen Sie die IR-Fenster an @val und der Dockingstation mit einem sauberen, trockenen Tuch. (520)",
        },
        "en": {
            "title": "@val\xa0can't communicate with its Dock",
            "content": "Clean the IR windows on\xa0@val\xa0and the dock with a clean, dry cloth. (520)",
        },
        "es": {
            "title": "@val no puede comunicarse con la base",
            "content": "Limpia las ventanas de infrarrojos de @val y la base con un paño limpio y seco. (520)",
        },
        "fr": {
            "title": "@val ne peut pas communiquer avec sa station d’accueil",
            "content": "Nettoyez les fenêtres IR de @val et de la station d’accueil avec un chiffon propre et sec. (520)",
        },
        "it": {
            "title": "@val non riesce a comunicare con la sua base",
            "content": "Pulire le finestre a infrarossi su @val e sulla base con un panno pulito e asciutto. (520)",
        },
        "nl": {
            "title": "@val kan niet communiceren met het basisstation",
            "content": "Maak de IR-vensters op @val en het dock schoon met een schone, droge doek. (520)",
        },
        "pl": {
            "title": "Robot @val nie może nawiązać połączenia ze stacją dokującą",
            "content": "Wyczyść okienka podczerwieni na robocie @val i stacji dokującej czystą, suchą szmatką. (520)",
        },
        "pt": {
            "title": "@val não consegue comunicar com a base",
            "content": "Limpe as janelas IR em @val e na base com um pano limpo e seco. (520)",
        },
    },
    653: {
        "de": {
            "title": "Schmutzwassertank fehlt",
            "content": "Setzen Sie den Schmutzwassertank wieder ein, um Wischen und Moppwäsche zu ermöglichen. (653)",
        },
        "en": {
            "title": "Dirty water tank missing",
            "content": "Reinstall dirty water tank to enable mopping and mop wash. (653)",
        },
        "es": {
            "title": "Falta el tanque de agua sucia",
            "content": "Vuelve a instalar el tanque de agua sucia para permitir el fregado y el lavado de la mopa. (653)",
        },
        "fr": {
            "title": "Réservoir d’eau sale manquant",
            "content": "Réinstallez le réservoir d’eau sale pour activer le nettoyage à la serpillière et le lavage de serpillière. (653)",
        },
        "it": {
            "title": "Serbatoio dell'acqua sporca mancante",
            "content": "Reinstallare il serbatoio dell'acqua sporca per abilitare il lavaggio e la pulizia del panno. (653)",
        },
        "nl": {
            "title": "Vuilwatertank ontbreekt",
            "content": "Installeer de vuilwatertank opnieuw om te kunnen dweilen en de dweil te wassen. (653)",
        },
        "pl": {
            "title": "Brak zbiornika na brudną wodę",
            "content": "Zamontuj ponownie zbiornik na brudną wodę, aby umożliwić mycie mopem i mycie mopa. (653)",
        },
        "pt": {
            "title": "Depósito de água suja em falta",
            "content": "Volte a instalar o depósito de água suja para ativar a lavagem e a limpeza da mopa. (653)",
        },
    },
    654: {
        "de": {
            "title": "Schmutzwassertank voll",
            "content": "Leeren Sie den Schmutzwassertank und setzen Sie ihn wieder ein, um das Wischen und die Moppwäsche zu ermöglichen. (654)",
        },
        "en": {
            "title": "Dirty water tank full",
            "content": "Empty dirty water tank and reinstall to enable mopping and mop wash. (654)",
        },
        "es": {
            "title": "Tanque de agua sucia lleno",
            "content": "Vacía el tanque de agua sucia y vuelve a instalarlo para permitir el fregado y el lavado de la mopa. (654)",
        },
        "fr": {
            "title": "Réservoir d’eau sale plein",
            "content": "Videz le réservoir d’eau sale et réinstallez-le pour activer le nettoyage à la serpillière et le lavage de serpillière. (654)",
        },
        "it": {
            "title": "Serbatoio dell'acqua sporca pieno",
            "content": "Svuotare il serbatoio dell'acqua sporca e reinstallarlo per abilitare il lavaggio e la pulizia del panno. (654)",
        },
        "nl": {
            "title": "Vuilwatertank vol",
            "content": "Leeg de vuilwatertank en plaats deze terug om het dweilen en het wassen van de dweil in te schakelen. (654)",
        },
        "pl": {
            "title": "Zapełniony zbiornik na brudną wodę",
            "content": "Opróżnij zbiornik na brudną wodę i zamontuj go ponownie, aby umożliwić mycie mopem i mycie mopa. (654)",
        },
        "pt": {
            "title": "Depósito de água suja cheio",
            "content": "Esvazie o depósito de água suja e volte a instalar para ativar a lavagem e a limpeza da mopa. (654)",
        },
    },
    660: {
        "de": {
            "title": "Kommunikationsproblem mit der Dockingstation während der Moppwäsche",
            "content": "Stecken Sie die Dockingstation vom Stromnetz aus und reinigen Sie die Ladekontakte an Roboter und Dockingstation mit einem feuchten Schmutzradierer. (660)",
        },
        "en": {
            "title": "Dock communication issue during mop wash",
            "content": "Unplug the Dock, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (660)",
        },
        "es": {
            "title": "Problema de comunicación con la base durante el lavado de la mopa",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un pañuelo ligeramente húmedo. (660)",
        },
        "fr": {
            "title": "Problème de communication avec la station d’accueil pendant le lavage de serpillière",
            "content": "Débranchez la station d’accueil, puis essuyez les contacts de chargement du robot et de la station d’accueil avec un mouchoir légèrement humide. (660)",
        },
        "it": {
            "title": "Problema di comunicazione della base durante la pulizia del panno",
            "content": "Scollegare la base, quindi pulire i contatti di ricarica sul robot e sulla base con un fazzoletto leggermente umido. (660)",
        },
        "nl": {
            "title": "Communicatieprobleem met het dock tijdens het wassen van de dweil",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de oplaadcontacten op de robot en het basisstation schoon met een licht vochtig doekje. (660)",
        },
        "pl": {
            "title": "Problem z komunikacją ze stacją dokującą podczas mycia mopa",
            "content": "Odłącz stację dokującą, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (660)",
        },
        "pt": {
            "title": "Problema de comunicação com a base durante a lavagem da mopa",
            "content": "Desligue a base e limpe os contactos de carregamento no robô e na base com um lenço ligeiramente húmido. (660)",
        },
    },
    668: {
        "de": {
            "title": "Kein Mopp angebracht",
            "content": "Bitte installieren Sie den Mopp oder setzen Sie ihn neu ein, um Wischen und Moppwäsche zu ermöglichen. (668)",
        },
        "en": {
            "title": "No mop attached",
            "content": "Please install or reseat mop to enable mopping and mop wash. (668)",
        },
        "es": {
            "title": "Mopa no instalada",
            "content": "Instala o vuelve a colocar la mopa para permitir el fregado y el lavado de la mopa. (668)",
        },
        "fr": {
            "title": "Aucune serpillière fixée",
            "content": "Veuillez installer ou repositionner la serpillière pour activer le nettoyage à la serpillière et le lavage de serpillière. (668)",
        },
        "it": {
            "title": "Nessun panno di lavaggio inserito",
            "content": "Installare o reinserire il panno per abilitare il lavaggio del pavimento e la pulizia del panno. (668)",
        },
        "nl": {
            "title": "Geen dweil bevestigd",
            "content": "Installeer of plaats de dweil opnieuw om dweilen en dweilwassen in te schakelen. (668)",
        },
        "pl": {
            "title": "Nie podłączono mopa",
            "content": "Zamontuj lub popraw mopa, aby włączyć mycie mopem i mycie mopa. (668)",
        },
        "pt": {
            "title": "Sem mopa instalada",
            "content": "Instale ou reposicione a mopa para ativar a lavagem e a limpeza da mopa. (668)",
        },
    },
    669: {
        "de": {
            "title": "Mopp hat sich während der Moppwäsche verklemmt",
            "content": "Prüfen Sie den Mopp auf Blockierungen und starten Sie den Roboter neu. Nehmen Sie den Roboter aus der Dockingstation und drücken Sie den Netzschalter 10 Sekunden lang, um ihn auszuschalten. Drücken Sie ihn dann erneut 3 Sekunden lang, um ihn einzuschalten. (669)",
        },
        "en": {
            "title": "Mop got stuck during mop wash",
            "content": "Check Mop for obstructions and restart the Robot. Move the Robot out of the Dock and press the power button for 10 seconds to turn it off, then press again for 3 seconds to turn it on. (669)",
        },
        "es": {
            "title": "La mopa se ha atascado durante el lavado de la mopa",
            "content": "Comprueba si la mopa está obstruida y reinicia el robot. Saca el robot de la base y mantén pulsado el botón de encendido durante 10 segundos para apagarlo. Luego vuelve a pulsarlo durante 3 segundos para encenderlo. (669)",
        },
        "fr": {
            "title": "La serpillière s’est bloquée pendant le lavage de serpillière",
            "content": "Vérifiez que la serpillière n’est pas bloquée et redémarrez le robot. Sortez le robot de la station d’accueil, appuyez sur le bouton d’alimentation pendant 10 secondes pour l’éteindre, puis appuyez à nouveau pendant 3 secondes pour le rallumer. (669)",
        },
        "it": {
            "title": "Il panno si è bloccato durante la pulizia del panno",
            "content": "Controlla che il panno non sia ostruito e riavvia il robot. Sposta il robot fuori dalla base e premi il pulsante di accensione per 10 secondi per spegnerlo, quindi premilo di nuovo per 3 secondi per accenderlo. (669)",
        },
        "nl": {
            "title": "Dweil is vastgelopen tijdens het wassen van de dweil",
            "content": "Controleer de Mop op verstoppingen en start de Robot opnieuw. Haal de Robot uit de Dock en druk 10 seconden op de aan/uit-knop om hem uit te schakelen. Druk daarna opnieuw 3 seconden om hem in te schakelen. (669)",
        },
        "pl": {
            "title": "Mop zablokował się podczas mycia mopa",
            "content": "Sprawdź, czy mop nie jest zablokowany, i uruchom robota ponownie. Wyjmij robota ze stacji dokującej i naciśnij przycisk zasilania na 10 sekund, aby go wyłączyć, a następnie ponownie naciśnij przez 3 sekund, aby go włączyć. (669)",
        },
        "pt": {
            "title": "A mopa ficou presa durante a lavagem",
            "content": "Verifique se a mopa está obstruída e reinicie o Robot. Retire o Robot da Dock e prima o botão de alimentação durante 10 segundos para o desligar. Depois, prima novamente durante 3 segundos para o ligar. (669)",
        },
    },
    670: {
        "de": {
            "title": "Mopp-Reinigungsbecken benötigt Aufmerksamkeit",
            "content": "Stellen Sie sicher, dass das Mopp-Reinigungsbecken der Dockingstation und der Filter ordnungsgemäß installiert sind, um Wischen und Wischtuch-Wäsche zu ermöglichen. (670)",
        },
        "en": {
            "title": "Mop wash basin needs attention",
            "content": "Make sure the Dock's Mop Cleaning Tray and Filter are properly installed to enable Mopping and Mop Wash. (670)",
        },
        "es": {
            "title": "La cubeta de lavado de la mopa requiere atención",
            "content": "Asegúrate de que la cubeta de lavado de la mopa y el filtro de la base estén instalados correctamente para permitir el fregado y el lavado de la mopa. (670)",
        },
        "fr": {
            "title": "Le bac de lavage de serpillière nécessite une intervention",
            "content": "Assurez-vous que le bac de lavage de serpillière de la station d’accueil et le filtre sont correctement installés pour activer le nettoyage à la serpillière et le lavage de lingette. (670)",
        },
        "it": {
            "title": "La vaschetta di lavaggio del panno richiede attenzione",
            "content": "Assicurarsi che la vaschetta di lavaggio del panno della base e il filtro siano installati correttamente per abilitare il lavaggio del pavimento e il lavaggio del panno. (670)",
        },
        "nl": {
            "title": "De dweilwasbak heeft aandacht nodig",
            "content": "Zorg ervoor dat de wasbak en het filter van het basisstation goed zijn geïnstalleerd om dweilen en het wassen van de dweil mogelijk te maken. (670)",
        },
        "pl": {
            "title": "Niecka mycia mopa wymaga uwagi",
            "content": "Upewnij się, że niecka mycia mopa oraz filtr są prawidłowo zamontowane, aby umożliwić mycie mopem i mycie nakładki. (670)",
        },
        "pt": {
            "title": "O recipiente de lavagem da mopa precisa de atenção",
            "content": "Certifique-se de que o recipiente de lavagem da mopa da base e o filtro estão corretamente instalados para ativar a lavagem e limpeza da mopa. (670)",
        },
    },
    671: {
        "de": {
            "title": "Dockingstation-Tank ist leer oder nicht installiert",
            "content": "Bitte füllen Sie den Dockingstation-Tank auf und installieren Sie ihn, um Wischen und Moppwäsche zu ermöglichen. (671)",
        },
        "en": {
            "title": "Clean Water Tank empty or not installed",
            "content": "Fill up and install the clean water tank to enable mopping and mop wash. (671)",
        },
        "es": {
            "title": "El tanque de la base está vacío o no está instalado",
            "content": "Rellena e instala el tanque de la base para permitir el fregado y el lavado de la mopa. (671)",
        },
        "fr": {
            "title": "Le réservoir de la station d’accueil est vide ou n’est pas installé",
            "content": "Veuillez remplir et installer le réservoir de la station d’accueil pour activer le nettoyage à la serpillière et le lavage de serpillière. (671)",
        },
        "it": {
            "title": "Serbatoio della base vuoto o non installato",
            "content": "Riempire e installare il serbatoio della base per abilitare il lavaggio del pavimento e la pulizia del panno. (671)",
        },
        "nl": {
            "title": "Tank van het basisstation is leeg of niet geïnstalleerd",
            "content": "Vul de tank van het basisstation bij en installeer deze om te kunnen dweilen en de dweil te wassen. (671)",
        },
        "pl": {
            "title": "Zbiornik na czystą wodę jest pusty lub nie został zamontowany",
            "content": "Napełnij zbiornik i zamontuj go w stacji dokującej, aby umożliwić mycie mopem i mycie mopa. (671)",
        },
        "pt": {
            "title": "O depósito da base está vazio ou não instalado",
            "content": "Encha e instale o depósito da base para ativar a lavagem e a limpeza da mopa. (671)",
        },
    },
    672: {
        "de": {
            "title": "Schmutzwassertank ist voll oder nicht installiert",
            "content": "Bitte leeren und installieren Sie den Schmutzwassertank der Dockingstation, um das Wischen und die Moppwäsche zu ermöglichen. (672)",
        },
        "en": {
            "title": "Dirty water tank is full or not installed",
            "content": "Empty and install the Dock's Dirty Water Tank to enable Mopping and Mop Wash. (672)",
        },
        "es": {
            "title": "Tanque de agua sucia lleno o no instalado",
            "content": "Vacía e instala el tanque de agua sucia de la base para permitir el fregado y el lavado de la mopa. (672)",
        },
        "fr": {
            "title": "Le réservoir d’eau sale est plein ou non installé",
            "content": "Veuillez vider et installer le réservoir d’eau sale de la station d’accueil pour activer le nettoyage à la serpillière et le lavage de serpillière. (672)",
        },
        "it": {
            "title": "Il serbatoio dell'acqua sporca è pieno o non installato",
            "content": "Per consentire il lavaggio del pavimento e la pulizia del panno, svuotare e installare il serbatoio dell'acqua sporca della base. (672)",
        },
        "nl": {
            "title": "Vuilwatertank is vol of niet geïnstalleerd",
            "content": "Leeg de vuilwatertank van het basisstation en plaats deze terug om te kunnen dweilen en de dweil te wassen. (672)",
        },
        "pl": {
            "title": "Zbiornik na brudną wodę jest pełny lub niezamontowany",
            "content": "Opróżnij i zamontuj zbiornik na brudną wodę w stacji dokującej, aby umożliwić mycie mopem i mycie mopa. (672)",
        },
        "pt": {
            "title": "O depósito de água suja está cheio ou não instalado",
            "content": "Esvazie e instale o depósito de água suja da base para ativar a lavagem e a limpeza da mopa. (672)",
        },
    },
    751: {
        "de": {
            "title": "Mopptrocknung nicht verfügbar: Gebläseproblem",
            "content": "Stecken Sie die Dockingstation aus, warten Sie 30 Sekunden und stecken Sie sie wieder ein. (751)",
        },
        "en": {
            "title": "Mop dry unavailable: blower issue",
            "content": "Unplug the Dock, wait 30s and plug back in. (751)",
        },
        "es": {
            "title": "Secado de la mopa no disponible: problema del ventilador",
            "content": "Desenchufa la base, espera 30\xa0segundos y vuelve a enchufarla. (751)",
        },
        "fr": {
            "title": "Séchage de la serpillière indisponible : problème de soufflerie",
            "content": "Débranchez la station d’accueil, attendez 30 secondes et rebranchez-la. (751)",
        },
        "it": {
            "title": "Asciugatura panno non disponibile: problema alla ventola",
            "content": "Scollegare la stazione di ricarica, attendere 30 secondi e ricollegarla. (751)",
        },
        "nl": {
            "title": "Dweildrogen niet beschikbaar: probleem met ventilator",
            "content": "Haal de stekker van het basisstation uit het stopcontact, wacht 30 seconden en steek deze er weer in. (751)",
        },
        "pl": {
            "title": "Suszenie mopa niedostępne: problem z dmuchawą",
            "content": "Odłącz stację dokującą od zasilania, odczekaj 30\xa0sekund i podłącz ponownie. (751)",
        },
        "pt": {
            "title": "Secagem da mopa indisponível: problema no ventilador",
            "content": "Desligue a base, aguarde 30 segundos e volte a ligar. (751)",
        },
    },
    752: {
        "de": {
            "title": "Mopptrocknung nicht verfügbar: Mopp konnte zum Trocknen nicht angehoben werden",
            "content": "Prüfen Sie den Wischmopp auf Hindernisse und starten Sie den Roboter neu: Nehmen Sie den Roboter von der Dockingstation, halten Sie die Ein-/Aus-Taste 10 s und dann 3s gedrückt. (752)",
        },
        "en": {
            "title": "Mop dry unavailable: mop could not lift to dry",
            "content": "Check Mop for obstructions and restart the Robot: Move the Robot out of the Dock, hold the Power button for 10s then 3s. (752)",
        },
        "es": {
            "title": "Secado de la mopa no disponible: la mopa no se ha podido levantar para secarse",
            "content": "Comprueba si la mopa tiene obstrucciones y reinicia el robot: saca el robot de la base, mantén pulsado el botón de encendido 10 s y luego 3s. (752)",
        },
        "fr": {
            "title": "Séchage de la serpillière indisponible : la serpillière n’a pas pu se soulever pour le séchage",
            "content": "Vérifiez que la serpillière n’est pas obstruée et redémarrez le robot : sortez le robot de la station d’accueil, maintenez le bouton d’alimentation enfoncé 10 s puis 3s. (752)",
        },
        "it": {
            "title": "Asciugatura panno non disponibile: impossibile sollevare il panno per l'asciugatura",
            "content": "Controlla che il mop non sia ostruito e riavvia il robot: sposta il robot fuori dalla base, tieni premuto il pulsante di accensione per 10 s e poi per 3s. (752)",
        },
        "nl": {
            "title": "Dweildrogen niet beschikbaar: dweil kon niet omhoog komen om te drogen",
            "content": "Controleer de mop op obstakels en start de robot opnieuw: haal de robot van het basisstation, houd de aan/uit-knop 10 s en daarna 3s ingedrukt. (752)",
        },
        "pl": {
            "title": "Suszenie mopa niedostępne: nie udało się unieść mopa do osuszenia",
            "content": "Sprawdź, czy mop nie jest zablokowany, i uruchom ponownie robota: Zdejmij robota ze stacji dokującej, przytrzymaj przycisk zasilania przez 10 s, a następnie przez 3s. (752)",
        },
        "pt": {
            "title": "Secagem da mopa indisponível: a mopa não conseguiu levantar para secar",
            "content": "Verifique se existem obstruções na esfregona e reinicie o robô: retire o robô da base, mantenha o botão de alimentação premido por 10 s e depois por 3s. (752)",
        },
    },
    756: {
        "de": {
            "title": "Mopptrocknung nicht verfügbar: Kein Mopp angebracht",
            "content": "Bitte installieren Sie den Mopp oder setzen Sie ihn neu ein. (756)",
        },
        "en": {
            "title": "Mop dry unavailable: no mop attached",
            "content": "Please install or reseat mop. (756)",
        },
        "es": {
            "title": "Secado de la mopa no disponible: mopa no instalada",
            "content": "Instala o vuelve a colocar la mopa. (756)",
        },
        "fr": {
            "title": "Séchage de la serpillière indisponible : aucune serpillière fixée",
            "content": "Veuillez installer ou repositionner la serpillière. (756)",
        },
        "it": {
            "title": "Asciugatura panno non disponibile: nessun panno installato",
            "content": "Installare o riposizionare il panno. (756)",
        },
        "nl": {
            "title": "Dweildrogen niet beschikbaar: geen dweil bevestigd",
            "content": "Installeer de dweil of plaats deze opnieuw. (756)",
        },
        "pl": {
            "title": "Suszenie mopa niedostępne: nie przymocowano mopa",
            "content": "Zamontuj lub popraw mopa. (756)",
        },
        "pt": {
            "title": "Secagem da mopa indisponível: sem mopa instalada",
            "content": "Instale ou reposicione a mopa. (756)",
        },
    },
    757: {
        "de": {
            "title": "Mopptrocknung nicht verfügbar: Kommunikationsproblem mit der Dockingstation",
            "content": "Stecken Sie die Dockingstation vom Stromnetz aus und reinigen Sie die Ladekontakte an Roboter und Dockingstation mit einem feuchten Schmutzradierer. (757)",
        },
        "en": {
            "title": "Mop dry unavailable: dock communication issue",
            "content": "Unplug the Dock, then wipe the Charging Contacts on Robot and Dock with a slightly damp tissue. (757)",
        },
        "es": {
            "title": "Secado de la mopa no disponible: problema de comunicación con la base",
            "content": "Desenchufa la base y limpia los contactos de carga del robot y de la base con un pañuelo ligeramente húmedo. (757)",
        },
        "fr": {
            "title": "Séchage de la serpillière indisponible : problème de communication avec la station d’accueil",
            "content": "Débranchez la station d’accueil, puis essuyez les contacts de chargement du robot et de la station d’accueil avec un mouchoir légèrement humide. (757)",
        },
        "it": {
            "title": "Asciugatura panno non disponibile: problema di comunicazione della base",
            "content": "Scollegare la base, quindi pulire i contatti di ricarica sul robot e sulla base con un fazzoletto leggermente umido. (757)",
        },
        "nl": {
            "title": "Dweildrogen niet beschikbaar: communicatieprobleem met dock",
            "content": "Haal de stekker van het basisstation uit het stopcontact en veeg de oplaadcontacten op de robot en het basisstation schoon met een licht vochtig doekje. (757)",
        },
        "pl": {
            "title": "Suszenie mopa niedostępne: problem z komunikacją ze stacją dokującą",
            "content": "Odłącz stację dokującą, a następnie przetrzyj styki ładowania robota i stacji dokującej lekko wilgotną ściereczką. (757)",
        },
        "pt": {
            "title": "Secagem da mopa indisponível: problema de comunicação da base",
            "content": "Desligue a base e limpe os contactos de carregamento no robô e na base com um lenço ligeiramente húmido. (757)",
        },
    },
    1000: {
        "de": {
            "title": "Linke Seitenbürste klemmt",
            "content": "Ziehen Sie verhedderte Fasern und Schmutz heraus, damit sich die Seitenbürste frei drehen kann. (1000)",
        },
        "en": {
            "title": "Left side brush is stuck",
            "content": "Pull tangled fibers and debris from the side brush can spin freely. (1000)",
        },
        "es": {
            "title": "El cepillo de bordes izquierdo está atascado",
            "content": "Retira las fibras enredadas y los residuos del cepillo de bordes para que pueda girar libremente. (1000)",
        },
        "fr": {
            "title": "La brosse latérale gauche est bloquée",
            "content": "Retirez les fibres et les débris emmêlés de la brosse latérale pour qu’elle puisse tourner librement. (1\xa0000)",
        },
        "it": {
            "title": "La spazzola laterale sinistra è bloccata",
            "content": "Rimuovere le fibre e i detriti aggrovigliati in modo che la spazzola laterale possa girare liberamente. (1000)",
        },
        "nl": {
            "title": "Linkerzijborstel zit vast",
            "content": "Verwijder verwarde vezels en vuil van de zijborstel, zodat deze weer vrij kan draaien. (1000)",
        },
        "pl": {
            "title": "Lewa szczotka boczna jest zablokowana",
            "content": "Usuń splątane włókna i zanieczyszczenia ze szczotki bocznej, aby mogła swobodnie się obracać. (1000)",
        },
        "pt": {
            "title": "A escova lateral esquerda está bloqueada",
            "content": "Remova fibras e resíduos emaranhados para que a escova lateral possa rodar livremente. (1000)",
        },
    },
    1001: {
        "de": {
            "title": "Rechte Seitenbürste klemmt",
            "content": "Ziehen Sie verhedderte Fasern und Schmutz heraus, damit sich die Seitenbürste frei drehen kann. (1001)",
        },
        "en": {
            "title": "Right side brush is stuck",
            "content": "Pull tangled fibers and debris from the side brush can spin freely. (1001)",
        },
        "es": {
            "title": "El cepillo de bordes derecho está atascado",
            "content": "Retira las fibras enredadas y los residuos del cepillo de bordes para que pueda girar libremente. (1001)",
        },
        "fr": {
            "title": "La brosse latérale droite est bloquée",
            "content": "Retirez les fibres et les débris emmêlés de la brosse latérale pour qu’elle puisse tourner librement. (1\xa0001)",
        },
        "it": {
            "title": "La spazzola laterale destra è bloccata",
            "content": "Tirare le fibre e i detriti aggrovigliati in modo che la spazzola laterale possa girare liberamente. (1001)",
        },
        "nl": {
            "title": "Rechterzijborstel zit vast",
            "content": "Verwijder verwarde vezels en vuil van de zijborstel, zodat deze weer vrij kan draaien. (1001)",
        },
        "pl": {
            "title": "Prawa szczotka boczna zablokowana",
            "content": "Usuń splątane włókna i zanieczyszczenia ze szczotki bocznej, aby mogła swobodnie się obracać. (1001)",
        },
        "pt": {
            "title": "A escova lateral direita está bloqueada",
            "content": "Remova fibras e resíduos emaranhados para que a escova lateral possa rodar livremente. (1001)",
        },
    },
    1008: {
        "de": {
            "title": "Motor für Moppanhebung blockiert",
            "content": "Dieser Motor hebt oder senkt die Wischplatte von @val. Prüfen Sie die Umgebung des Wischmopps auf Hindernisse und drücken Sie die Ein-/Aus-Taste",
        },
        "en": {
            "title": "Mop lifting motor stalled",
            "content": "This motor is for\xa0@val\xa0to lift or lower its mop plate. Check for obstructions around mop and press the Power button to resume Routine. (1008)",
        },
        "es": {
            "title": "Motor de elevación de la mopa atascado",
            "content": "Este motor permite a @val subir o bajar la placa de la mopa. Comprueba si hay obstrucciones alrededor de la mopa y pulsa el botón de encendido para reanudar la rutina. (1008)",
        },
        "fr": {
            "title": "Moteur de levage de la serpillière bloqué",
            "content": "Ce moteur permet à @val de soulever ou d’abaisser son support de serpillière. Vérifiez l’absence d’obstructions autour de la serpillière",
        },
        "it": {
            "title": "Motore di sollevamento del panno in stallo",
            "content": "Questo motore consente a @val di sollevare o abbassare la piastra del mop. Verifica che non vi siano ostruzioni intorno al mop e premi il pulsante di accensione per riprendere la routine. (1008)",
        },
        "nl": {
            "title": "Dweilhefmotor vastgelopen",
            "content": "Deze motor laat @val de mopplaat omhoog of omlaag bewegen. Controleer op obstakels rond de mop en druk op de aan/uit-knop om de routine te hervatten. (1008)",
        },
        "pl": {
            "title": "Silnik podnoszenia mopa zablokowany",
            "content": "Ten silnik umożliwia robotowi @val podnoszenie lub opuszczanie płytki mopującej. Sprawdź, czy wokół mopa nie ma przeszkód, i naciśnij przycisk zasilania, aby wznowić rutynę. (1008)",
        },
        "pt": {
            "title": "Motor de elevação da mopa bloqueado",
            "content": "Este motor permite que @val levante ou baixe a placa da esfregona. Verifique se existem obstruções à volta da esfregona e prima o botão de alimentação para retomar a rotina. (1008)",
        },
    },
    1010: {
        "de": {
            "title": "@val konnte nicht zur Dockingstation zurückkehren. Bewegen Sie ihn und stellen Sie ihn zum Laden auf die Dockingstation.",
            "content": "Stellen Sie sicher, dass der Pfad frei ist, damit @val zu seiner Dockingstation zurückkehren kann. Überprüfen Sie, ob die Dockingstation eingesteckt ist und sich an ihrem ursprünglichen Standort befindet. (1010)",
        },
        "en": {
            "title": "@val\xa0couldn't return to Dock. Move and place it on the Dock for charging.",
            "content": "Make sure the path is clear for\xa0@val\xa0to return to its Dock. Check that the dock is plugged in and in its original location. (1010)",
        },
        "es": {
            "title": "@val no ha podido volver a la base. Muévelo y colócalo en la base para cargarlo.",
            "content": "Asegúrate de que no haya obstáculos en el camino de vuelta a la base de @val. Comprueba que la base esté enchufada y en su ubicación original. (1010)",
        },
        "fr": {
            "title": "@val n’a pas pu retourner à la station d’accueil. Déplacez-le et placez-le sur la station d’accueil pour le charger.",
            "content": "Assurez-vous que le chemin est dégagé pour que @val puisse retourner à sa station d’accueil. Vérifiez que la station d’accueil est branchée et qu’elle se trouve à son emplacement d’origine. (1\xa0010)",
        },
        "it": {
            "title": "@val non è riuscito a tornare alla base. Spostalo e posizionalo sulla base per la ricarica.",
            "content": "Assicurarsi che il percorso sia libero affinché @val possa tornare alla sua base. Controllare che la base sia collegata e si trovi nella posizione originale. (1010)",
        },
        "nl": {
            "title": "@val kon niet terugkeren naar het basisstation. Verplaats hem en plaats hem op het basisstation om op te laden.",
            "content": "Zorg ervoor dat het pad vrij is zodat @val kan terugkeren naar het basisstation. Controleer of het dock is aangesloten en op de oorspronkelijke locatie staat. (1010)",
        },
        "pl": {
            "title": "Robot @val nie mógł wrócić do stacji dokującej. Przesuń go i umieść na stacji dokującej w celu ładowania.",
            "content": "Upewnij się, że droga jest wolna, aby robot @val mógł wrócić do stacji dokującej. Sprawdź, czy stacja dokująca jest podłączona do zasilania i znajduje się w swoim pierwotnym miejscu. (1010)",
        },
        "pt": {
            "title": "@val não conseguiu regressar à base. Mova-o e coloque-o na base para carregar.",
            "content": "Certifique-se de que o caminho está livre para @val regressar à base. Verifique se a base está ligada e na sua localização original. (1010)",
        },
    },
    1025: {
        "de": {
            "title": "Lasersensor-Problem",
            "content": "Starten Sie @val neu, um den Fehler zu beheben. Entfernen Sie ihn von der Dockingstation und halten Sie dann die Ein-/Aus-Taste 10 Sekunden lang gedrückt. Halten Sie sie anschließend 3s lang gedrückt. (1025)",
        },
        "en": {
            "title": "Laser sensor issue",
            "content": "Restart\xa0@val\xa0to fix the issue. Move the Robot out of the Dock, hold the Power button for 10s then 3s. (1025)",
        },
        "es": {
            "title": "Problema del sensor láser",
            "content": "Reinicia @val para solucionar el error. Retíralo de la base y mantén pulsado el botón de encendido durante 10\xa0segundos. Luego mantenlo presionado 3s. (1025)",
        },
        "fr": {
            "title": "Problème de capteur laser",
            "content": "Redémarrez @val pour effacer l’erreur. Retirez-le de la station d’accueil, puis maintenez le bouton d’alimentation enfoncé pendant 10 secondes. (1\xa0025) Puis maintenez-le enfoncé pendant 3s.",
        },
        "it": {
            "title": "Problema al sensore laser",
            "content": "Riavviare @val per risolvere l'errore. Rimuovere dalla base, quindi tenere premuto il pulsante di accensione per 10 secondi. Quindi tienilo premuto per 3 s. (1025)",
        },
        "nl": {
            "title": "Probleem met lasersensor",
            "content": "Start @val opnieuw op om de fout te wissen. Verwijder het van het basisstation en houd de aan/uit-knop 10 seconden ingedrukt. Houd deze daarna 3 s ingedrukt. (1025)",
        },
        "pl": {
            "title": "Problem z czujnikiem laserowym",
            "content": "Uruchom ponownie robota @val w celu usunięcia błędu. Wyjmij ze stacji dokującej, a następnie naciśnij i przytrzymaj przycisk zasilania przez 10\xa0sekund. Następnie przytrzymaj przez 3 s. (1025)",
        },
        "pt": {
            "title": "Problema no sensor laser",
            "content": "Reinicie @val para corrigir o erro. Retire da base e depois prima sem soltar o botão de alimentação durante 10 segundos. Em seguida, mantenha premido por 3 s. (1025)",
        },
    },
    1026: {
        "de": {
            "title": "Mopp ist verheddert oder klemmt",
            "content": "Überprüfen Sie den Mopp auf Verhedderungen oder Hindernisse und drücken Sie die Ein-/Aus-Taste, um die Routine fortzusetzen. (1026)",
        },
        "en": {
            "title": "Mop is tangled or stuck",
            "content": "Check mop for tangles or obstructions and press Power button to resume routine. (1026)",
        },
        "es": {
            "title": "La mopa está atascada o enredada",
            "content": "Comprueba si la mopa está atascada u obstruida y pulsa el botón de encendido para reanudar la rutina. (1026)",
        },
        "fr": {
            "title": "La serpillière est emmêlée ou bloquée",
            "content": "Vérifiez que la serpillière n'est pas emmêlée ou bloquée et appuyez sur le bouton d’alimentation pour reprendre la routine. (1\xa0026)",
        },
        "it": {
            "title": "Il panno è aggrovigliato o bloccato",
            "content": "Controllare se il panno presenta grovigli o ostruzioni e premere il pulsante di accensione per riprendere la routine. (1026)",
        },
        "nl": {
            "title": "Dweil is verstrikt of zit vast",
            "content": "Controleer de dweil op klitten of obstakels en druk op de aan-/uitknop om de routine te hervatten. (1026)",
        },
        "pl": {
            "title": "Mop jest splątany lub zablokowany",
            "content": "Sprawdź, czy mop nie jest splątany ani zablokowany, po czym naciśnij przycisk zasilania, aby wznowić rutynę. (1026)",
        },
        "pt": {
            "title": "A mopa está enredada ou bloqueada",
            "content": "Verifique se existem enredos ou obstruções na mopa e prima o botão de alimentação para retomar a rotina. (1026)",
        },
    },
    1027: {
        "de": {
            "title": "Der saubere Wassertank ist nicht eingesetzt oder der Wasserstand ist zu niedrig.",
            "content": "Überprüfen Sie, ob der saubere Wassertank richtig installiert ist und ob er nachgefüllt werden muss.",
        },
        "en": {
            "title": "Clean water tank is not in place or water level is too low",
            "content": "Check whether the clean water tank is properly installed and see if it needs refilling.",
        },
        "es": {
            "title": "El depósito de agua limpia no está colocado o el nivel de agua es demasiado bajo.",
            "content": "Compruebe que el depósito de agua limpia está correctamente instalado y vea si necesita rellenarse.",
        },
        "fr": {
            "title": "Le réservoir d'eau propre n'est pas en place ou le niveau d'eau est trop bas.",
            "content": "Vérifiez que le réservoir d'eau propre est correctement installé et voyez s'il doit être rempli.",
        },
        "it": {
            "title": "Il serbatoio dell'acqua pulita non è in posizione o il livello dell'acqua è troppo basso.",
            "content": "Verificare che il serbatoio dell'acqua pulita sia installato correttamente e vedere se necessita di riempimento.",
        },
        "nl": {
            "title": "De schone watertank is niet op zijn plaats of het waterniveau is te laag.",
            "content": "Controleer of de schone watertank correct is geïnstalleerd en of deze moet worden bijgevuld.",
        },
        "pl": {
            "title": "Zbiornik na czystą wodę nie jest na miejscu lub poziom wody jest zbyt niski.",
            "content": "Sprawdź, czy zbiornik na czystą wodę jest prawidłowo zainstalowany i czy wymaga uzupełnienia.",
        },
        "pt": {
            "title": "O depósito de água limpa não está no lugar ou o nível de água está demasiado baixo.",
            "content": "Verifique se o depósito de água limpa está instalado corretamente e veja se precisa de ser reabastecido.",
        },
    },
    1028: {
        "de": {
            "title": "Schmutzwasserbehälter oder Wischtuch-Waschbecken möglicherweise verstopft",
            "content": "Prüfen Sie den Bereich um die Dockingstation auf Lecks und leeren Sie den Schmutzwasserbehälter des Roboters. Befolgen Sie danach die Schritte zur Fehlerbehebung, um mögliche Verstopfungen zu beseitigen. (1028)",
        },
        "en": {
            "title": "Dirty water tank or washing basin may be clogged.",
            "content": "Check for leaks around the dock and empty the robot dirty water Container. Next, follow steps to troubleshoot and clear any possible clogs. (1028)",
        },
        "es": {
            "title": "El depósito de agua sucia o la cubeta de lavado de la mopa pueden estar obstruidos",
            "content": "Comprueba si hay fugas alrededor de la base y vacía el depósito de agua sucia del robot. A continuación, sigue los pasos de resolución de problemas y retira cualquier posible obstrucción. (1028)",
        },
        "fr": {
            "title": "Le bac d’eau sale ou le bac de lavage de la lingette est peut-être bouché",
            "content": "Vérifiez s’il y a des fuites autour de la station d’accueil et videz le bac d’eau sale du robot. Ensuite, suivez les étapes de dépannage pour éliminer toute obstruction éventuelle. (1\xa0028)",
        },
        "it": {
            "title": "Il serbatoio dell'acqua sporca o la vaschetta di lavaggio del panno potrebbero essere ostruiti",
            "content": "Cercare eventuali perdite intorno alla stazione di ricarica e svuotare il serbatoio dell'acqua sporca del robot. Quindi, seguire i passaggi per risolvere il problema e rimuovere eventuali ostruzioni. (1028)",
        },
        "nl": {
            "title": "Vuilwatertank of wasbak voor pads is mogelijk verstopt",
            "content": "Controleer op lekken rond het basisstation en leeg de vuilwatertank van de robot. Volg daarna de stappen om problemen op te lossen en eventuele verstoppingen te verwijderen. (1028)",
        },
        "pl": {
            "title": "Zbiornik na brudną wodę lub niecka myjąca nakładki mogą być zatkane",
            "content": "Sprawdź, czy wokół stacji dokującej brak wycieków i opróżnij zbiornik na brudną wodę robota. Następnie postępuj zgodnie z instrukcjami, aby rozwiązać problem i usunąć ewentualne zatory. (1028)",
        },
        "pt": {
            "title": "O depósito de água suja ou o recipiente de lavagem pode estar obstruído",
            "content": "Verifique se existem fugas à volta da base e esvazie o depósito de água suja do robô. De seguida, siga os passos para resolver e remover possíveis obstruções. (1028)",
        },
    },
    1029: {
        "de": {
            "title": "Inkompatible Karte",
            "content": 'Bitte löschen Sie die aktuelle Karte von @val und senden Sie den Roboter los, um über die Registerkarte "Mein Zuhause" eine neue Karte zu erstellen. (1029)',
        },
        "en": {
            "title": "Map Incompatible",
            "content": "Please delete\xa0@val's current map and send it to create a new map from the My Home tab. (1029)",
        },
        "es": {
            "title": "Mapa incompatible",
            "content": "Elimina el mapa actual de @val y envíalo a crear uno nuevo desde la pestaña Mi casa. (1029)",
        },
        "fr": {
            "title": "Carte incompatible",
            "content": "Veuillez supprimer la carte actuelle de @val et ordonnez-lui de créer une nouvelle carte à partir de l’onglet Mon domicile. (1\xa0029)",
        },
        "it": {
            "title": "Mappa incompatibile",
            "content": "Eliminare la mappa attuale di @val e creare una nuova mappa dalla scheda La mia casa. (1029)",
        },
        "nl": {
            "title": "Incompatibele kaart",
            "content": "Verwijder de huidige kaart van @val en stuur hem/haar opnieuw in om een nieuwe kaart te maken vanaf het tabblad my home. (1029)",
        },
        "pl": {
            "title": "Niekompatybilna mapa",
            "content": "Usuń obecną mapę robota @val i wyślij go, aby utworzył nową mapę w zakładce Mój dom. (1029)",
        },
        "pt": {
            "title": "Mapa incompatível",
            "content": "Elimine o mapa atual de @val e envie-o para criar um novo mapa a partir do separador A minha casa. (1029)",
        },
    },
    1030: {
        "de": {
            "title": "@val hat sich in einer Nicht-Wischen-Zone festgefahren",
            "content": "Bewegen Sie @val an einen neuen Ort und setzen Sie die Reinigung fort. (1030)",
        },
        "en": {
            "title": "@val\xa0got stuck in a No Mop Zone",
            "content": "Move\xa0@val\xa0to a new location and resume cleaning. (1030)",
        },
        "es": {
            "title": "@val se ha atascado en una zona de no fregado",
            "content": "Mueve @val a una nueva ubicación y reanuda la limpieza. (1030)",
        },
        "fr": {
            "title": "@val est bloqué dans une zone sans nettoyage à la serpillière",
            "content": "Déplacez @val vers un nouvel endroit et reprenez le nettoyage. (1\xa0030)",
        },
        "it": {
            "title": "@val si è bloccato in una Zona di lavaggio vietato",
            "content": "Spostare @val in una nuova posizione e riprendere la pulizia. (1030)",
        },
        "nl": {
            "title": "@val is vastgelopen in een 'Niet-dweilen-zone'",
            "content": "Plaats @val op een nieuwe locatie en hervat de reiniging. (1030)",
        },
        "pl": {
            "title": "Robot @val utknął w strefie bez mopa",
            "content": "Przenieś robota @val w nowe miejsce i wznów sprzątanie. (1030)",
        },
        "pt": {
            "title": "@val ficou preso numa Zona Sem Mopa",
            "content": "Mova @val para uma nova localização e retome a limpeza. (1030)",
        },
    },
    1034: {
        "de": {
            "title": "Wischtuchplatte hat sich gelöst",
            "content": "Bringen Sie die Wischtuchplatte von @val wieder an und drücken Sie die Ein-/Aus-Taste, um das Wischen fortzusetzen. (1034)",
        },
        "en": {
            "title": "Pad Plate came off",
            "content": "Reinstall\xa0@val’s Pad Plate and press the Power button to resume mopping. (1034)",
        },
        "es": {
            "title": "Se ha soltado el soporte de la mopa",
            "content": "Vuelve a instalar el soporte de la mopa de @val y pulsa el botón de encendido para reanudar el fregado. (1034)",
        },
        "fr": {
            "title": "Le support de lingette s’est enlevé",
            "content": "Réinstallez le support de lingette de @val et appuyez sur le bouton d’alimentation pour reprendre le nettoyage à la serpillière. (1\xa0034)",
        },
        "it": {
            "title": "Piastra del panno staccata",
            "content": "Reinstallare la piastra del panno di @val e premere il pulsante di accensione per riprendere il lavaggio. (1034)",
        },
        "nl": {
            "title": "Dweilplaat is losgeraakt",
            "content": "Plaats de dweilplaat van @val terug en druk op de aan/uit-knop om het dweilen te hervatten. (1034)",
        },
        "pl": {
            "title": "Odłączyła się płytka nakładki",
            "content": "Ponownie zamontuj płytkę nakładki robota @val i naciśnij przycisk zasilania, aby wznowić mycie mopem. (1034)",
        },
        "pt": {
            "title": "A placa da mopa soltou-se",
            "content": "Volte a instalar a placa da mopa de @val e prima o botão de alimentação para retomar a lavagem. (1034)",
        },
    },
    3212: {
        "de": {
            "title": "Start nicht möglich: Verbinden Sie Ihr Telefon erneut mit dem Wi-Fi",
            "content": "Vergewissern Sie sich, dass Ihr Telefon mit dem Wi-Fi verbunden ist. Wenn weiterhin Probleme auftreten, stellen Sie die Verbindung über das Mobilfunknetz erneut her. (C210)",
        },
        "en": {
            "title": "Unable to start: Reconnect your phone to Wi-Fi",
            "content": "Check that your phone is connected to Wi-Fi. If you’re still having issues, reconnect using Cellular Data. (C210)",
        },
        "es": {
            "title": "No se puede iniciar: Vuelve a conectar el teléfono al Wi-Fi",
            "content": "Comprueba que tu teléfono esté conectado al Wi-Fi. Si sigues teniendo problemas, vuelve a conectarte usando los datos móviles. (C210)",
        },
        "fr": {
            "title": "Impossible de démarrer : Reconnectez votre téléphone au Wi-Fi",
            "content": "Vérifiez que votre téléphone est connecté au Wi-Fi. Si vous rencontrez toujours des problèmes, reconnectez-vous à l’aide des données cellulaires. (C210)",
        },
        "it": {
            "title": "Impossibile avviare: Riconnettere il telefono alla rete Wi-Fi",
            "content": "Verificare che il telefono sia connesso al Wi-Fi. Se si continua a riscontrare problemi, riconnettersi utilizzando i dati cellulare. (C210)",
        },
        "nl": {
            "title": "Starten mislukt: Verbind je telefoon opnieuw met Wi-Fi",
            "content": "Controleer of je telefoon met Wi-Fi is verbonden. Als je nog steeds problemen ondervindt, maak dan opnieuw verbinding via mobiele data. (C210)",
        },
        "pl": {
            "title": "Nie można rozpocząć: Ponownie podłącz telefon do sieci Wi-Fi",
            "content": "Sprawdź, czy telefon jest podłączony do sieci Wi-Fi. Jeśli nadal występują problemy, połącz ponownie przy użyciu danych komórkowych. (C210)",
        },
        "pt": {
            "title": "Não é possível iniciar: Reconecte o seu telemóvel ao Wi-Fi",
            "content": "Verifique se o seu telemóvel está ligado ao Wi-Fi. Se o problema persistir, reconecte utilizando os Dados Móveis. (C210)",
        },
    },
    3310: {
        "de": {
            "title": "Roboter-Verbindungsfehler",
            "content": 'Tippen Sie auf "So wird\'s gemacht", um in wenigen schnellen Schritten die App-Verbindung wiederherzustellen, damit @val weiter reinigen kann. (C310)',
        },
        "en": {
            "title": "Robot connection abnormal",
            "content": "Tap “Show me how” to follow quick steps to reconnect the app and get\xa0@val\xa0back to cleaning. (C310)",
        },
        "es": {
            "title": "Conexión anómala del robot",
            "content": "Toca “Mostrar cómo” para seguir unos rápidos pasos para volver a conectar la app y que @val vuelva a limpiar. (C310)",
        },
        "fr": {
            "title": "Connexion anormale du robot",
            "content": "Appuyez sur “Montrez-moi comment” pour suivre les étapes rapides afin de reconnecter l’application et de permettre à @val de reprendre le nettoyage. (C310)",
        },
        "it": {
            "title": "Connessione anomala del robot",
            "content": "Toccare “Mostrami come” per seguire dei rapidi passaggi per riconnettere l'app e far riprendere @val a pulire. (C310)",
        },
        "nl": {
            "title": "Afwijkende robotverbinding",
            "content": "Tik op ‘Laat me zien hoe’ om de snelle stappen te volgen om de app opnieuw te verbinden en @val weer te laten schoonmaken. (C310)",
        },
        "pl": {
            "title": "Nieprawidłowe połączenie z robotem",
            "content": "Stuknij przycisk „Pokaż mi jak”, aby wykonać szybkie kroki w celu ponownego podłączenia aplikacji i przywrócenia robota @val do sprzątania. (C310)",
        },
        "pt": {
            "title": "Ligação anómala do robô",
            "content": 'Toque em "Mostrar como" para seguir os passos rápidos e voltar a ligar a aplicação e retomar a limpeza de @val. (C310)',
        },
    },
    4001: {
        "de": {
            "title": "Bei der Aktualisierung von @val ist ein Problem aufgetreten",
            "content": "Lassen Sie @val auf seiner Dockingstation und vergewissern Sie sich, dass eine gute Wi-Fi-Verbindung besteht.\n\nBestimmte Funktionen sind erst nach Abschluss des Updates verfügbar. Wir werden weiterhin im Hintergrund versuchen, das Update durchzuführen. (4001)",
        },
        "en": {
            "title": "@val\xa0is having some trouble updating",
            "content": "Keep\xa0@val\xa0on its dock and make sure you have a good Wi-Fi connection.\nCertain features will not be available until update is complete. We will continue retrying the update in the background. (4001)",
        },
        "es": {
            "title": "@val tiene problemas para actualizarse",
            "content": "Mantén a @val en su base y asegúrate de tener una buena conexión Wi-Fi.\n\nAlgunas funciones no estarán disponibles hasta que se complete la actualización. Seguiremos intentando realizar la actualización en segundo plano. (4001)",
        },
        "fr": {
            "title": "@val rencontre des problèmes de mise à jour",
            "content": "Laissez @val sur sa station d’accueil et assurez-vous de disposer d’une bonne connexion Wi-Fi.\n\nCertaines fonctionnalités ne seront pas disponibles tant que la mise à jour n’est pas terminée. Nous continuerons d’essayer d’effectuer la mise à jour en arrière-plan. (4001)",
        },
        "it": {
            "title": "@val sta riscontrando problemi durante l'aggiornamento",
            "content": "Tenere @val sulla base e assicurarsi di avere una buona connessione Wi-Fi.\n\nAlcune funzioni non saranno disponibili finché l'aggiornamento non sarà completato. Continueremo a ritentare l'aggiornamento in background. (4001)",
        },
        "nl": {
            "title": "@val heeft wat problemen met het updaten",
            "content": "Houd @val op het dock en zorg voor een goede Wi-Fi-verbinding.\n\nBepaalde functies zijn niet beschikbaar totdat de update is voltooid. We blijven de update op de achtergrond opnieuw proberen. (4001)",
        },
        "pl": {
            "title": "Wystąpił problem z aktualizacją robota @val",
            "content": "Pozostaw robota @val w stacji dokującej i upewnij się, że masz dobre połączenie z siecią Wi-Fi.\n\nNiektóre funkcje nie będą dostępne do momentu zakończenia aktualizacji. Będziemy kontynuować próby aktualizacji w tle. (4001)",
        },
        "pt": {
            "title": "@val está com alguns problemas de atualização",
            "content": "Mantenha @val na base e certifique-se de que tem uma boa ligação Wi-Fi.\n\nAlgumas funcionalidades não estarão disponíveis até que a atualização esteja concluída. Continuaremos a tentar atualizar em segundo plano. (4001)",
        },
    },
    4002: {
        "de": {
            "title": "Bei der Aktualisierung von @val ist ein Problem aufgetreten",
            "content": "Vergewissern Sie sich, dass @val bei guter Wi-Fi-Verbindung angedockt ist. Wir versuchen weiterhin, das Update im Hintergrund durchzuführen, und senden eine Benachrichtigung, wenn es fertig ist. (4002)",
        },
        "en": {
            "title": "@val\xa0is having some trouble updating",
            "content": "Make sure\xa0@val\xa0is docked with a good Wi-Fi connection. We'll keep trying the update in the background and send a notification when it's complete. (4002)",
        },
        "es": {
            "title": "@val tiene problemas para actualizarse",
            "content": "Asegúrate de que @val esté en la base y tenga una buena conexión Wi-Fi. Seguiremos intentando realizar la actualización en segundo plano y enviaremos una notificación cuando se haya completado. (4002)",
        },
        "fr": {
            "title": "@val rencontre des problèmes de mise à jour",
            "content": "Assurez-vous que @val est sur sa station d’accueil et dispose d’une bonne connexion Wi-Fi. Nous continuerons d’essayer d’effectuer la mise à jour en arrière-plan et vous enverrons une notification lorsqu’elle sera terminée. (4002)",
        },
        "it": {
            "title": "@val sta riscontrando problemi durante l'aggiornamento",
            "content": "Assicurarsi che @val sia posizionato sulla base con una buona connessione Wi-Fi. Continueremo a provare a eseguire l'aggiornamento in background e invieremo una notifica una volta completato. (4002)",
        },
        "nl": {
            "title": "@val heeft wat problemen met het updaten",
            "content": "Zorg ervoor dat @val op het basisstation staat en een goede Wi-Fi-verbinding heeft. We blijven de update op de achtergrond proberen en sturen een melding wanneer deze voltooid is. (4002)",
        },
        "pl": {
            "title": "Wystąpił problem z aktualizacją robota @val",
            "content": "Upewnij się, że robot @val znajduje się w stacji dokującej i ma dobre połączenie z siecią Wi-Fi. Będziemy nadal próbować przeprowadzić aktualizację w tle i wyślemy powiadomienie, gdy się zakończy. (4002)",
        },
        "pt": {
            "title": "@val está com alguns problemas de atualização",
            "content": "Certifique-se de que @val está na base e ligado a uma rede Wi-Fi com bom sinal. Continuaremos a tentar atualizar em segundo plano e enviar-lhe-emos uma notificação quando estiver concluída. (4002)",
        },
    },
    4003: {
        "de": {
            "title": "Roboter wird aktualisiert",
            "content": "Dies kann bis zu 1 Stunde dauern. Belassen Sie @val auf seiner Dockingstation, bis das Update fertig ist. (4003)",
        },
        "en": {
            "title": "Robot is updating",
            "content": "This can take up to 1h. Keep\xa0@val\xa0on its Dock until update is complete. (4003)",
        },
        "es": {
            "title": "El robot se está actualizando",
            "content": "Este proceso puede tardar hasta 1\xa0hora. Deja @val en su base hasta que se complete la actualización. (4003)",
        },
        "fr": {
            "title": "Le robot est en cours de mise à jour",
            "content": "Cela peut prendre jusqu’à 1 heure. Laissez @val sur sa station d’accueil jusqu’à ce que la mise à jour soit terminée. (4\xa0003)",
        },
        "it": {
            "title": "Il robot è in aggiornamento",
            "content": "Potrebbe richiedere fino a 1 ora. Lasciare @val sulla base fino al completamento dell'aggiornamento. (4003)",
        },
        "nl": {
            "title": "De robot wordt bijgewerkt",
            "content": "Dit kan tot 1 uur duren. Laat @val op het basisstation staan tot de update is voltooid. (4003)",
        },
        "pl": {
            "title": "Robot jest aktualizowany",
            "content": "Może to potrwać maksymalnie godzinę. Pozostaw robota @val w stacji dokującej do zakończenia aktualizacji. (4003)",
        },
        "pt": {
            "title": "O robô está a ser atualizado",
            "content": "Isto pode demorar até 1 hora. Mantenha @val na base até a atualização estar concluída. (4003)",
        },
    },
    4004: {
        "de": {
            "title": "Roboter wird aktualisiert",
            "content": "Dies kann bis zu 1 Stunde dauern. Belassen Sie @val auf seiner Dockingstation, bis das Update fertig ist. (4004)",
        },
        "en": {
            "title": "Robot is updating",
            "content": "This can take up to 1h. Keep\xa0@val\xa0on its Dock until update is complete. (4004)",
        },
        "es": {
            "title": "El robot se está actualizando",
            "content": "Este proceso puede tardar hasta 1\xa0hora. Deja @val en su base hasta que se complete la actualización. (4004)",
        },
        "fr": {
            "title": "Le robot est en cours de mise à jour",
            "content": "Cela peut prendre jusqu’à 1 heure. Laissez @val sur sa station d’accueil jusqu’à ce que la mise à jour soit terminée. (4\xa0004)",
        },
        "it": {
            "title": "Il robot è in aggiornamento",
            "content": "Potrebbe richiedere fino a 1 ora. Lasciare @val sulla base fino al completamento dell'aggiornamento. (4004)",
        },
        "nl": {
            "title": "De robot wordt bijgewerkt",
            "content": "Dit kan tot 1 uur duren. Laat @val op het basisstation staan tot de update is voltooid. (4004)",
        },
        "pl": {
            "title": "Robot jest aktualizowany",
            "content": "Może to potrwać maksymalnie godzinę. Pozostaw robota @val w stacji dokującej do zakończenia aktualizacji. (4004)",
        },
        "pt": {
            "title": "O robô está a ser atualizado",
            "content": "Isto pode demorar até 1 hora. Mantenha @val na base até a atualização estar concluída. (4004)",
        },
    },
}


def vendor_error_text(
    code: int, language: str = "en"
) -> VendorErrorText | None:
    """Return the vendor's wording for a fault code, or None.

    Falls back to English when the language is unavailable, and to ``None``
    when the code is unknown, so a caller never has to guard the lookup.
    """
    texts = VENDOR_ERROR_TEXTS.get(code)
    if texts is None:
        return None
    return texts.get(language) or texts.get("en")
