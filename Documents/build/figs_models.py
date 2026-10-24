import os
from diag2 import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'diagrams'); os.makedirs(OUT, exist_ok=True)
def P(n): return os.path.join(OUT, n + '.svg'), os.path.join(OUT, n + '.png')

# ------------------------------------------------------------------ class diagrams
def class1():
    s = Svg(900, 640)
    A = class_box(s, 20, 20, 230, 'SosOrchestrator', ['- activeEvent: SosEvent', '- mode: SosMode'], ['+ start(trigger, mode)', '+ cancel()', '+ stopAlarm()', '+ complete()'])
    B = class_box(s, 330, 20, 240, 'SosEvent', ['- id: String', '- startedAt: DateTime', '- trigger: Trigger', '- mode: SosMode', '- location: GeoPoint', '- locationAge: Duration', '- status: SosStatus'], ['+ addDelivery(d)', '+ close()'])
    C = class_box(s, 650, 20, 230, 'Trustee', ['- id: String', '- name: String', '- phone: String', '- email: String?', '- channels: Set<Channel>'], ['+ validate()'])
    D = class_box(s, 330, 270, 240, 'ChannelDelivery', ['- channel: Channel', '- status: DeliveryStatus', '- attempts: int', '- lastAttempt: DateTime'], ['+ markSent()', '+ markFailed()'])
    E = class_box(s, 650, 270, 230, 'OutboundQueue', ['- items: List<ChannelDelivery>'], ['+ enqueue(d)', '+ flush(tier)', '+ retryDue()'])
    F = class_box(s, 20, 270, 230, 'EvidenceRecording', ['- id: String', '- startedAt: DateTime', '- duration: Duration', '- trigger: Trigger', '- encryptedPath: String'], ['+ stop()', '+ delete()', '+ export()'])
    G = class_box(s, 20, 470, 230, 'EscalationManager', ['- timer: Duration = 3 min', '- warning: Duration = 30 s'], ['+ onDispatched(e)', '+ onAcknowledged(a)', '+ escalate(e)'])
    H = class_box(s, 330, 470, 240, 'Acknowledgement', ['- source: Trustee|Helper', '- receivedAt: DateTime'], ['+ record()'])
    I = class_box(s, 650, 470, 230, 'DeliveryManager', ['- tier: ConnectivityTier'], ['+ dispatch(event)', '+ onTierChange(t)'])
    assoc(s, anchor(A, 'r'), anchor(B, 'l'), '1', '0..*', 'creates')
    assoc(s, anchor(B, 'r'), anchor(C, 'l'), '', '', 'sent to', via=None)
    assoc(s, anchor(B, 'b', .5), anchor(D, 't', .5), '1', '0..*', 'has')
    assoc(s, anchor(C, 'b', .5), anchor(D, 'r', .3), '1', '0..*', via=[(765, 230), (600, 230), (600, 330)])
    assoc(s, anchor(D, 'r', .75), anchor(E, 'l', .5), '0..*', '1', 'queued in')
    assoc(s, anchor(B, 'l', .85), anchor(F, 't', .5), '1', '0..1', 'records', via=[(290, 195), (135, 195)])
    assoc(s, anchor(G, 'r', .4), anchor(H, 'l', .4), '1', '0..*', 'tracks')
    assoc(s, anchor(H, 't', .5), anchor(D, 'b', .5), '', '', '', via=None, dashed=True)
    assoc(s, anchor(I, 't', .5), anchor(E, 'b', .5), '1', '1', 'uses')
    assoc(s, (20, 100), (20, 505), '', '', '', via=[(7, 100), (7, 505)])
    s.save(*P('class_core'))

