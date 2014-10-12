#!/usr/bin/python
# -*- coding: UTF-8 -*-

# ------------------------------------------------------------------------------
def b_swap( b ):
	'swap nibbles'
	return ((b >> 4) & 0xF) | ((b << 4) & 0xF0)

# ------------------------------------------------------------------------------
def bin2bcd( n ):
	'convert binary to BCD'
	bcd,shift = 0,0
	while n != 0:
		bcd |= (n % 10) << shift
		n //= 10
		shift += 4
	return bcd
def bcd2bin( bcd ):
	'convert BCD to binary'
	n,mul = 0,1
	while bcd != 0:
		n += (bcd & 0xF) * mul
		bcd >>= 4
		mul *= 10
	return n

# ------------------------------------------------------------------------------
def n2h4( n ):
	'convert 4 bits to 1 hex char'
	n &= 0xF
	return chr( (n + 48) if ( n < 10 ) else (n + 55) )
def n2h8( n ):
	'convert 8 bits to 2 hex chars'
	return n2h4( n >> 4 ) + n2h4( n )
def n2h16( n ):
	'convert 16 bits to 4 hex chars'
	return n2h8( n >> 8 ) + n2h8( n )
def n2h( n ):
	'convert number to Hex'
	h = []
	while (n > 0):
		h.insert(0, n2h4(n))
		n >>= 4
	h = ['0'] if len(h) == 0 else h
	return ''.join(h)

# ------------------------------------------------------------------------------
def h2n4( h ):
	'convert Hex digit to number'
	b = ord(h[0])
	b = (b - 48) if (48 <= b <= 57)  else b
	b = (b - 55) if (65 <= b <= 90)  else b
	b = (b - 87) if (97 <= b <= 122) else b
	return b & 0xF
def h2n( h ):
	'convert Hex string to number'
	n = 0
	for c in h:
		n = (n << 4) | h2n4(c)
	return n

# ------------------------------------------------------------------------------
def s_is_7bit( s ):
	'check if all chars of s is 7-bit'
	for c in s:
		if ( ord(c) > 127 ):
			return False
	return True

# ------------------------------------------------------------------------------
def s_to_bytes( s ):
	'convert string to array of bytes'
	return [ ord(c) for c in s ]
def bytes_to_s( a ):
	'convert array of bytes to string'
	return u''.join([ chr(b) for b in a ])

# ------------------------------------------------------------------------------
def bytes_to_hex( a ):
	'convert array of bytes to Hex string'
	return ''.join([ n2h8(b) for b in a ])
