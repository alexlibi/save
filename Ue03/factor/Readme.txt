A) Allgemeines
--------------

Das Programm "factor" ist ein Konsolenprogramm und stellt eine "Weiterentwicklung" des gleichnamigen Unixkommandos dar. Es basiert auf der freien GNU Multiple Precision Arithmetic Library (GMP) und kann daher beliebig lange Integerzahlen auswerten.

Es werden folgende Verfahren benutzt:
1. Primtest, um Primfaktoren zu identifizieren.
2. Probedivision zur Entfernung von Trivialteilern.
3. Pollard-Rho-Verfahren, um Teiler mittlerer Laenge zu bekommen.
4. ECM mit sich automatisch anpassenden Schranken B1 und B2.

Die Verfahren arbeiten randomisiert. Es ist also problemlos moeglich, zur Erhoehung der Erfolgsaussichten dieselbe Zahl auf verschiedenen Rechnern zu faktorisieren. Es werden keine Berechnungen wiederholt.

B) Verwendung
-------------

Linux:
Eine Shell oeffnen und in das Programmverzeichnis wechseln. Nach Eingabe von

./factor <Zahl>

wird die Primfaktorzerlegung von <Zahl> ausgegeben. (Vorsicht: Vergisst man das "./", so wird der gleichnamige Unixbefehl ausgefuehrt!)

Windows:
Mit Start/Ausfuehren und Eingabe von "cmd" eine Konsole oeffnen und in das Programmverzeichnis wechseln. Danach Eingabe von

factor <Zahl>

und man bekommt die Faktorzerlegung.

C) Uebersetzung des Quelltextes
------------------------------

1. Die Gnu Compiler Collection (gcc) muss installiert werden. Wird bei Linuxdistributionen normalerweise mitgeliefert; wenn nicht installiert, dann sicher auf der Installations-CD/DVD enthalten. Oder herunterladen von http://gcc.gnu.org/
2. Die gmp von http://gmplib.org/ herunterladen und installieren.
3. In das Quelltextverzeichnis wechseln. Nach Eingabe von "gcc -O2 factor.c -lgmp -o factor" auf der Konsole wird das Programm uebersetzt.

Ich bin offen fuer jeden Verbesserungsvorschlag das Programm betreffend ;-)