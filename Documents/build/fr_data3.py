from fr_common import F

# ---------------------------------------------------------------- MOD-15 Consent and Privacy
F(15,1,'Onboarding Consent',
  u='The Primary User shall be able to read, and accept or decline, a plain-language statement of what the detection and voice engines listen for.',
  s='During onboarding the system shall explain that the microphone is used to detect distress sounds and the enrolled phrases, that this processing stays on the device, that no audio is stored by these engines, that location is shared only as the user chooses, and that evidence recording begins only after an SOS starts. The system shall enable no microphone function until the user accepts.',
  why='Listening needs informed consent.',
  br='BR-09', dep='-',
  acc=['The consent text covers detection, voice, location and evidence recording.','Declining leaves the microphone functions off.','The acceptance and its time are stored.'])
F(15,2,'Permission and Feature Toggles',
  u='The Primary User shall be able to turn microphone detection and voice activation on or off separately at any time, and to turn location sharing on at any time and off through the stop-sharing screen.',
  s='When a toggle changes, the system shall apply it immediately, shall stop the related service when the toggle is turned off and shall ask for the required Android permission when it is turned on.',
  why='Users must stay in control of each sensor.',
  br='BR-09', dep='FR-15.01',
  acc=['Turning microphone detection off stops the monitoring service.','Switching the sharing toggle off on the stop-sharing screen (FR-05.02) stops location publication.','Each toggle works independently of the others.'])
F(15,3,'Privacy Summary',
  u='The Primary User shall be able to view a summary of what the application stores, what stays on the device and what reaches the backend.',
  s='The system shall present a summary screen that lists, in plain language, the data held on the server (profile, trustees, circles, shared locations, reports and helper status), the data that stays on the device (audio buffers, evidence recordings, library, models and event log) and the data sent to external channels during an SOS.',
  why='Transparency builds trust.',
  br='BR-07, BR-32', dep='-',
  acc=['The summary names the three categories of data.','The summary matches the behaviour of the application.'])

# ---------------------------------------------------------------- MOD-16 Admin Dashboard
F(16,1,'User Overview',
  u='The Administrator shall be able to view the number of registrations over time and the verification status of helpers.',
  s='The system shall show registration counts by day, counts of helper applications by status and a user list with masked phone numbers. It shall show no message content, location or evidence.',
  why='Administrators need an overview without access to private content.',
  br='BR-31', dep='FR-16.05',
  acc=['Phone numbers are masked.','No location or evidence data appears.'])
F(16,2,'Moderation Queue',
  u='The Administrator shall be able to review flagged heatmap reports and missing-child reports and approve, remove or suspend the author.',
  s='The system shall list flagged reports with their content, let the administrator decide, apply the decision and record the administrator, time and decision.',
  why='Crowd-sourced content needs human moderation.',
  br='BR-15, BR-27, BR-31', dep='FR-07.05, FR-17.05, FR-16.05',
  acc=['A flagged report appears in the queue.','A removed report no longer counts in the heatmap.','The decision is logged with administrator and time.'])
F(16,3,'Helper Review Queue',
  u='The Administrator shall be able to approve, reject or revoke a Verified Helper.',
  s='The system shall show each pending application with the identity image, apply the decision, notify the applicant, delete the identity image and record the decision.',
  why='Only checked people should receive help requests.',
  br='BR-18, BR-31', dep='FR-08.01, FR-16.05',
  acc=['An approved helper starts receiving requests.','A revoked helper stops receiving requests.','The identity image is deleted after the decision.'])
F(16,4,'Health Monitoring',
  u='The Administrator shall be able to view delivery success by channel and backend errors.',
  s='The system shall aggregate delivery outcomes per channel and shall list backend function errors with time and function name, without user identities.',
  why='Reliability of delivery is a core objective and must be observable.',
  br='BR-31', dep='FR-01.06, FR-16.05',
  acc=['Delivery success is shown per channel for a chosen period.','Backend errors are listed with time and function name.'])
F(16,5,'Administrator Authentication',
  s='The system shall allow access to the admin website only to accounts that have the administrator role, shall sign in with email and password through Firebase Authentication, and shall deny every other account.',
  why='Administrative functions must be separated from ordinary users.',
  br='BR-31', dep='DEP-1',
  acc=['An ordinary user account cannot open any admin page.','An administrator account can.'], src='Added during specification: needed to protect FR-16.01 to FR-16.04')

# ---------------------------------------------------------------- MOD-17 Missing-Child Report
F(17,1,'Missing-Child Report Form',
  u='The Guardian shall be able to report a missing child by entering the child\'s name and age, a photo, a description, the last-seen place and time, and the guardian\'s contact number.',
  s='When the guardian submits the form, the system shall validate that all required fields are present, that the age is between 0 and 17, that the photo is a JPEG or PNG of at most 5 MB and that the guardian has confirmed being the child\'s guardian, and shall create the report with the status "active".',
  why='A complete report helps others recognise the child.',
  br='BR-25, BR-26, BR-27', dep='FR-14.01',
  acc=['A report with a missing field is rejected.','A photo larger than 5 MB is rejected.','A valid report has the status "active".'])
