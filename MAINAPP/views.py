from django.shortcuts import render
from . import forms
from .models import *
from MAINAPP.forms import UserForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.contrib.auth import authenticate , login , logout
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import joblib
import numpy as np
import keras
import tensorflow as tf
from django.templatetags.static import static
from django.utils import timezone
import pymongo


RFClassifierDiabetes=joblib.load('Models/RFClassifierDiabetes.pkl')
RFRegressorDiabetes=joblib.load('Models/RFRegressorDiabetes.pkl')
RFCHeart=joblib.load('Models/RFCHeartModel.pkl')
RFRHeart=joblib.load('Models/RFRHeartModel.pkl')
RFCBrainTumor=joblib.load('Models/RFCBrainTumor.pkl')
RFRBrainTumor=joblib.load('Models/RFRBrainTumor.pkl')
GBClassifierLiver=joblib.load('Models/GBClassifierLiver.pkl')
GBRegressorLiver=joblib.load('Models/GBRegressorLiver.pkl')
SVCmodelDPS=joblib.load('Models/SVCmodelDPS.pkl')
mentalhealthmodel = keras.models.load_model('Models/mentalhealthmodel')
RFClassifierDiet=joblib.load('Models/RFClassifierDiet.pkl')
RFClassifierASD=joblib.load('Models/RFClassifierModelASD.pkl')

# Create your views here.
def home(request):
	pages = Disease.objects.all()
	ct_form = forms.ContactMessageForm()
	if request.method =='POST':
		ct_form = forms.ContactMessageForm(request.POST)
		to = request.POST['reviewer_email']
		subject = 'The MediTrack'
		body = 'Hello'+'<p style="font-size:12px;">Thank you for reaching us, your message has been receieved & We will contact you shortly.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
		if ct_form.is_valid():
			ct_form.save()
			messages.info(request,"Successfully submitted !")
			return HttpResponseRedirect(reverse('home'))
		else:
			messages.error(request,"Invalid Details")
			return HttpResponseRedirect(reverse('home'))
	context = {'pages':pages, 'ct_form':ct_form}
	return render(request, 'MAINAPP/home.html', context)

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('home'))


def register(request):
	registered = False
	if request.method =='POST':
		user_form =UserForm(data = request.POST)

		if user_form.is_valid():
			 user =user_form.save()
			 user.set_password(user.password)
			 user.save()
			 registered = True
			 to = request.POST['email']
			 subject = 'Welcome to the MediTrack'
			 body = 'Welcome'+'<p style="font-size:13px;">Thank you for registration with MediTrack, we are glad to welcome you.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
			 msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
			 msg.content_subtype = "html"
			 msg.send(fail_silently=False)

			 messages.info(request,"Successfully Registered")
		else:
			print(user_form.errors)
	else :
		user_form =UserForm
	return render(request ,'MAINAPP/register.html',{'user_form': user_form ,'registered' : registered })

def registerasexpert(request):
	registered = False
	if request.method =='POST':
		uname=request.POST.get('username')
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		expname= fname +" "+ lname
		expemail=request.POST.get('email')
		expdesig=request.POST.get('expert_designation')
		if request.POST.get('expert_specialization')== "None":
			expspecial=request.POST.get('expert_specialization2')
		else :
			expspecial=request.POST.get('expert_specialization')
		expaddr=request.POST.get('expert_address')
		expcontact=request.POST.get('expert_contact')
		expimage=request.FILES.get('expert_image')
		o = HealthcareExpert(expert_username =uname, expert_name =expname, expert_email =expemail, expert_designation=expdesig, expert_specialization=expspecial, expert_address=expaddr, expert_contact=expcontact, expert_image = expimage)
		o.save()
		user_form =UserForm(data = request.POST)

		if user_form.is_valid():
			 user =user_form.save()
			 user.set_password(user.password)
			 user.save()
			 registered = True
			 to = request.POST['email']
			 subject = 'Welcome to the MediTrack'
			 body = 'Welcome'+'<p style="font-size:13px;">Thank you for registration with MediTrack, we are glad to welcome you.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
			 msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
			 msg.content_subtype = "html"
			 msg.send(fail_silently=False)

			 messages.info(request,"Successfully Registered")
		else:
			print(user_form.errors)
	else :
		user_form =UserForm
	context = {'user_form': user_form ,'registered' : registered }
	return render(request, 'MAINAPP/registerasexpert.html', context)



def user_login(request):
	if request.method =='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username , password=password )
		if user:
			if user.is_active:
				login(request , user)
				return HttpResponseRedirect(reverse('home'))

			else:
				return HttpResponse("ACCOUNT NOT ACTIVE")
		else:
			messages.error(request,"Invalid login details.")
			return HttpResponseRedirect("/user_login")
	else:
		return render(request , 'MAINAPP/login.html',{})





def diabetes_risk(request):

	return render(request, 'MAINAPP/diabetes.html')

