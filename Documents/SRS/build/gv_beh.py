from gvdiag import *
from gv_uml import esc, class_style

def _wrap(t, n=30):
    out = []; cur = ''
    for w in t.split(' '):
        if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    out.append(cur); return out

def stt(id_, name, entry=None, do=None, exit_=None, fill='#EAF1F8', color=BLUE):
    rows = '<TR><TD ALIGN="CENTER"><FONT POINT-SIZE="13"><B>%s</B></FONT></TD></TR>' % esc(name)
    acts = []
    for lab, v in (('entry / ', entry), ('do / ', do), ('exit / ', exit_)):
        if v:
            ls = _wrap(lab + v, 32)
            acts.append(ls[0] + ''.join('<BR ALIGN="LEFT"/>' + '      ' + esc(x) for x in ls[1:]) if False else '<BR ALIGN="LEFT"/>'.join([esc(ls[0])] + ['    ' + esc(x) for x in ls[1:]]))
    if acts:
        rows += '<HR/><TR><TD ALIGN="LEFT" BALIGN="LEFT"><FONT POINT-SIZE="11">%s<BR ALIGN="LEFT"/></FONT></TD></TR>' % '<BR ALIGN="LEFT"/>'.join(acts)
    return '%s [shape=plain, label=<<TABLE BORDER="1" STYLE="ROUNDED" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" COLOR="%s" BGCOLOR="%s">%s</TABLE>>];\n' % (id_, color, fill, rows)

def init(id_='start'): return '%s [shape=circle, style=filled, fillcolor="%s", color="%s", label="", width=0.2, height=0.2, fixedsize=true];\n' % (id_, NAVY, NAVY)
def fin(id_='end'): return '%s [shape=doublecircle, style=filled, fillcolor="%s", color="%s", label="", width=0.2, height=0.2, fixedsize=true];\n' % (id_, NAVY, NAVY)
def tr(a, b, label='', extra=''): return '%s -> %s [label="%s"%s];\n' % (a, b, label, (', ' + extra) if extra else '')

def head(rankdir='TB', ranksep=0.6, nodesep=0.5):
    return class_style(rankdir, ranksep, nodesep) + 'edge [fontsize=11];\n'

# ---------------------------------------------------------------- state diagrams
def st_sos_a():
    d = 'digraph sosa {\n' + head('TB', 0.7, 0.6)
    d += init()
    d += stt('Idle', 'Idle', 'monitoring may be on')
    d += stt('Count', 'Countdown', '20 s; vibrate (loud) or stay silent;\\nshow cancel (loud)')
    d += stt('Can', 'Cancelled', 'nothing is sent')
    d += stt('Active', 'Active', 'request location; start recording and timer', 'siren (loud) or none (silent)')
    d += stt('Disp', 'Dispatching', None, 'send per tier; queue failures')
    d += stt('Wait', 'Awaiting response', 'start T_ack = 3 min', fill='#F2F5F7', color=GREY)
    d += tr('start', 'Idle')
    d += tr('Idle', 'Count', 'automatic or voice trigger\\n[consent given]')
    d += tr('Idle', 'Active', 'manual trigger\\n(hold 1 s or lock screen)')
    d += tr('Count', 'Can', 'user cancels')
    d += tr('Count', 'Active', '20 s elapsed')
    d += tr('Can', 'Idle', 'resume monitoring', 'constraint=false')
    d += tr('Active', 'Disp', 'fix obtained, or cached\\nafter T_fix = 10 s')
    d += tr('Disp', 'Wait', 'sent or queued')
    d += '{rank=same; Count; Can}\n'
    return render('state_sos_a', d + '}\n')