def class2():
    s = Svg(900, 620)
    A = class_box(s, 20, 20, 240, 'AudioMonitor', ['- ambientLevel: double', '- running: bool'], ['+ start()', '+ stop()', '+ onFrame(level)'])
    B = class_box(s, 330, 20, 240, 'SoundClassifier', ['- model: TFLiteModel', '- thetaAudio: double'], ['+ score(buffer): double'])
    C = class_box(s, 650, 20, 230, 'MotionAnalyzer', ['- window: Duration'], ['+ anomaly(window): bool'])
    D = class_box(s, 330, 220, 240, 'FusionRule', ['- thetaHigh: double'], ['+ evaluate(score, motion): bool'])
    E = class_box(s, 20, 220, 240, 'CountdownController', ['- duration: Duration = 20 s', '- state: CountdownState'], ['+ begin(trigger)', '+ cancel()', '+ onExpire()'])
    F = class_box(s, 650, 220, 230, 'TriggerEngine', ['- defaultMode: SosMode'], ['+ onManual()', '+ onAutomatic()', '+ onVoice(phrase)'])
    G = class_box(s, 20, 420, 240, 'KeywordSpotter', ['- profile: PhraseProfile', '- running: bool'], ['+ start()', '+ stop()', '+ setContext(ctx)'])
    H = class_box(s, 330, 420, 240, 'PhraseProfile', ['- safePhrase: String', '- duressPhrase: String', '- sensitivity: double'], ['+ enrol(phrase, samples)', '+ validate()'])
    I = class_box(s, 650, 420, 230, 'ConsentSettings', ['- micDetection: bool', '- voiceActivation: bool', '- locationSharing: bool'], ['+ accept()', '+ toggle(name)'])
    assoc(s, anchor(A, 'r', .3), anchor(B, 'l', .3), '1', '1', 'passes burst')
    assoc(s, anchor(B, 'b', .5), anchor(D, 't', .5), '1', '1', 'score')
    assoc(s, anchor(C, 'b', .5), anchor(D, 'r', .3), '1', '1', 'motion', via=[(765, 190), (600, 190), (600, 250)])
    assoc(s, anchor(D, 'l', .5), anchor(E, 'r', .5), '1', '1', 'starts')
    assoc(s, anchor(E, 'r', .85), anchor(F, 'l', .85), '', '', 'on expire', via=[(290, 320), (290, 345), (620, 345), (620, 300)], arrow=True)
    assoc(s, anchor(G, 'r', .5), anchor(H, 'l', .5), '1', '1', 'uses')
    assoc(s, anchor(G, 't', .5), anchor(E, 'b', .5), '', '', 'detection', arrow=True)
    assoc(s, anchor(I, 'l', .5), anchor(H, 'r', .5), '', '', 'enables', dashed=True)
    assoc(s, anchor(I, 't', .5), anchor(F, 'b', .5), '', '', '', dashed=True)
    s.save(*P('class_detect'))

def class3():
    s = Svg(900, 700)
    A = class_box(s, 20, 20, 230, 'Account', ['- uid: String', '- phone: String', '- name: String', '- template: String', '- defaultMode: SosMode'], ['+ signIn()', '+ recover()'])
    B = class_box(s, 330, 20, 230, 'Circle', ['- id: String', '- createdBy: String'], ['+ invite(phone)', '+ members()'])
    C = class_box(s, 650, 20, 230, 'Membership', ['- state: MemberState', '- sharing: bool', '- lastShared: DateTime'], ['+ accept()', '+ stopSharing()', '+ leave()'])
    D = class_box(s, 650, 230, 230, 'LocationShare', ['- lat, lng: double', '- publishedAt: DateTime', '- live: bool'], ['+ publish(point)', '+ freeze()'])
    E = class_box(s, 20, 230, 230, 'IncidentReport', ['- category: Category', '- geohash: String', '- createdAt: DateTime', '- note: String?'], ['+ submit()', '+ weight(now)'])
    F = class_box(s, 330, 230, 230, 'CellScore', ['- geohash: String', '- counts: Map', '- score: double'], ['+ recompute()'])
    G = class_box(s, 20, 430, 230, 'HelperProfile', ['- status: HelperStatus', '- verifiedAt: DateTime'], ['+ apply()', '+ revoke()'])
    H = class_box(s, 330, 430, 230, 'HelpRequest', ['- createdAt: DateTime', '- radius: int', '- status: String'], ['+ broadcast()', '+ accept(helper)'])
    I = class_box(s, 650, 430, 230, 'MissingChildReport', ['- status: ReportStatus', '- childName, age: ...', '- lastSeen: Place, Time', '- expiresAt: DateTime'], ['+ markFound()', '+ renew()', '+ expire()'])
    assoc(s, anchor(A, 'r', .3), anchor(B, 'l', .3), '1', '0..*', 'creates')
    assoc(s, anchor(B, 'r', .3), anchor(C, 'l', .3), '1', '2..*', 'has')
    assoc(s, anchor(C, 'b', .5), anchor(D, 't', .5), '1', '0..1', 'shares')
    assoc(s, anchor(A, 'b', .5), anchor(E, 't', .5), '1', '0..*', 'submits')
    assoc(s, anchor(E, 'r', .5), anchor(F, 'l', .5), '0..*', '1', 'counted in')
    assoc(s, (20, 110), (20, 470), '1', '0..1', '', via=[(7, 110), (7, 470)])
    assoc(s, anchor(G, 'r', .5), anchor(H, 'l', .5), '0..*', '0..*', 'responds to')
    assoc(s, anchor(A, 't', .8), anchor(I, 'r', .5), '1', '0..*', '', via=[(204, 8), (895, 8), (895, 495)])
    s.save(*P('class_community'))

