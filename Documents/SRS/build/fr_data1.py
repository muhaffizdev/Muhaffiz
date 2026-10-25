from fr_common import F

# ---------------------------------------------------------------- MOD-01 SOS Alert System
F(1,1,'Manual SOS Trigger',
  u='The Primary User shall be able to start an SOS by pressing and holding the SOS control on the home screen for 1 second, or by tapping the SOS action on the lock screen.',
  s='When the hold completes or the lock-screen action is tapped, the system shall start the SOS dispatch pipeline immediately, without a confirmation countdown, and record the trigger method as "manual". If the control is released before 1 second, no SOS shall start.',
  why='The control must be usable with one hand under stress; the 1-second hold prevents accidental starts from the home screen.',
  br='BR-01, BR-02', dep='FR-01.02, FR-14.01',
  acc=['Holding the control for 1 second starts the dispatch pipeline within 1 second.','Releasing at 0.5 seconds starts nothing.','The lock-screen action starts an SOS while the phone is locked.','The event log records the trigger method "manual".'])
F(1,2,'Multi-Channel Dispatch',
  u=None,
  s='When an SOS starts, the system shall send the user\'s location and the preset message to every trustee on each channel that the trustee has enabled: SMS sent by the device, push notification through FCM, email through a backend function, and a prefilled WhatsApp message. SMS, push and email shall be started in parallel without waiting for one another. The WhatsApp message shall be prepared through the WhatsApp share link and requires the user\'s confirmation to send; it shall not be used when the SOS is silent. If a channel fails, the remaining channels shall continue and the failure shall be logged.',
  why='Several channels raise the chance that a trustee sees the alert; automatic channels cannot depend on user interaction.',
  br='BR-04, BR-05, BR-06, BR-32', dep='FR-01.05, FR-12.01, FR-13.01',
  acc=['With two trustees on different channels, each receives the alert on its enabled channels.','The message contains coordinates, a map link, the time, the user\'s name and the preset text.','Disabling the network does not prevent SMS dispatch.','Failure of one channel does not stop the others.','No WhatsApp message is prepared in silent mode.'])
F(1,3,'Loud Alarm',
  u='The Primary User shall be able to stop the alarm with a single control on the SOS screen.',
  s='When an SOS starts in loud mode, the system shall play a siren through the alarm audio stream at maximum volume until the user stops it. The alarm shall not be played in silent mode.',
  why='A loud sound attracts the attention of people nearby.',
  br='BR-03', dep='FR-01.01',
  acc=['The siren starts within 1 second of the SOS start in loud mode.','The alarm stream is at its maximum volume while the siren plays.','The stop control ends the siren.','No siren is played in silent mode.'])
F(1,4,'Silent Mode',
  u='The Primary User shall be able to choose silent as the default SOS mode in the settings.',
  s='When an SOS is started in silent mode, by the setting or by the duress phrase, the system shall play no sound, shall not vibrate, shall show no SOS indication on the screen and shall use neutral wording in any system notification, while dispatch continues in the background.',
  why='A user who is hiding must not reveal that an alert is being sent.',
  br='BR-03', dep='FR-01.02, FR-03.04',
  acc=['No sound or vibration occurs during a silent SOS.','The screen shows no SOS text or alert colour.','The status bar notification text does not mention SOS or safety.','The event log shows dispatch on the enabled channels.'])
F(1,5,'Trustee Management',
  u='The Primary User shall be able to add, edit and remove trustees, and to choose for each trustee the channels (SMS, push, email, WhatsApp) on which alerts are sent.',
  s='When a trustee is saved, the system shall validate that the name is not empty and that the phone number is a valid mobile number, and shall store the channel preferences. If no channel is selected the system shall use SMS. The system shall require at least one trustee before the user completes onboarding and shall allow up to 10 trustees. Removing a trustee shall exclude that trustee from later alerts.',
  why='Alerts must reach people the user has chosen, over channels that suit each of them.',
  br='BR-04', dep='FR-14.03',
  acc=['An invalid phone number is rejected with an explanatory message.','A saved trustee appears in the list with its channels.','A removed trustee receives no later alert.','Onboarding cannot finish without one trustee.'])
F(1,6,'SOS Event Log',
  u='The Primary User shall be able to view a list of past SOS events.',
  s='For every SOS the system shall record the time, the location, the trigger method (manual, automatic or voice) and, for each trustee and channel, the delivery status, and shall update the status as it changes. The log shall be kept on the device.',
  why='The user needs to know whether and how an alert was delivered.',
  br='BR-05', dep='FR-01.02, FR-12.03', pri='Medium',
  acc=['Each SOS creates one log entry with time, location and trigger method.','Delivery status per channel changes from queued to sent or failed as events occur.','The log remains after the application is closed.'])

