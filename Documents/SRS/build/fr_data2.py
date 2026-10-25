from fr_common import F

# ---------------------------------------------------------------- MOD-07 Danger Heatmap
F(7,1,'Incident Report Form',
  u='The Primary User shall be able to report an unsafe incident by choosing a category (harassment, theft or felt unsafe), confirming or editing the location and optionally adding a note of up to 280 characters.',
  s='When the user submits a report, the system shall validate the category and the location, fill the location from the current position by default, store the report with a time stamp and the geohash of its location, and show a confirmation. If validation fails, the system shall report the problem and keep the entered data.',
  why='Crowd-sourced reports are the data of the heatmap.',
  br='BR-15, BR-17', dep='FR-14.01, FR-07.05',
  acc=['A report without a category is rejected.','The location is filled automatically and can be moved on the map.','A valid report is stored with a time stamp and geohash.','A note longer than 280 characters is rejected.'])
F(7,2,'Geohash Grid Aggregation',
  s='The system shall assign every report to the geohash cell of precision 7 that contains its location and shall keep, for each cell, the number of reports per category and the weighted score.',
  why='Fixed cells hide exact positions and make density comparable.',
  br='BR-17', dep='FR-07.01',
  acc=['Two reports in the same cell increase that cell\'s count by two.','Reports in different cells are counted separately.'])
F(7,3,'Recency Weighting',
  s='The system shall weight each report by 0.5 raised to the power of its age divided by 90 days, and shall compute the cell score as the sum of the weights.',
  why='The map should show current risk and not permanently mark an area.',
  br='BR-16', dep='FR-07.02',
  acc=['A report that is 90 days old counts half of a new report.','A report that is 180 days old counts one quarter.'])
F(7,4,'Heatmap Overlay',
  u='The Primary User shall be able to view a map in which each cell is coloured from green to red by its score, and to tap a cell to see the report categories and counts.',
  s='The system shall draw the cells on the map, scale the colour by the score, and on a tap show the category counts without any information that identifies a reporter. When there is no data connection the system shall show the last downloaded data with the time of the download.',
  why='The overlay turns reports into a view of the safer and less safe areas.',
  br='BR-16, BR-17', dep='FR-07.03',
  acc=['Cells with a higher score are drawn in a redder colour.','The tap panel shows category counts and no reporter information.','Offline, the map shows the last downloaded data with its time.'])
F(7,5,'Rate Limits and Abuse Checks',
  s='The system shall reject a sixth report from the same user within 24 hours, shall reject a report by the same user within 100 m and one hour of a previous report, and shall place a report in the moderation queue when more than 10 reports reach one cell within one hour.',
  why='Rate limits stop spam and malicious flagging of an area.',
  br='BR-15', dep='FR-16.02',
  acc=['The sixth report in 24 hours is rejected with a message.','A near-duplicate report is rejected.','A burst of reports in one cell appears in the moderation queue.'])

# ---------------------------------------------------------------- MOD-08 Near Help
F(8,1,'Verified-Helper Registration',
  u='The Primary User shall be able to apply to become a Verified Helper by submitting their name, phone number and a photo of an identity document.',
  s='When the user submits the verification request with the required documents, the system shall store it with the status "pending", shall store the uploaded documents so that only administrators can read them, and shall make the user a Verified Helper only after an administrator has reviewed the documents manually and approved the request. The system shall perform no automated verification of any document. After the decision the system shall delete the identity image.',
  why='A helper network is an attack surface if anyone can join it.',
  br='BR-18', dep='FR-14.01, FR-16.03',
  acc=['A new application has the status "pending".','The user receives help requests only after approval.','No document is checked automatically; only the administrator\'s decision changes the status.','The identity image is not readable by other users and is deleted after the decision.'])
F(8,2,'Help Request Broadcast',
  u='The Primary User shall be able to request nearby help.',
  s='When a help request is made, manually or as part of an SOS when the user has enabled it, the system shall send a push notification to every Verified Helper within the set radius (default 1 km). The notification shall show the approximate distance and age of the request and shall not show the exact location.',
  why='Nearby people can reach a person faster than distant trustees.',
  br='BR-19, BR-32', dep='FR-08.01, FR-12.01',
  acc=['Helpers inside the radius receive a notification and helpers outside do not.','The notification shows distance and age and not the exact location.'])
F(8,3,'Accept or Decline Screen',
  u='A Verified Helper shall be able to accept or decline a help request.',
  s='When a helper accepts, the system shall show the requester\'s exact location to that helper, notify the requester and record an acknowledgement. When a helper declines, the system shall record nothing visible to the requester.',
  why='Responders choose whether to respond.',
  br='BR-19', dep='FR-08.02, FR-19.01',
  acc=['After acceptance the helper sees the exact location and the requester is notified.','A decline creates no message for the requester.'])
