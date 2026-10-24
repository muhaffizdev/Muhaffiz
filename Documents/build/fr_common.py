# Shared FR registry for Chapter 3 (and traceability later)
FRS = []
MODNAME = {1:'SOS Alert System',2:'Automatic Danger Detection Engine',3:'Voice Activation and Safe-Phrase Engine',4:'Family Circle Management',
 5:'Location Sharing and Privacy Controls',6:'Decoy Mode',7:'Danger Heatmap',8:'Near Help',9:'Content Library Management',10:'Semantic Search Engine',
 11:'Emergency Services Directory',12:'Tiered Delivery System',13:'Offline Data Caching',14:'Authentication and Account Management',
 15:'Consent and Privacy Controls',16:'Admin Dashboard',17:'Missing-Child Report',18:'Evidence Recording on SOS',19:'Escalation to Authorities',
 20:'Safe-Location Navigation',21:'App Disguise'}
MODPRIO = {m:'High' for m in (1,2,3,4,5,6,12,13,14,15)}
MODPRIO.update({m:'Medium' for m in (7,8,9,10,11,16,17,18,19)})
MODPRIO.update({m:'Low' for m in (20,21)})
MODSRC = {
 1:'survey (SOS button 74%)', 2:'survey (55%); scope document', 3:'survey (secret phrase 58%)', 4:'survey (family map 68%); scope document',
 5:'survey (13% forced-sharing barrier); scope document', 6:'survey (decoy 87%); interview (MBBS student)', 7:'survey (unsafe-areas map 84%)',
 8:'survey (58%)', 9:'scope document; survey (68%)', 10:'scope document; survey (68%)', 11:'survey (84%)', 12:'survey (internet barrier 71%)',
 13:'survey (internet barrier 71%)', 14:'scope document', 15:'interviews (trust in data handling)', 16:'scope document', 17:'survey (77%)',
 18:'survey (77%); interviews', 19:'survey (81%)', 20:'interview (male university student); survey (77%)', 21:'survey open-ended response'}

def F(mod, n, title, s, why, br, dep, acc, u=None, pri=None, src=None):
    fid = 'FR-%02d.%02d' % (mod, n)
    FRS.append(dict(id=fid, mod=mod, n=n, title=title, u=u, s=s, why=why, br=br, dep=dep, acc=acc,
                    pri=pri or MODPRIO[mod],
                    src=src or ('Feature Document 7.%d.%d; %s' % (mod, n, MODSRC[mod]) if mod <= 19 else 'Interview and survey; %s' % MODSRC[mod])))
