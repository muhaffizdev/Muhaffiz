from gvdiag import *

def architecture():
    n = lambda id_, label, **kw: '%s [label="%s"%s];' % (id_, label, ''.join(', %s="%s"' % (k, v) for k, v in kw.items()))
    app = ''
    app += cluster('pres', 'Presentation layer', n('screens', 'Screens and widgets\\n(Home, Family, Map, Library, More)') + n('prov', 'State providers\\n(Riverpod)') + '{rank=same; screens; prov}', fill='#F3F8FB', color=BLUE, pen=1.4)
    app += cluster('appl', 'Application layer', ''.join([n('trig', 'TriggerEngine'), n('sos', 'SosOrchestrator'), n('del', 'DeliveryManager'), n('esc', 'EscalationManager'), n('shr', 'SharingManager'), n('cons', 'ConsentManager')]) + '{rank=same; trig; sos; del; esc; shr; cons}', fill='#F3F8FB', color=BLUE, pen=1.4)
    app += cluster('data', 'Domain and data layer', ''.join([n('ldb', 'Local repositories\\n(SQLite via Drift)'), n('vault', 'Evidence vault\\n(AES-256-GCM files)'), n('rrepo', 'Remote repositories\\n(Firestore, Storage, Functions)'), n('lcache', 'Location cache')]) + '{rank=same; ldb; vault; rrepo; lcache}', fill='#FFFBEF', color=AMBER, pen=1.4)
    app += cluster('ml', 'On-device intelligence', ''.join([n('cls', 'Sound classifier\\n(TFLite)'), n('kws', 'Keyword spotter\\n(offline)'), n('emb', 'Sentence embedder\\n(library search)')]) + '{rank=same; cls; kws; emb}', fill='#F3F8FB', color=BLUE, pen=1.4)
    app += cluster('plat', 'Platform layer (Kotlin, platform channels)', ''.join([n('fg', 'Foreground\\nservices'), n('smsm', 'SMS manager'), n('sens', 'Audio and\\nmotion sensors'), n('loc', 'Fused location'), n('ks', 'Android Keystore'), n('wm', 'WorkManager'), n('alias', 'Launcher\\naliases')]) + '{rank=same; fg; smsm; sens; loc; ks; wm; alias}', fill='#F3F8FB', color=BLUE, pen=1.4)
    fb = cluster('fb', 'Firebase backend', ''.join([n('auth', 'Authentication'), n('fs', 'Cloud Firestore\\n+ security rules'), n('fcm', 'Cloud Messaging'), n('stor', 'Cloud Storage\\n+ storage rules'), n('fn', 'Cloud Functions'), n('host', 'Hosting')]) + '{rank=same; auth; fs; fcm}{rank=same; stor; fn; host}', fill='#F1FAF7', color=TEAL, pen=2)
    web = cluster('web', 'Web front ends', n('admin', 'Admin website\\nmuhaffiz.me (Flutter web)') + n('alertp', 'Alert page for trustees\\n(Firebase Hosting)'), fill='#F1FAF7', color=TEAL, pen=1.4)
    ext = ''.join([n('sms', 'Cellular SMS network', fillcolor=LAMBER, color=AMBER), n('wa', 'WhatsApp', fillcolor=LAMBER, color=AMBER), n('gmap', 'Google Maps Platform', fillcolor=LAMBER, color=AMBER), n('omap', 'Open map-data source', fillcolor=LAMBER, color=AMBER), n('mail', 'Email service', fillcolor=LAMBER, color=AMBER)])
    cluster_app = cluster('app', 'Android application (Flutter)', app, fill='#FFFFFF', color=TEAL, pen=2.2)
    edges = '''
 screens -> trig [ltail=cluster_pres, lhead=cluster_appl, label="  events, state"];
 trig -> cls [ltail=cluster_appl, lhead=cluster_ml, style=invis];
 sos -> ldb [ltail=cluster_appl, lhead=cluster_data, label="  repositories"];
 ldb -> cls [ltail=cluster_data, lhead=cluster_ml, label="  models, results"];
 cls -> fg [ltail=cluster_ml, lhead=cluster_plat, label="  audio, sensors"];
 rrepo -> fs [lhead=cluster_fb, label="  HTTPS,\\n  real-time"];
 fn -> mail [label="email"];
 smsm -> sms [label="SMS", ltail=cluster_plat];
 alias -> wa [label="share link", style=invis];
 admin -> fs [label="HTTPS", lhead=cluster_fb];
 host -> alertp [label="serves", style=dashed];
 ldb -> omap [style=invis];
'''
    dot = 'digraph architecture {\n' + style('TB', nodesep=0.3, ranksep=0.55) + cluster_app + fb + web + ext + edges + '}\n'
    return render('architecture', dot)

if __name__ == '__main__': print(architecture())
