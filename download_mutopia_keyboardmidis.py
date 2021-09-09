import requests
import pandas as pd
import numpy as np
import re
from tqdm import tqdm
import os

#from a requests Response object, obtain midi file links
#only works with Mutopia
def get_midis_from_page(page_html):
	midi_links = []
	for l in page_html.iter_lines():
		matched_links = re.match('.+\"(.+.mid)\".+',str(l))
		if matched_links:
			midi_links.append(matched_links.groups(0)[0])
	return midi_links

#get link attached to the next 10 links
def get_next_page_midis(page_html):
	next_page = None
	for l in page_html.iter_lines():
		matched_link = re.match('.+\"(.+)\">Next 10.+', str(l))
		if matched_link:
			next_page = matched_link.groups(0)[0]
	if next_page:
		url_next = 'https://www.mutopiaproject.org/cgibin/' + next_page
		return requests.get(url_next)
	return next_page  

#get composer midis by looping through pages until none exist
def get_composer_midis(composer):
	url = 'https://www.mutopiaproject.org/cgibin/make-table.cgi?searchingfor=' + composer + '+' + 'piano'
	r = requests.get(url)
	all_midis = []
	all_midis.extend(get_midis_from_page(r))

	u = get_next_page(r)
	while u is not None:
		all_midis.etend(get_midis_from_page(u))
		u = get_next_page(u)

	return all_midis

def save_midi(link, directory):
	if not os.path.exists(directory):
		os.mkdir(directory)
	filename = link.split('/')[-1]
	response = requests.get(link, allow_redirects=True)
	with open(directory + '/' + filename, 'wb') as dir_file:
		dir_file.write(response.content)

composer_names = ['Bach', 'Mozart', 'Chopin', 
'Beethoven', 'Schubert', 'Schumann', 
'Rachmaninoff', 'Satie', 'Czerny']

all_composer_midis = {}
for c in tqdm(composer_names, leave = True, position = 0):
	all_composer_midis[c] = get_composer_midis[c]

for composer in all_composer_midis:
	for midi in tqdm(all_composer_midis[composer], leave = True, position = 0):
		save_midi(midi, 'Data/' + composer + 'KeyboardPieces')

