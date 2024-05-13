#!/usr/bin/perl

# U repozitoriju na stranici predmeta nalaze se dvije log-datoteke jednog web poslužitelja. To su
# tekst datoteke koje se generiraju svakoga dana, a datum je sadržan u imenu datoteke. Svaki redak
# odgovara jednom pristupanju poslužitelju.
# Napisati skriptu u Perlu koja će za svaki sat u danu ispisati broj pristupa poslužitelju. Kao argu-
# menti naredbenog retka pri pozivu se navode imena log datoteka koje treba analizirati (datoteke
# ne moraju biti u tekućem direktoriju). Ako se ne navede niti jedna datoteka, skripta podatke treba
# čitati sa standardnog ulaza (sjetite se operatora <>).

my %access_counter;

while (defined($row = <>)) {
    if ($row =~ /^\s*$/) {
        last;
    }

    if($row =~ m/\[(\d{2})\/\w+\/(\d{4}):(\d{2}):/ ) {
        my $day = $1;
        my $year = $2;
        my $hour = $3;
        my $real_date = "$year-$day";
        $access_counter{$real_date}{$hour}++;
    }
}

foreach my $real_date (sort keys %access_counter) {
    print "Datum: $real_date\n";
    print "sat: broj pristupa\n";
    print "-------------------------------\n";
    foreach my $hour (0..23) {
        my $format_hour = sprintf("%02d", $hour);
        printf("%02d : %d\n", $format_hour, $access_counter{$real_date}{$format_hour} // 0);
    }
    print "\n";
}