# ---------------------------------------------------------------- MOD-02 Automatic Danger Detection
F(2,1,'Ambient Monitoring Service',
  s='While microphone detection is enabled, the system shall run a low-power foreground service that measures the sound level of short audio frames in memory and discards each frame immediately. The service shall not classify audio until the level rises suddenly above the threshold relative to the recent ambient level. The service shall show a persistent notification, and shall restart after the device restarts.',
  why='Classification is expensive, so it must run only when something loud happens.',
  br='BR-07, BR-08, BR-09', dep='FR-15.02',
  acc=['In a quiet room no classification is started.','A sudden loud sound starts one classification.','No audio frame is written to storage.','After a restart the service resumes without opening the application.'])
F(2,2,'Distress Sound Classification',
  s='When the monitoring service reports a sudden loud sound, the system shall run the on-device sound classifier on the buffered burst and shall produce a distress score for sounds such as screaming and shouting. The system shall not transcribe speech and shall discard the buffer after classification.',
  why='Recognising a distress sound is a smaller problem than understanding speech and keeps the content of conversations private.',
  br='BR-07, BR-08', dep='FR-02.01',
  acc=['A labelled distress clip yields a score above the distress threshold.','A labelled non-distress loud clip yields a score below it.','No transcript is produced and no audio is stored.'])
F(2,3,'Motion-Signal Fusion',
  s='For the same time window, the system shall read the accelerometer and gyroscope, shall detect a sudden drop or struggle movement, and shall combine this with the audio score under the fusion rule of Section {sec:algorithms}. The system shall start the confirmation countdown only when the fusion rule is satisfied.',
  why='Using two independent signals reduces false alarms from loud but harmless sounds.',
  br='BR-02', dep='FR-02.02',
  acc=['A distress sound with no motion anomaly does not start the countdown unless the audio score is above the high-confidence threshold.','A distress sound with a motion anomaly starts the countdown.','Motion data are not stored.'])
F(2,4,'Confirmation Countdown',
  u='The Primary User shall be able to cancel a pending automatic, voice or duress alert during a 20-second countdown, by the cancel method that the user chose in the settings.',
  s='When the fusion rule is satisfied, or a safe phrase or the duress phrase is detected, the system shall start a countdown of 20 seconds. In a loud countdown the system shall vibrate with a mild pattern, make no sound and present a cancel control. In a silent countdown (the duress phrase, or silent mode) the system shall not vibrate, shall make no sound and shall show no indication of the countdown. In the settings the user shall be able to enable any of three cancel methods, and at least one shall always be enabled (the default is the swipe): swiping the cancel control away (in a silent countdown, a swipe gesture on the decoy screen that has no on-screen hint), speaking the safe phrase, or typing the safe phrase. If the user cancels, nothing shall be sent. If the 20 seconds pass without a cancel, the system shall start the SOS (FR-01.02) with the trigger method of the countdown.',
  why='An automated decision must not send an irreversible alert without a chance to stop it, and the cancel method must suit the situation of the user.',
  br='BR-01, BR-02, BR-03', dep='FR-02.03, FR-01.02, FR-03.05',
  acc=['The vibration of a loud countdown lasts 20 seconds and no sound is played.','A silent countdown has no vibration, sound or on-screen indication.','Each enabled cancel method (swipe, spoken safe phrase, typed safe phrase) stops the countdown and sends nothing.','A cancel method that is not enabled does not stop the countdown, and the last enabled method cannot be disabled.','Without a cancel the SOS starts after 20 seconds with the trigger method of the countdown.'])
F(2,5,'On-Device Processing Guarantee',
  s='The system shall confine the audio buffers, classifier output and sensor windows of this module to the device: the module shall make no network request and shall write no audio or sensor data to persistent storage.',
  why='Users consent to listening only because nothing leaves the phone.',
  br='BR-07, BR-08', dep='FR-02.01, FR-02.02, FR-02.03',
  acc=['A network capture during detection shows no traffic from the module.','Inspection of device storage after a detection shows no audio or sensor files.'])

# ---------------------------------------------------------------- MOD-03 Voice
F(3,1,'Safe-Phrase Enrolment',
  u='The Primary User shall be able to enter a safe phrase and confirm it by speaking it three times.',
  s='When the user submits a phrase of two to five words, the system shall check that it is not empty and differs from the duress phrase, shall collect three spoken samples to set the detection sensitivity, and shall store the phrase and its sensitivity on the device. If a sample is not recognised, the system shall ask the user to repeat it.',
  why='The user chooses a phrase that is memorable and that others cannot guess.',
  br='BR-07, BR-09', dep='FR-15.02',
  acc=['A phrase with one word or more than five words is rejected.','A phrase equal to the duress phrase is rejected.','After three recognised samples the phrase is saved.'])