def st_sos_b():
    d = 'digraph sosb {\n' + head('TB', 0.7, 0.6)
    d += fin()
    d += stt('Wait', 'Awaiting response', 'start T_ack = 3 min', fill='#F2F5F7', color=GREY)
    d += stt('Ack', 'Acknowledged', 'stop timer; show acknowledgement', fill='#E3F2EE', color=TEAL)
    d += stt('Warn', 'Escalation warning', 'vibrate 30 s; show cancel')
    d += stt('Esc', 'Escalated', 'send message to authority numbers; log')
    d += stt('Closed', 'Closed', 'stop alarm and recording; finalise log')
    d += tr('Wait', 'Ack', 'acknowledgement')
    d += tr('Wait', 'Warn', 'T_ack expires\\n[no acknowledgement]')
    d += tr('Warn', 'Ack', 'acknowledgement', 'constraint=false')
    d += tr('Warn', 'Esc', '30 s elapsed')
    d += tr('Warn', 'Closed', 'user cancels warning')
    d += tr('Esc', 'Closed', 'message sent or queued')
    d += tr('Ack', 'Closed', 'user ends the SOS')
    d += tr('Closed', 'end')
    d += '{rank=same; Wait; Ack}\n'
    return render('state_sos_b', d + '}\n')

def st_countdown():
    d = 'digraph cnt {\n' + head('TB', 0.7, 0.55)
    d += init() + fin()
    d += stt('Idle', 'Idle')
    d += stt('Arm', 'Counting', 'loud: vibrate and show cancel;\\nsilent: no vibration, no indication', 'update remaining seconds')
    d += stt('Can', 'Cancelled', 'stop vibration; discard trigger')
    d += stt('Exp', 'Expired', 'stop vibration; hand over to SOS')
    d += tr('start', 'Idle'); d += tr('Idle', 'Arm', 'begin(trigger, mode)\\n[fusion rule satisfied, or voice phrase]')
    d += tr('Arm', 'Can', 'cancel()\\n[remaining > 0]'); d += tr('Arm', 'Exp', 'T_count = 20 s elapsed')
    d += tr('Can', 'Idle'); d += tr('Exp', 'end', 'start SOS')
    return render('state_countdown', d + '}\n')

def st_share():
    d = 'digraph share {\n' + head('TB', 0.7, 0.55)
    d += init() + fin()
    d += stt('Not', 'Not in circle')
    d += stt('Inv', 'Invited', 'invitation pending (7 days)')
    d += 'subgraph cluster_member {\n label=<<B>Member of the circle</B>>; style="rounded,filled"; fillcolor="#F4FAF8"; color="%s"; fontsize=12; margin=14;\n' % TEAL
    d += stt('Acc', 'Accepted', 'show circle; sharing is off', fill='#fff')
    d += stt('Sh', 'Sharing', 'show persistent indicator; publish on movement', 'publish location', fill='#E3F2EE', color=TEAL)
    d += stt('Stop', 'Stopped', 'stop publishing; freeze last location', 'others see "Not live"', fill='#FFF4D6', color=AMBER)
    d += '}\n'
    d += stt('Left', 'Left circle', 'remove membership; delete stored location')
    d += tr('start', 'Not'); d += tr('Not', 'Inv', 'invited by a member')
    d += tr('Inv', 'Acc', 'accepts'); d += tr('Inv', 'Not', 'declines or 7 days pass')
    d += tr('Acc', 'Sh', 'member enables sharing'); d += tr('Sh', 'Stop', 'safe phrase, then\\ntoggle off')
    d += tr('Stop', 'Sh', 'member resumes sharing')
    d += tr('Acc', 'Left', 'leave circle', 'ltail=cluster_member')
    d += tr('Stop', 'Left', 'leave circle')
    d += tr('Left', 'end')
    d += '{rank=same; Sh; Stop}\n'
    return render('state_share', d + '}\n')

def st_invite():
    d = 'digraph inv {\n' + head('TB', 0.7, 0.55) + init() + fin()
    d += stt('P', 'Pending', 'notify invitee; set expiry (7 days)'); d += stt('A', 'Accepted', 'create membership', fill='#E3F2EE', color=TEAL)
    d += stt('D', 'Declined'); d += stt('E', 'Expired')
    d += tr('start', 'P', 'invite(phone)'); d += tr('P', 'A', 'accept'); d += tr('P', 'D', 'decline'); d += tr('P', 'E', '7 days elapse')
    for x in 'ADE': d += tr(x, 'end')
    return render('state_invite', d + '}\n')

