Benötigte Python-Modules:
- python-rtmidi
- mido
- numpy

Starten:
$ python sokoban.py < boards.txt

Steuerung:
- linkes Turntable: links / rechts bewegen
- rechtes Turntable: hoch / runter bewegen
- Pfeile rechts unterhalb der Turntables legen das Verhalten des rechten Turntable fest:
   > drücken für Linksdrehung hoch, Rechtsdrehung runter
   < drücken für Rechtsdrehung hoch, Linksdrehung runter
- OUT für Spiel beenden
- zyklische Pfeile direkt über OUT um aktuelles Level zurückzusetzen
- nach Beenden des letzten Levels wird 5 Sekunden der Game Over Screen angezeigt, danach startet wieder das erste Level
