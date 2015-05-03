# Create your views here.
from django.shortcuts import render, get_object_or_404
from news.models import Hot,Dataset,Categories,Info
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template.defaultfilters import slugify
import csv

def articles(request):
	# get the blog posts that are published
	session_user="none"
	session_password="none"
	#vector Based
	sheet = list(csv.reader(open('news/csv/VectorBased.csv','rU')))

	if 'username' in request.session and request.session['username'] != "" and request.session['username'] != "none" :
		session_user=request.session['username']
		session_password=request.session['password']
		# print session_user
		userDocs = Info.objects.filter(user_id=int(session_user))
		flag = 0
		for row in sheet[1:]:
			if int(row[0]) == int(session_user):
				docs = zip(sheet[0][1:],row[1:])
				docs = sorted(docs,key=lambda l:l[1], reverse=True)
				print docs[0]
				print docs[1]
				flag = 1
				break
		firstTen = []
		if flag == 1:
			j = 10
			i = 0
			#print userDocs.count()
			pp = userDocs.filter(doc_id=215)
			#print pp.count()
			while i < j:
				# print i
				findSame = userDocs.filter(doc_id=int(docs[i][0]))
				if findSame.count() > 0:
					j+=1
				else:
					firstTen.append(docs[i])
				i += 1
			print firstTen
			vector = []
			for i in range(0,len(firstTen)):
				l =  Dataset.objects.filter(docid=int(firstTen[i][0]))
				list1=list()
				for x in l:
					list1.append(x.docid)
					list1.append(x.headline)
					list1.append(x.trailText)
					list1.append(x.byline)
					list1.append(x.body)
					list1.append(x.webURL)
					list1.append(x.published)
					list1.append(x.imageLink)
					list1.append(x.tags)
					list1.append(x.section)
					list1.append(x.clicks)
					list1.append(x.upvotes)
					list1.append(x.downvotes)
					print x.headline
				vector.append(list1)
				#print vector
				# print list2
				c={}
				c.update(csrf(request))
		# print "printing ------------------------------------"
		# print firstTen

	
	s = Hot.objects.all().order_by("-hottness")[:15]
	cat = Categories.objects.all().order_by("-occurences")
	
	list2=list()
	for i in range(0,15):
		l=Dataset.objects.filter(docid=s[i].docid)
		list1=list()
		for x in l:
			list1.append(x.docid)
			list1.append(x.headline)
			list1.append(x.trailText)
			list1.append(x.byline)
			list1.append(x.body)
			list1.append(x.webURL)
			list1.append(x.published)
			list1.append(x.imageLink)
			list1.append(x.tags)
			list1.append(x.section)
			list1.append(x.clicks)
			list1.append(x.upvotes)
			list1.append(x.downvotes)
			
		list2.append(list1)
		# print list2
		c={}
		c.update(csrf(request))
	#collaborative Filter
	sheetForCollaborative = list(csv.reader(open('news/csv/funkSVD3.csv','rU')))

	if 'username' in request.session and request.session['username'] != "" and request.session['username'] != "none" :
		session_user=request.session['username']
		session_password=request.session['password']
		# print session_user
		userDocsCollaborative = Info.objects.filter(user_id=int(session_user))
		flagCollaborative = 0
		for row in sheetForCollaborative[1:]:
			if int(row[0]) == int(session_user):
				docsCollaborative = zip(sheetForCollaborative[0][1:],row[1:])
				docsCollaborative = sorted(docsCollaborative,key=lambda l:l[1], reverse=True)
				
				flagCollaborative = 1
				break
		firstTenCollaborative = []
		if flagCollaborative == 1:
			j = 10
			i = 0
			
			while i < j:
				# print i
				findSameCollaborative = userDocsCollaborative.filter(doc_id=int(docsCollaborative[i][0]))
				if findSameCollaborative.count() > 0:
					j+=1
				else:
					firstTenCollaborative.append(docsCollaborative[i])
				i += 1
			print firstTenCollaborative
			vectorCollaborative = []
			for i in range(0,len(firstTenCollaborative)):
				l =  Dataset.objects.filter(docid=int(firstTenCollaborative[i][0]))
				list1=list()
				for x in l:
					list1.append(x.docid)
					list1.append(x.headline)
					list1.append(x.trailText)
					list1.append(x.byline)
					list1.append(x.body)
					list1.append(x.webURL)
					list1.append(x.published)
					list1.append(x.imageLink)
					list1.append(x.tags)
					list1.append(x.section)
					list1.append(x.clicks)
					list1.append(x.upvotes)
					list1.append(x.downvotes)
					print x.headline
				vectorCollaborative.append(list1)
	if session_user != "none" and  session_user != "":
		return render(request, 'user.html', {'username': session_user, 'categories' : cat, 'list2' : vector, 'popular': list2 ,'collaborative':vectorCollaborative})
	else:	 
		return render (request,'index.html',{'username':session_user, 'categories' : cat,'list2':list2})

def auth_view(request):
	username=request.POST.get('username','')   
	password=request.POST.get('password','')
	user=auth.authenticate(username=username,password=password )
	if user is not None:
		auth.login(request, user)
		request.session['username']=request.user.username
		request.session['password']=request.user.password
		return HttpResponseRedirect('/news/')
	else:
		return HttpResponseRedirect('/blog/invalid')