def hex_to_bytes( h ):
	'convert Hex string to bytes'
	return [ h2n(h[i*2 : (i+1)*2]) for i in range(len(h) // 2) ]



# ------------------------------------------------------------------------------
def phone_clean( s ):
	'clean non-number chars from phone string'
	p = []
	for c in s:
		if ( 48 <= ord(c) <= 57 ):
			p.append(c)
	return ''.join(p)
def phone_digits( s ):
	'number of phone digits'
	s = phone_unpack(s) if phone_packed(s) else s
	return len( phone_clean( s ))
def phone_packed( s ):
	'check if s is packed'
	return not isinstance(s, str)
def phone_pack( p ):
	'pack phone number string to byte array'
	p = phone_clean(p)
	p = hex_to_bytes( (p + 'F') if ((len(p) % 2) == 1) else p )
	for i in range(len(p)):
		p[i] = b_swap(p[i])
	return p
def phone_unpack( p ):
	'unpack phone number bytes to string'
	s = ['+']
	for n in p:
		s.append( n2h8(b_swap(n)) )
	s = ''.join(s)
	return s[:-1] if (s[-1] == 'F') else s



# ------------------------------------------------------------------------------
def pdu_7to8( a ):
	'pack 7-bit array to 8-bit'
	if len(a) > 0:
		lenOut = len(a) - (len(a) >> 3)
		a.append(0)
		for i1 in range(len(a)-2):
			for i2 in range(len(a)-2, i1-1, -1):
				a[i2] |= ( 0x80 if ((a[i2+1] & 1) != 0) else 0 )
				a[i2+1] >>= 1
		a = a[0:lenOut]
	return a
def pdu_8to7( a ):
	'unpack 8-bit array to 7-bit'
	lenOut = len(a) + (len(a) >> 3) #+ (1 if ((len(a) & 7) != 0) else 0)
	while (len(a) < lenOut):
		a.append(0)
	if (len(a) > 0):
		for i1 in range(lenOut-1):
			for i2 in range(lenOut-2, i1-1, -1):
				a[i2+1] = (a[i2+1] << 1) | (1 if ((a[i2] & 0x80) != 0) else 0)
	for i in range(len(a)):
		a[i] &= 0x7F
	return a

def pdu_ucs2_to_bytes( a ):
	'convert UCS2 words to bytes'
	b = []
	for w in a:
		b.append( (w >> 8) & 0xFF )
		b.append( w & 0xFF )
	return b

def pdu_s_len( s ):
	'calculate length of char/UCS2 string'
	return len(s) if s_is_7bit(s) else len(s)*2

def pdu_s_pack( s ):
	'pack char/UCS2 string to bytes'
	a = s_to_bytes(s)
	return pdu_7to8(a) if s_is_7bit(s) else pdu_ucs2_to_bytes(a)
def pdu_s_unpack( a, ucs2 ):
	'unpack bytes to char/UCS2 string, ucs2=False/True'
	return bytes_to_s( [(a[i] << 8) + a[i+1] for i in range(0, len(a), 2)] if ucs2 else pdu_8to7(a) )



# ------------------------------------------------------------------------------
def date_pack( year,month,date, hour,minute,second, tz ):
	'pack date fields to byte array'
	return [
		b_swap( bin2bcd( year   % 100)),
		b_swap( bin2bcd( month  % 13)),
		b_swap( bin2bcd( date   % 32)),
		b_swap( bin2bcd( hour   % 25)),
		b_swap( bin2bcd( minute % 60)),
		b_swap( bin2bcd( second % 60)),
		b_swap( bin2bcd( tz))
	]
def date_unpack( a ):
	'unpack packed date array to unpacked [year,month,date, hour,minute,second,tz]'
	return [
		bcd2bin( b_swap( a[0] )) + 2000,
		bcd2bin( b_swap( a[1] )),
		bcd2bin( b_swap( a[2] )),
		bcd2bin( b_swap( a[3] )),
		bcd2bin( b_swap( a[4] )),
		bcd2bin( b_swap( a[5] )),
		bcd2bin( b_swap( a[6] )),
	]


# ------------------------------------------------------------------------------
class Sms:
	'Sms message class, for generation and parsing'
	
	def __init__(self, o={}):
		self.error                                         = True
		self.smsc,self.smscLen,self.smscType               = '',0,145
		self.sender,self.senderLen,self.senderType         = '',0,145
		self.text,self.textLen,self.textBytes,self.textRaw = '',0,0,[]
		self.smsSubmit,self.firstOctet                     = 0,0x11
		self.tpMsgRef,self.tpPID,self.tpDCS,self.tpVP      = 0,0,0xFF,0xAA
		self.year,self.month,self.date,self.hour,self.minute,self.second,self.tz = 2000,1,1,0,0,0,0

		self.pdu,self.pduHex,self.pduLen                = [],'',0
		
		self.join(o)

	def join(self, o={}):
		'joins o dict with this Sms'
		for k in o:
			if k in self.__dict__:
				self.__dict__[k] = o[k]

	def decode_in( self, pdu ):
		'decode incoming SMS PDU hex/bytes'
		
		if isinstance(pdu, str):
			pdu = hex_to_bytes(pdu)
		self.pdu,self.pduHex,i = pdu,bytes_to_hex(pdu),0
		if len(pdu) >= 25:
			self.smscLen = pdu[0]
			if self.smscLen > 0:
				self.smscType = pdu[1]
				self.smsc = phone_unpack( pdu[2 : self.smscLen + 1] )
			i += self.smscLen + 1

			self.firstOctet = pdu[i]; i += 1
			
			self.senderLen  = (pdu[i] >> 1) + (pdu[i] & 1); i += 1
			self.senderType = pdu[i]; i += 1
			self.sender     = phone_unpack( pdu[ i : i+self.senderLen ] ); i += self.senderLen
			
			self.tpPID      = pdu[i]; i += 1
			self.tpDCS      = pdu[i]; i += 1
			
			date = date_unpack( pdu[i : i + 7] )
			self.year,self.month,self.date,self.hour,self.minute,self.second,self.tz = date[0],date[1],date[2], date[3],date[4],date[5], date[6]
			i += 7
			
			self.textLen   = pdu[i]; i += 1
			self.textBytes = (self.textLen - (self.textLen >> 3)) if (self.tpDCS == 0) else self.textLen
			print( bytes_to_hex(pdu[ i : i+self.textBytes ]))
			self.text      = pdu_s_unpack( pdu[ i : i+self.textBytes ], self.tpDCS == 8 )

			'''			
			sms.textLen = sms.bytes[sms.smscLen + sms.senderLen + 13];
			sms.textRaw = sms.bytes.slice(sms.smscLen + sms.senderLen + 14, sms.smscLen + sms.senderLen + 14 + sms.textLen);
			sms.text    = tools.bytesToString(tools.gsm.pdu.to7bit(sms.textRaw));
			'''
			self.error = False

		return self
		
	def encode_out( self, o={} ):
		'encode outcoming PDU SMS'
		self.join( o )
		
		pdu = []
		
		if len(self.smsc) != 0:
			smsc = phone_pack( self.smsc )
			pdu = [ len(smsc) + 1, self.smscType ] + smsc
		else:
			pdu = [0]

		self.tpDCS = 0 if s_is_7bit(self.text) else 8
		pdu += [ self.firstOctet, self.tpMsgRef ]
		pdu += [ phone_digits( self.sender ), self.senderType ] + phone_pack( self.sender )
		pdu += [ self.tpPID, self.tpDCS, self.tpVP ]
		pdu += [ len( self.text ) if (self.tpDCS == 0) else len( self.text ) * 2 ]
		pdu += pdu_s_pack( self.text )
		
		self.pdu,self.pduHex = pdu,bytes_to_hex(pdu)
		return self
		