# ------------------------------------------------------------------ sequence diagrams
def seqs():
    sequence(*P('seq_ssd_sos'), ['Primary User', 'Muhaffiz\n(system)', 'Trustee', 'Verified\nHelper'], [
        ('m', 0, 1, 'Hold SOS control (1 s)'), ('m', 1, 0, 'Loud: siren / Silent: none', True),
        ('m', 1, 2, 'SOS alert: location,\nmessage (SMS, push, email)'), ('m', 1, 3, 'Help request (if enabled)'),
        ('m', 2, 1, 'Acknowledge', True), ('m', 3, 1, 'Accept', True), ('m', 1, 0, 'Show acknowledgements', True)], colw=170)
    sequence(*P('seq_dispatch'), ['SOS\nController', 'Location\nService', 'Evidence\nRecorder', 'Delivery\nManager', 'SMS\nGateway', 'Firebase\n(FCM, Functions)'], [
        ('n', 0, 'Trigger accepted (UC-01)'), ('m', 0, 1, 'requestFix(10 s)'), ('m', 1, 0, 'fix or cached + age', True),
        ('m', 0, 2, 'start recording'), ('m', 0, 3, 'dispatch(event)'),
        ('f', 'par: automatic channels', 6, 8),
        ('m', 3, 4, 'send SMS (each trustee)'), ('m', 3, 5, 'push + email request'), ('m', 5, 3, 'accepted / error', True),
        ('m', 4, 3, 'sent / failed', True),
        ('f', 'alt: channel failed', 10, 11),
        ('m', 3, 3, 'enqueue for retry'), ('m', 3, 0, 'delivery statuses', True)], colw=130)
    sequence(*P('seq_auto'), ['Audio\nMonitor', 'Sound\nClassifier', 'Motion\nAnalyzer', 'Fusion\nRule', 'Countdown\nController', 'User', 'SOS\nController'], [
        ('m', 0, 0, 'level spike over ambient'), ('m', 0, 1, 'buffer (2 s, in memory)'), ('m', 1, 3, 'distress score'),
        ('m', 2, 3, 'motion anomaly?'), ('m', 3, 4, 'rule satisfied'),
        ('m', 4, 5, 'vibrate 20 s, show cancel'),
        ('f', 'alt: user cancels', 6, 7),
        ('m', 5, 4, 'tap cancel'), ('m', 4, 0, 'back to monitoring', True),
        ('f', 'else: no cancel', 9, 10),
        ('m', 4, 6, 'start SOS (automatic)'), ('n', 0, 'buffers discarded; nothing stored or sent')], colw=118)
    sequence(*P('seq_optout'), ['Member', 'Stop-sharing\nscreen', 'Keyword\nSpotter', 'Sharing\nManager', 'Firestore', 'Other\nmember'], [
        ('m', 0, 1, 'open Stop sharing'), ('m', 1, 2, 'setContext(confirm)'), ('m', 0, 2, 'speaks safe phrase'),
        ('m', 2, 1, 'phrase recognised', True), ('m', 1, 3, 'stopSharing()'), ('m', 3, 4, 'sharing=false,\nfreeze last location'),
        ('m', 1, 0, 'private confirmation', True), ('n', 5, 'no message or push to other members'),
        ('m', 4, 5, 'last location, "Not live"', True)], colw=135)
    sequence(*P('seq_escalate'), ['SOS\nController', 'Escalation\nManager', 'Firestore\n(acks)', 'User', 'SMS\nGateway', 'Authority\nContact'], [
        ('m', 0, 1, 'onDispatched(event)'), ('m', 1, 1, 'start 3-minute timer'),
        ('f', 'alt: acknowledgement arrives', 3, 4),
        ('m', 2, 1, 'ack recorded', True), ('m', 1, 1, 'stop timer'),
        ('f', 'else: timer expires', 6, 10),
        ('m', 1, 3, 'warning 30 s + cancel'), ('m', 3, 1, 'no cancel', True),
        ('m', 1, 4, 'escalation message'), ('m', 4, 5, 'SMS: location, time,\ntrigger, evidence flag'), ('m', 1, 1, 'write escalation log')], colw=132)
    sequence(*P('seq_queue'), ['Delivery\nManager', 'Outbound\nQueue (SQLite)', 'Connectivity\nMonitor', 'WorkManager', 'Firebase'], [
        ('m', 0, 1, 'enqueue(message)'), ('n', 0, 'Tier 1: SMS sent; other channels queued'),
        ('m', 2, 0, 'tier changed to 2 or 3'), ('m', 0, 3, 'schedule flush'), ('m', 3, 1, 'readDue()'),
        ('m', 1, 3, 'queued messages', True), ('m', 3, 4, 'send each message'), ('m', 4, 3, 'ok / error', True),
        ('f', 'alt: error', 9, 10),
        ('m', 3, 1, 'markAttempt, backoff'), ('m', 3, 1, 'markDelivered / update log')], colw=150)

