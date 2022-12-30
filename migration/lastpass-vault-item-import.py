#!/usr/bin/env python3

# This script will create vaults and login items from a LastPass export 
# generated through their web-based exported or the lpass CLI (this has not 
# been tested on exports from their browser extension or other methods). 
# Shared/Nested folders in 1Password will have separate, non-nested 
# vaults created. Items not belonging to any shared folder will be created 
# in the user's Private vault.
# The script expects your export to reside in the same directory as 
# the script with the name export.csv. 
# 
# Note: Currently TOTP secrets are not migrated. 
# Credit to @jbsoliman


import csv, os
vault_list = []
with open('export.csv', newline='') as csvfile:
    linereader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(linereader)
    
    for row in linereader:
        url = row[0]
        username = row[1]
        password = row[2]
        otp_secret = row[3]
        notes= row[4]
        title = row[5]
        vault = row[6]
        
        # omitting Secure Notes
        if url == "http://sn":
            continue

        if otp_secret != "":
            otp_secret_create = "one-time-password[otp]=%s" % otp_secret
        
        if not vault or vault == "":
            if otp_secret != "":
                os.system('''op item create --vault="Private" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    "%s" \\
                    username="%s" \\
                    password="%s" \\
                    notes="%s"
                    ''' % (vault, title, url, otp_secret_create, username, password, notes))
                continue

            if otp_secret == "":
                os.system('''op item create --vault="Private" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    username="%s" \\
                    password="%s" \\
                    notes="%s"
                    ''' % (vault, title, url, username, password, notes))
                continue
            continue

        if vault not in vault_list:
            vault_list.append(vault) 
            # create vault
            os.system('op vault create "%s"'% vault)
            # create item
            if otp_secret != "":
                os.system('''op item create --vault="%s" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    "%s" \\
                    username="%s" \\
                    password="%s" \\
                    notes="%s"
                    ''' % (vault, vault, title, url, otp_secret_create, username, password, notes))
                continue

            if otp_secret == "":
                os.system('''op item create --vault="%s" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    username="%s" \\
                    password="%s"
                    notes="%s"
                    ''' % (vault, vault, title, url, username, password, notes))
                continue
            continue

        if vault in vault_list:
            # create item
            if otp_secret != "":
                os.system('''op item create --vault="%s" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    "%s" \\
                    username="%s" \\
                    password="%s" \\
                    notes="%s"
                    ''' % (vault, vault, title, url, otp_secret_create, username, password, notes))
                continue

            if otp_secret == "":
                os.system('''op item create --vault="%s" \\
                    --tags="%s" \\
                    --category=login \\
                    --title="%s" \\
                    --url="%s" \\
                    username="%s" \\
                    password="%s"
                    notes="%s"
                    ''' % (vault, vault, title, url, username, password, notes))
                continue
            continue
        
        