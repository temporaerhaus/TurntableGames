# TurntableGames

Warum nicht mal ein DJ-Pult als Eingabegerät für eine Spielekonsole nutzen? Das ist die Idee hinter Turntable Games!

Zum aktuellen Zeitpunkt sind DJ-Pong und DJ-Sokoban voll einsatzbereit, der Rest befindet sich noch in der Entwicklung.

Wer eigene Spiele beisteuern möchte, ist herzlich eingeladen, pull requests zu stellen. 

Die Drehbewegungen der beiden großen Räder werden als `control changes` auf der control `22` als Midi-Message gesendet. Umso weiter der Wert von 64 entfernt ist, umso schneller wurde gedreht, kleinere Werte bezeichnen die eine Richtung, größere die andere. Beispiele zum auslesen der Messages sind die Zeilen 64, 79 ff in DJPong/midi_test.py.

Viel Spaß!
