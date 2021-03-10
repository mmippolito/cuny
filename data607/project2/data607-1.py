#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import io
import time
import re
import random
import string

# Init
mainHtmlFile = "pw_org_main_output.html"		# Html output file for the main web page
mainCsvFile = "data607-main.csv"				# Main csv output file
agencyCsvFile = "data607-agency.csv"			# Agency csv output file
linkDict = {}									# Dictionary of links to each agency's page

# Next block needed to remove non-printable characters
def remove_control_chars(s):
    return ''.join(list(filter(lambda x: x in string.printable, s)))

# See if the main page has already been scraped (i.e., if the main output file already exists);
# this will prevent going to the page every single time the script is run.
if not os.path.exists(mainHtmlFile):

	# Scrape main page and save output to text file
	cmd = "curl -k -s -XGET https://www.pw.org/literary_agents?filter0=All&field_electronic_submissions_value=All&items_per_page=All"
	print("-------------")
	print("Executing curl command: " + cmd)
	r = os.popen(cmd).read()
	fhout = open(mainHtmlFile, "w")
	fhout.write(r)
	fhout.close()

# Open the output file and read it into variable r.
print("-------------")
print("Reading main output file: " + mainHtmlFile)
fhin = open(mainHtmlFile, "r")
r = ""
while True:
	l = fhin.readline()
	if not l:
		break
	r += l
fhin.close()

# Open the main CSV output file.
fhcsv = open(mainCsvFile, "w")
print("-------------")
print("Parsing main output")

# Parse the output. Each entry will be enclosed by an <li></li> element, like this:
#
# <li class="views-row views-row-57 views-row-odd">  
#   <div class="views-field views-field-title">        <h2 class="field-content title with-subtitle"><a href="/literary_agents/seth_fishman">Seth Fishman</a></h2>  </div>  
#   <div class="views-field views-field-field-agency-name">        <h2 class="field-content title subtitle">The Gernert Company</h2>  </div>  
#   <div class="views-field views-field-taxonomy-vocabulary-20 list-inline">    <span class="views-label views-label-taxonomy-vocabulary-20">Interested in Representing: </span>    <div class="field-content"><a href="/literary_agents?filter0=9678">Commercial Fiction</a>, <a href="/literary_agents?filter0=9662">Graphic/Illustrated</a>, <a href="/literary_agents?filter0=9677">Literary Fiction</a></div>  </div>  
#   <div class="views-field views-field-field-representative-authors label-headroom">    <span class="views-label views-label-field-representative-authors">Representative Authors: </span>    <div class="field-content">Kate Beaton, Anna Bond, Stephanie Feldman, Alex Grecian, Porochista Khakpour, Ann Leckie, Randall Munroe, Téa Obreht</div>  </div></li>
#
# First find each stanza enclosing a single agent. Variable ma will be an array of agents.
#
agentArray = re.findall('<li class="views-row views-row-(\\d+) views-row-(odd|even)( views-row-(first|last))?">(.+?)</li>', r, re.DOTALL)

# Parse each agent stanza
for agentElement in agentArray:

	# Agent ID returned from <li> element above
	agentId = agentElement[0]

	# Agent name and link to agent's page
	agentMatch = re.findall('<div class="views-field views-field-title">.+?<a href="(.+?)">(.+?)</a>', agentElement[4])
	agentLink = agentMatch[0][0]
	agentName = agentMatch[0][1]

	# Populate agency link dictionary
	linkDict[agentId] = agentLink

	# Agency
	agentMatch = re.findall('<div class="views-field views-field-field-agency-name">.+?<h2 class="field-content title subtitle">(.+)</h2>', agentElement[4])
	agentAgency = agentMatch[0]

	# Taxonomy (genres)
	agentMatch = re.findall('<div class="views-field views-field-taxonomy-vocabulary-20 list-inline">.+?<div class="field-content">(.+?)</div>', agentElement[4])

	# The above will return all genres. Need to parse out each genre. Use the pipe symbol | to separate genres in the output csv.
	agentSubmatches = re.findall('<a href="/literary_agents\\?filter0=\\d+">(.+?)</a>', agentMatch[0])
	agentGenres = ""
	for agentSubmatch in agentSubmatches:
		agentGenres += agentSubmatch + "|"
	if agentGenres[-1:] == "|":					# Trim trailing pipe
		agentGenres = agentGenres[0:-1]

	# Representative authors
	agentMatch = re.findall('<div class="views-field views-field-field-representative-authors label-headroom">.+?<div class="field-content">(.+?)</div>', agentElement[4])

	# The above will return all representative authors. Need to parse out each author. Use the pipe symbol | to separate authors in the output csv.
	# Sometimes hard spaces are used; convert these to plain old spaces.
	agentMatch[0] = re.sub('&nbsp;', ' ', agentMatch[0])
	# Sometimes there are no representative authors listed, and a single </div> is returned; remove it!
	agentMatch[0] = re.sub('</div>', '', agentMatch[0])
	# Sometimes semicolons are used instead of commas; convert these to commas.
	agentMatch[0] = re.sub(';', ',', agentMatch[0])
	# Make things easier by first replace ', ' with just plain ',' in order to be able to use a simple split().
	agentMatch[0] = re.sub(', *', ',', agentMatch[0])
	agentSubmatches = agentMatch[0].split(',')
	agentAuthors = ""
	for agentSubmatch in agentSubmatches:
		agentAuthors += agentSubmatch + "|"
	if agentAuthors[-1:] == "|":					# Trim trailing pipe
		agentAuthors = agentAuthors[0:-1]

	# Output to main csv.
	outLine = agentId + "," + agentName + "," + agentLink + "," + agentAgency + "," + agentGenres + "," + agentAuthors

	# Check for commas in any of the output fields, which would get in my kitchen.
	if "," in agentId or "," in agentName or "," in agentLink or "," in agentAgency or "," in agentGenres or "," in agentAuthors:
		print("Comma in one or more fields: " + outLine)

	# Output to screen and file
	print(outLine)
	fhcsv.write(outLine + "\n")