def st_child():
    d = 'digraph child {\n' + head('TB', 0.7, 0.55) + init() + fin()
    d += stt('Sub', 'Submitted', 'validate fields and photo; if invalid, show errors and keep the entries')
    d += stt('Act', 'Active', 'alert trustees and helpers within 5 km; queue for review', 'expiry timer 72 h; a renewal restarts it', fill='#E3F2EE', color=TEAL)
    d += stt('Found', 'Found', 'stop alerts; delete photo'); d += stt('Exp', 'Expired', 'stop alerts; delete photo'); d += stt('Rem', 'Removed', 'delete report; author may be suspended', color=AMBER, fill='#FFF4D6')
    d += tr('start', 'Sub', 'guardian submits'); d += tr('Sub', 'Act', 'valid')
    d += tr('Act', 'Found', 'guardian marks found'); d += tr('Act', 'Exp', '72 h, no renewal')
    d += tr('Act', 'Rem', 'administrator removes\\nas false')
    for x in ('Found', 'Exp', 'Rem'): d += tr(x, 'end')
    return render('state_child', d + '}\n')

def st_helper():
    d = 'digraph helper {\n' + head('TB', 0.7, 0.55) + init() + fin()
    d += stt('App', 'Applied', 'store application (pending); image visible to administrators only')
    d += stt('Ver', 'Verified Helper', 'receives help requests within the radius', fill='#E3F2EE', color=TEAL)
    d += stt('Rej', 'Rejected', 'delete identity image'); d += stt('Rev', 'Revoked', 'stop requests')
    d += tr('start', 'App', 'user applies'); d += tr('App', 'Ver', 'administrator approves\\n(image deleted)'); d += tr('App', 'Rej', 'administrator rejects')
    d += tr('Ver', 'Rev', 'administrator revokes'); d += tr('Rej', 'end'); d += tr('Rev', 'end')
    return render('state_helper', d + '}\n')

def st_tier():
    d = 'digraph tier {\n' + head('TB', 0.9, 0.7) + init()
    d += stt('T1', 'Tier 1: no data connection', 'send SMS only; queue other channels')
    d += stt('T2', 'Tier 2: any data connection', 'send all enabled channels; flush queue')
    d += stt('T3', 'Tier 3: good data connection', 'all channels, heatmap and content sync', fill='#E3F2EE', color=TEAL)
    d += tr('start', 'T1', 'application starts')
    d += tr('T1', 'T2', 'probe succeeds within T_probe = 3 s\\n[round trip > T_good = 1 s]'); d += tr('T2', 'T3', 'round trip <= 1 s')
    d += tr('T3', 'T2', 'round trip > 1 s'); d += tr('T2', 'T1', 'probe fails or times out')
    d += tr('T1', 'T3', 'probe succeeds\\n[round trip <= 1 s]', 'constraint=false'); d += tr('T3', 'T1', 'connection lost', 'constraint=false')
    return render('state_tier', d + '}\n')

def st_evidence():
    d = 'digraph ev {\n' + head('TB', 0.7, 0.55) + init() + fin()
    d += stt('Not', 'Not recording', None, 'if permission is missing: SOS continues, log entry'); d += stt('Rec', 'Recording', 'open microphone; create encrypted stream', 'write encrypted audio')
    d += stt('Stp', 'Stopped', 'close stream; save metadata (time, location, trigger)'); d += stt('Sto', 'Stored', 'listed in the evidence list', 'retention timer; export a copy on request')
    d += stt('Del', 'Deleted', 'remove file and key')
    d += tr('start', 'Not'); d += tr('Not', 'Rec', 'SOS starts\\n[permission granted]')
    d += tr('Rec', 'Stp', 'user stops, SOS closes,\\nor storage is full'); d += tr('Stp', 'Sto', 'encryption finished')
    d += tr('Sto', 'Del', 'user deletes, or retention reached'); d += tr('Del', 'end')
    return render('state_evidence', d + '}\n')