F(3,2,'Duress-Phrase Enrolment',
  u='The Primary User shall be able to enter a second phrase, different from the safe phrase, that starts a silent SOS.',
  s='When the user submits the duress phrase, the system shall apply the same checks and sampling as FR-03.01 and shall additionally check that the phrase is not a substring of, and does not contain, the safe phrase.',
  why='A second phrase lets the user call for help silently while appearing to comply.',
  br='BR-03, BR-07', dep='FR-03.01',
  acc=['A duress phrase that contains the safe phrase is rejected.','After three recognised samples the phrase is saved.'])
F(3,3,'Offline Keyword Spotting',
  s='While voice activation is enabled, the system shall run an on-device keyword-spotting engine that listens for the enrolled phrases, needs no network, no account and no access key, performs no general speech transcription and stores no audio.',
  why='Voice activation must work where there is no connection.',
  br='BR-07, BR-08, BR-09', dep='FR-03.01, FR-03.02, FR-15.02',
  acc=['With the network disabled, a spoken safe phrase is detected.','Other speech does not produce a detection.','No audio is written to storage.'])
F(3,4,'Voice-Triggered SOS',
  s='When the safe phrase is detected outside a confirmation context, the system shall start the confirmation countdown of FR-02.04 and then an SOS in the user\'s default mode with trigger "voice". When the duress phrase is detected, the system shall start the same 20-second countdown in its silent form and then a silent SOS with trigger "voice".',
  why='Voice triggers reuse the same pipeline as automatic detection, so every trigger behaves in the same way.',
  br='BR-01, BR-02, BR-03', dep='FR-03.03, FR-02.04',
  acc=['The safe phrase starts the countdown and then a loud or silent SOS according to the default mode.','The duress phrase starts a silent countdown and then always results in a silent SOS.','Cancelling during the countdown, by an enabled method, sends nothing.'])
F(3,5,'Shared Duress-Confirmation Hook',
  s='The system shall expose phrase detections as events to other modules. When the stop-sharing screen of FR-05.02 is open, the safe phrase shall be delivered to that module as a confirmation and shall not start an SOS. When a countdown is running and speaking the safe phrase is an enabled cancel method (FR-02.04), the safe phrase shall be delivered to the countdown as a cancel and shall not start an SOS. When the duress phrase is detected the system shall inform Decoy Mode (FR-06.01).',
  why='One engine for all duress-sensitive actions keeps their behaviour consistent.',
  br='BR-01, BR-02, BR-11, BR-28', dep='FR-03.03, FR-02.04, FR-05.02, FR-06.01',
  acc=['The safe phrase spoken on the stop-sharing screen unlocks the sharing toggle and starts no SOS.','The safe phrase spoken during a countdown cancels it when the spoken cancel method is enabled.','The same phrase spoken elsewhere starts the voice SOS countdown.','The duress phrase causes the decoy screen to appear.'])

# ---------------------------------------------------------------- MOD-04 Family Circle
F(4,1,'Circle Creation and Bilateral Invitation',
  u='The Primary User shall be able to create a family circle and invite a person by phone number, and the invited person shall be able to accept or decline.',
  s='When a circle is created or an invitation is sent, the system shall store the invitation as pending and shall start no sharing. Sharing between the two people shall begin only after the invited person accepts and the inviter\'s own sharing is enabled. A pending invitation shall expire after 7 days.',
  why='Both people must agree before anyone can see anyone\'s location.',
  br='BR-10', dep='FR-14.01',
  acc=['No location is shared while the invitation is pending.','Sharing begins after the invitee accepts.','A declined or expired invitation leaves no sharing.'])
F(4,2,'Circle Membership List',
  u='The Primary User shall be able to view all members of a circle.',
  s='The system shall show each member\'s name, current sharing status (sharing or stopped) and the time of the last location update, and shall update the list in real time.',
  why='Members must always be able to see who is in the circle and who is sharing.',
  br='BR-13', dep='FR-05.05',
  acc=['Each member appears with a status and a last-update time.','A status change on one device appears on the others within the target of NFR-PER-04.'])
F(4,3,'Leave a Circle',
  u='The Primary User shall be able to leave a circle completely.',
  s='When the user confirms, the system shall remove the user from the circle, stop publishing their location and delete their stored location from the circle. Leaving shall be separate from stopping sharing. The system shall not send a notification about the departure.',
  why='A person must be able to end their membership without anyone\'s approval.',
  br='BR-14', dep='FR-04.01',
  acc=['After leaving, the user no longer appears in the other members\' list.','The stored location of the user is deleted.','No push notification about leaving is sent.'])