F(17,2,'Alert to Contacts and Nearby Helpers',
  s='When a report becomes active, the system shall send it to the guardian\'s trustees and by push notification to Verified Helpers within 5 km of the last-seen place. The notification shall show the description, the last-seen place and time and the guardian\'s contact number.',
  why='Quick local attention is most useful in the first hours.',
  br='BR-26, BR-32', dep='FR-17.01, FR-08.01, FR-12.01',
  acc=['Trustees and helpers within 5 km are notified.','Helpers beyond 5 km are not.'])
F(17,3,'Report Status Handling',
  u='The Guardian shall be able to mark a report as found, or renew it.',
  s='The system shall set the status to "found" when the guardian marks it, and to "expired" 72 hours after it was created or renewed unless the guardian renews it. When a report is found or expired the system shall stop alerts and shall delete the photo.',
  why='Reports must not stay active after the child is found.',
  br='BR-25, BR-26', dep='FR-17.01',
  acc=['"Found" stops alerts and deletes the photo.','After 72 hours without renewal the status is "expired".'])
F(17,4,'Hand-Off to Official Channels',
  u='The Guardian shall be able to call an official missing-child helpline or share the report text.',
  s='The system shall provide a call control for the configured helpline number (default 1099) and a share control that opens the Android share sheet with the report text. The system shall make no direct connection to any official system.',
  why='Official channels exist and have authority that the application does not.',
  br='BR-27', dep='FR-17.01',
  acc=['The call control dials the configured number.','The share control opens the share sheet with the report text.'])
F(17,5,'Moderation and Abuse Prevention',
  s='The system shall publish a report and send its alerts immediately, before any review, shall then place every report in the moderation queue for review, shall limit a user to 3 reports in 24 hours, and, when an administrator removes a report as false, shall remove it from all lists, shall stop its further alerts and may suspend the author.',
  why='Immediate alerts matter, and false reports must be handled.',
  br='BR-27, BR-31', dep='FR-16.02',
  acc=['Every report appears in the moderation queue.','A fourth report in 24 hours is rejected.','The alerts are sent before the report is reviewed.','A removed report disappears from all lists and sends no further alerts.'])
F(17,6,'Child-Data Privacy',
  s='The system shall show the child\'s photo only to the guardian, the alerted trustees and the notified helpers while the report is active, shall store the photo so that no other user can read it, and shall delete it when the report is found or expired.',
  why='Children\'s images need the strongest protection.',
  br='BR-26', dep='FR-17.03',
  acc=['A user who is not alerted cannot read the photo.','The photo is deleted when the report is found or expired.'])

# ---------------------------------------------------------------- MOD-18 Evidence Recording
F(18,1,'Automatic Recording on SOS',
  s='When an SOS starts by any trigger, the system shall start recording audio from the microphone within 1 second. If the microphone permission is missing or the microphone is in use, the SOS shall continue without recording and the event log shall note it.',
  why='Audio can later support the user\'s account.',
  br='BR-23', dep='FR-01.01, FR-15.01',
  acc=['Recording starts after a manual, an automatic and a voice SOS.','A missing permission does not stop the SOS.'])
F(18,2,'Encrypted On-Device Storage',
  s='The system shall encrypt each recording with AES-256-GCM using a key held in the Android Keystore, store it in the private storage of the application, exclude it from backups and never upload it.',
  why='Recordings are sensitive and must remain with the user.',
  br='BR-23', dep='FR-18.01',
  acc=['The stored file is unreadable without the key.','No recording is sent over the network.','Another application cannot read the file.'])
F(18,3,'Evidence List',
  u='The Primary User shall be able to see a list of recordings.',
  s='The system shall list each recording with its time, location, trigger method and duration, linked to the SOS event.',
  why='The user needs to find the right recording later.',
  br='BR-23', dep='FR-18.02, FR-01.06',
  acc=['Each recording shows time, location, trigger and duration.'])
F(18,4,'Evidence Controls',
  u='The Primary User shall be able to stop a recording, delete a recording, export a recording and choose the retention period.',
  s='The system shall stop recording on request, delete a recording on confirmation, export a decrypted copy through the share sheet only when the user asks, and delete recordings automatically after the retention period (7, 30 or 90 days; default 30).',
  why='The user stays in control of the evidence.',
  br='BR-23', dep='FR-18.03',
  acc=['Stop ends the recording and keeps the file.','Delete removes the file.','A recording older than the retention period is deleted.'])
F(18,5,'Consent Disclosure',
  s='The consent text of FR-15.01 shall state that recording begins only after an SOS starts, that it is stored only on the device and how to delete it.',
  why='Recording is a sensitive action and requires disclosure.',
  br='BR-09, BR-23', dep='FR-15.01',
  acc=['The onboarding consent contains the recording disclosure.'])

