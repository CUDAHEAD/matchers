import pandas as pd
import requests
import time
import os 
import subprocess


def download_images(type):

	df= pd.read_csv('./params/'+type+'.csv', usecols=[3,4]) 
	for index, row in df.iterrows(): 
		if index < 50:
			continue
		if index < 80:
			time.sleep(3)
			url =  row[0]
			try:
				r = requests.get(url, allow_redirects=True)
			except:
				print "failed fetching " + url
			open('./data/' + type + '_' + str(index) + '_1' , 'wb').write(r.content)
			url =  row[1]
			try:
				r = requests.get(url, allow_redirects=True)
			except:
				print "failed fetching " + url
			open('./data/' + type + '_' + str(index) + '_2' , 'wb').write(r.content)
			#print row[0] #print row['w1_img_link']
			print index


def run_matchers_on_images(type):
	data = []	
	for i in range(80):
		if i < 50:
			continue
		try:
			output = subprocess.Popen(['python', './sift_image_matcher.py', './data/'+type+'_'+str(i)+'_1', './data/'+type+'_'+str(i)+'_2'] ,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		except: 
			print str(i)+" failed to run.." 
			stdout_sift = "-1"
		else:
			stdout_sift, stderr = output.communicate()
			exit_code = output.wait()
			if exit_code != 0:
				stdout_sift = -1
			print("sift:" + str(stdout_sift))#, stderr, exit_code)
		
		try:
			output = subprocess.Popen(['python', './flann_image_matcher.py', './data/'+type+'_'+str(i)+'_1', './data/'+type+'_'+str(i)+'_2'] ,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		except: 
			print str(i)+" failed to run.." 
			stdout_flann = "-1"
		else:
			stdout_flann, stderr = output.communicate()
			exit_code = output.wait()
			if exit_code != 0:
				stdout_flann = -1
			print("flann:" + str(stdout_flann))#, stderr, exit_code)
	
		try:
			output = subprocess.Popen(['python', './surf_image_matcher.py', './data/'+type+'_'+str(i)+'_1', './data/'+type+'_'+str(i)+'_2'] ,stderr=subprocess.PIPE, stdout=subprocess.PIPE)
		except: 
			print str(i)+" failed to run.." 
			stdout_surf = "-1"
		else:
			stdout_surf, stderr = output.communicate()
			exit_code = output.wait()
			if exit_code != 0:
				stdout_surf = -1
			print("surf:" + str(stdout_surf))#, stderr, exit_code)
		
		print [str(stdout_sift).strip(), str(stdout_flann).strip(),str(stdout_surf).strip()]
		data.append([str(stdout_sift).strip(), str(stdout_flann).strip(),str(stdout_surf).strip()])

	
	df = pd.DataFrame(data, columns = ['sift', 'flann', 'surf'])
	print df

#download_images('notequal')
run_matchers_on_images('notequal')