F(8,4,'Offline State',
  s='When there is no data connection, the system shall show "unavailable, no connection" on the Near Help screens and shall not drop a pending request silently. A request made while offline shall be queued with its creation time and sent when a connection returns, and the SOS shall continue by SMS to the trustees.',
  why='Near Help cannot work without a connection, and the user must know that.',
  br='BR-05', dep='FR-12.03',
  acc=['Offline, the Near Help screen shows the unavailable message.','A queued request is sent when the connection returns and shows its age to helpers.','SMS dispatch to trustees is unaffected.'])

# ---------------------------------------------------------------- MOD-09 Content Library
F(9,1,'Curated Content',
  s='The system shall provide articles, videos and links on prevention and post-incident care, each with a title, category and summary, in the categories Prevention, Emergency Response, After-Incident Care and Emotional Support.',
  why='Reliable guidance supports prevention and recovery.',
  br='BR-20', dep='-',
  acc=['Every item has a title, category and summary.','Items are grouped into the four categories.'])
F(9,2,'Offline Bundling',
  s='The system shall store the article text, titles, summaries and metadata in the application package so that they can be read with no connection. Videos and external links shall be listed offline and shall open when a connection exists.',
  why='Users may need guidance where there is no connection.',
  br='BR-20', dep='FR-13.02',
  acc=['With the network disabled all articles open.','A video or link entry shows a notice that a connection is needed.'])
F(9,3,'Browsing, Filters and Bookmarks',
  u='The Primary User shall be able to browse the library, filter by category and bookmark items.',
  s='The system shall list items by category, apply the chosen filter, store bookmarks on the device and show them in a bookmarks list.',
  why='Users need to find and return to useful content.',
  br='BR-20', dep='FR-09.01',
  acc=['The filter shows only items of the chosen category.','A bookmarked item appears in the bookmarks list after the application restarts.'])

# ---------------------------------------------------------------- MOD-10 Semantic Search
F(10,1,'Precomputed Content Embeddings',
  s='The system shall include, for every library item, an embedding computed before release with the same model that is used for queries, and shall load these embeddings from the application package.',
  why='Precomputing avoids heavy work on the phone.',
  br='BR-20', dep='FR-09.02',
  acc=['The package contains one embedding for each library item.','The embedding dimension matches the query model.'])
F(10,2,'On-Device Query Embedding',
  u='The Primary User shall be able to search the library by typing a question or description in their own words.',
  s='When the user submits a query, the system shall convert it into an embedding on the device with a compact sentence-embedding model and shall make no network request.',
  why='Query text can be sensitive and must not leave the phone.',
  br='BR-20', dep='FR-10.01',
  acc=['The query embedding is computed with the network disabled.','No network request is made during search.'])
F(10,3,'Cosine-Similarity Ranking',
  s='The system shall compute the cosine similarity between the query embedding and every content embedding and shall rank the items from the highest similarity to the lowest.',
  why='Ranking by meaning finds relevant content even when the words differ.',
  br='BR-20', dep='FR-10.02',
  acc=['An item whose meaning matches the query ranks above an unrelated item.','The ranking is repeatable for the same query.'])
F(10,4,'Keyword-Search Fallback',
  s='When the embedding model cannot be loaded, or when the highest similarity is below 0.30, the system shall run a keyword search over titles, summaries and text and shall show those results with a notice.',
  why='Search must still work when the model fails or the query has no close meaning match.',
  br='BR-20', dep='FR-09.01',
  acc=['With the model file missing, a keyword search returns matching items.','A query with a top similarity below 0.30 returns keyword results.'])
F(10,5,'Ranked Result Cards',
  u='The Primary User shall be able to open or bookmark a search result.',
  s='The system shall show each result as a card with the title, category, summary and a relevance indicator derived from the similarity, and shall provide open and bookmark actions.',
  why='Users should see how relevant each result is.',
  br='BR-20', dep='FR-10.03, FR-09.03',
  acc=['Each card shows a relevance indicator.','Open shows the item and bookmark adds it to the bookmarks list.'])

# ---------------------------------------------------------------- MOD-11 Directory
F(11,1,'Localized Directory',
  s='The system shall provide, in the application package, a directory of hospitals, police stations, helplines and emergency numbers for Pakistan, including Rescue 1122 and women\'s helplines, each with a name, category, phone number and, for hospitals and police stations, coordinates.',
  why='Users need local emergency contacts at hand.',
  br='BR-21', dep='FR-13.02',
  acc=['The directory contains Rescue 1122 and at least one women\'s helpline.','Hospital and police entries contain coordinates.'])
F(11,2,'One-Tap Call',
  u='The Primary User shall be able to call any directory entry with one tap.',
  s='When the user taps the call control of an entry, the system shall place the call to its number, or open the dialer with the number filled in if the call permission has not been granted.',
  why='In an emergency time matters.',
  br='BR-21', dep='FR-11.01',
  acc=['One tap places the call when permission is granted.','Without permission the dialer opens with the number filled in.'])
