from gvdiag import *

def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
FS = 11.5

def cls(id_, name, attrs, ops, fill='#EAF1F8', stereo=None, color=BLUE):
    rows = ''
    hdr = '<TR><TD BGCOLOR="%s" ALIGN="CENTER"><FONT POINT-SIZE="%s"><B>%s</B></FONT></TD></TR>' % ('#DCE9F5' if fill == '#EAF1F8' else fill, FS + 1, esc(name))
    a = '<BR ALIGN="LEFT"/>'.join(esc(x) for x in attrs) + ('<BR ALIGN="LEFT"/>' if attrs else '')
    o = '<BR ALIGN="LEFT"/>'.join(esc(x) for x in ops) + ('<BR ALIGN="LEFT"/>' if ops else '')
    body = ('<TR><TD ALIGN="LEFT" BALIGN="LEFT"><FONT POINT-SIZE="%s">%s</FONT></TD></TR><TR><TD ALIGN="LEFT" BALIGN="LEFT"><FONT POINT-SIZE="%s">%s</FONT></TD></TR>' % (FS, a or ' ', FS, o or ' '))
    return ('%s [shape=plaintext, label=<<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4" COLOR="%s" BGCOLOR="white">%s%s</TABLE>>];\n'
            % (id_, color, hdr, body))

def edge(a, b, kind='assoc', label='', ta='', ha='', constraint=True, extra=''):
    attrs = {'assoc': 'arrowhead=none', 'nav': 'arrowhead=vee', 'comp': 'arrowhead=none, arrowtail=diamond, dir=back', 'agg': 'arrowhead=none, arrowtail=odiamond, dir=back',
             'dep': 'arrowhead=vee, style=dashed', 'gen': 'arrowhead=empty', 'impl': 'arrowhead=empty, style=dashed'}[kind]
    s = '%s -> %s [%s' % (a, b, attrs)
    if label: s += ', label="  %s  "' % label
    if ta: s += ', taillabel="%s"' % ta
    if ha: s += ', headlabel="%s"' % ha
    if not constraint: s += ', constraint=false'
    return s + (', ' + extra if extra else '') + ', labeldistance=1.8, labelfontsize=11];\n'

def class_style(rankdir='TB', ranksep=0.7, nodesep=0.5):
    return ('graph [rankdir=%s, fontname="%s", pad=0.25, nodesep=%s, ranksep=%s, splines=true, bgcolor="white"];\n'
            'node [fontname="%s", fontsize=%s];\nedge [color="%s", fontname="%s", fontsize=11, arrowsize=0.9, penwidth=1.3];\n' % (rankdir, FONT, nodesep, ranksep, FONT, FS, NAVY, FONT))

def stub(id_, name, ops=None): return cls(id_, name, [], ops or [], fill='#F2F5F7', color=GREY)

def class_core():
    d = 'digraph core {\n' + class_style('TB', 0.9, 0.45)
    d += cls('Orch', 'SosOrchestrator', ['- activeEvent: SosEvent', '- mode: SosMode'], ['+ start(trigger, mode)', '+ cancel()', '+ stopAlarm()', '+ complete()'])
    d += cls('Mon', 'ConnectivityMonitor', ['- tier: Tier'], ['+ probe(): Tier'])
    d += cls('Event', 'SosEvent', ['- id: String', '- startedAt: DateTime', '- trigger: Trigger', '- mode: SosMode', '- location: GeoPoint', '- locationAge: Duration', '- status: SosStatus'], ['+ addDelivery(d)', '+ close()'])
    d += cls('Mgr', 'DeliveryManager', ['- tier: Tier'], ['+ dispatch(event, loc)', '+ onTierChange(t)'])
    d += cls('Trustee', 'Trustee', ['- id: String', '- name: String', '- phone: String', '- email: String?', '- channels: Set'], ['+ validate(): bool'])
    d += cls('Deliv', 'ChannelDelivery', ['- channel: Channel', '- status: Status', '- attempts: int', '- lastAttempt: DateTime'], ['+ markSent()', '+ markFailed()'])
    d += cls('Queue', 'OutboundQueue', ['- items: List<QueueItem>'], ['+ enqueue(item)', '+ flush(tier)', '+ retryDue(now)'])
    d += edge('Orch', 'Event', 'comp', 'creates', '1', '0..*')
    d += edge('Orch', 'Mgr', 'nav', 'dispatch', '1', '1')
    d += edge('Mon', 'Mgr', 'nav', 'tier', '1', '1')
    d += edge('Event', 'Deliv', 'comp', 'has', '1', '0..*')
    d += edge('Event', 'Trustee', 'nav', 'sent to', '0..*', '1..10')
    d += edge('Mgr', 'Deliv', 'dep', '«creates»')
    d += edge('Mgr', 'Queue', 'assoc', 'uses', '1', '1')
    d += edge('Queue', 'Deliv', 'agg', 'holds', '1', '0..*')
    d += edge('Deliv', 'Trustee', 'nav', 'for', '0..*', '1')
    d += '{rank=same; Orch; Mon}\n{rank=same; Mgr; Event}\n{rank=same; Queue; Deliv; Trustee}\n'
    return render('class_core', d + '}\n')

