#!/usr/bin/perl

# U datoteci su zapisani podaci o terminima laboratorijskih vježbi pojedinih studenata, te vrijeme
# njihove predaje (zakljuˇcavanja) izlaznog testa, u obliku:
# JMBAG;Prezime;Ime;Termin;Zaključano
# 0036438919;Bagarić;Magdalena;2011-03-14 08:00 11:00 A209;2011-03-14 08:45:02
# 0036433049;Bajac;Darko;2011-03-14 08:00 11:00 A209;2011-03-14 08:48:19
# ...
# 0036436684;Lombarović;Mladen;2011-03-14 11:00 14:00 A210;2011-03-14 12:08:26
# 0036325839;Matošić;Luka;2011-03-14 11:00 14:00 A210;2011-03-15 11:49:26
# ...
# Napišite skriptu u Perlu, koja će za svakog studenta provjeriti je li zaključao svoj izlazni test unutar
# prvih sat vremena laboratorijskog termina (može se pretpostaviti da termini počinju na puni sat).
# Ispisati podatke o studentima za koje taj uvjet nije ispunjen, kao u primjeru. Ime datoteke se navodi
# kao argument pri pozivu skripte. Ako se ne navede ime datoteke, skripta podatke treba čitati sa
# standardnog ulaza.

my $file_given = @ARGV ? 1 : 0;

while (defined($row = <>)) {
    if ($row =~ /^\s*$/) {
        last;
    }

    chomp $row;

    if ($file_given) {
        $file_given = 0;
        next;
    }

    my ($JMBAG, $lastname, $firstname, $when, $locked) = split(";", $row);
    my ($date, $time_start, $time_end, $classroom) = split(" ", $when);
    my ($hour_start, $minute_start) = split(":", $time_start);
    my ($date_locked, $time_locked) = split(" ", $locked);
    my ($hour_locked, $minute_locked, $seconds_locked) = split(":", $time_locked);

    if (($hour_locked - $hour_start > 0)) {
        if (!(($hour_locked - $hour_start == 1) && ($minute_locked == 0) && ($seconds_locked == 0))) {
            print "$JMBAG $lastname $firstname - PROBLEM: $date $time_start --> $locked\n"; 
        }
    }
}