F(11,3,'Nearest Facilities First',
  s='When a location is available, the system shall order hospitals and police stations by distance from the user; otherwise it shall order entries by category and name.',
  why='The nearest help is the most useful.',
  br='BR-21', dep='FR-11.01, FR-13.01',
  acc=['With location, the nearest hospital is first.','Without location, entries are ordered by category and name.'])

# ---------------------------------------------------------------- MOD-12 Tiered Delivery
F(12,1,'Connectivity Tier Detection',
  s='The system shall classify the device connectivity as Tier 1 (no data connection), Tier 2 (any data connection) or Tier 3 (good data connection) and shall update the tier when connectivity changes. The tier shall be shown in the status strip of the home screen.',
  why='Delivery must adapt to what the network can do.',
  br='BR-05', dep='-',
  acc=['With data disabled the tier is 1.','With a reachable backend over a slow link the tier is 2.','With a fast link the tier is 3.'])
F(12,2,'SMS Delivery at Tier 1',
  s='At Tier 1 the system shall send the SOS by SMS to every trustee through the device\'s SMS capability and shall not depend on any data connection. The SMS shall contain the user\'s name, the preset text, the coordinates and the time.',
  why='SMS is the only channel that works with no data.',
  br='BR-05, BR-06', dep='FR-01.02',
  acc=['With mobile data and Wi-Fi off, an SOS sends SMS to every trustee.','The SMS contains name, text, coordinates and time.'])
F(12,3,'Queue and Retry',
  s='When a channel cannot be delivered, the system shall store the message in the on-device outbound queue and shall retry automatically when the connection returns, until it is delivered, and shall update the SOS event log. The queue shall survive closing the application and restarting the device.',
  why='Nothing created offline should be lost.',
  br='BR-05', dep='FR-13.02, FR-01.06',
  acc=['A message queued offline is sent after the connection returns.','Queued messages remain after the device restarts.','The event log shows the status change.'])

# ---------------------------------------------------------------- MOD-13 Offline Caching
F(13,1,'Last-Known Location Cache',
  s='The system shall keep the most recent location fix with its time on the device. When an SOS starts and a fresh fix is not obtained within 10 seconds, the system shall use the cached location and shall state its age in the message.',
  why='An alert with an older location is better than an alert without one.',
  br='BR-06', dep='-',
  acc=['With GPS unavailable, the SOS uses the cached location.','The message states how old the location is.'])
F(13,2,'On-Device Database',
  s='The system shall store the library content, the directory, the outbound queue, the SOS event log and the map data for up to three user-selected frequent areas in an on-device database and files. The map data shall be downloaded while online from an open map-data source that permits offline storage.',
  why='Offline operation needs local data.',
  br='BR-05, BR-20', dep='-',
  acc=['With the network disabled the library, directory and SOS log can be read.','A frequent area downloaded online can be shown offline.'])

# ---------------------------------------------------------------- MOD-14 Authentication
F(14,1,'Phone-Number Sign-Up and Login',
  u='The Primary User shall be able to sign up and log in with their mobile phone number.',
  s='When the user enters a valid number, the system shall send a one-time code through Firebase Authentication and, when the correct code is entered, shall sign the user in and create the account if it does not exist. A wrong code shall be rejected, and the number shall be locked for sending codes for 10 minutes after five wrong attempts.',
  why='Phone numbers are the usual identity for users in Pakistan.',
  br='BR-22', dep='DEP-1',
  acc=['A correct code signs in the user.','A wrong code is rejected with a message.','Five wrong attempts lock further attempts for 10 minutes.'])
F(14,2,'Session Handling',
  s='The system shall keep the user signed in, renew the session token automatically, and require a new login if the token is revoked. The SOS, detection, voice, library, directory and evidence functions shall not require a valid session to operate offline.',
  why='Safety functions must not fail because a session expired.',
  br='BR-22', dep='FR-14.01',
  acc=['The user stays signed in after restarting the application.','A revoked token leads to the login screen.','An SOS can be started offline with an expired token.'])
F(14,3,'Profile and Settings',
  u='The Primary User shall be able to edit their name, the emergency message template, the linked trustees and the default SOS mode.',
  s='The system shall validate and save these settings, and shall use the template as the preset text of every SOS. A template shall not be empty and shall not exceed 160 characters.',
  why='The alert text must be personal and short enough for one SMS.',
  br='BR-22', dep='FR-01.05',
  acc=['An empty template is rejected.','The saved template appears in the next SOS message.'])
F(14,4,'Account Recovery',
  u='The Primary User shall be able to recover the account on a new device after losing the old one.',
  s='When the user logs in on a new device with the same phone number and the correct code, the system shall restore the account data held on the server, shall end the sessions on all other devices and shall report that evidence recordings, which exist only on the old device, cannot be restored.',
  why='A lost phone should not mean a lost account.',
  br='BR-22, BR-23', dep='FR-14.01',
  acc=['The new device shows the profile, trustees and circles.','The old device is signed out.','The user is told that evidence recordings are not restored.'])