# ---------------------------------------------------------------- activity diagrams
def act(id_, label, fill='#EAF1F8', color=BLUE): return '%s [label="%s", shape=box, style="rounded,filled", fillcolor="%s", color="%s", margin="0.16,0.08", fontsize=12.5];\n' % (id_, label, fill, color)
def dec(id_, label): return '%s [label="%s", shape=diamond, style=filled, fillcolor="#FFF4CC", color="#B08900", fontsize=12, margin="0.02,0.02"];\n' % (id_, label)
def bar(id_): return '%s [label="", shape=box, style=filled, fillcolor="%s", color="%s", width=2.8, height=0.07, fixedsize=true];\n' % (id_, NAVY, NAVY)
def lane(name, label, body, fill='#F7FAFD'):
    return 'subgraph cluster_%s {\n label=<<B>%s</B>>; style="filled"; fillcolor="%s"; color="#9fb0c4"; fontsize=12; margin=12;\n%s}\n' % (name, label, fill, body)

def ad_sos_a():
    d = 'digraph ad1a {\n' + head('TB', 0.45, 0.45) + init() + fin()
    d += act('trig', 'Trigger received') + dec('type', 'Trigger\\ntype?')
    d += act('man', 'Hold SOS 1 s, or tap the\\nlock-screen action') + act('cd', 'Show 20 s countdown;\\nvibrate, no sound') + dec('canc', 'User\\ncancels?')
    d += act('disc', 'Discard trigger;\\nresume monitoring') + act('startsos', 'Start SOS: record trigger\\nand mode (loud or silent)') + act('loc', 'Obtain location: fix within\\n10 s, or cached with age')
    d += bar('fork') + act('ev', 'Start evidence\\nrecording') + act('tm', 'Start 3-minute\\ntimer') + act('al', 'Siren (loud) or\\nquiet (silent)') + act('dp', 'Dispatch by tier\\n(SMS, push, email)') + bar('join')
    d += act('log', 'Update SOS event log')
    d += tr('start', 'trig') + tr('trig', 'type')
    d += tr('type', 'man', 'manual') + tr('type', 'cd', 'automatic / voice')
    d += tr('cd', 'canc') + tr('canc', 'disc', 'yes') + tr('disc', 'end') + tr('canc', 'startsos', 'no, 20 s elapsed') + tr('man', 'startsos')
    d += tr('startsos', 'loc') + tr('loc', 'fork')
    for x in ('ev', 'tm', 'al', 'dp'): d += tr('fork', x) + tr(x, 'join')
    d += tr('join', 'log') + tr('log', 'end', 'continues with the response phase', 'style=dashed')
    return render('activity_sos_a', d + '}\n')

def ad_sos_b():
    d = 'digraph ad1b {\n' + head('TB', 0.5, 0.5) + init() + fin()
    d += act('w', 'SOS dispatched; 3-minute\\ntimer running') + dec('ack', 'Acknowledged\\nin 3 min?') + act('ok', 'Stop timer; show\\nacknowledgement')
    d += act('warn', 'Show 30 s warning\\nwith one-tap cancel') + dec('can2', 'Cancelled?') + act('escm', 'Send escalation message;\\nwrite escalation log') + act('cancel', 'No escalation;\\nlog as cancelled') + act('close', 'User ends the SOS:\\nstop alarm and recording')
    d += tr('start', 'w') + tr('w', 'ack') + tr('ack', 'ok', 'yes') + tr('ack', 'warn', 'no') + tr('warn', 'can2') + tr('can2', 'escm', 'no') + tr('can2', 'cancel', 'yes')
    d += tr('ok', 'close') + tr('escm', 'close') + tr('cancel', 'close') + tr('close', 'end')
    return render('activity_sos_b', d + '}\n')