def diabetes_risk_result(request):
	experts = HealthcareExpert.objects.all()
	if request.method == 'POST':
		Pregnancies=request.POST.get('val1')
		Glucose=request.POST.get('val2')
		BloodPressure=request.POST.get('val3')
		SkinThickness=request.POST.get('val4')
		Insulin=request.POST.get('val5')
		BMI=request.POST.get('val6')
		DiabetesPedigreeFunction=request.POST.get('val7')
		Age=request.POST.get('val8')
	input_data = (Pregnancies ,Glucose ,BloodPressure,SkinThickness ,Insulin ,BMI ,DiabetesPedigreeFunction ,Age)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictModelRFC = RFClassifierDiabetes.predict(input_data_reshaped)
	PredictModelRFR= RFRegressorDiabetes.predict(input_data_reshaped)*100
	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictModelRFR[0])
		if PredictModelRFC[0]==0:
			outcome="Lower chances of diabetes."
		else:
			outcome="Higher risk of diabetes, consult your local medical authority for advice."

		for i in experts :
			if i.expert_specialization == "Diabetes":
				to = i.expert_email
				subject = 'Validate Diagnosis Results'
				body = 'Hello '+i.expert_name+'<p style="font-size:13px;"><b>Below are the diagnosis results (Diabetes) of the MediTrack user. Kindly validate the results and revert to the user. User Email ID is mentioned below, along with the health metrics.</b></p>'+"User Email : "+request.user.email+'<br>'+'<p style="font-size:15px;"><b>Measures provided by the user :</b></p>'+'Pregnancies. &nbsp;&nbsp;'+Pregnancies+'<br>'+'Glucose. &nbsp;&nbsp;'+Glucose+'<br>'+'Blood Pressure. &nbsp;&nbsp;'+BloodPressure+'<br>'+'Skin Thickness. &nbsp;&nbsp;'+SkinThickness+'<br>'+'Insulin. &nbsp;&nbsp;'+Insulin+'<br>'+'BMI. &nbsp;&nbsp;'+BMI+'<br>'+'Diabetes pedigree func. &nbsp;&nbsp;'+DiabetesPedigreeFunction+'<br>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Diabetes Risk</b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
				msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
				msg.content_subtype = "html"
				msg.send(fail_silently=False)

		to = request.user.email
		subject = 'MediTrack'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at meditrack@gururaja.in</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Pregnancies. &nbsp;&nbsp;'+Pregnancies+'<br>'+'Glucose. &nbsp;&nbsp;'+Glucose+'<br>'+'Blood Pressure. &nbsp;&nbsp;'+BloodPressure+'<br>'+'Skin Thickness. &nbsp;&nbsp;'+SkinThickness+'<br>'+'Insulin. &nbsp;&nbsp;'+Insulin+'<br>'+'BMI. &nbsp;&nbsp;'+BMI+'<br>'+'Diabetes pedigree func. &nbsp;&nbsp;'+DiabetesPedigreeFunction+'<br>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Diabetes Risk</b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
		history=DiabetesDiagnosisHistory(username=request.user.username,Pregnancies=Pregnancies, Glucose=Glucose, BloodPressure=BloodPressure, SkinThickness=SkinThickness, Insulin=Insulin, BMI=BMI, DiabetesPedigreeFunction=DiabetesPedigreeFunction, Age=Age, outcome=outcome, risk_score=risk)
		history.save()
	context={'output1':PredictModelRFR[0] ,'output2':PredictModelRFC[0] ,'p':Pregnancies,'g':Glucose,'bp':BloodPressure,'st':SkinThickness,'insulin':Insulin,'bmi':BMI,'dpf':DiabetesPedigreeFunction,'age':Age}
	return render(request, 'MAINAPP/diabetes.html',context)



def cvd_prediction(request):
	context = {}
	return render(request, 'MAINAPP/heart.html', context)

