#!/usr/bin/env python

from _pybgpstream import BGPStream, BGPRecord, BGPElem
import sys
import time
import datetime
import ciso8601
import mysql.connector
from mysql.connector import errorcode
import MySQLdb
import sys


class DBEditor(object):

	def __init__(self, db):
		self.db = db
		self.cursor = db.cursor()
	def insertRecord(self, prefix, prefixLength, asPath, BGPcommunities, 
					nextHop, collector, timestamp):		
		query = "INSERT INTO recordsTable(prefix, prefixLength, asPath, \
					BGPcommunities, nextHop, collector, timestamp)  \
					VALUES (%s, %s, %s, %s, %s, %s, %s)" 
		args = (prefix, prefixLength, asPath, BGPcommunities, nextHop, collector, timestamp)
		self.cursor.execute(query, args)
		self.db.commit()

db = MySQLdb.connect(host="localhost",          # host
						     user="root",       # username
						     passwd="password", # password
						     db="RecordsDB")    # name of the data base
db_editor = DBEditor(db)


print '\n\n-----------------  Welcome to the DDoS Observatory  -----------------\n\n'
	
# Create a new bgpstream instance and a reusable bgprecord instance
stream = BGPStream()
rec = BGPRecord()

start_date = sys.argv[1]
end_date = sys.argv[2]
startTime = time.mktime(ciso8601.parse_datetime(start_date).timetuple()) # pip install ciso8601
endTime = time.mktime(ciso8601.parse_datetime(end_date).timetuple())

 #Consider RIPE RRC (Remote Route Collector) # if not specified it will omit all the collectors
'''
stream.add_filter('collector','rrc00') # Amsterdam
stream.add_filter('collector','rrc01') # London
stream.add_filter('collector','rrc02') # Paris, France
stream.add_filter('collector','rrc03') # Amsterdam
stream.add_filter('collector','rrc04') # Geneva
stream.add_filter('collector','rrc05') # Vienna
stream.add_filter('collector','rrc06') # Otemachi
stream.add_filter('collector','rrc07') # Stockholm
stream.add_filter('collector','rrc08') # San Jose (CA), USA
stream.add_filter('collector','rrc09') # Zurich, Switzerland
stream.add_filter('collector','rrc10') # Milan, Italy
stream.add_filter('collector','rrc11') # NY USA
stream.add_filter('collector','rrc12') # Frankfurt, Germany
stream.add_filter('collector','rrc13') # Moscow, Russia
stream.add_filter('collector','rrc14') # Palo Alto, USA
stream.add_filter('collector','rrc15') # Sao Paulo, Brazil
stream.add_filter('collector','rrc16') # Miami, USA
stream.add_filter('collector','rrc18') # Barcelona, Spain.
stream.add_filter('collector','rrc19') # Johannesburg, South Africa
stream.add_filter('collector','rrc20') # Zurich, Switzerland
stream.add_filter('collector','rrc21') # Paris, France
stream.add_filter('collector','rrc22') # Bucharest, Romania
stream.add_filter('collector','rrc23') # Singapore
'''
stream.add_filter('project', 'ris')

# User Inputs Time Intervals - Starting and timestamps
# User enters date in DD/MM/YY format and it is converted to int format.
'''
isValid=False
while not isValid:
	userIn = raw_input("Please provide the starting date in the format 'YYYY-MM-DD'.\n")
	try: 
		startTime = time.mktime(ciso8601.parse_datetime(userIn).timetuple()) # pip install ciso8601    
		isValid=True
	except:
		print "Try again!\n"

isValid=False
while not isValid:
	userIn = raw_input("Please provide the ending date in the format 'YYYY-MM-DD'.\n")
	try: 
		endTime = time.mktime(ciso8601.parse_datetime(userIn).timetuple())
		isValid=True
	except:
		print "Try again!\n"
'''

# Time interval:
stream.add_interval_filter(int(startTime),int(endTime))

# Start the stream
stream.start()
print "\n"
print "----------------------------------------------------------------------------------------------------------------"
print "|                         Record                       |                         Element                       |"
print "----------------------------------------------------------------------------------------------------------------"			
print "| Project | Collector |  Type  |    Time    |  Status  | Type |  Peer Address  | Peer ASN |       Prefix       |"

# Get next record
while(stream.get_next_record(rec)):
	# Print the record information only if it is not a valid record
	if rec.status != "valid":
		#print "--INVALID RECORD--"
		print '|  {:6s} | {:9s} | {:6s} | {:10d} | {:8s} '.format(rec.project, rec.collector, rec.type, rec.time, rec.status)
		#print "-----------------------------"
	else:
		elem = rec.get_next_elem()
		while (elem):
			#make sure all needed keys in element are existant
			if 'as-path' in elem.fields and 'prefix' and 'communities' and 'next-hop' in elem.fields:
				communities = []
				for c in elem.fields['communities']:
					community = "{}:{}".format(c['asn'], c['value'])
					communities.append(community)
				#if it contains : it's a IPv6, then don't include it
				#AND only include records with larger than /24 prefixes
				if ":" not in elem.peer_address and int(elem.fields['prefix'].split("/")[1]) > 24:
					# Print record and elem information
					print '|  {:6s} | {:9s} | {:6s} | {:10d} | {:8s} '.format(rec.project, rec.collector, rec.type, rec.time, rec.status),
					print '| {:4s} | {:14s} | {:8d} | {:18s} |'.format(elem.type, elem.peer_address, elem.peer_asn, elem.fields['prefix'])#, elem.fields, " |"
					#add the record to the database
					db_editor.insertRecord(str(elem.fields['prefix']), elem.fields['prefix'].split("/")[1],\
							str(elem.fields['as-path']), str(elem.fields['communities']), str(elem.fields['next-hop']), rec.collector, rec.time)
			elem = rec.get_next_elem()
			
db_editor.db.close()
print("end of timeframe")