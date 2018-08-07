# -*- coding: utf-8 -*-

import struct, sys, socket

# The packed format is an 8 byte integer of the number of ranges. Then 44
# bytes per range, consisting of 16 byte packed IP being the lower bound IP of
# the range, then 16 bytes of the upper, inclusive bound, 8 bytes for the
# offset of the description from the end of the packed ranges, and 4 bytes
# for the length of the description. After these packed ranges, are the
# concatenated descriptions.

class iplist:

    def bytesToInt(self, bytesRead):
        result = 0
        for b in bytesRead:
            result = result * 256 + b
        return result

    def intToBytes(self, number, length):
        byteArray = []
        for i in range(0, length):
            byteArray.append(0)
        for i in range(0, length):
            byte = number % 256
            byteArray[i] = byte
            number = (number - byte) / 256;
        return byteArray

    def unpackBytes(self, bytesRead):
        return struct.unpack('<' + 'B'*len(bytesRead), bytesRead)

    def parseInt(self, bytesRead, littleEndian = True, unpack = True):
        if unpack:
            bytesRead = self.unpackBytes(bytesRead)
        if littleEndian:
            bytesRead = reversed(bytesRead)

        return self.bytesToInt(bytesRead)

    def parseIpv6(self, bytesRead, littleEndian = False, unpack = True):
        ipv6 = []
        for x in range(0, 8):
            ipv6.append(self.parseInt(bytesRead[x*2:x*2+2], littleEndian, unpack))
        return ipv6

    def isGreaterThen(self, ip1, ip2):
        for x in range(0, 8):
            if ip1[x] > ip2[x]:
                return True
            elif ip1[x] == ip2[x]:
                if x == 7:
                    return True
                continue
            else:
                return False

    def convertToIpv4(self, ipv6, littleEndian = False):
        initSum = 0
        for x in range(0, 5):
            initSum += ipv6[x]
        if initSum == 0 and ipv6[5] == ((256*256)-1):
            p4 = ipv6[6]%256
            p3 = (ipv6[6]-p4)/256

            p2 = ipv6[7]%256
            p1 = (ipv6[7]-p2)/256
            if (littleEndian):
                return [p4, p3, p2, p1]
            else:
                return [p3, p4, p1, p2]
        else:
            return None

    def ipv4ToString(self, ipv4):
        return ipv4[0]+'.'+ipv4[1]+'.'+ipv4[2]+'.'+ipv4[3]

    def findRange(self, findIpv6, ranges):
        indx = 0
        for r in ranges:
            if self.isGreaterThen(findIpv6, r['lower']) and self.isGreaterThen(r['upper'], findIpv6):
                return r, indx
            indx += 1
        return None, None

    def getIpv6FromDomain(self, domain):
        dnsIp = self.getIpFromDomain(domain)
        dnsIpArr = dnsIp.split('.')
        ipv4 = []
        ipv4.append(int(dnsIpArr[0]))
        ipv4.append(int(dnsIpArr[1]))
        ipv4.append(int(dnsIpArr[2]))
        ipv4.append(int(dnsIpArr[3]))
        return self.getIpv6FromIpv4(ipv4)

    def getIpFromDomain(self, domain):
        return socket.gethostbyname(domain)

    def getIpv6FromIpv4(self, ipv4):
        ipArr = [0,0,0,0,0,0,0,0,0,0,255,255]
        ipArr.append(ipv4[0])
        ipArr.append(ipv4[1])
        ipArr.append(ipv4[2])
        ipArr.append(ipv4[3])
        return self.parseIpv6(ipArr, False, False)

    def parseFromFile(self, filepath):
        bytes_read = open(filepath, "rb").read()
        numRanges = self.parseInt(bytes_read[0:8])
        ranges = []
        offset = 8
        packedOffset = offset + (numRanges * 44)
        while numRanges > 0:
            descOffset = self.parseInt(bytes_read[offset+32 : offset+40])
            descLen = self.parseInt(bytes_read[offset+40 : offset+44])
            ranges.append({
                'lower' : self.parseIpv6(bytes_read[offset : offset+16]),
                'upper' : self.parseIpv6(bytes_read[offset+16 : offset+32]),
                'desc'  : "".join(map(chr, self.unpackBytes(bytes_read[packedOffset + descOffset : packedOffset + descOffset + descLen])))
            })
            offset += 44
            numRanges -= 1
        return ranges

    def findAndRemove(self, seekIpv6, ranges):
        foundRange, indx = self.findRange(seekIpv6, ranges)
        if foundRange:
            ranges.insert(indx+1, {
                'lower' : self.plusOneIp(seekIpv6),
                'upper' : foundRange['upper'],
                'desc'  : foundRange['desc']
            })
            ranges[indx]['upper'] = self.minusOneIp(seekIpv6)
            return foundRange, indx, ranges
        else:
            return None, None, ranges

    def minusOneIp(self, ipv6):
        ipv4 = self.convertToIpv4(ipv6)
        if ipv4[3] > 0 and ipv4[3] < 255:
            ipv4[3] -= 1
            return self.getIpv6FromIpv4(ipv4)
        else:
            raise Exception('IP out of bounds for subtraction')

    def plusOneIp(self, ipv6):
        ipv4 = self.convertToIpv4(ipv6)
        if ipv4[3] > 0 and ipv4[3] < 255:
            ipv4[3] += 1
            return self.getIpv6FromIpv4(ipv4)
        else:
            raise Exception('IP out of bounds for addition')

    def ipv6ToBytes(self, ipv6):
        byteArray = []
        for x in range(0, 8):
            ipPartBytes = self.intToBytes(ipv6[x], 2)
            byteArray.append(ipPartBytes[1])
            byteArray.append(ipPartBytes[0])
        return byteArray

    def writeToFile(self, filepath, ranges):
        newFile = open(filepath, "wb")

        # Num of ranges
        newFile.write(bytearray(self.intToBytes(len(ranges), 8)))

        seenDescs = {}
        seenDescsArr = []

        # All ranges
        offset = 0
        for r in ranges:
            newFile.write(bytearray(self.ipv6ToBytes(r['lower'])))
            newFile.write(bytearray(self.ipv6ToBytes(r['upper'])))

            descLen = len(r['desc'])

            if r['desc'] not in seenDescs:
                seenDescs[r['desc']] = offset
                seenDescsArr.append(r['desc'])
                foundOffset = offset
                offset += descLen
            else:
                foundOffset = seenDescs[r['desc']]

            newFile.write(bytearray(self.intToBytes(foundOffset, 8)))
            newFile.write(bytearray(self.intToBytes(descLen, 4)))
        
        # All descriptions
        for d in range(0, len(seenDescsArr)):
            newFile.write(bytearray(seenDescsArr[d]))