def cvd_prediction_result(request):
	experts = HealthcareExpert.objects.all()
	if request.method == 'POST':
		age=request.POST.get('val1')
		sex=request.POST.get('val2')
		cp=request.POST.get('val3')
		trestbps=request.POST.get('val4')
		chol=request.POST.get('val5')
		fbs=request.POST.get('val6')
		restecg=request.POST.get('val7')
		thalach=request.POST.get('val8')
		exang=request.POST.get('val9')
		oldpeak=request.POST.get('val10')
		slope=request.POST.get('val11')
	input_data = (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictRFCHeart= RFCHeart.predict(input_data_reshaped)
	PredictRFRHeart= RFRHeart.predict(input_data_reshaped)*100
	if sex== '1':
		genderText="Male"
	else:
		genderText="Female"

	if fbs== '1':
		fbsText="Yes"
	else:
		fbsText="No"

	if cp== '3':
		cpText="Typical angina"
	elif cp=='2':
		cpText="Non-anginal pain"
	elif cp=='1':
		cpText='Atypical angina'
	else:
		cpText='Asymptomatic'

	if restecg=='2':
		restecgText="Having ST-T wave abnormality"
	elif restecg=='1':
		restecgText="Normal"
	else:
		restecgText="Probable/definite left ventricular hypertrophy"

	if exang=='1':
		exangText ="Yes"
	else:
		exangText ="No"

	if slope=='2':
		slopeText="Upsloping"
	elif slope=='1':
		slopeText="Flat"
	else:
		slopeText="Downsloping"

	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictRFRHeart[0])
		if PredictRFCHeart[0]==0:
			outcome="Lower possibility of  cardiovascular disease"
		else:
			outcome="Higher risk of cardiovascular disease, consult your local medical authority for advice."

		for i in experts :
			if i.expert_specialization == "Heart Disease":
				to = i.expert_email
				subject = 'Validate Diagnosis Results'
				body = 'Hello '+i.expert_name+'<p style="font-size:13px;"><b>Below are the diagnosis results (heart disease) of the MediTrack user. Kindly validate the results and revert to the user. User Email ID is mentioned below, along with the health metrics.</b></p>'+"User Email : "+request.user.email+'<br>'+'<p style="font-size:15px;"><b>Measures provided by the user :</b></p>'+'Age. &nbsp;&nbsp;'+age+'<br>'+'Resting blood pressure. &nbsp;&nbsp;'+trestbps+'<br>'+'Cholesterol. &nbsp;&nbsp;'+chol+'<br>'+'Thalach. &nbsp;&nbsp;'+thalach+'<br>'+'Oldpeak. &nbsp;&nbsp;'+oldpeak+'<br>'+'Gender. &nbsp;&nbsp;'+genderText+'<br>'+'Fasting blood sugar > 120 mg/dl. &nbsp;&nbsp;'+fbsText+'<br>'+'Chest pain type. &nbsp;&nbsp;'+cpText+'<br>'+'Resting electrocardiographic results. &nbsp;&nbsp;'+restecgText+'<br>'+'Exercise induced angina. &nbsp;&nbsp;'+exangText+'<br>'+'Slope of the peak exercise ST segment. &nbsp;&nbsp;'+slopeText+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>CVD Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
				msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
				msg.content_subtype = "html"
				msg.send(fail_silently=False)

		to = request.user.email
		subject = 'The MediTrack'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at meditrack@gururaja.in</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Age. &nbsp;&nbsp;'+age+'<br>'+'Resting blood pressure. &nbsp;&nbsp;'+trestbps+'<br>'+'Cholesterol. &nbsp;&nbsp;'+chol+'<br>'+'Thalach. &nbsp;&nbsp;'+thalach+'<br>'+'Oldpeak. &nbsp;&nbsp;'+oldpeak+'<br>'+'Gender. &nbsp;&nbsp;'+genderText+'<br>'+'Fasting blood sugar > 120 mg/dl. &nbsp;&nbsp;'+fbsText+'<br>'+'Chest pain type. &nbsp;&nbsp;'+cpText+'<br>'+'Resting electrocardiographic results. &nbsp;&nbsp;'+restecgText+'<br>'+'Exercise induced angina. &nbsp;&nbsp;'+exangText+'<br>'+'Slope of the peak exercise ST segment. &nbsp;&nbsp;'+slopeText+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>CVD Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
		history= HeartDiseaseDiagnosisHistory(username=request.user.username, age=age, sex=genderText, cp=cpText, trestbps=trestbps, chol=chol, fbs=fbsText, restecg=restecgText, thalach=thalach, exang=exangText, oldpeak=oldpeak, slope=slopeText, outcome=outcome, risk_score=risk)
		history.save()
	context={'output1':PredictRFRHeart[0] ,'output2':PredictRFCHeart[0] ,'age':age, 'sex':sex, 'cp':cp, 'tb':trestbps, 'cl':chol, 'fb':fbs, 'rst':restecg, 'thal':thalach, 'ex':exang, 'old':oldpeak, 'slp':slope, 'genderText':genderText,'fbsText':fbsText,'cpText':cpText,'restecgText':restecgText,'exangText':exangText,'slopeText':slopeText}
	return render(request, 'MAINAPP/heart.html', context)


def detect_brain_tumor(request):

	context = {}
	return render(request, 'MAINAPP/brain.html', context)

