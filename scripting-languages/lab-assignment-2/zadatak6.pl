#!/usr/bin/perl

# Napisati Perl skriptu koja će u datoteci koja se zadaje kao argument naredbenog retka izbrojati
# riječi sa zajedničkim prefiksom. Duljina prefiksa zadaje se kao zadnji argument naredbenog retka,
# a prethode mu imena datoteka (može ih biti i više). Ako se ne navede niti jedno ime datoteke,
# skripta treba tekst čitati sa standardnog ulaza.
# U datoteci je običan tekst, a rijeći su odvojene proizvoljnim brojem razmaka (uključujući i tabula-
# tore i prelaske u novi red) te znakovima interpunkcije. Prilikom usporedbe riječi treba zanemariti
# razliku između velikih i malih slova. Lista prefiksa treba biti poredana po abecedi, a iza svakog
# prefiksa treba navesti broj pojavljivanja. 

use utf8;
use locale;
use open ':locale';

die "Usage: $0 file1 [file2 ...] prefix_length\n" if @ARGV < 1;

my $prefix_length = pop @ARGV;
die "Prefix length must be a positive integer\n" unless $prefix_length =~ /^\d+$/ && $prefix_length > 0;

my %prefix_count;
while (<>) {
    s/[^\w\s]//g;
    foreach my $word (split /\s+/) {
        $word = lc $word;
        my $prefix = substr($word, 0, $prefix_length);
        $prefix_count{$prefix}++ if length($prefix) == $prefix_length;
    }
}

foreach my $prefix (sort keys %prefix_count) {
    print "$prefix : $prefix_count{$prefix}\n";
}