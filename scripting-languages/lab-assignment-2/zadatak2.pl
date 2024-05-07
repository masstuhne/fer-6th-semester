#!/usr/bin/perl

# Napišite Perl skriptu koja će učitati niz brojeva u listu, te izračunati i ispisati aritmetičku sredinu
# učitanih brojeva.

print("Enter a series of numbers (separated by a space): ");
my $number_input = <STDIN>;

my @number_list = split(" ", $number_input);
my $len_number_list = scalar @number_list;

if ($len_number_list == 0) {
    print("No numbers have been entered!\n");
    exit;
}

my $sum = 0;
foreach my $number (@number_list) {
    $sum += $number;
}

my $average = $sum / $len_number_list;
print("Arithmetic mean: $average\n");