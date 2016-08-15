# defcon24-demos
Code/videos/supporting files for the demos of my Defcon24 talk, "Let's Get Physical: Network Attacks Against Physical Security Systems"

## Code
### door/scan.rb
* scan network for all HID door controllers and show responses
```
USAGE: ./scan.rb
```
### door/alohomora.rb
* scan network for all HID door controllers and unlock them
* should work on all EVO-based HID controllers vuln to command injection bug
* there's a bit of a cheat in my demo exploit where the values of QUERY_STRING are prepopulated for my setup. it should be possible to use diagnostics_status.cgi to pull actual values for these fields
```
USAGE: ./alohomora.rb
```
### door/mischief_managed.rb
* repair the damage done by alohomora.rb
* should work on all EVO-based HID controllers vuln to command injection bug
* there's a bit of a cheat in my demo exploit where the values of QUERY_STRING are prepopulated for my setup. it should be possible to use diagnostics_status.cgi to pull actual values for these fields
```
USAGE: ./mischief_managed.rb
```
### camera/static.py
* replace video feed of ubiquiti aircam with 'static' to make it seem like the feed was 'cut'
* relies on mitmproxy/mitmdump running in as a proxy that you can tunnel/force camera traffic through
```
USAGE:  mitmdump -q --script './static.py ./static/'
```
### camera/loop.py
* loop X number of seconds of a ubiquiti aircam video stream
* relies on mitmproxy/mitmdump running in as a proxy that you can tunnel/force camera traffic through
```
USAGE:  mitmdump -q --script './loop.py [number of seconds to loop]'
```
### camera/reface.py
* replace faces detected in ubiquiti aircam video stream with 'laughing man' animation from Ghost in the Shell
* relies on mitmproxy/mitmdump running in as a proxy that you can tunnel/force camera traffic through
* also requires python opencv for face detection
```
USAGE:  mitmdump -q --script './reface.py ./laughing_man/ /path/to/haarcascade.xml'
```
