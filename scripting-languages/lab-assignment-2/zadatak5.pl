#!/usr/bin/perl

# Napišite skriptu u Perlu koja će iz datoteke čije je ime navedeno kao argument pri pozivu skripte
# učitati podatke o rezultatima studenata. U prvom retku datoteke zapisan je niz brojeva, odvojenih
# znakom ";", koji predstavljaju faktore s kojima se svaka komponenta ocjene množi. Slijede retci
# s podacima o svakom pojedinom studentu: matični broj, prezime i ime kao jedno polje, te niz
# brojeva koji predstavljaju ostvarene rezultate pojedinih komponenti ocjene studenta. Pojedina polja
# odvojena su znakom ";". Ako neka bodovna komponenta nedostaje, označena je znakom "-". U
# datoteci su dozvoljeni i komentirani retci (prvi znak u retku je #), kao i prazni retci – prazne i
# komentirane retke treba preskočiti (zanemariti).

# Skripta treba na temelju učitanih rezultata generirati rang-listu studenata, u kojoj će biti označen
# rang studenta, njegovo prezime i ime, te ukupni ostvareni broj bodova (dobije se zbrajanjem svih
# komponenti rezultata pomnoženih s pripadnim faktorima). Funkciji sort može se zadati blok
# naredbi ili potprogram koji obavlja usporedbu dva elementa liste koja se sortira. Za detalje pogle-
# dati dokumentaciju funkcije sort

die "Usage: $0 filename\n" unless @ARGV == 1;

my $filename = $ARGV[0];

open my $fh, '<', $filename or die "Cannot open file $filename: $!";

my @students;
my @factors;    

while (my $line = <$fh>) {
    next if $line =~ /^\s*$/ || $line =~ /^#/;

    chomp $line;

    if (!@factors) {
        @factors = split(";", $line);
        next;
    }

    my @fields = split(";", $line);
    my $student_id = shift @fields;
    my $surname = shift @fields;
    my $name = shift @fields;
    my @results = @fields;

    my $total_score = 0;
    for (my $i = 0; $i < @factors; $i++) {
        next if $results[$i] eq '-';
        $total_score += $results[$i] * $factors[$i];
    }

    push @students, {
        id => $student_id,
        name => "$surname $name",
        score => $total_score
    };
}

close $fh;

@students = sort { $b->{score} <=> $a->{score} } @students;

my $max_student_length = 0;
foreach my $student (@students) {
    my $student_length = length($student->{name});
    $max_student_length = $student_length if $student_length > $max_student_length;
}

print("Lista po rangu:\n");
print("-------------------\n");
for (my $i = 0; $i < @students; $i++) {
    printf "%3d. %-*s (%s) : %.2f\n", $i + 1, $max_student_length, $students[$i]{name}, $students[$i]{id}, $students[$i]{score};
}