def ad_tier():
    d = 'digraph ad2 {\n' + head('TB', 0.45, 0.5) + init() + fin()
    d += act('a', 'dispatch(event, location)') + act('t', 'Detect tier: probe backend\\n(T_probe = 3 s, T_good = 1 s)') + dec('tier', 'Tier?')
    d += act('sms1', 'Tier 1: send SMS to\\nevery trustee') + act('q1', 'Queue push, email,\\nWhatsApp and Near Help')
    d += act('sms2', 'Tier 2 or 3: send SMS, push\\nand email in parallel') + dec('wa', 'Loud SOS and\\nWhatsApp enabled?') + act('wa1', 'Offer WhatsApp message;\\nuser confirms send') + dec('fail', 'Channel\\nfailed?')
    d += act('enq', 'Enqueue; back-off\\n(15 s doubling, max 15 min)') + act('mark', 'Mark delivered;\\nupdate event log')
    d += act('ret', 'Connectivity returns:\\nflush queue within 30 s', fill='#FFF4D6', color=AMBER)
    d += tr('start', 'a') + tr('a', 't') + tr('t', 'tier')
    d += tr('tier', 'sms1', 'Tier 1') + tr('tier', 'sms2', 'Tier 2 / 3') + tr('sms1', 'q1') + tr('q1', 'ret', 'later', 'style=dashed')
    d += tr('sms2', 'wa') + tr('wa', 'wa1', 'yes') + tr('wa', 'fail', 'no') + tr('wa1', 'fail') + tr('fail', 'enq', 'yes') + tr('fail', 'mark', 'no')
    d += tr('enq', 'ret', 'retry', 'style=dashed') + tr('ret', 'mark', 'sent', 'constraint=false') + tr('mark', 'end')
    return render('activity_tier', d + '}\n')

def ad_onboard():
    d = 'digraph ad3 {\n' + head('TB', 0.4, 0.5) + init() + fin()
    u = act('u1', 'Open the application') + act('u2', 'Enter mobile number and\\none-time code') + act('u3', 'Read the consent statement') + dec('u4', 'Accept?') + act('u5', 'Add at least one trustee') + act('u6', 'Enter safe and duress phrases;\\nspeak three samples each')
    s = act('s1', 'Verify code; create or\\nrestore account') + act('s2', 'Store consent and time;\\nenable feature choices') + act('s3', 'Keep microphone features off;\\nshow Home screen', fill='#FFF4D6', color=AMBER) + act('s4', 'Validate trustee and phrases;\\nsave on the device') + act('s5', 'Request Android permissions;\\nstart services') + act('s6', 'Show Home screen')
    d += lane('user', 'Primary User', u) + lane('sys', 'Muhaffiz', s)
    d += tr('start', 'u1') + tr('u1', 'u2') + tr('u2', 's1') + tr('s1', 'u3') + tr('u3', 'u4') + tr('u4', 's2', 'yes') + tr('u4', 's3', 'no') + tr('s3', 'end')
    d += tr('s2', 'u5') + tr('u5', 'u6') + tr('u6', 's4') + tr('s4', 's5') + tr('s5', 's6') + tr('s6', 'end')
    return render('activity_onboard', d + '}\n')

def ad_voice():
    d = 'digraph ad4 {\n' + head('TB', 0.4, 0.5) + init() + fin()
    d += act('a', 'Keyword spotter hears\\nan enrolled phrase') + dec('ctx', 'Stop-sharing\\nscreen open?') + dec('which', 'Safe phrase?')
    d += act('opt', 'Unlock the sharing toggle;\\nno SOS') + act('cd', 'Start 20 s countdown\\n(silent for duress)') + dec('can', 'Cancelled by swipe,\\nspoken or typed phrase?')
    d += act('nothing', 'Send nothing; resume listening') + dec('dur', 'Duress phrase?') + act('loud', 'Start SOS in the user\'s\\ndefault mode (voice)') + act('sil', 'Start silent SOS (voice);\\nshow decoy screen')
    d += tr('start', 'a') + tr('a', 'ctx') + tr('ctx', 'which', 'no') + tr('ctx', 'opt', 'yes, safe phrase', 'constraint=false')
    d += tr('which', 'cd', 'yes') + tr('which', 'cd', 'no (duress)', 'style=dashed')
    d += tr('cd', 'can') + tr('can', 'nothing', 'yes') + tr('can', 'dur', 'no, 20 s elapsed') + tr('dur', 'loud', 'no') + tr('dur', 'sil', 'yes')
    for x in ('opt', 'nothing', 'loud', 'sil'): d += tr(x, 'end')
    return render('activity_voice', d + '}\n')