def login(request):
	if 'username' in request.session and request.session['username'] != "none" and request.session['username'] != "" :
		return HttpResponseRedirect('/news/')
	else:
		return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	request.session['username']="none"
	request.session['password']="none"
	return HttpResponseRedirect('/news/')

def about(request):
	return render(request, 'about.html')

def page(request):
	return render(request,'page.html')

def article(request, docid = 504):
	session_user="none"
	session_password="none"

	if 'username' in request.session and request.session['username'] != "" and request.session['username'] != "none" :
		session_user=request.session['username']
		session_password=request.session['password']

	l = Dataset.objects.filter(docid=docid)
	newsArticle = list()
	for x in l:
		newsArticle.append(x.docid)
		newsArticle.append(x.headline)
		newsArticle.append(x.trailText)
		newsArticle.append(x.byline)
		newsArticle.append(x.body)
		newsArticle.append(x.webURL)
		newsArticle.append(x.published)
		newsArticle.append(x.imageLink)
		newsArticle.append(x.tags)
		newsArticle.append(x.section)
		newsArticle.append(x.clicks)
		newsArticle.append(x.upvotes)
		newsArticle.append(x.downvotes)
	# print newsArticle

	s = Hot.objects.all().order_by("-hottness")[:15]
	cat = Categories.objects.all().order_by("-occurences")
	
	list2=list()
	for i in range(0,15):
		l=Dataset.objects.filter(docid=s[i].docid)
		list1=list()
		for x in l:
			list1.append(x.docid)
			list1.append(x.headline)
			list1.append(x.trailText)
			list1.append(x.byline)
			list1.append(x.body)
			list1.append(x.webURL)
			list1.append(x.published)
			list1.append(x.imageLink)
			list1.append(x.tags)
			list1.append(x.section)
			list1.append(x.clicks)
			list1.append(x.upvotes)
			list1.append(x.downvotes)
			
		list2.append(list1)
		# print list2
		c={}
		c.update(csrf(request))




	if session_user != "none" and  session_user != "":
		
		userStatus=Info.objects.filter(user_id=(int)(session_user),doc_id=docid)
		
		status=""
		if userStatus.exists():
			print userStatus[0]
			if userStatus[0].user_like==-1:
				status="dislike"
			elif userStatus[0].user_like==1:
				status="clicked"
				#print "h"
			else:
				status="liked"
		else:
			#print "hhhhh"
			p=Info(doc_id=docid,user_id=(int)(session_user),user_like=1)
			#print p.user_id
			#print p.user_like
			#print p.doc_id
			p.save()
			status="clicked"
			#print status
		return render(request, 'article.html', {'username': session_user, 'article': newsArticle, 'popular': list2 ,'status':status,'categories' : cat})
	else:	 
		return HttpResponseRedirect('/news/')


def contact(request):
	return render(request, 'contact.html')



def category(request,categoryName="technology"):
	#print categoryName
	session_user="none"
	session_password="none"
	if 'username' in request.session and request.session['username'] != "" and request.session['username'] != "none" :
		session_user=request.session['username']
		session_password=request.session['password']



	s = Hot.objects.all().order_by("-hottness")
	cat = Categories.objects.all().order_by("-occurences")
	#print "hi"
	ArticlesFromCategory=list()
	i=0
	
	for hot in s:
		#print hot.docid
		l=Dataset.objects.get(docid=hot.docid)
		#print l.section
		#print categoryName
		list1=list()
		
		if (slugify(l.section).lower())==(categoryName.lower()):
			print l.section
			#break;
			list1.append(l.docid)
			list1.append(l.headline)
			list1.append(l.trailText)
			list1.append(l.byline)
			list1.append(l.body)
			list1.append(l.webURL)
			list1.append(l.published)
			list1.append(l.imageLink)
			list1.append(l.tags)
			list1.append(l.section)
			list1.append(l.clicks)
			list1.append(l.upvotes)
			list1.append(l.downvotes)
			ArticlesFromCategory.append(list1)
			i+=1
		
		if i==10:
			#print ArticlesFromCategory
			break;
	
	#print "h"
	list2=list()
	for i in range(0,15):
		l=Dataset.objects.filter(docid=s[i].docid)
		list1=list()
		for x in l:
			list1.append(x.docid)
			list1.append(x.headline)
			list1.append(x.trailText)
			list1.append(x.byline)
			list1.append(x.body)
			list1.append(x.webURL)
			list1.append(x.published)
			list1.append(x.imageLink)
			list1.append(x.tags)
			list1.append(x.section)
			list1.append(x.clicks)
			list1.append(x.upvotes)
			list1.append(x.downvotes)
			
		list2.append(list1)
	print ArticlesFromCategory
	return render(request, 'category.html',{'categories' : cat,'category':categoryName.upper(),'username': session_user,'ArticlesFromCategory':ArticlesFromCategory,'popular': list2 })


def like(request,docid=504,userid=60):
	t = Info.objects.get(doc_id=docid,user_id=userid)
	t.user_like=2
	t.save()
	url="/news/"+docid
	return HttpResponseRedirect(url)
def dislike(request,docid=504,userid=60):
	t = Info.objects.get(doc_id=docid,user_id=userid)
	t.user_like=-1
	t.save()
	url="/news/"+docid
	return HttpResponseRedirect(url)