def detect_brain_tumor_result(request):
	experts = HealthcareExpert.objects.all()
	if request.method == 'POST':
		Mean=request.POST.get('val1')
		Variance=request.POST.get('val2')
		StandardDeviation=request.POST.get('val3')
		Entropy=request.POST.get('val4')
		Skewness=request.POST.get('val5')
		Kurtosis=request.POST.get('val6')
		Contrast=request.POST.get('val7')
		Energy=request.POST.get('val8')
		ASM	=request.POST.get('val9')
		Homogeneity=request.POST.get('val10')
		Dissimilarity=request.POST.get('val11')
		Correlation=request.POST.get('val12')
		Coarseness=request.POST.get('val13')
		PSNR=request.POST.get('val14')
		SSIM=request.POST.get('val15')
		MSE=request.POST.get('val16')
		DC=request.POST.get('val17')
	input_data = (Mean, Variance, StandardDeviation, Entropy, Skewness, Kurtosis, Contrast, Energy, ASM, Homogeneity, Dissimilarity, Correlation, Coarseness, PSNR, SSIM, MSE, DC)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictRFCBrainTumor= RFCBrainTumor.predict(input_data_reshaped)
	PredictRFRBrainTumor= RFRBrainTumor.predict(input_data_reshaped)*100
	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictRFRBrainTumor[0])
		if PredictRFCBrainTumor[0]==0:
			outcome="Possibility of brain tumour is negligible."
		else:
			outcome="Higher possibility of brain tumour detected."

		for i in experts :
			if i.expert_specialization == "Brain Tumor":
				to = i.expert_email
				subject = 'Validate Diagnosis Results'
				body = 'Hello '+i.expert_name+'<p style="font-size:13px;"><b>Below are the diagnosis results (Brain Tumor) of the MediTrack user. Kindly validate the results and revert to the user. User Email ID is mentioned below, along with the health metrics.</b></p>'+"User Email : "+request.user.email+'<br>'+'<p style="font-size:15px;"><b>Measures provided by the user :</b></p>'+'Mean. &nbsp;&nbsp;'+Mean+'<br>'+'Variance. &nbsp;&nbsp;'+Variance+'<br>'+'Standard Deviation. &nbsp;&nbsp;'+StandardDeviation+'<br>'+'Entropy. &nbsp;&nbsp;'+Entropy+'<br>'+'Skewness. &nbsp;&nbsp;'+Skewness	+'<br>'+'Kurtosis. &nbsp;&nbsp;'+Kurtosis+'<br>'+'Contrast. &nbsp;&nbsp;'+Contrast+'<br>'+'Energy. &nbsp;&nbsp;'+Energy+'<br>'+'ASM. &nbsp;&nbsp;'+ASM+'<br>'+'Homogeneity. &nbsp;&nbsp;'+Homogeneity+'<br>'+'Dissimilarity. &nbsp;&nbsp;'+Dissimilarity+'<br>'+'Correlation. &nbsp;&nbsp;'+Correlation+'<br>'+'Coarseness. &nbsp;&nbsp;'+Coarseness+'<br>'+'PSNR. &nbsp;&nbsp;'+PSNR+'<br>'+'SSIM. &nbsp;&nbsp;'+SSIM+'<br>'+'MSE. &nbsp;&nbsp;'+MSE+'<br>'+'DC. &nbsp;&nbsp;'+DC+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Possibility. </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
				msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
				msg.content_subtype = "html"
				msg.send(fail_silently=False)

		to = request.user.email
		subject = 'The MediTrack'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at meditrack@gururaja.in</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Mean. &nbsp;&nbsp;'+Mean+'<br>'+'Variance. &nbsp;&nbsp;'+Variance+'<br>'+'Standard Deviation. &nbsp;&nbsp;'+StandardDeviation+'<br>'+'Entropy. &nbsp;&nbsp;'+Entropy+'<br>'+'Skewness. &nbsp;&nbsp;'+Skewness	+'<br>'+'Kurtosis. &nbsp;&nbsp;'+Kurtosis+'<br>'+'Contrast. &nbsp;&nbsp;'+Contrast+'<br>'+'Energy. &nbsp;&nbsp;'+Energy+'<br>'+'ASM. &nbsp;&nbsp;'+ASM+'<br>'+'Homogeneity. &nbsp;&nbsp;'+Homogeneity+'<br>'+'Dissimilarity. &nbsp;&nbsp;'+Dissimilarity+'<br>'+'Correlation. &nbsp;&nbsp;'+Correlation+'<br>'+'Coarseness. &nbsp;&nbsp;'+Coarseness+'<br>'+'PSNR. &nbsp;&nbsp;'+PSNR+'<br>'+'SSIM. &nbsp;&nbsp;'+SSIM+'<br>'+'MSE. &nbsp;&nbsp;'+MSE+'<br>'+'DC. &nbsp;&nbsp;'+DC+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Possibility. </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
		history=BrainTumorDiagnosisHistory(username= request.user.username, Mean=Mean , Variance= Variance, StandardDeviation=StandardDeviation , Entropy= Entropy , Skewness=Skewness , Kurtosis=Kurtosis , Contrast= Contrast, Energy= Energy, ASM=ASM , Homogeneity=Homogeneity , Dissimilarity=Dissimilarity , Correlation= Correlation, Coarseness=Coarseness , PSNR=PSNR , SSIM=SSIM , MSE=MSE , DC= DC, outcome= outcome, risk_score=risk)
		history.save()
	context={'output1':PredictRFRBrainTumor[0] ,'output2':PredictRFCBrainTumor[0] ,'Mean':Mean, 'Variance':Variance, 'StandardDeviation':StandardDeviation, 'Entropy':Entropy, 'Skewness':Skewness, 'Kurtosis':Kurtosis,'Contrast': Contrast, 'Energy':Energy, 'ASM':ASM, 'Homogeneity':Homogeneity, 'Dissimilarity':Dissimilarity, 'Correlation':Correlation, 'Coarseness':Coarseness, 'PSNR':PSNR, 'SSIM':SSIM, 'MSE':MSE, 'DC':DC}
	return render(request, 'MAINAPP/brain.html', context)


def liver_diagnosis(request):

	context = {}
	return render(request, 'MAINAPP/liver.html', context)