def ad_child():
    d = 'digraph ad5 {\n' + head('TB', 0.4, 0.5) + init() + fin()
    g = act('g1', 'Open the report form') + act('g2', 'Enter child details, photo,\\nlast seen, contact; confirm guardianship') + act('g3', 'Submit') + act('g8', 'Mark found, or renew\\nbefore 72 h', fill='#E3F2EE', color=TEAL)
    s = dec('s1', 'Valid?') + act('s2', 'Show errors;\\nkeep entries') + act('s3', 'Store report (active);\\nrestrict photo access') + act('s4', 'Alert trustees and helpers\\nwithin 5 km') + act('s5', 'Place report in the\\nmoderation queue') + act('s6', 'Stop alerts; delete photo;\\nset found or expired')
    a = act('a1', 'Review report') + dec('a2', 'False?') + act('a3', 'Remove report; may\\nsuspend author') + act('a4', 'Approve (keep active)')
    d += lane('g', 'Guardian', g) + lane('s', 'Muhaffiz', s) + lane('a', 'Administrator', a)
    d += tr('start', 'g1') + tr('g1', 'g2') + tr('g2', 'g3') + tr('g3', 's1') + tr('s1', 's2', 'no') + tr('s2', 'g2', '', 'constraint=false') + tr('s1', 's3', 'yes') + tr('s3', 's4') + tr('s4', 's5')
    d += tr('s5', 'a1') + tr('a1', 'a2') + tr('a2', 'a3', 'yes') + tr('a2', 'a4', 'no') + tr('a3', 'end') + tr('a4', 'g8', '', 'style=dashed') + tr('g8', 's6') + tr('s6', 'end')
    return render('activity_child', d + '}\n')

def ad_report():
    d = 'digraph ad6 {\n' + head('TB', 0.4, 0.5) + init() + fin()
    u = act('u1', 'Choose category;\\nconfirm or move location') + act('u2', 'Submit') + act('u3', 'Open Danger map; tap a cell')
    a = dec('a1', 'Within limits?\\n(5 per 24 h, no duplicate)') + act('a2', 'Reject with message') + act('a3', 'Write IncidentReport\\n(geohash7, time)') + act('a4', 'Draw cells green to red;\\nshow zone panel')
    b = act('b1', 'Read reports of\\nchanged cells') + act('b2', 'Score = sum of\\n0.5 ^ (age / 90 days)') + act('b3', 'Write CellScore') + dec('b4', 'Burst of reports\\nin one cell?') + act('b5', 'Add to moderation\\nqueue')
    d += lane('u', 'Primary User', u) + lane('a', 'Application', a) + lane('b', 'Scheduled function', b)
    d += tr('start', 'u1') + tr('u1', 'u2') + tr('u2', 'a1') + tr('a1', 'a2', 'no') + tr('a2', 'end') + tr('a1', 'a3', 'yes') + tr('a3', 'b1', 'later') + tr('b1', 'b2') + tr('b2', 'b3') + tr('b3', 'b4')
    d += tr('b4', 'b5', 'yes') + tr('b4', 'u3', 'no', 'style=dashed') + tr('b5', 'u3', '', 'style=dashed') + tr('u3', 'a4') + tr('a4', 'end')
    return render('activity_report', d + '}\n')