# ---------------------------------------------------------------- MOD-19 Escalation
F(19,1,'Response Tracking',
  s='After an SOS is dispatched, the system shall record an acknowledgement when a trustee confirms through the application or through the acknowledgement link in the message, or when a Verified Helper accepts a request, and shall show it on the SOS screen.',
  why='Escalation depends on knowing whether anyone responded.',
  br='BR-24', dep='FR-01.02, FR-08.03, UC-29',
  acc=['A trustee confirmation is shown on the SOS screen.','A helper acceptance is shown on the SOS screen.'])
F(19,2,'No-Response Timer',
  s='When an SOS is dispatched, the system shall start a 3-minute timer on the device that stops when the first acknowledgement is recorded. If the device is offline, the timer shall still run.',
  why='The wait must be long enough for people to react and short enough to help.',
  br='BR-24', dep='FR-19.01',
  acc=['The timer stops at the first acknowledgement.','Offline, the timer expires after 3 minutes.'])
F(19,3,'Warning Countdown',
  u='The Primary User shall be able to cancel the escalation during a warning countdown.',
  s='When the timer expires without an acknowledgement, the system shall start a 30-second warning with a one-tap cancel (vibration only in silent mode) and shall escalate if it is not cancelled.',
  why='A warning limits false escalations.',
  br='BR-24', dep='FR-19.02',
  acc=['A cancel stops the escalation.','Without a cancel the escalation starts after 30 seconds.'])
F(19,4,'Authority Channel Settings',
  u='The Primary User shall be able to choose which authority numbers receive the escalation and by which channel.',
  s='The system shall provide a settings screen with the numbers (default Police 15 and Rescue 1122) and, for each number, the channel (SMS, call or share), and shall use SMS by default.',
  why='The user must control which authorities are contacted and how.',
  br='BR-24', dep='FR-14.03',
  acc=['The default numbers are Police 15 and Rescue 1122.','Changing the channel changes how the message is sent.'])
F(19,5,'Escalation Message',
  s='The system shall compose the escalation message with the user\'s name and callback number, the location (with its age if cached), the time, the trigger type and whether an evidence recording exists, and shall not include audio.',
  why='Authorities need the facts to act.',
  br='BR-24, BR-32', dep='FR-19.03, FR-18.01',
  acc=['The message contains name, number, location, time, trigger type and evidence status.','The message contains no audio.'])
F(19,6,'Escalation Log',
  u='The Primary User shall be able to view the escalation log.',
  s='The system shall record each escalation with the time, recipient, channel and delivery status.',
  why='The user should know what was sent.',
  br='BR-24', dep='FR-19.05',
  acc=['Each escalation appears in the log with time, recipient, channel and status.'])

# ---------------------------------------------------------------- MOD-20 Safe-Location Navigation
F(20,1,'Nearest Safe Location',
  s='When the user asks for the nearest safe location, the system shall compute it from the hospital and police-station entries of the bundled directory by straight-line distance from the current or last-known location. If no location exists, the system shall ask the user to enable location.',
  why='A nearby safe place is the first goal of a person in danger.',
  br='BR-30', dep='FR-11.01, FR-13.01',
  acc=['The nearest hospital or police station is chosen.','Without any location a message asks to enable it.'])
F(20,2,'One-Tap Directions Online',
  u='The Primary User shall be able to get directions to the nearest safe location with one tap.',
  s='When a data connection exists, the system shall open turn-by-turn directions to the safe location in the Google Maps application.',
  why='Turn-by-turn directions are the most helpful when online.',
  br='BR-30', dep='FR-20.01',
  acc=['One tap opens directions to the nearest safe location.'])
F(20,3,'Offline Guidance',
  s='When there is no data connection, the system shall show the distance and compass direction to the safe location and, if an offline map of the area is stored, a straight line on that map.',
  why='The feature must still help when offline.',
  br='BR-30', dep='FR-20.01, FR-13.02',
  acc=['Offline, the screen shows distance and direction.','If an offline map exists, the line is drawn on it.'])

# ---------------------------------------------------------------- MOD-21 App Disguise
F(21,1,'Disguise Options',
  u='The Primary User shall be able to choose one of three neutral launcher appearances for the application.',
  s='The system shall offer three predefined neutral names and icons and apply the chosen one to the launcher entry.',
  why='A neutral appearance avoids revealing the purpose of the application.',
  br='BR-29', dep='-',
  acc=['The user can choose among three appearances.','The launcher entry shows the chosen name and icon.'])
F(21,2,'Apply and Restore',
  u='The Primary User shall be able to restore the original appearance.',
  s='The system shall apply a change to the launcher entry and restore the original name and icon on request. The system shall tell the user that some launchers show the change only after they refresh.',
  why='The change must be reversible.',
  br='BR-29', dep='FR-21.01',
  acc=['Restoring returns the original name and icon.','The notice about launcher refresh is shown.'])
F(21,3,'Unchanged Functions',
  s='The system shall keep all functions, data and settings unchanged while a disguise is applied, and shall use neutral wording for its persistent notification.',
  why='A disguise must not disable safety.',
  br='BR-29', dep='FR-21.01, FR-01.04',
  acc=['SOS, detection and voice work with a disguise applied.','The notification text does not mention safety.'])