def liver_diagnosis_result(request):
	experts = HealthcareExpert.objects.all()
	if request.method == 'POST':
		Age=request.POST.get('val1')
		Gender=request.POST.get('val2')
		Total_Bilirubin=request.POST.get('val3')
		Direct_Bilirubin=request.POST.get('val4')
		Alkaline_Phosphotase=request.POST.get('val5')
		Alamine_Aminotransferase=request.POST.get('val6')
		Aspartate_Aminotransferase=request.POST.get('val7')
		Total_Protiens=request.POST.get('val8')
		Albumin=request.POST.get('val9')
		Albumin_and_Globulin_Ratio=request.POST.get('val10')
	input_data = (Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictGBClassifierLiver = GBClassifierLiver.predict(input_data_reshaped)
	PredictGBRegressorLiver= GBRegressorLiver.predict(input_data_reshaped)*100
	if Gender== '1':
		GenderText="Male"
	else:
		GenderText="Female"

	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		risk=str(PredictGBRegressorLiver[0])
		if PredictGBClassifierLiver[0]==0:
			outcome="Lower possibility of  liver disease"
		else:
			outcome="Higher risk of liver disease, consult your local medical authority for advice."

		for i in experts :
			if i.expert_specialization == "Liver Disease":
				to = i.expert_email
				subject = 'Validate Diagnosis Results'
				body = 'Hello '+i.expert_name+'<p style="font-size:13px;"><b>Below are the diagnosis results (Liver Disease) of the MediTrack user. Kindly validate the results and revert to the user. User Email ID is mentioned below, along with the health metrics.</b></p>'+"User Email : "+request.user.email+'<br>'+'<p style="font-size:15px;"><b>Measures provided by the user :</b></p>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'Gender. &nbsp;&nbsp;'+GenderText+'<br>'+'Total Bilirubin. &nbsp;&nbsp;'+Total_Bilirubin+'<br>'+'Direct Bilirubin. &nbsp;&nbsp;'+Direct_Bilirubin+'<br>'+'Alkaline Phosphotase. &nbsp;&nbsp;'+Alkaline_Phosphotase+'<br>'+'Alamine Aminotransferase. &nbsp;&nbsp;'+Alamine_Aminotransferase+'<br>'+'Aspartate Aminotransferase. &nbsp;&nbsp;'+Aspartate_Aminotransferase+'<br>'+'Total Protiens. &nbsp;&nbsp;'+Total_Protiens+'<br>'+'Albumin. &nbsp;&nbsp;'+Albumin+'<br>'+'Albumin and Globulin Ratio. &nbsp;&nbsp;'+Albumin_and_Globulin_Ratio+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
				msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
				msg.content_subtype = "html"
				msg.send(fail_silently=False)

		to = request.user.email
		subject = 'The MediTrack'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;"><b>Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of measures provided by you. For any queries drop us a mail at meditrack@gururaja.in</b></p>'+'<p style="font-size:15px;"><b>Measures provided by you :</b></p>'+'Age. &nbsp;&nbsp;'+Age+'<br>'+'Gender. &nbsp;&nbsp;'+GenderText+'<br>'+'Total Bilirubin. &nbsp;&nbsp;'+Total_Bilirubin+'<br>'+'Direct Bilirubin. &nbsp;&nbsp;'+Direct_Bilirubin+'<br>'+'Alkaline Phosphotase. &nbsp;&nbsp;'+Alkaline_Phosphotase+'<br>'+'Alamine Aminotransferase. &nbsp;&nbsp;'+Alamine_Aminotransferase+'<br>'+'Aspartate Aminotransferase. &nbsp;&nbsp;'+Aspartate_Aminotransferase+'<br>'+'Total Protiens. &nbsp;&nbsp;'+Total_Protiens+'<br>'+'Albumin. &nbsp;&nbsp;'+Albumin+'<br>'+'Albumin and Globulin Ratio. &nbsp;&nbsp;'+Albumin_and_Globulin_Ratio+'<br>'+'<p style="font-size:18px;text-align:center"><b>Outcomes</b></p>'+'<b>Risk </b> &nbsp;&nbsp; '+risk+' % <br>'+'<b>Remarks. &nbsp;&nbsp;</b>'+outcome+'<hr><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
		history=LiverDiseaseDiagnosisHistory(username=request.user.username, Age=Age, Gender=GenderText, Total_Bilirubin=Total_Bilirubin, Direct_Bilirubin=Direct_Bilirubin, Alkaline_Phosphotase=Alkaline_Phosphotase, Alamine_Aminotransferase=Alamine_Aminotransferase, Aspartate_Aminotransferase=Aspartate_Aminotransferase, Total_Protiens=Total_Protiens, Albumin=Albumin, Albumin_and_Globulin_Ratio=Albumin_and_Globulin_Ratio, outcome=outcome, risk_score=risk)
		history.save()
	context={'output1':PredictGBRegressorLiver[0] ,'output2':PredictGBClassifierLiver[0] ,'Age':Age, 'Gender':Gender, 'TBIL':Total_Bilirubin,'DBIL':Direct_Bilirubin, 'ALKP':Alkaline_Phosphotase, 'Alamine':Alamine_Aminotransferase, 'Aspartate':Aspartate_Aminotransferase, 'Protiens':Total_Protiens, 'Albumin':Albumin, 'AGR':Albumin_and_Globulin_Ratio,'GenderText':GenderText}
	return render(request, 'MAINAPP/liver.html', context)

def diagnosistools(request):
	context = {}
	return render(request, 'MAINAPP/diagnosistools.html', context)

def symptomsdiagnosis(request):

	context = {}
	return render(request, 'MAINAPP/symptomsdiagnosis.html', context)

def symptomsdiagnosis_result(request):
	if request.method == 'POST':
		symptom1=request.POST.get('symptom1')
		symptom2=request.POST.get('symptom2')
		symptom3=request.POST.get('symptom3')
		symptom4=request.POST.get('symptom4')
		symptom5=request.POST.get('symptom5')
		symptom6=request.POST.get('symptom6')

	inputsymptoms=[symptom1,symptom2,symptom3,symptom4,symptom5,symptom6]
	nulls = [0,0,0,0,0,0,0,0,0,0,0]
	finalinput = [inputsymptoms + nulls]
	predict = SVCmodelDPS.predict(finalinput)
	query=predict[0]
	results_disease = Disease.objects.filter(disease_name__icontains=query)
	results_disease_description = Disease.objects.filter(disease_description__icontains=query)
	results_disease_medication = Disease.objects.filter(disease_medication__icontains=query)
	results_disease_precautions = Disease.objects.filter(disease_precautions__icontains=query)
	results =results_disease.union(results_disease_description,results_disease_medication,results_disease_precautions)
	if request.user.is_authenticated :
		userfirstname=request.user.first_name
		if symptom1 == "0" and symptom2 == "0" and symptom3 == "0" and symptom4 == "0" and symptom5 == "0" and symptom6 == "0":
			mailtext="No complications found. You are disease free."
		else:
			mailtext="You are suffering from "+predict[0]
		to = request.user.email
		subject = 'The MediTrack'
		body = 'Hello '+userfirstname+'<p style="font-size:13px;">Thank you for trusting our services, we are sending this email to let you know about the predicted outcomes on the basis of symptoms provided by you. For any queries drop us a mail at meditrack@gururaja.in</p>'+'<br> Results : <br>'+mailtext+'<br><p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'+'<p style="font-size:13px;color:#A6ACAF;text-align:center;"><i>These outcomes are for informational purposes only, Consult your local medical authority for advice.</i></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)
	context = { 'predict':predict[0], 'symptom1':symptom1, 'symptom2':symptom2, 'symptom3':symptom3, 'symptom4':symptom4, 'symptom5':symptom5, 'symptom6':symptom6, 'results':results}
	return render(request, 'MAINAPP/symptomsdiagnosis.html', context)



def article(request):

	pages = Disease.objects.all()
	topics =reversed(Disease.objects.all().order_by('id'))
	context = {'pages':pages ,'topics':topics}
	return render(request, 'MAINAPP/article.html', context)

def read_article(request ,id):
	page = Disease.objects.get(id=id)
	topics =reversed(Disease.objects.all().order_by('id'))
	context = {'page':page ,'topics':topics}
	return render(request, 'MAINAPP/read_article.html', context)

def mentalhealth(request):

	context = {}
	return render(request, 'MAINAPP/mentalhealth.html', context)

def postprocessor(preds):
  range = 43.391766-(-17.053513)
  norm_preds = []
  probab = []
  for i in preds:
    norm_preds.append((i - (-17.053513)) / range)
    probab.append((i - (-17.053513)) * 100 / range)
  return np.mean(probab)

def mentalhealth_results(request):
	if request.method == 'POST':
		question1=request.POST.get('question1')
		question2=request.POST.get('question2')
		question3=request.POST.get('question3')
		question4=request.POST.get('question4')
	answers = []
	answers.append(question1)
	answers.append(question2)
	answers.append(question3)
	answers.append(question4)
	results = mentalhealthmodel.predict(answers)
	score=postprocessor(results)
	if score < 0:
		score=0
	if score>100:
		score=100
	hlines =Helpline.objects.all()
	context = {'score':score, 'hlines':hlines}
	return render(request, 'MAINAPP/mentalhealth.html', context)
def ASDdiagnosis(request):
	context = {}
	return render(request, 'MAINAPP/ASDdiagnosis.html', context)

def ASDdiagnosis_result(request):
	if request.method == 'POST':
		Q1=request.POST.get('val1')
		Q2=request.POST.get('val2')
		Q3=request.POST.get('val3')
		Q4=request.POST.get('val4')
		Q5=request.POST.get('val5')
		Q6=request.POST.get('val6')	
		Q7=request.POST.get('val7')
		Q8=request.POST.get('val8')
		Q9=request.POST.get('val9')
		Q10=request.POST.get('val10')
		Q11=request.POST.get('val11')
		Q12=request.POST.get('val12')
		Q13=request.POST.get('val13')
		Q14=request.POST.get('val14')
		Q15=request.POST.get('val15')						
	input_data = (Q1,Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Q10,Q11,Q12,Q13,Q14,Q15)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictModelRFC = RFClassifierASD.predict(input_data_reshaped)

	
	if PredictModelRFC[0]==0:
		outcome="No significant evidence of Autism Spectrum Disorder (ASD) traits in the child. "
	else:
		outcome="The results indicate the presence of potential Autism Spectrum Disorder (ASD) traits in the child."

	context={'output1':outcome,'Q1':Q1,'Q2':Q2,'Q3':Q3,'Q4':Q4,'Q5':Q5,'Q6':Q6,'Q7':Q7,'Q8':Q8,'Q9':Q9,'Q10':Q10,'Q11':Q11,'Q12':Q12,'Q13':Q13,'Q14':Q14,'Q15':Q15}
	return render(request, 'MAINAPP/ASDdiagnosis.html', context)

def search(request):
	query=request.GET['query']
	pages_posted_on = Disease.objects.filter(posted_on__icontains=query)
	pages_article_name = Disease.objects.filter(disease_name__icontains=query)
	pages_article_caption = Disease.objects.filter(disease_caption__icontains=query)
	pages_article_description = Disease.objects.filter(disease_description__icontains=query)
	pages_article_symptoms = Disease.objects.filter(disease_symptoms__icontains=query)
	pages_article_precautions = Disease.objects.filter(disease_precautions__icontains=query)
	pages_article_medication = Disease.objects.filter(disease_medication__icontains=query)

	pages =pages_posted_on.union( pages_article_name, pages_article_caption, pages_article_description, pages_article_symptoms , pages_article_precautions,pages_article_medication)

	tools_tool_name = DiagnosisTool.objects.filter(tool_name__icontains=query)
	tools_tool_accuracy = DiagnosisTool.objects.filter(tool_accuracy__icontains=query)
	tools_tool_technology = DiagnosisTool.objects.filter(tool_technology__icontains=query)
	tools_tool_detail = DiagnosisTool.objects.filter(tool_detail__icontains=query)
	tools=tools_tool_name.union(tools_tool_accuracy,tools_tool_technology,tools_tool_detail )
	context = {'tools':tools ,'pages':pages ,'query':query }
	return render(request, 'MAINAPP/search.html', context)



def about(request):
	context = {}
	return render(request, 'MAINAPP/about.html', context)

def  page_not_found(request ,exception=None):
	return render(request, 'MAINAPP/404.html')

def diet_plan(request):

	context = {}
	return render(request, 'MAINAPP/diet.html', context)
def diet_plan_result(request):
	if request.method == 'POST':
		age=request.POST.get('val1')
		sex=request.POST.get('val2')
		height=request.POST.get('val3')
		weight=request.POST.get('val4')
		user_is_diabetic=request.POST.get('val5')
		veg_only=request.POST.get('veg_only')
	bmi=float(weight)//(float(height)*float(height))
	input_data = (age,sex,bmi)
	input_data_as_numpy_array= np.asarray(input_data)
	input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)
	PredictModelRFC = RFClassifierDiet.predict(input_data_reshaped)
	query=PredictModelRFC[0]
	plans = Food.objects.filter(diet_category__icontains=query)
	vegfood=False
	if veg_only == "True":
		vegfood= True
	context = {'output':PredictModelRFC[0],'bmi':bmi,'plans':plans,'user_is_diabetic':user_is_diabetic,'vegfood':vegfood}
	return render(request, 'MAINAPP/diet.html', context)