def class_evidence():
    d = 'digraph evid {\n' + class_style('TB', 0.9, 0.45)
    d += stub('Orch', 'SosOrchestrator', ['+ start(trigger, mode)'])
    d += stub('Event', 'SosEvent', ['+ close()'])
    d += cls('Vault', 'EvidenceVault', ['- retention: Duration'], ['+ startRecording(event)', '+ list(): List', '+ purgeExpired()'])
    d += cls('Evid', 'EvidenceRecording', ['- id: String', '- startedAt: DateTime', '- duration: Duration', '- trigger: Trigger', '- encryptedPath: String'], ['+ stop()', '+ delete()', '+ export()'])
    d += cls('Esc', 'EscalationManager', ['- timer: Duration = 3 min', '- warning: Duration = 30 s'], ['+ onDispatched(event)', '+ onAcknowledged(ack)', '+ escalate(event)'])
    d += cls('Ack', 'Acknowledgement', ['- source: Trustee | Helper', '- receivedAt: DateTime'], ['+ record()'])
    d += cls('Auth', 'AuthorityNumber', ['- number: String', '- channel: Channel'], ['+ send(message)'])
    d += cls('ER', 'EscalationRecord', ['- number: String', '- status: String', '- at: DateTime'], [])
    d += edge('Orch', 'Vault', 'nav', 'records', '1', '1')
    d += edge('Orch', 'Esc', 'nav', 'starts', '1', '1')
    d += edge('Vault', 'Evid', 'comp', '', '1', '0..*')
    d += edge('Event', 'Evid', 'assoc', 'recorded as', '1', '0..1')
    d += edge('Esc', 'Event', 'nav', 'monitors', '1', '1')
    d += edge('Event', 'Ack', 'comp', 'receives', '1', '0..*')
    d += edge('Esc', 'Auth', 'nav', 'sends to', '1', '1..*')
    d += edge('Esc', 'ER', 'comp', 'logs', '1', '0..*')
    d += '{rank=same; Vault; Event; Esc}\n{rank=same; Evid; Ack; Auth; ER}\n'
    return render('class_evidence', d + '}\n')

def class_detect():
    d = 'digraph detect {\n' + class_style('TB', 0.9, 0.5)
    d += cls('Mon', 'AudioMonitor', ['- ambientLevel: double', '- running: bool', '- ring: RingBuffer (2 s)'], ['+ start()', '+ stop()', '+ onFrame(level)'])
    d += cls('Cls', 'SoundClassifier', ['- model: TFLiteModel', '- thetaAudio: double'], ['+ score(burst): double'])
    d += cls('Mot', 'MotionAnalyzer', ['- window: Duration = 5 s', '- aDev, gRot: double'], ['+ anomaly(window): bool', '+ available(): bool'])
    d += cls('Fus', 'FusionRule', ['- thetaHigh: double'], ['+ evaluate(score, motion)'])
    d += cls('Cnt', 'CountdownController', ['- duration: Duration = 20 s', '- state: CountdownState'], ['+ begin(trigger, mode)', '+ cancel()', '+ onExpire()'])
    d += cls('Trig', 'TriggerEngine', ['- defaultMode: SosMode'], ['+ onManual()', '+ onAutomatic()', '+ onVoice(phrase)'])
    d += stub('Orch', 'SosOrchestrator', ['+ start(trigger, mode)'])
    d += edge('Mon', 'Cls', 'nav', 'burst', '1', '1')
    d += edge('Cls', 'Fus', 'nav', 'score', '1', '1')
    d += edge('Mot', 'Fus', 'nav', 'motion', '1', '1')
    d += edge('Fus', 'Cnt', 'nav', 'starts', '1', '1')
    d += edge('Cnt', 'Trig', 'nav', 'on expire', '1', '1')
    d += edge('Trig', 'Orch', 'nav', 'start SOS', '1', '1')
    d += '{rank=same; Mon; Mot}\n{rank=same; Cls; Fus}\n{rank=same; Cnt; Trig}\n'
    return render('class_detect', d + '}\n')