# ------------------------------------------------------------------ state diagrams
def states():
    s = Svg(900, 440)
    dot(s, 30, 90); st = {}
    st['idle'] = state(s, 70, 65, 110, 50, 'Idle')
    st['cd'] = state(s, 250, 65, 150, 50, 'Countdown\n(20 s, automatic/voice)')
    st['act'] = state(s, 480, 65, 130, 50, 'Active\n(alarm, recording)')
    st['disp'] = state(s, 690, 65, 170, 50, 'Dispatching\n(channels, queue)')
    st['wait'] = state(s, 690, 200, 170, 50, 'Awaiting response\n(3-minute timer)')
    st['ack'] = state(s, 480, 200, 150, 50, 'Acknowledged')
    st['warn'] = state(s, 690, 330, 170, 50, 'Escalation warning\n(30 s)')
    st['esc'] = state(s, 480, 330, 150, 50, 'Escalated')
    st['can'] = state(s, 250, 200, 150, 50, 'Cancelled')
    st['closed'] = state(s, 250, 330, 150, 50, 'Closed')
    arrow(s, [(38, 90), (70, 90)], '')
    arrow(s, [(180, 80), (250, 80)], 'automatic or\nvoice trigger', toff=(0, -22))
    arrow(s, [(125, 65), (125, 30), (545, 30), (545, 65)], 'manual trigger', tpos=0.5, toff=(0, -10))
    arrow(s, [(400, 90), (480, 90)], 'no cancel', toff=(0, -10))
    arrow(s, [(325, 115), (325, 200)], 'user cancels', toff=(42, 0))
    arrow(s, [(610, 90), (690, 90)], 'dispatch', toff=(0, -10))
    arrow(s, [(775, 115), (775, 200)], 'sent / queued', toff=(40, 0))
    arrow(s, [(690, 225), (630, 225)], 'first ack', toff=(0, -10))
    arrow(s, [(775, 250), (775, 330)], 'timer expires', toff=(46, 0))
    arrow(s, [(690, 355), (630, 355)], 'no cancel', toff=(0, -10))
    arrow(s, [(480, 355), (400, 355)], 'logged', toff=(0, -10))
    arrow(s, [(325, 250), (325, 330)], 'closed', toff=(30, 0))
    arrow(s, [(555, 250), (555, 292), (380, 292), (380, 330)], 'closed', tpos=0.5, toff=(0, -9))
    arrow(s, [(690, 365), (560, 415), (325, 415), (325, 380)], 'user cancels warning', tpos=0.5, toff=(0, -10))
    s.save(*P('state_sos'))

    s = Svg(900, 360)
    dot(s, 30, 80)
    state(s, 70, 55, 120, 50, 'Not in circle'); state(s, 270, 55, 120, 50, 'Invited')
    state(s, 470, 55, 120, 50, 'Sharing', fill='#D8F0E4'); state(s, 470, 200, 120, 50, 'Stopped\n(last location, Not live)', size=10.5)
    state(s, 700, 130, 120, 50, 'Left circle')
    arrow(s, [(38, 80), (70, 80)]); arrow(s, [(190, 80), (270, 80)], 'invitation sent', toff=(0, -12))
    arrow(s, [(390, 80), (470, 80)], 'both accepted', toff=(0, -12))
    arrow(s, [(530, 105), (530, 200)], 'safe phrase\n(stop sharing)', toff=(56, 0))
    arrow(s, [(500, 200), (500, 105)], 'member resumes', toff=(-52, 0))
    arrow(s, [(590, 80), (700, 150)], 'leave circle', tpos=0.5, toff=(10, -14))
    arrow(s, [(590, 225), (700, 165)], 'leave circle', tpos=0.5, toff=(14, 12))
    arrow(s, [(330, 55), (330, 15), (130, 15), (130, 55)], 'declined / expired (7 days)', toff=(0, -10))
    s.save(*P('state_share'))

    s = Svg(900, 320)
    dot(s, 30, 80)
    state(s, 70, 55, 130, 50, 'Submitted'); state(s, 280, 55, 130, 50, 'Active', fill='#D8F0E4')
    state(s, 520, 20, 130, 50, 'Found'); state(s, 520, 140, 130, 50, 'Expired'); state(s, 520, 230, 130, 50, 'Removed (false)')
    arrow(s, [(38, 80), (70, 80)]); arrow(s, [(200, 80), (280, 80)], 'valid, alerts sent', toff=(0, -14))
    arrow(s, [(410, 70), (520, 45)], 'marked found', toff=(0, -12)); arrow(s, [(410, 95), (520, 165)], '72 h, no renewal', toff=(10, 12))
    arrow(s, [(345, 105), (345, 160), (410, 160), (410, 110)], 'renewed', toff=(0, 12))
    arrow(s, [(380, 105), (520, 255)], 'admin removes', toff=(-18, 12))
    s.text(700, 45, 'photo deleted; alerts stop', 10.5, anchor='start', italic=True); s.text(700, 165, 'photo deleted; alerts stop', 10.5, anchor='start', italic=True)
    s.save(*P('state_child'))

    s = Svg(900, 260)
    dot(s, 30, 80)
    state(s, 70, 55, 120, 50, 'Applied\n(pending)'); state(s, 290, 55, 130, 50, 'Verified Helper', fill='#D8F0E4'); state(s, 520, 55, 120, 50, 'Revoked')
    state(s, 290, 160, 130, 50, 'Rejected')
    arrow(s, [(38, 80), (70, 80)]); arrow(s, [(190, 80), (290, 80)], 'admin approves', toff=(0, -12))
    arrow(s, [(420, 80), (520, 80)], 'admin revokes', toff=(0, -12)); arrow(s, [(130, 105), (130, 185), (290, 185)], 'admin rejects', toff=(0, -10))
    s.text(160, 235, 'The identity image is deleted after the decision.', 10.5, italic=True, anchor='start')
    s.save(*P('state_helper'))

def make():
    class1(); class2(); class3(); seqs(); states()
if __name__ == '__main__': make(); print('ok')