def accounts(request):
	created = False
	profiles = MedicalProfile.objects.all()
	if request.user.is_authenticated :
		for i in profiles:
			if i.username == request.user.username:
				created = True
	history1=DiabetesDiagnosisHistory.objects.all()
	history2=HeartDiseaseDiagnosisHistory.objects.all()
	history3=LiverDiseaseDiagnosisHistory.objects.all()
	history4=BrainTumorDiagnosisHistory.objects.all()
	flag1=False
	flag2=False
	flag3=False
	flag4=False
	if request.user.is_authenticated :
		for i in history1:
			if i.username == request.user.username:
				flag1=True
				break
		for i in history2:
			if i.username == request.user.username:
				flag2=True
				break
		for i in history3:
			if i.username == request.user.username:
				flag3=True
				break
		for i in history4:
			if i.username == request.user.username:
				flag4=True
				break

	context = {'profiles':profiles,'created':created,'history1':history1,'history2':history2,'history3':history3,'history4':history4, 'flag1':flag1,'flag2':flag2,'flag3':flag3,'flag4':flag4}

	return render(request, 'MAINAPP/accounts.html', context)


def rating(request):
	reviews=Rating.objects.all()
	if request.method == 'POST':
		rating_parameter=request.POST.get('rating_parameter')
		rating_message=request.POST.get('rating_message')
		rating_tool=request.POST.get('rating_tool')
		user=request.POST.get('user')
		if rating_tool is  None:
			rating_tool ='General'
		if request.user.is_authenticated :
				userfirstname=request.user.first_name
				userlastname=request.user.last_name
				name=userfirstname +" "+ userlastname
				o = Rating(rating_user=name,rating_tool=rating_tool,rating_parameter=rating_parameter,rating_message=rating_message)
		else :
			o = Rating(rating_user=user,rating_tool=rating_tool,rating_parameter=rating_parameter,rating_message=rating_message)
		o.save()
	context = {'reviews':reviews}
	return render(request, 'MAINAPP/rating.html', context)