def class_voice():
    d = 'digraph voice {\n' + class_style('TB', 0.9, 0.5)
    d += cls('Cons', 'ConsentSettings', ['- micDetection: bool', '- voiceActivation: bool', '- locationSharing: bool', '- acceptedAt: DateTime'], ['+ accept()', '+ toggle(name)'])
    d += cls('Kws', 'KeywordSpotter', ['- profile: PhraseProfile', '- context: Context', '- running: bool'], ['+ start()', '+ stop()', '+ setContext(ctx)'])
    d += cls('Prof', 'PhraseProfile', ['- safePhrase: String', '- duressPhrase: String', '- sensitivity: double'], ['+ enrol(phrase, samples)', '+ validate(): bool'])
    d += cls('Dec', 'DecoyMode', ['- enabled: bool'], ['+ show()', '+ revealGesture(): bool'])
    d += stub('Trig', 'TriggerEngine', ['+ onVoice(phrase)'])
    d += stub('Share', 'SharingManager', ['+ stopSharing()'])
    d += stub('Mon', 'AudioMonitor', ['+ start()'])
    d += edge('Cons', 'Kws', 'dep', '«enables»')
    d += edge('Cons', 'Mon', 'dep', '«enables»')
    d += edge('Kws', 'Prof', 'assoc', 'uses', '1', '1')
    d += edge('Kws', 'Trig', 'nav', 'phraseDetected', '1', '1')
    d += edge('Kws', 'Share', 'dep', 'confirmation context')
    d += edge('Kws', 'Dec', 'dep', 'duress phrase')
    return render('class_voice', d + '}\n')

def class_family():
    d = 'digraph fam {\n' + class_style('TB', 0.9, 0.5)
    d += cls('Acc', 'Account', ['- uid: String', '- phone: String', '- name: String', '- messageTemplate: String', '- defaultMode: SosMode'], ['+ signIn()', '+ recover()'])
    d += cls('Circ', 'Circle', ['- id: String', '- createdBy: String', '- createdAt: DateTime'], ['+ invite(phone)', '+ members(): List'])
    d += cls('Inv', 'Invitation', ['- toPhone: String', '- status: InviteStatus', '- expiresAt: DateTime'], ['+ accept()', '+ decline()', '+ expire()'])
    d += cls('Mem', 'Membership', ['- state: MemberState', '- sharing: bool', '- lastShared: LocationShare'], ['+ stopSharing()', '+ resumeSharing()', '+ leave()'])
    d += cls('Loc', 'LocationShare', ['- lat, lng: double', '- publishedAt: DateTime', '- live: bool'], ['+ publish(point)', '+ freeze()'])
    d += cls('Shr', 'SharingManager', ['- threshold: double = 50 m'], ['+ onLocation(point)', '+ stopSharing()'])
    d += edge('Acc', 'Circ', 'comp', 'creates', '1', '0..*')
    d += edge('Circ', 'Inv', 'comp', 'issues', '1', '0..*')
    d += edge('Circ', 'Mem', 'comp', 'has', '1', '2..*')
    d += edge('Acc', 'Mem', 'assoc', 'is', '1', '0..*')
    d += edge('Mem', 'Loc', 'assoc', 'shares', '1', '0..1')
    d += edge('Shr', 'Mem', 'nav', 'updates', '1', '1')
    d += '{rank=same; Acc; Circ}\n{rank=same; Inv; Mem; Shr}\n'
    return render('class_family', d + '}\n')

