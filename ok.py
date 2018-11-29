import textfsm

# Run text through the FSM.
# The argument 'template' is a file handle and 'raw_text_data' is a string.
template = open('files/textfsm/ltm-pool-members.txt')

raw_text_data = """
ltm pool /Common/pss1clktriggersstg {
    members {
        /Common/foo:80 {
            address 10.6.8.39
        }
        /Common/bar:80 {
            address 1.1.1.1
        }
    }
    monitor /Common/pss1clktriggersstg
}
ltm pool /Common/pss1webappsstg.corp.iqorams.net_pool {
    members {
        /Common/ATL2WSTGWEB01:80 {
            address 10.6.8.40
        }
        /Common/alice:80 {
            address 3.4.5.5
        }
        /Common/bob:80 {
            address 1.3.4.5
        }
    }
    monitor /Common/pss1webappsstg
}
"""
re_table = textfsm.TextFSM(template)
data = re_table.ParseText(raw_text_data)

# Display result as CSV
# First the column headers
print( ', '.join(re_table.header) )
# Each row of the table.
for row in data:
  print( ', '.join(row) )