def report(request):
	rt_form = forms.ReportForm()
	if request.method =='POST':
		rt_form= forms.ReportForm(request.POST,request.FILES)
		if rt_form.is_valid():
			rt_form.save()
			messages.info(request,"Successfully submitted !")
			return HttpResponseRedirect("/report")
		else:
			messages.error(request,"Invalid Details")
			print(rt_form.errors.as_data())
			return HttpResponseRedirect("/report")
	context = {'rt_form':rt_form}
	return render(request, 'MAINAPP/report.html', context)


def healthcareexperts(request):
	experts = HealthcareExpert.objects.all()
	context = {'experts':experts}
	return render(request, 'MAINAPP/healthcareexperts.html', context)





def create_medical_profile(request):
	created = False
	profiles = MedicalProfile.objects.all()
	if request.user.is_authenticated :
		for i in profiles:
			if i.username == request.user.username:
				created = True

	if request.user.is_authenticated :
		if created == False :
			if request.method == 'POST':
				mp_age =request.POST.get('age')
				mp_gender =request.POST.get('gender')
				mp_blood_group =request.POST.get('blood_group')
				mp_height =request.POST.get('height')
				mp_weight =request.POST.get('weight')
				mp_emergency_contact =request.POST.get('emergency_contact')
				mp_diabetic =request.POST.get('diabetic')
				my_profile = MedicalProfile(username =request.user.username, age = mp_age, gender = mp_gender ,blood_group =mp_blood_group , height = mp_height , weight = mp_weight, emergency_contact =mp_emergency_contact , diabetic = mp_diabetic )
				my_profile.save()
				return HttpResponseRedirect("/accounts")

	context = {'created':created}
	return render(request, 'MAINAPP/create_medical_profile.html', context)

