import os
from diag import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams')

def make():
    os.makedirs(OUT, exist_ok=True)
    res = {}
    def mk(name, title, ucs, left, right, links):
        usecase_diagram(os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'), title, ucs, left, right, links)
        res[name] = (os.path.join(OUT, name + '.svg'), os.path.join(OUT, name + '.png'))
    # A: alerting
    ucs = [('UC-01', 'UC-01 Trigger Manual SOS'), ('UC-02', 'UC-02 Handle Automatic\nDistress Alert'), ('UC-03', 'UC-03 Trigger SOS by\nVoice Phrase'),
           ('UC-04', 'UC-04 Manage Trustees'), ('UC-05', 'UC-05 View SOS Event Log'), ('UC-06', 'UC-06 Enrol Safe and\nDuress Phrases'),
           ('UC-24', 'UC-24 Manage Evidence\nRecordings'), ('UC-25', 'UC-25 Escalate to\nAuthorities'), ('UC-29', 'UC-29 Acknowledge\nSOS Alert')]
    links = [('Primary User', u) for u in ('UC-01', 'UC-02', 'UC-03', 'UC-04', 'UC-05', 'UC-06', 'UC-24', 'UC-25')] + \
            [('Trustee', 'UC-01'), ('Trustee', 'UC-29'), ('Verified Helper', 'UC-29'), ('Authority Contact', 'UC-25')]
    mk('uc_alert', 'Muhaffiz: emergency alerting', ucs, ['Primary User'], ['Trustee', 'Verified Helper', 'Authority Contact'], links)
    # B: family and decoy
    ucs = [('UC-07', 'UC-07 Create Circle and\nInvite Member'), ('UC-08', 'UC-08 Share Location and\nView Members'), ('UC-09', 'UC-09 Stop Sharing by\nSafe Phrase'),
           ('UC-10', 'UC-10 Leave Family Circle'), ('UC-11', 'UC-11 Use Decoy Mode'), ('UC-27', 'UC-27 Change App Disguise')]
    links = [('Primary User', 'UC-07'), ('Primary User', 'UC-11'), ('Primary User', 'UC-27'), ('Family Circle Member', 'UC-07'),
             ('Family Circle Member', 'UC-08'), ('Family Circle Member', 'UC-09'), ('Family Circle Member', 'UC-10')]
    mk('uc_family', 'Muhaffiz: family network and disguise', ucs, ['Primary User'], ['Family Circle Member'], links)
    # C: community and information
    ucs = [('UC-12', 'UC-12 Submit Incident Report'), ('UC-13', 'UC-13 View Danger Heatmap'), ('UC-14', 'UC-14 Register as\nVerified Helper'),
           ('UC-15', 'UC-15 Request and Respond\nto Nearby Help'), ('UC-23', 'UC-23 File Missing-Child\nReport'), ('UC-16', 'UC-16 Browse Library'),
           ('UC-17', 'UC-17 Search Library'), ('UC-18', 'UC-18 Call Emergency Service'), ('UC-26', 'UC-26 Navigate to Nearest\nSafe Location')]
    links = [('Primary User', u) for u in ('UC-12', 'UC-13', 'UC-14', 'UC-15', 'UC-16', 'UC-17', 'UC-18', 'UC-26')] + \
            [('Guardian', 'UC-23'), ('Verified Helper', 'UC-15'), ('Verified Helper', 'UC-23'), ('Administrator', 'UC-14')]
    mk('uc_community', 'Muhaffiz: community, library and directory', ucs, ['Primary User', 'Guardian'], ['Verified Helper', 'Administrator'], links)
    # D: account and administration
    ucs = [('UC-19', 'UC-19 Sign Up and Log In'), ('UC-28', 'UC-28 Recover Account'), ('UC-20', 'UC-20 Manage Consent and\nPrivacy Settings'),
           ('UC-21', 'UC-21 Moderate Reports and\nReview Helpers'), ('UC-22', 'UC-22 Monitor System Health')]
    links = [('Primary User', 'UC-19'), ('Primary User', 'UC-28'), ('Primary User', 'UC-20'), ('Administrator', 'UC-21'), ('Administrator', 'UC-22')]
    mk('uc_admin', 'Muhaffiz: account, consent and administration', ucs, ['Primary User'], ['Administrator'], links)
    return res

if __name__ == '__main__': print(make())
