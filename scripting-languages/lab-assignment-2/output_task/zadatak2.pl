#!/usr/bin/perl

my $filename = $ARGV[0];

my $curr_sender;

my %email_count_dict;

if ($filename) {
    open my $fh, '<', $filename or die "Cannot open file $filename: $!";
    while (my $line = <$fh>) {
        chomp $line;
        if($line =~ /^From nobody/) {
            $curr_sender = undef;
        }
        if(defined $curr_sender) {
            next;
        } elsif ($line =~ /^From:.*<(.+)>/) {
            # $1 is the matched regex expression
            my $sender_email = $1;
            if ($sender_email =~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) {
                $curr_sender = $sender_email;
                $email_count_dict{$sender_email}++;
            }
        }
    }
    close($fh);
} else {
    while (my $line = <>) {
        chomp $line;
        last if $line =~ /^-STOP-$/;
        if($line =~ /^From nobody/) {
            $curr_sender = undef;
        }
        if(defined $curr_sender) {
            next;
        } elsif ($line =~ /^From: .*<.+>/) {
            # $1 is the matched regex expression
            my $sender_email = $1;
            if ($sender_email =~ /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/) {
                $curr_sender = $sender_email;
                $email_count_dict{sender_email}++;
            }
        }
    }
}

my @sorted_email_count_list = sort { $email_count_dict{$a} <=> $email_count_dict{$b} } keys %email_count_dict;

my $max_sender_length = 0;
$max_sender_length = length($_) > $max_sender_length ? length($_) : $max_sender_length for @sorted_email_count_list;

foreach my $temp_email (@sorted_email_count_list) {
    my $temp_count = $email_count_dict{$temp_email};
    my $num_of_stars = '*' x $temp_count;
    printf("%${max_sender_length}s: %s (%d)\n", $temp_email, $num_of_stars, $temp_count);
}