def update_medical_profile(request, id):
	created = False
	profiles = MedicalProfile.objects.all()
	if request.user.is_authenticated :
		for i in profiles:
			if i.username == request.user.username:
				created = True
	profile = MedicalProfile.objects.get(id=id)
	update_form = forms.MedicalProfileUpdateForm(instance=profile)
	if request.method =='POST':
		update_form= forms.MedicalProfileUpdateForm(request.POST,instance=profile)
		if update_form.is_valid():
			update_form.save()
			messages.info(request,"Successfully updated")
			return HttpResponseRedirect("/accounts")
		else:
			messages.error(request,"Invalid Details")
			print(update_form.errors.as_data())
			return HttpResponseRedirect("/update_medical_profile")
	update_date=timezone.now
	context = {'update_form':update_form,'created':created,'profile':profile,'update_date':update_date}
	return render(request, 'MAINAPP/update_medical_profile.html', context)


def appointment(request ,id):
	expert = HealthcareExpert.objects.get(id=id)
	if request.method =='POST':
		apt_booked_by =request.POST.get('booked_by')
		apt_preferred_date=request.POST.get('preferred_date')
		apt_user_email=request.POST.get('user_email')
		apt_problem=request.POST.get('problem')
		o = Appointment(preferred_date=apt_preferred_date, booked_by = apt_booked_by, user_email =apt_user_email, expert_username = expert.expert_username, expert_email = expert.expert_email, problem =apt_problem)
		o.save()
		to = apt_user_email
		subject = 'Appointment Booked'
		body = 'Hello '+apt_booked_by+'<p style="font-size:12px;">Your appointment has been successfully booked. The expert will contact you within 48 Hrs for confirmation and other details. <br> Note: Booking does not guarantee your appointment confirmation, your expert may accept or decline your appointment.</p>'+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
		msg = EmailMultiAlternatives(subject, body,'guru@disroot.org', [to])
		msg.content_subtype = "html"
		msg.send(fail_silently=False)


		to2 = expert.expert_email
		subject2 = 'User Appointment Request'
		body2 = 'Hello '+expert.expert_name+'<p style="font-size:12px;">The appointment details of the user are mentioned below, kindly revert to the user within 48 Hrs of the request.</p>'+"Name : "+apt_booked_by+"<br>"+"Email : "+apt_user_email+"<br>"+"Preferred Date : "+apt_preferred_date+"<br>"+"Appointment Note : "+apt_problem+'<p style="margin-bottom:0px;">Thanks & Regards,</p>'+'<p style="margin-top:2px;"><b>The MediTrack Team</b></p>'
		msg2 = EmailMultiAlternatives(subject2, body2,'guru@disroot.org', [to2])
		msg2.content_subtype = "html"
		msg2.send(fail_silently=False)
		messages.info(request,"Successfully submitted !")
		
		# MongoDB connection
		client = pymongo.MongoClient("mongodb+srv://gr25:R7BA498tLAwBFaUh@cluster0.r1r4f.mongodb.net/appointments?retryWrites=true&w=majority")
		db = client["your_database"]
		collection = db["appointments"]
		
		# Generate patient ID
		existing = collection.find_one({"expert_id": expert.id})
		if existing and "patients" in existing:
			next_id_num = len(existing["patients"]) + 1
		else:
			next_id_num = 1
		patient_id = f"PAT{next_id_num:03}"
		
		patient = {
			"id": patient_id,
			"name": apt_booked_by,
			"email": apt_user_email,
			"problem": apt_problem,
			"req_date": apt_preferred_date
		}
		
		# Insert or update the document in MongoDB
		collection.update_one(
			{"expert_id": expert.id},
			{
				"$set": {"expert_name": expert.expert_name},
				"$push": {"patients": patient}
			},
			upsert=True
		)

		redirecturl="/"+str(expert.id)+"/appointment"
		return HttpResponseRedirect(redirecturl)
	context = {'expert':expert}
	return render(request, 'MAINAPP/appointment.html', context)

specializations = [
    "Heart Disease",
    "Diet and Nutrition",
    "Diabetes",
    "Liver Disease",
    "ASD",
    "braintumor"
]

def healthcareexperts(request):
    selected_specialization = request.GET.get('specialization', 'All')
    if selected_specialization == 'All':
        experts = HealthcareExpert.objects.all()
    else:
        experts = HealthcareExpert.objects.filter(expert_specialization=selected_specialization)
    context = {
        'experts': experts,
        'specializations': specializations,
        'selected_specialization': selected_specialization
    }
    return render(request, 'MAINAPP/healthcareexperts.html', context)