def class_community():
    d = 'digraph comm {\n' + class_style('TB', 0.9, 0.5)
    d += stub('Acc', 'Account', ['+ uid: String'])
    d += cls('Rep', 'IncidentReport', ['- category: Category', '- geohash7: String', '- createdAt: DateTime', '- note: String?'], ['+ submit()', '+ weight(now): double'])
    d += cls('Cell', 'CellScore', ['- geohash7: String', '- counts: Map', '- score: double'], ['+ recompute()'])
    d += cls('Help', 'HelperProfile', ['- status: HelperStatus', '- verifiedAt: DateTime'], ['+ apply()', '+ revoke()'])
    d += cls('Req', 'HelpRequest', ['- geohash: String', '- radius: int = 1000', '- status: String', '- createdAt: DateTime'], ['+ broadcast()', '+ accept(helper)'])
    d += cls('Child', 'MissingChildReport', ['- status: ReportStatus', '- childName: String', '- age: int', '- photoRef: String', '- lastSeen: Place, Time', '- expiresAt: DateTime'], ['+ markFound()', '+ renew()', '+ expire()'])
    d += edge('Acc', 'Rep', 'assoc', 'submits', '1', '0..*')
    d += edge('Rep', 'Cell', 'assoc', 'counted in', '0..*', '1')
    d += edge('Acc', 'Help', 'assoc', 'applies', '1', '0..1')
    d += edge('Help', 'Req', 'assoc', 'answers', '0..*', '0..*')
    d += edge('Acc', 'Req', 'assoc', 'creates', '1', '0..*')
    d += edge('Acc', 'Child', 'assoc', 'files (guardian)', '1', '0..*')
    return render('class_community', d + '}\n')

def class_knowledge():
    d = 'digraph know {\n' + class_style('TB', 0.9, 0.5)
    d += cls('Sem', 'SemanticSearch', ['- tau: double = 0.30', '- k: int = 10'], ['+ search(query): List'])
    d += cls('Emb', 'SentenceEmbedder', ['- model: TFLiteModel'], ['+ embed(text): float[384]', '+ available(): bool'])
    d += cls('Kw', 'KeywordSearch', [], ['+ search(query): List'])
    d += cls('Lib', 'LibraryItem', ['- id: String', '- title: String', '- category: Category', '- summary, body: String', '- embedding: float[384]'], ['+ matches(query): bool'])
    d += cls('Book', 'Bookmark', ['- itemId: String', '- createdAt: DateTime'], ['+ toggle()'])
    d += cls('Dir', 'DirectoryEntry', ['- name: String', '- category: Category', '- phone: String', '- lat, lng: double?'], ['+ call()', '+ distanceTo(p)'])
    d += cls('Safe', 'SafeLocationFinder', [], ['+ nearest(p): Result', '+ directions(entry)'])
    d += edge('Sem', 'Emb', 'nav', 'uses', '1', '1')
    d += edge('Sem', 'Lib', 'nav', 'ranks', '1', '1..*')
    d += edge('Sem', 'Kw', 'dep', 'fallback')
    d += edge('Kw', 'Lib', 'nav', 'scans', '1', '1..*')
    d += edge('Book', 'Lib', 'nav', 'marks', '0..*', '1')
    d += edge('Safe', 'Dir', 'nav', 'chooses', '1', '1..*')
    return render('class_knowledge', d + '}\n')

def class_admin():
    d = 'digraph adm {\n' + class_style('TB', 0.9, 0.5)
    d += cls('Auth', 'AuthService', ['- uid: String?', '- lockedUntil: DateTime?'], ['+ sendCode(phone)', '+ verify(code)', '+ signOut()'])
    d += cls('Sess', 'SessionManager', ['- token: String', '- expires: DateTime'], ['+ renew()', '+ revoke()'])
    d += cls('Dis', 'AppDisguise', ['- current: Appearance'], ['+ apply(a)', '+ restore()'])
    d += cls('Admin', 'AdminUser', ['- uid: String', '- role = administrator'], ['+ signIn()'])
    d += cls('Mod', 'ModerationQueue', ['- items: List<FlaggedItem>'], ['+ decide(item, decision)', '+ log(decision)'])
    d += cls('Dec', 'AdminDecision', ['- adminUid: String', '- target: String', '- decision: Decision', '- at: DateTime'], [])
    d += edge('Auth', 'Sess', 'comp', 'opens', '1', '0..1')
    d += edge('Admin', 'Auth', 'dep', '«uses»')
    d += edge('Admin', 'Mod', 'nav', 'reviews', '1', '1')
    d += edge('Mod', 'Dec', 'comp', 'records', '1', '0..*')
    return render('class_admin', d + '}\n')

def make():
    for f in (class_core, class_evidence, class_detect, class_voice, class_family, class_community, class_knowledge, class_admin): f()
if __name__ == '__main__': make(); print('ok')