# ---------------------------------------------------------------- MOD-05 Location sharing
F(5,1,'Movement-Based Location Updates',
  s='While a member\'s sharing is enabled, the system shall publish the member\'s location when the device has moved more than the movement threshold since the last published location, and shall not run continuous GPS polling.',
  why='Updating on significant movement saves battery.',
  br='BR-13', dep='FR-04.01, FR-15.02',
  acc=['A stationary device publishes no new location.','A move beyond the threshold publishes a location.','The published document holds a time stamp.'])
F(5,2,'Stop Sharing by Safe Phrase and Toggle',
  u='The Primary User shall be able to stop sharing their location by speaking the safe phrase on the stop-sharing screen and then switching the sharing toggle off.',
  s='When the stop-sharing screen is open, the system shall keep its sharing toggle locked and shall listen for the safe phrase. When the safe phrase is recognised, the system shall unlock the toggle. When the user switches the toggle off, the system shall disable the user\'s sharing immediately, shall require no approval from any other person and shall notify no other member. If the phrase is not recognised within 15 seconds, the screen shall close and sharing shall continue.',
  why='Stopping must be quick and must not depend on anyone else, and the spoken phrase prevents another person from switching sharing off by chance or by force.',
  br='BR-11', dep='FR-03.05, FR-05.01',
  acc=['The toggle stays locked until the safe phrase is recognised.','Switching the toggle off after the phrase stops publication of location at once.','No message is sent to other members.','An unrecognised phrase leaves sharing on.'])
F(5,3,'Private Opt-Out Confirmation',
  s='After sharing stops, the system shall show a confirmation only on the device of the member who stopped it. The system shall create no message, notification or visible event for other members.',
  why='A visible "opted out" message could provoke confrontation.',
  br='BR-11', dep='FR-05.02',
  acc=['The confirmation appears only on the stopping member\'s device.','Other members\' devices show no event when sharing stops.'])
F(5,4,'Last-Known Location Display',
  u='A Family Circle Member shall be able to see where another member last shared their location.',
  s='After a member stops sharing, the system shall show to the other members only the last published location with its time stamp, labelled "Not live", and shall publish no further updates.',
  why='A stale location with a clear time stamp cannot be mistaken for live tracking.',
  br='BR-12', dep='FR-05.01',
  acc=['The marker is labelled "Not live" with the time of the last update.','The marker does not move after sharing stops.'])
F(5,5,'Real-Time Sharing Status',
  u='A Family Circle Member shall be able to see at all times whether they and the other members are sharing.',
  s='The system shall propagate each sharing change to the circle through real-time listeners, shall show a persistent indicator on the member\'s own device while their location is being shared, and shall provide no mode that shares location without that indicator. Only the member shall be able to resume their own sharing.',
  why='Hidden or silent tracking must be impossible.',
  br='BR-13', dep='FR-04.02',
  acc=['The indicator is present on the sharing member\'s device whenever location is published.','No other member can switch another member\'s sharing on.','A change is visible on the other devices within the target of NFR-PER-04.'])

# ---------------------------------------------------------------- MOD-06 Decoy Mode
F(6,1,'Disguised Interface',
  u='The Primary User shall be able to turn on Decoy Mode in the settings.',
  s='When Decoy Mode is on, and when a silent SOS is started by the duress phrase, the system shall show a neutral calculator screen in place of the real interface whenever the application is opened. The decoy screen shall contain no reference to safety.',
  why='If someone forces the user to unlock the phone, the application must not reveal its purpose.',
  br='BR-28', dep='FR-03.05',
  acc=['With Decoy Mode on, opening the application shows the calculator.','The calculator performs basic arithmetic.','A duress-phrase SOS switches the application to the decoy screen.'])
F(6,2,'Hidden Re-entry Gesture',
  u='The Primary User shall be able to return to the real application by a hidden gesture.',
  s='When the user presses and holds the equals key of the decoy calculator for 2 seconds, the system shall show the real interface. No other action shall reveal it.',
  why='The genuine user must be able to get back without an obvious control.',
  br='BR-28', dep='FR-06.01',
  acc=['A 2-second hold on the equals key opens the real application.','A short press on the equals key only calculates.'])
F(6,3,'Background Pass-Through',
  s='While the decoy screen is shown, the system shall continue SOS triggers, voice detection, location updates and evidence recording without any visible sign.',
  why='Protection must not stop because the interface is disguised.',
  br='BR-28', dep='FR-06.01, FR-03.03',
  acc=['The duress phrase starts a silent SOS while the decoy screen is shown.','Location updates continue under the decoy screen.'])