def ad_search():
    d = 'digraph ad7 {\n' + head('TB', 0.4, 0.5) + init() + fin()
    d += act('q', 'User types a query') + dec('m', 'Embedding model\\navailable?') + act('e', 'Embed the query on the\\ndevice (384 values)') + act('c', 'Cosine similarity with every\\nbundled embedding; sort; take top K') + dec('t', 'Best similarity\\n>= 0.30?')
    d += act('k', 'Keyword search over titles,\\nsummaries and text; add notice') + act('r', 'Show ranked cards\\nwith relevance indicators') + act('o', 'Open or bookmark a result')
    d += tr('start', 'q') + tr('q', 'm') + tr('m', 'e', 'yes') + tr('m', 'k', 'no') + tr('e', 'c') + tr('c', 't') + tr('t', 'r', 'yes') + tr('t', 'k', 'no') + tr('k', 'r') + tr('r', 'o') + tr('o', 'end')
    return render('activity_search', d + '}\n')

def _ent(id_, name, attrs, local=False, fs=10):
    col = AMBER if local else BLUE; hdr = '#FFF1C9' if local else '#DCE9F5'
    rows = ''.join('<TR><TD ALIGN="LEFT"><FONT POINT-SIZE="%s">%s%s</FONT></TD></TR>' % (fs, '<B>PK </B>' if a.startswith('PK ') else ('<I>FK </I>' if a.startswith('FK ') else '      '), esc(a[3:] if a[:3] in ('PK ', 'FK ') else a)) for a in attrs)
    return '%s [shape=plain, label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3" COLOR="%s" BGCOLOR="white"><TR><TD BGCOLOR="%s"><B>%s</B></TD></TR><HR/>%s</TABLE>>];\n' % (id_, col, hdr, esc(name), rows)

def _rel(a, b, one_a, many_b, label=''):
    m = {'1': 'teetee', '0..1': 'teeodot', '0..*': 'crowodot', '1..*': 'crowtee'}
    return '%s -> %s [dir=both, arrowtail=%s, arrowhead=%s, label="  %s  ", arrowsize=1.0, color="%s", fontsize=10];\n' % (a, b, m[one_a], m[many_b], label, NAVY)

def er_users():
    d = 'digraph eru {\n' + head('TB', 1.1, 0.6)
    d += _ent('Acc', 'Account', ['PK uid', 'phone (unique)', 'name', 'messageTemplate', 'defaultMode', 'createdAt'], fs=11.5)
    d += _ent('Tr', 'Trustee', ['PK id', 'FK uid', 'name', 'phone', 'email', 'channels'], fs=11.5)
    d += _ent('Circ', 'Circle', ['PK id', 'FK createdBy', 'createdAt'], fs=11.5)
    d += _ent('Mem', 'Membership', ['PK id', 'FK circleId', 'FK uid', 'state', 'sharing', 'lastShared (lat, lng, time)'], fs=11.5)
    d += _ent('Inv', 'Invitation', ['PK id', 'FK circleId', 'toPhone', 'status', 'expiresAt'], fs=11.5)
    d += _ent('Adm', 'AdminDecision', ['PK id', 'FK adminUid', 'target', 'decision', 'at'], fs=11.5)
    d += _rel('Acc', 'Tr', '1', '0..*', 'has')
    d += _rel('Acc', 'Circ', '1', '0..*', 'creates')
    d += _rel('Circ', 'Mem', '1', '1..*', 'has')
    d += _rel('Acc', 'Mem', '1', '0..*', 'is')
    d += _rel('Circ', 'Inv', '1', '0..*', 'issues')
    d += _rel('Acc', 'Adm', '1', '0..*', 'decides (admin)')
    d += '{rank=same; Tr; Circ; Adm}\n{rank=same; Mem; Inv}\n'
    return render('er_users', d + '}\n')

