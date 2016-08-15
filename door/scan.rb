#!/usr/bin/env ruby
require 'socket'
require 'timeout'

BROADCAST_ADDR = "255.255.255.255"
BIND_ADDR = "0.0.0.0"
PORT = 4070
IFACE = nil
timeout = 5

# socket setup
socket = UDPSocket.new
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BROADCAST, true)
socket.setsockopt(Socket::SOL_SOCKET, Socket::SO_BINDTODEVICE, IFACE) if IFACE
socket.bind(BIND_ADDR, PORT)

# magic probe
buffer = "discover;013;"

puts "sending discover request"

socket.send(buffer,0,BROADCAST_ADDR,PORT)

puts "waiting #{timeout} second#{"s" if timeout > 1} for responses..."
puts ""

while true
  begin
    Timeout::timeout(timeout) do
      resp, addr = socket.recvfrom(1024)
      # response is in the form of: discovered;[3-digit packet len];[mac addy];[hostname];[ip addy];[some digit(s)];[model];[firmware ver];[firmware date?];
      if resp && resp =~ /^discovered/
        puts addr.last.center(21,"-")
        puts "#{resp}"
      end
    end
  rescue Timeout::Error, Interrupt
    break
  end
end

# socket teardown
socket.close

puts "-" * 21
puts "done"
