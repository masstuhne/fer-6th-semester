#!/usr/bin/perl

# Napišite Perl skriptu koja će od korisnika zatražiti (i učitati) niz znakova i broj ponavljanja (n).
# Učitani znakovni niz treba ispisati n puta (svaki put u novom redu).

print "Enter a string: ";
my $string = <STDIN>;
chomp $string;

print "Enter the number of repetitions: ";
my $number = <STDIN>;
chomp $number;

for (my $i = 0; $i < $number; $i++) {
    print "$string\n";
}
