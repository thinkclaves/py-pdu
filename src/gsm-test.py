#!/usr/bin/python
# -*- coding: UTF-8 -*-

import ul_gsm as gsm

# SMS-SUBMIT encode test
#sms = gsm.Sms().encode_out( { 'smsc':'+38068240656', 'sender':'+380993435400', 'text':u'юыо' } )
#print( sms.pduHex )
#print( gsm.pdu_s_pack(u'юыо') )

# SMS-DELIVER decode test
#pdu = '07917238010010F5040BC87238880900F10000993092516195800AE8329BFD4697D9EC37'
#pdu = '07911326040000F0040B911346610089F60000208062917314080CC8F71D14969741F977FD07'
#sms = gsm.Sms().decode_in( pdu )
#print(sms.smsc, sms.smscType, sms.firstOctet, sms.senderLen, sms.senderType, sms.sender, sms.tpPID, sms.tpDCS)
#print(sms.year,sms.month,sms.date, sms.hour,sms.minute,sms.second, sms.tz)
#print(sms.textLen, sms.textBytes, sms.text)

# date pack/unpack
#print( gsm.date_unpack( gsm.date_pack( 2014,10,12, 17,5,30, 0 )))
#print( gsm.bytes_to_hex( gsm.date_pack( 2014,10,12, 17,5,30, 0 )))

# string pack/unpack
#print( bytes_to_hex( pdu_s_pack(u'0123456789') ) )
#print( pdu_s_unpack( pdu_s_pack(u'0123456789абв'), True ) )

# phone pack/unpack
#print(phone_unpack(phone_pack('+38099-343-54-07-01')))
#print hex_to_bytes('0001020304aabbeeff')
#print(bytes_to_s( s_to_bytes( u'01234абвыв' ) ))