# Close main csv
fhcsv.close()

# Scrape agency pages
print("-------------")
print("Scraping agency pages")
for linkId in linkDict.keys():

	# Build file name
	agencyFilename = "pw_org_agency_output_id_" + str(linkId) + ".html"

	# See if this agency's web page has already been scraped.
	if not os.path.exists(agencyFilename):

		# Scrape agency's page and save output to text file
		cmd = "curl -k -s -XGET https://www.pw.org" + linkDict[linkId]
		print("Executing curl command: " + cmd)
		#r = os.popen(cmd).read()
		fhout = open(agencyFilename, "w")
		fhout.write(r)
		fhout.close()

		#sleep a random amount of time between 1.5 and 15 seconds to (hopefully) avoid detection
		random.seed()
		sleepSec = 15 * (random.random()) + 1.5
		print("Sleeping " + str(int(sleepSec * 1000)) + " milliseconds")
		time.sleep(sleepSec)

# Open the output csv
fhout = open(agencyCsvFile, "w")

# Open each agency page's html output and parse it.
print("-------------")
print("Scraping agency pages")
for linkId in linkDict.keys():

	# Build file name
	agencyFilename = "pw_org_agency_output_id_" + str(linkId) + ".html"

	# Open html file and read it in to variable r.
	fhin = open(agencyFilename, "r")
	r = ""
	while True:
		l = fhin.readline()
		if not l:
			break
		r += l
	fhin.close()

	# Parse; each line will look like this:
	#   <div class="collapsible required-fields"><div class="field field-name-field-agency-name field-type-text field-label-inline clearfix"><div class="field-label">Literary Agency:&nbsp;</div><div class="field-items"><div class="field-item even" property="schema:worksFor">DeFiore and Company</div></div></div><div class="field field-name-field-address-0 field-type-text field-label-inline clearfix"><div class="field-label">Address:&nbsp;</div><div class="field-items"><div class="field-item even" property=""><div class="address-block location vcard" property="schema:address" itemscope="" typeof="schema:PostalAddress"><div class="adr"><span class="fn rdf-meta element-hidden" value="Laurie  Abkemeier"></span><div class="street street-address" property="schema:streetAddress">47 East 19th Street</div><div class="additional extended-address" property="schema:streetAddress">Third Floor</div></div><span class="locality" property="schema:addressLocality">New York , </span><span class="province region" property="schema:addressRegion">NY </span><span class="postal-code" property="schema:postalCode">10003</span></div></div></div></div></div><div class="field-group-div"><div class="field field-name-field-agent-phone field-type-text field-label-inline clearfix"><div class="field-label">Phone:&nbsp;</div><div class="field-items"><div class="field-item even" property="schema:telephone">(212) 925-7744</div></div></div><div class="field field-name-field-agent-web field-type-link-field field-label-inline clearfix"><div class="field-label">Website:&nbsp;</div><div class="field-items"><div class="field-item even"><a href="http://www.defliterary.com" target="_blank" rel="nofollow" property="schema:url">http://www.defliterary.com</a></div></div></div><div class="field field-name-field-agent-email field-type-email field-label-inline clearfix"><div class="field-label">E-mail:&nbsp;</div><div class="field-items"><div class="field-item even" property="schema:email"><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#108;&#97;&#117;&#114;&#105;&#101;&#64;&#100;&#101;&#102;&#108;&#105;&#116;&#101;&#114;&#97;&#114;&#121;&#46;&#99;&#111;&#109;">&#108;&#97;&#117;&#114;&#105;&#101;&#64;&#100;&#101;&#102;&#108;&#105;&#116;&#101;&#114;&#97;&#114;&#121;&#46;&#99;&#111;&#109;</a></div></div></div><div class="field field-name-field-twitter-handle field-type-text field-label-inline clearfix"><div class="field-label">Twitter:&nbsp;</div><div class="field-items"><div class="field-item even" property=""><a href="https://twitter.com/LaurieAbkemeier" title="Twitter @LaurieAbkemeier" alt="Link to Twitter" target="_blank">@LaurieAbkemeier</a></div></div></div></div><div class="collapsible required-fields field-group-div"><div class="field field-name-field-electronic-submissions field-type-list-text field-label-inline clearfix"><div class="field-label">Accepts E-mail Queries:&nbsp;</div><div class="field-items"><div class="field-item even">Yes</div></div></div><div class="field field-name-taxonomy-vocabulary-20 field-type-taxonomy-term-reference field-label-inline clearfix"><div class="field-label">Interested in Representing:&nbsp;</div><div class="field-items"><div class="field-item even"><span class="textformatter-list">BIPOC Voices, Journalism/Investigative Reporting, Narrative Nonfiction, Nonfiction, Pop Culture</span></div></div></div><div class="field field-name-field-representative-authors field-type-text-long field-label-inline clearfix"><div class="field-label">Clients Include:&nbsp;</div><div class="field-items"><div class="field-item even">Jennifer Keishin Armstrong, John Grogan, Nathalia Holt, Cal Newport, Jessica Lahey, Yumi Sakugawa</div></div></div></div><span property="schema:jobTitle" content="Literary Agent" class="element-hidden"></span><span rel="schema:url" resource="/literary_agents/laurie_abkemeier" class="rdf-meta element-hidden"></span>

	# Street address
	# <div class="street street-address" property="schema:streetAddress">47 East 19th Street</div>
	reMatch = re.findall('<div class="street street-address" property="schema:streetAddress">(.+?)</div>', r)
	agentAddress = ""
	if len(reMatch) > 0:
		agentAddress = reMatch[0]

	# Extended address
	# <div class="additional extended-address" property="schema:streetAddress">Third Floor</div>
	reMatch = re.findall('<div class="additional extended-address" property="schema:streetAddress">(.+?)</div>', r)
	agentAExtAddr = ""
	if len(reMatch) > 0:
		agentExtAddr = reMatch[0]

	# Locality
	# <span class="locality" property="schema:addressLocality">New York , </span>
	reMatch = re.findall('<span class="locality" property="schema:addressLocality">(.+?)</span>', r)
	agentLocality = ""
	if len(reMatch) > 0:
		agentLocality = reMatch[0]
		agentLocality = re.sub(', *', '', agentLocality)		#remove comma-space sequence, if it exists

	# Region
	# <span class="province region" property="schema:addressRegion">NY </span>
	reMatch = re.findall('<span class="province region" property="schema:addressRegion">(.+?)</span>', r)
	agentRegion = ""
	if len(reMatch) > 0:
		agentRegion = reMatch[0]
		agentRegion = agentRegion.strip()			#remove leading and trailing whitespace

	# Postal code
	# <span class="postal-code" property="schema:postalCode">10003</span>
	reMatch = re.findall('<span class="postal-code" property="schema:postalCode">(.+?)</span>', r)
	agentPostal = ""
	if len(reMatch) > 0:
		agentPostal = reMatch[0]

	# Telephone
	# <div class="field-item even" property="schema:telephone">(212) 925-7744</div>
	reMatch = re.findall('<div class="field-item (?:even|odd)" property="schema:telephone">(.+?)</div>', r)
	agentPhone = ""
	if len(reMatch) > 0:
		agentPhone = reMatch[0]
	agentPhone = re.sub('[^0-9 \\-\\(\\)]', '', agentPhone)			#remove non phone number characters

	# Website
	# <div class="field field-name-field-agent-web field-type-link-field field-label-inline clearfix"><div class="field-label">Website:&nbsp;</div><div class="field-items"><div class="field-item even"><a href="http://www.defliterary.com" target="_blank" rel="nofollow" property="schema:url">http://www.defliterary.com</a></div>
	reMatch = re.findall('<div class="field field-name-field-agent-web .+?<a href="(.+?)"', r)
	agentWebsite = ""
	if len(reMatch) > 0:
		agentWebsite = reMatch[0]

	# Email
	# <div class="field field-name-field-agent-email field-type-email field-label-inline clearfix"><div class="field-label">E-mail:&nbsp;</div><div class="field-items"><div class="field-item even" property="schema:email"><a href="&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#108;&#97;&#117;&#114;&#105;&#101;&#64;&#100;&#101;&#102;&#108;&#105;&#116;&#101;&#114;&#97;&#114;&#121;&#46;&#99;&#111;&#109;">&#108;&#97;&#117;&#114;&#105;&#101;&#64;&#100;&#101;&#102;&#108;&#105;&#116;&#101;&#114;&#97;&#114;&#121;&#46;&#99;&#111;&#109;</a></div>
	reMatch = re.findall('<div class="field field-name-field-agent-email.+?property="schema:email"><a href="(.+?)"', r)
	agentEmail = ""
	if len(reMatch) > 0:
		# Convert encoded email to human-readable
		reChar = re.findall('&#(\d+);', reMatch[0])
		for c in reChar:
			agentEmail += chr(int(c))
	agentEmail = re.sub('mailto:', '', agentEmail)			# Remove 'mailto:' in email links

	# Twitter
	# <div class="field field-name-field-twitter-handle field-type-text field-label-inline clearfix"><div class="field-label">Twitter:&nbsp;</div><div class="field-items"><div class="field-item even" property=""><a href="https://twitter.com/LaurieAbkemeier" title="Twitter @LaurieAbkemeier" alt="Link to Twitter" target="_blank">@LaurieAbkemeier</a></div>
	reMatch = re.findall('<div class="field field-name-field-twitter-handle.+?<a .+>(@.+?)</a>', r)
	agentTwitter = ""
	if len(reMatch) > 0:
		agentTwitter = reMatch[0]

	# Accepts email queries
	# <div class="field field-name-field-electronic-submissions field-type-list-text field-label-inline clearfix"><div class="field-label">Accepts E-mail Queries:&nbsp;</div><div class="field-items"><div class="field-item even">Yes</div>
	reMatch = re.findall('<div class="field field-name-field-electronic-submissions.+?<div class="field-item (?:even|odd)">(Yes|No)</div>', r)
	agentElectronicSubmissions = ""
	if len(reMatch) > 0:
		agentElectronicSubmissions = reMatch[0]

	# Submission guidelines
	# <div class="field-group-div node-page-field-group"><h3><span>Submission Guidelines</span></h3><div class="field field-name-field-submission-guidelines field-type-text-long field-label-hidden"><div class="field-items"><div class="field-item even"><p>We only accept submissions via e-mail. Queries should be directed to <a href="mailto:query@psliterary.com">query@psliterary.com</a>.</p>
	#<p>We do not accept or respond to phone, paper or social media queries.</p>
	#</div>
	reMatch = re.findall('<div class="field-group-div node-page-field-group"><h3><span>Submission Guidelines</span>.+?<div class="field-item (?:even|odd)">(.+?)</div>', r, re.DOTALL)
	agentSubmissionGuidelines = ""
	if len(reMatch) > 0:
		agentSubmissionGuidelines = reMatch[0]
		agentSubmissionGuidelines = re.sub('(<p>|</p>)', '', agentSubmissionGuidelines)		#remove paragraph markup
		agentSubmissionGuidelines = re.sub('"', "'", agentSubmissionGuidelines)				#convert double quotes
		agentSubmissionGuidelines = re.sub('\n', " ", agentSubmissionGuidelines)			#convert newlines
		agentSubmissionGuidelines = agentSubmissionGuidelines.strip()						#strip leading and trailing whitespace

	# Tips from the agent
	# <div class="field-group-div node-page-field-group"><h3><span>Tips From the Agent</span></h3><div class="field field-name-field-editorial-tips field-type-text field-label-hidden"><div class="field-items"><div class="field-item even"><p>Check our website for the most up-to-date <a href="http://www.psliterary.com/submissions/" target="_blank">submission guidelines</a> and tips.</p>
	#</div>
	reMatch = re.findall('<div class="field-group-div node-page-field-group"><h3><span>Tips From the Agent</span>.+?<div class="field-item even">(.+?)</div>', r, re.DOTALL)
	agentTips = ""
	if len(reMatch) > 0:
		agentTips = reMatch[0]
		agentTips = re.sub('(<p>|</p>)', '', agentTips)			#remove paragraph markup
		agentTips = re.sub('"', "'", agentTips)					#convert double quotes
		agentTips = re.sub('\n', " ", agentTips)				#convert newlines
		agentTips = agentTips.strip()							#strip leading and trailing whitespace

	# Make output string
	outLine = linkId + ",\"" + agentAddress + "\",\"" + agentExtAddr + "\",\"" + agentLocality + "\",\"" + agentRegion + "\",\"" + agentPostal + \
		"\",\"" + agentPhone + "\",\"" + agentWebsite + "\",\"" + agentEmail + "\",\"" + agentTwitter + "\",\"" + agentElectronicSubmissions + \
		"\",\"" + agentSubmissionGuidelines + "\",\"" + agentTips + "\""
	outLine = remove_control_chars(outLine)						#remove non-printing characters

	# Print to screen and output file
	print(outLine)
	fhout.write(outLine + "\n")

# Close agency csv output file
fhout.close()
