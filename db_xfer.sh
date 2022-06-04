#!/bin/bash

#Version 0.0.1

dry_run=''
#dry_run='echo '

fail () {
	echo "$@ , exiting." >&2
	exit 1
}


Usage () {
	cat <<EOTEXT
Usage:
$0 [--remove-source|--bidir] src_host src_db dest_host dest_db

--remove-source: erase any records in dest from source.
--bidir: bidirectional copy.  all src records go to dest, all dest records go to source.
Only one of the above can be picked (or neither, which only copies from source to dest).

src_host and dest_host can be anything to which you can ssh or "" for databases on localhost
src_db and dest_db should be a full path (or relative to HOME on remote hosts or relative to current directory on localhost)
EOTEXT
	exit 0
}

if [ "z$1" = "z--remove-source" ]; then
	remove_source='True'
	shift
elif [ "z$1" = "z--bidir" ]; then
	bidir='True'
	shift
elif [ "z$1" = "z-h" -o "z$1" = "z--help" ]; then
	Usage
fi

if [ -z "$4" -o -n "$5" ]; then
	Usage
fi

src_host="$1"
src_db="$2"
dest_host="$3"
dest_db="$4"

if [ "$src_host" = 'localhost' -o "$src_host" = '127.0.0.1' -o "$src_host" = '::1' -o "$src_host" = '' ]; then
	src_host=''
	src_ssh=''
else
	src_ssh='ssh'
fi

if [ "$dest_host" = 'localhost' -o "$dest_host" = '127.0.0.1' -o "$dest_host" = '::1' -o "$dest_host" = '' ]; then
	dest_host=''
	dest_ssh=''
else
	dest_ssh='ssh'
fi

#outbound_records=`mktemp -q -t "db_xfer.XXXXXX" </dev/null` || fail "Unable to make outbound_records temp file"

#Requires sqlite3, merge_into_db.py, remove_from_db.py, and db_lib.py in your path on source and dest
for util in sqlite3 merge_into_db.py remove_from_db.py db_lib.py ; do
	$src_ssh $src_host type -path "$util" >/dev/null 2>&1 || fail "$src_host missing utility $util"
	$dest_ssh $dest_host type -path "$util" >/dev/null 2>&1 || fail "$dest_host missing utility $util"
done
#This system needs mktemp .  mbuffer is optional
for util in mktemp ; do
	type -path "$util" >/dev/null 2>&1 || fail "localhost missing utility $util"
done

if [ -z "$dry_run" ]; then
	$src_ssh $src_host sqlite3 -readonly 'file:'"${src_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \
	 | if type -path mbuffer >/dev/null 2>&1 ; then mbuffer -q -t -m 100M 2>/dev/null ; else cat ; fi \
	 | $dest_ssh $dest_host merge_into_db.py -w "$dest_db"
else
	echo $src_ssh $src_host sqlite3 -readonly 'file:'"${src_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \| mbuffer -q -t -m 100M \| $dest_ssh $dest_host merge_into_db.py -w "$dest_db"
fi

#Later: tee command goes after mbuffer
# | tee "$outbound_records" \


if [ "$bidir" = 'True' ]; then
	if [ -z "$dry_run" ]; then
		$dest_ssh $dest_host sqlite3 -readonly 'file:'"${dest_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \
		 | if type -path mbuffer >/dev/null 2>&1 ; then mbuffer -q -t -m 100M 2>/dev/null ; else cat ; fi \
		 | $src_ssh $src_host merge_into_db.py -w "${src_db}"
	else
		echo $dest_ssh $dest_host sqlite3 -readonly 'file:'"${dest_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \| mbuffer -q -t -m 100M \| $src_ssh $src_host merge_into_db.py -w "${src_db}"
	fi
elif [ "$remove_source" = 'True' ]; then
	if [ -z "$dry_run" ]; then
		$dest_ssh $dest_host sqlite3 -readonly 'file:'"${dest_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \
		 | if type -path mbuffer >/dev/null 2>&1 ; then mbuffer -q -t -m 100M 2>/dev/null ; else cat ; fi \
		 | $src_ssh $src_host remove_from_db.py -d "${src_db}"
	else
		echo $dest_ssh $dest_host sqlite3 -readonly 'file:'"${dest_db}"'?mode=ro' 'select KEY_STR, JSON_STR from main' \| mbuffer -q -t -m 100M \| $src_ssh $src_host remove_from_db.py -d "${src_db}"
	fi
fi
echo