def er_community():
    d = 'digraph erc {\n' + head('TB', 1.1, 0.6)
    d += _ent('Acc', 'Account', ['PK uid'], fs=11.5)
    d += _ent('Rep', 'IncidentReport', ['PK id', 'FK uid', 'category', 'note', 'geohash7', 'createdAt', 'status'], fs=11.5)
    d += _ent('Cell', 'CellScore', ['PK geohash7', 'counts', 'score', 'updatedAt'], fs=11.5)
    d += _ent('Help', 'HelperProfile', ['PK uid', 'status', 'verifiedAt'], fs=11.5)
    d += _ent('Req', 'HelpRequest', ['PK id', 'FK uid', 'geohash', 'radius', 'status', 'createdAt'], fs=11.5)
    d += _ent('Ack', 'Acknowledgement', ['PK id', 'FK sosId', 'source', 'at'], fs=11.5)
    d += _ent('Child', 'MissingChildReport', ['PK id', 'FK guardianUid', 'childName, age', 'photoRef', 'lastSeen (place, time)', 'status', 'expiresAt'], fs=11.5)
    d += _rel('Acc', 'Rep', '1', '0..*', 'submits')
    d += _rel('Cell', 'Rep', '1', '0..*', 'counts')
    d += _rel('Acc', 'Help', '1', '0..1', 'applies')
    d += _rel('Help', 'Req', '0..*', '0..*', 'answers')
    d += _rel('Acc', 'Req', '1', '0..*', 'creates')
    d += _rel('Req', 'Ack', '1', '0..*', 'receives')
    d += _rel('Acc', 'Child', '1', '0..*', 'files')
    d += '{rank=same; Rep; Help; Child}\n'
    return render('er_community', d + '}\n')

def er_device():
    d = 'digraph erd {\n' + head('TB', 1.0, 0.6)
    d += _ent('Tr', 'Trustee (copy of server record)', ['PK id', 'name', 'phone', 'email', 'channels'], True, fs=11.5)
    d += _ent('Sos', 'SosEvent', ['PK id', 'startedAt', 'trigger, mode', 'location, locationAge', 'status'], True, fs=11.5)
    d += _ent('Del', 'ChannelDelivery', ['PK id', 'FK sosId', 'FK trusteeId', 'channel, status', 'attempts, lastAttempt'], True, fs=11.5)
    d += _ent('Que', 'QueueItem', ['PK id', 'FK deliveryId', 'payload', 'dueAt'], True, fs=11.5)
    d += _ent('Evi', 'EvidenceRecording', ['PK id', 'FK sosId', 'startedAt, duration', 'trigger', 'encryptedPath'], True, fs=11.5)
    d += _ent('Esc', 'EscalationRecord', ['PK id', 'FK sosId', 'number, channel', 'status, at'], True, fs=11.5)
    d += _ent('Auth', 'AuthorityNumber (setting)', ['number', 'channel'], True, fs=11.5)
    d += _rel('Sos', 'Del', '1', '0..*', 'has')
    d += _rel('Tr', 'Del', '1', '0..*', 'receives')
    d += _rel('Del', 'Que', '1', '0..1', 'waits in')
    d += _rel('Sos', 'Evi', '1', '0..1', 'records')
    d += _rel('Sos', 'Esc', '1', '0..*', 'escalates')
    d += _rel('Auth', 'Esc', '1', '0..*', 'sent to')
    d += '{rank=same; Tr; Sos; Auth}\n{rank=same; Del; Evi; Esc}\n'
    return render('er_device', d + '}\n')

def er_content():
    d = 'digraph erk {\n' + head('LR', 1.0, 0.6)
    d += _ent('Lib', 'LibraryItem (bundled)', ['PK id', 'title, category', 'summary, body', 'embedding[384]'], True, fs=11.5)
    d += _ent('Book', 'Bookmark', ['PK itemId', 'createdAt'], True, fs=11.5)
    d += _ent('Dir', 'DirectoryEntry (bundled)', ['PK id', 'name, category', 'phone', 'lat, lng'], True, fs=11.5)
    d += _ent('Con', 'ConsentRecord (setting)', ['micDetection', 'voiceActivation', 'locationSharing', 'acceptedAt'], True, fs=11.5)
    d += _rel('Lib', 'Book', '1', '0..*', 'bookmarked')
    return render('er_content', d + '}\n')

def make():
    for f in (st_sos_a, st_sos_b, st_countdown, st_share, st_invite, st_child, st_helper, st_tier, st_evidence, ad_sos_a, ad_sos_b, ad_tier, ad_voice, ad_search, er_users, er_community, er_device, er_content):
        f()
if __name__ == '__main__': make(); print('ok')
