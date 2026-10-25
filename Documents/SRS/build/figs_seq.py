from seq2 import sequence

def make():
    sequence('seq_ssd_sos', [('Primary User', 'actor'), ('Muhaffiz\n(system)', 'obj'), ('Trustee', 'actor'), ('Verified\nHelper', 'actor')], [
        ('m', 0, 1, 'Hold the SOS control for 1 second'),
        ('m', 1, 0, 'Siren (loud) or no indication (silent)', 'ret'),
        ('m', 1, 2, 'SOS alert: location, time, message (SMS, push, email)'),
        ('m', 1, 3, 'Help request with distance and age (if enabled)'),
        ('m', 2, 1, 'Acknowledge', 'ret'),
        ('m', 3, 1, 'Accept request', 'ret'),
        ('m', 1, 0, 'Show acknowledgements on the SOS screen', 'ret'),
        ('act', 1, 0, 6),
    ], colw=195)

    sequence('seq_dispatch', [('SOS\nController', 'obj'), ('Location\nService', 'obj'), ('Evidence\nRecorder', 'obj'), ('Delivery\nManager', 'obj'), ('SMS\nGateway', 'ext'), ('Firebase\n(Functions, FCM)', 'db')], [
        ('note', 0, 1, 'Trigger accepted (UC-01); mode and trigger recorded'),
        ('m', 0, 1, 'requestFix(T_fix = 10 s)'),
        ('m', 1, 0, 'fresh fix, or cached location with its age', 'ret'),
        ('m', 0, 2, 'startRecording(event)'),
        ('m', 0, 3, 'dispatch(event, location)'),
        ('m', 3, 4, 'send SMS to each trustee'),
        ('m', 3, 5, 'push and email requests (API-01, API-02)'),
        ('m', 4, 3, 'sent / failed', 'ret'),
        ('m', 5, 3, 'accepted / error', 'ret'),
        ('self', 3, 'enqueue failed items for retry'),
        ('m', 3, 0, 'delivery status per trustee and channel', 'ret'),
        ('frame', 'par', [('automatic channels in parallel', 5, 8)]),
        ('frame', 'alt', [('a channel failed', 9, 9)]),
        ('act', 3, 4, 10), ('act', 0, 0, 10),
    ], colw=134)

    sequence('seq_auto', [('Audio\nMonitor', 'obj'), ('Sound\nClassifier', 'obj'), ('Motion\nAnalyzer', 'obj'), ('Fusion\nRule', 'obj'), ('Countdown\nController', 'obj'), ('Primary User', 'actor'), ('SOS\nController', 'obj')], [
        ('self', 0, 'level exceeds ambient by D_spike for two frames'),
        ('m', 0, 1, 'burst (2 s, in memory only)'),
        ('m', 1, 3, 'distress score (0 to 1)'),
        ('m', 0, 2, 'read motion window (5 s)'),
        ('m', 2, 3, 'motion anomaly: yes / no', 'ret'),
        ('m', 3, 4, 'rule satisfied: begin(automatic)'),
        ('m', 4, 5, '20 s countdown; cancel by swipe, spoken or typed phrase'),
        ('m', 5, 4, 'cancel (swipe, spoken or typed phrase)'),
        ('m', 4, 0, 'back to monitoring; nothing sent', 'ret'),
        ('m', 4, 6, 'start SOS (trigger = automatic)'),
        ('note', 0, 1, 'The burst, score and sensor window are discarded after the decision'),
        ('frame', 'alt', [('user cancels within 20 s', 7, 8), ('no cancel within 20 s', 9, 9)]),
    ], colw=118)

    sequence('seq_voice', [('Primary User', 'actor'), ('Keyword\nSpotter', 'obj'), ('Trigger\nEngine', 'obj'), ('Countdown\nController', 'obj'), ('SOS\nController', 'obj'), ('Decoy\nMode', 'obj')], [
        ('m', 0, 1, 'speaks the safe or the duress phrase'),
        ('self', 1, 'match against enrolled phrases (offline)'),
        ('m', 1, 2, 'phraseDetected(type, context)'),
        ('note', 1, 2, 'In the stop-sharing context the safe phrase unlocks the toggle (UC-09)'),
        ('m', 2, 3, 'begin(voice, mode)'),
        ('m', 3, 0, '20 s countdown (silent for duress)'),
        ('m', 0, 3, 'cancel: swipe, spoken or typed phrase'),
        ('m', 3, 2, 'cancelled; nothing sent', 'ret'),
        ('m', 3, 4, 'start SOS (voice): default mode, or silent for the duress phrase'),
        ('m', 2, 5, 'show decoy screen'),
        ('frame', 'alt', [('user cancels', 6, 7), ('no cancel', 8, 8)]),
        ('frame', 'opt', [('duress phrase', 9, 9)]),
    ], colw=134)

    sequence('seq_optout', [('Family Circle\nMember', 'actor'), ('Stop-sharing\nscreen', 'obj'), ('Keyword\nSpotter', 'obj'), ('Sharing\nManager', 'obj'), ('Firestore', 'db'), ('Other member\n(device)', 'obj')], [
        ('m', 0, 1, 'open Stop sharing'),
        ('m', 1, 2, 'setContext(stopSharing)'),
        ('m', 0, 2, 'speaks the safe phrase'),
        ('m', 2, 1, 'phrase recognised; unlock toggle', 'ret'),
        ('m', 0, 1, 'switch the toggle off'),
        ('m', 1, 3, 'stopSharing()'),
        ('m', 3, 4, 'sharing = false; freeze last location'),
        ('m', 3, 1, 'stopped', 'ret'),
        ('m', 1, 0, 'private confirmation on this device only', 'ret'),
        ('note', 4, 5, 'No message, push or event about the opt-out is sent to other members'),
        ('m', 4, 5, 'listener: last location with time, "Not live"', 'ret'),
        ('m', 1, 0, 'screen closes; sharing continues', 'ret'),
        ('frame', 'alt', [('safe phrase heard within 15 s', 3, 10), ('no phrase within 15 s', 11, 11)]),
    ], colw=134)

    sequence('seq_escalate', [('SOS\nController', 'obj'), ('Escalation\nManager', 'obj'), ('Firestore\n(acknowledgements)', 'db'), ('Primary User', 'actor'), ('SMS\nGateway', 'ext'), ('Authority\nContact', 'actor')], [
        ('m', 0, 1, 'onDispatched(event)'),
        ('self', 1, 'start timer T_ack = 3 minutes'),
        ('m', 2, 1, 'acknowledgement recorded (listener)', 'ret'),
        ('self', 1, 'stop timer; no escalation'),
        ('m', 1, 3, 'warning for 30 s with one-tap cancel (vibration only if silent)'),
        ('m', 3, 1, 'cancel'),
        ('self', 1, 'log "cancelled"; no escalation'),
        ('m', 1, 4, 'escalation message(s) by the configured channel'),
        ('m', 4, 5, 'SMS: location, time, trigger, evidence flag'),
        ('self', 1, 'write escalation log; show status to the user'),
        ('frame', 'alt', [('acknowledgement within 3 minutes', 2, 3), ('timer expires', 4, 4)]),
        ('frame', 'alt', [('user cancels the warning', 5, 6), ('no cancel within 30 s', 7, 9)]),
    ], colw=134)

    sequence('seq_queue', [('Delivery\nManager', 'obj'), ('Outbound queue\n(SQLite)', 'db'), ('Connectivity\nMonitor', 'obj'), ('WorkManager', 'obj'), ('Firebase', 'ext')], [
        ('m', 0, 1, 'enqueue(message, channel)'),
        ('note', 0, 1, 'Tier 1: SMS is sent at once; push, email and Near Help are queued'),
        ('m', 2, 0, 'tierChanged(2 or 3)'),
        ('m', 0, 3, 'scheduleFlush()'),
        ('m', 3, 1, 'readDue()'),
        ('m', 1, 3, 'queued messages', 'ret'),
        ('m', 3, 4, 'send message'),
        ('m', 4, 3, 'ok / error', 'ret'),
        ('m', 3, 1, 'markDelivered(); update the SOS log'),
        ('m', 3, 1, 'markAttempt(); next delay = min(2 x d, 15 min)'),
        ('frame', 'loop', [('for each queued message', 6, 9)]),
        ('frame', 'alt', [('ok', 8, 8), ('error', 9, 9)]),
    ], colw=158)

    sequence('seq_invite', [('Inviter', 'actor'), ('Inviter\napplication', 'obj'), ('Firestore', 'db'), ('Messaging\n(FCM / SMS)', 'ext'), ('Invitee\napplication', 'obj'), ('Invitee', 'actor')], [
        ('m', 0, 1, 'invite(phone number)'),
        ('m', 1, 2, 'create Invitation (pending, expires in 7 days)'),
        ('m', 2, 3, 'notify the invitee'),
        ('m', 3, 4, 'push, or SMS if there is no account'),
        ('m', 5, 4, 'accept'),
        ('m', 4, 2, 'Membership created; Invitation = accepted'),
        ('m', 2, 1, 'listener: new member', 'ret'),
        ('m', 1, 0, 'member list updated', 'ret'),
        ('m', 5, 4, 'decline'),
        ('m', 4, 2, 'Invitation = declined (or expired after 7 days)'),
        ('note', 1, 4, 'No location is shared until each member enables their own sharing'),
        ('frame', 'alt', [('invitee accepts', 4, 7), ('invitee declines, or 7 days pass', 8, 9)]),
    ], colw=134)

    sequence('seq_nearhelp', [('Requester\napplication', 'obj'), ('Cloud\nFunction', 'obj'), ('Firestore', 'db'), ('Cloud\nMessaging', 'ext'), ('Helper\napplication', 'obj'), ('Verified\nHelper', 'actor')], [
        ('m', 0, 1, 'POST /v1/help-requests {lat, lng}'),
        ('m', 1, 2, 'query Verified Helpers within R_help = 1 km (geohash)'),
        ('m', 2, 1, 'helper tokens', 'ret'),
        ('m', 1, 3, 'push: distance and age, no exact location'),
        ('m', 3, 4, 'notification'),
        ('m', 5, 4, 'accept'),
        ('m', 4, 2, 'write acknowledgement; reveal exact location to this helper'),
        ('m', 2, 0, 'listener: a helper accepted', 'ret'),
        ('self', 0, 'show "unavailable, no connection"; queue the request'),
        ('frame', 'alt', [('data connection available', 0, 7), ('no connection', 8, 8)]),
    ], colw=134)

    sequence('seq_child', [('Guardian', 'actor'), ('Application', 'obj'), ('Cloud\nStorage', 'db'), ('Firestore', 'db'), ('Cloud\nFunction', 'obj'), ('Trustees and\nhelpers (5 km)', 'ext'), ('Administrator', 'actor')], [
        ('m', 0, 1, 'fill in the form; confirm guardianship; submit'),
        ('self', 1, 'validate fields and photo (5 MB)'),
        ('m', 1, 2, 'upload photo (restricted access)'),
        ('m', 1, 3, 'create report (status = active)'),
        ('m', 3, 4, 'trigger: report created'),
        ('m', 4, 5, 'alert: description, last seen, contact number'),
        ('m', 4, 6, 'add to moderation queue'),
        ('m', 6, 4, 'remove as false report'),
        ('m', 4, 3, 'delete report; suspend author'),
        ('m', 0, 1, 'mark as found (or 72 h pass without renewal)'),
        ('m', 1, 3, 'status = found or expired'),
        ('m', 3, 4, 'trigger: status changed'),
        ('m', 4, 2, 'delete photo; stop alerts'),
        ('frame', 'opt', [('administrator finds the report false', 7, 8)]),
        ('frame', 'opt', [('guardian marks found, or report expires', 9, 12)]),
    ], colw=116)

    sequence('seq_search', [('Primary User', 'actor'), ('Search\nscreen', 'obj'), ('Sentence\nembedder', 'obj'), ('Embedding index\n(bundled)', 'db'), ('Keyword\nsearch', 'obj')], [
        ('m', 0, 1, 'types a query in their own words'),
        ('m', 1, 2, 'embed(query)'),
        ('m', 2, 1, 'vector with 384 values', 'ret'),
        ('m', 1, 3, 'cosine similarity with every item'),
        ('m', 3, 1, 'items ranked by similarity', 'ret'),
        ('m', 1, 0, 'ranked cards with relevance indicators', 'ret'),
        ('m', 1, 4, 'search titles, summaries and text'),
        ('m', 4, 1, 'matching items', 'ret'),
        ('m', 1, 0, 'results with a notice', 'ret'),
        ('frame', 'alt', [('model available and best similarity at least 0.30', 1, 5), ('model missing or similarity below 0.30', 6, 8)]),
    ], colw=158)

    sequence('seq_helper', [('Applicant', 'actor'), ('Application', 'obj'), ('Cloud\nStorage', 'db'), ('Firestore', 'db'), ('Admin\nwebsite', 'obj'), ('Administrator', 'actor')], [
        ('m', 0, 1, 'submit name, phone and identity photo'),
        ('m', 1, 2, 'upload identity image (administrators only)'),
        ('m', 1, 3, 'HelperProfile (status = pending)'),
        ('m', 5, 4, 'open the helper review queue'),
        ('m', 4, 3, 'read pending applications'),
        ('m', 4, 2, 'read the identity image'),
        ('m', 5, 4, 'decision: approve, reject or revoke'),
        ('m', 4, 3, 'status updated; AdminDecision logged'),
        ('m', 4, 2, 'delete the identity image'),
        ('m', 3, 1, 'listener: new status', 'ret'),
        ('m', 1, 0, 'notify the applicant', 'ret'),
    ], colw=145)

    sequence('seq_report', [('Primary User', 'actor'), ('Application', 'obj'), ('Firestore', 'db'), ('Scheduled\nfunction', 'obj')], [
        ('m', 0, 1, 'choose category; confirm or move the location'),
        ('self', 1, 'rate limit: at most 5 in 24 h; no duplicate within 100 m and 1 h'),
        ('m', 1, 2, 'write IncidentReport (geohash7, time)'),
        ('m', 3, 2, 'read reports of changed cells'),
        ('self', 3, 'score = sum of 0.5 ^ (age / 90 days)'),
        ('m', 3, 2, 'write CellScore (counts, score)'),
        ('m', 0, 1, 'open the Danger map'),
        ('m', 1, 2, 'read CellScores for the viewport'),
        ('m', 2, 1, 'scores and category counts', 'ret'),
        ('m', 1, 0, 'cells drawn from green to red; zone panel on tap', 'ret'),
        ('frame', 'loop', [('scheduled aggregation', 3, 5)]),
    ], colw=195)

    sequence('seq_signin', [('Primary User', 'actor'), ('Application', 'obj'), ('Firebase\nAuthentication', 'db'), ('Firestore', 'db')], [
        ('m', 0, 1, 'enter mobile number'),
        ('m', 1, 2, 'verifyPhoneNumber(number)'),
        ('m', 2, 0, 'one-time code by SMS', 'ret'),
        ('m', 0, 1, 'enter the code'),
        ('m', 1, 2, 'confirm code'),
        ('m', 2, 1, 'ID token', 'ret'),
        ('m', 1, 3, 'read or create Account'),
        ('m', 3, 1, 'profile', 'ret'),
        ('m', 1, 0, 'Home screen', 'ret'),
        ('m', 2, 1, 'error; after five wrong codes sending is blocked for 10 minutes', 'ret'),
        ('frame', 'alt', [('code is correct', 5, 8), ('code is wrong', 9, 9)]),
    ], colw=195)

if __name__ == '__main__': make(); print('ok')
