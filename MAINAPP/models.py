from django.db import models
from django.contrib.auth.models import User
from django.db.models import TextField
from django.utils import timezone

# Create your models here.
class Disease(models.Model):
	posted_on=models.DateField(blank=True,default=timezone.now)
	disease_name = models.CharField(max_length= 200)
	disease_caption=models.TextField(blank=True)
	disease_description=models.TextField(blank=True)
	disease_symptoms =models.TextField(blank=True)
	disease_precautions =models.TextField(blank=True)
	disease_medication =models.TextField(blank=True)
	disease_image = models.ImageField(null=True, blank=True , help_text="crop image as square before upload to get uniform size in the page")
	add_disease_to_home = models.BooleanField(default=False,null=True, blank=True ,help_text="Yes will enable to display it on home page")
	def __str__(self):
		return self.disease_name

	@property
	def disease_imageURL(self):
		try:
			url = self.disease_image.url
		except:
			url = ''
		return url


class Helpline(models.Model):
	organization=models.CharField(max_length= 500)
	country = models.CharField(max_length= 500)
	helpline_number=models.CharField(max_length= 500)
	organization_details =models.TextField(blank=True)
	def __str__(self):
		return self.organization


class ContactMessage(models.Model):
	reviewer_name = models.CharField(max_length= 200 ,blank=True)
	reviewer_email=models.EmailField(max_length =200 ,blank=True)
	reviewer_message = models.TextField(max_length=5000,blank=True)

	def __str__(self):
		return self.reviewer_name

class DiagnosisTool(models.Model):
	tool_name = models.CharField(max_length= 200 ,blank=False)
	tool_accuracy = models.CharField(max_length= 200 ,blank=False)
	tool_technology = models.CharField(max_length= 200 ,blank=False)
	tool_detail = models.TextField(max_length=4000,blank=False)
	tool_link = models.CharField(max_length= 200 ,blank=False)
	def __str__(self):
		return self.tool_name

class Food(models.Model):
	food_name = models.CharField(max_length= 300)
	diet_category = models.CharField(max_length= 100 ,blank=False)
	diabetic = models.BooleanField(default=False,null=True, blank=True)
	veg_food = models.BooleanField(default=True,null=True, blank=True)
	Calories = models.CharField(max_length= 100 ,blank=False)
	Fats = models.CharField(max_length= 100 ,blank=False)
	Proteins = models.CharField(max_length= 100 ,blank=False)
	Iron = models.CharField(max_length= 100 ,blank=False)
	Calcium = models.CharField(max_length= 100 ,blank=False)
	Sodium = models.CharField(max_length= 100 ,blank=False)
	Potassium= models.CharField(max_length= 100 ,blank=False)
	Carb = models.CharField(max_length= 100 ,blank=False)
	Fibres = models.CharField(max_length= 100 ,blank=False)
	Sugars = models.CharField(max_length= 100 ,blank=False)

	def __str__(self):
		return self.food_name


class Rating(models.Model):
	rating_user = models.CharField(max_length= 300 ,blank=True)
	rating_tool=models.CharField(max_length =300 ,blank=True)
	rating_parameter=models.CharField(max_length =100 ,blank=True)
	rating_message = models.TextField(blank=True)
	rating_time=models.DateField(blank=True,default=timezone.now)

	def __str__(self):
		return self.rating_user


class DiabetesDiagnosisHistory(models.Model):
	username=models.CharField(max_length= 300 ,blank=True)
	Pregnancies=models.CharField(max_length= 300 ,blank=True)
	Glucose=models.CharField(max_length= 300 ,blank=True)
	BloodPressure=models.CharField(max_length= 300 ,blank=True)
	SkinThickness=models.CharField(max_length= 300 ,blank=True)
	Insulin=models.CharField(max_length= 300 ,blank=True)
	BMI=models.CharField(max_length= 300 ,blank=True)
	DiabetesPedigreeFunction=models.CharField(max_length= 300 ,blank=True)
	Age=models.CharField(max_length= 300 ,blank=True)
	outcome=models.CharField(max_length= 300 ,blank=True)
	risk_score=models.CharField(max_length= 300 ,blank=True)
	Diagnosis_Date=models.DateField(blank=True,default=timezone.now)
	def __str__(self):
		return self.username


class HeartDiseaseDiagnosisHistory(models.Model):
	username=models.CharField(max_length= 300 ,blank=True)
	age=models.CharField(max_length= 300 ,blank=True)
	sex=models.CharField(max_length= 300 ,blank=True)
	cp=models.CharField(max_length= 300 ,blank=True)
	trestbps=models.CharField(max_length= 300 ,blank=True)
	chol=models.CharField(max_length= 300 ,blank=True)
	fbs=models.CharField(max_length= 300 ,blank=True)
	restecg=models.CharField(max_length= 300 ,blank=True)
	thalach=models.CharField(max_length= 300 ,blank=True)
	exang=models.CharField(max_length= 300 ,blank=True)
	oldpeak=models.CharField(max_length= 300 ,blank=True)
	slope=models.CharField(max_length= 300 ,blank=True)
	outcome=models.CharField(max_length= 300 ,blank=True)
	risk_score=models.CharField(max_length= 300 ,blank=True)
	Diagnosis_Date=models.DateField(blank=True,default=timezone.now)
	def __str__(self):
		return self.username

class LiverDiseaseDiagnosisHistory(models.Model):
	username=models.CharField(max_length= 300 ,blank=True)
	Age=models.CharField(max_length= 300 ,blank=True)
	Gender=models.CharField(max_length= 300 ,blank=True)
	Total_Bilirubin=models.CharField(max_length= 300 ,blank=True)
	Direct_Bilirubin=models.CharField(max_length= 300 ,blank=True)
	Alkaline_Phosphotase=models.CharField(max_length= 300 ,blank=True)
	Alamine_Aminotransferase=models.CharField(max_length= 300 ,blank=True)
	Aspartate_Aminotransferase=models.CharField(max_length= 300 ,blank=True)
	Total_Protiens=models.CharField(max_length= 300 ,blank=True)
	Albumin=models.CharField(max_length= 300 ,blank=True)
	Albumin_and_Globulin_Ratio=models.CharField(max_length= 300 ,blank=True)
	outcome=models.CharField(max_length= 300 ,blank=True)
	risk_score=models.CharField(max_length= 300 ,blank=True)
	Diagnosis_Date=models.DateField(blank=True,default=timezone.now)
	def __str__(self):
		return self.username

class BrainTumorDiagnosisHistory(models.Model):
	username=models.CharField(max_length= 300 ,blank=True)
	Mean=models.CharField(max_length= 300 ,blank=True)
	Variance=models.CharField(max_length= 300 ,blank=True)
	StandardDeviation=models.CharField(max_length= 300 ,blank=True)
	Entropy=models.CharField(max_length= 300 ,blank=True)
	Skewness=models.CharField(max_length= 300 ,blank=True)
	Kurtosis=models.CharField(max_length= 300 ,blank=True)
	Contrast=models.CharField(max_length= 300 ,blank=True)
	Energy=models.CharField(max_length= 300 ,blank=True)
	ASM=models.CharField(max_length= 300 ,blank=True)
	Homogeneity=models.CharField(max_length= 300 ,blank=True)
	Dissimilarity=models.CharField(max_length= 300 ,blank=True)
	Correlation=models.CharField(max_length= 300 ,blank=True)
	Coarseness=models.CharField(max_length= 300 ,blank=True)
	PSNR=models.CharField(max_length= 300 ,blank=True)
	SSIM=models.CharField(max_length= 300 ,blank=True)
	MSE=models.CharField(max_length= 300 ,blank=True)
	DC=models.CharField(max_length= 300 ,blank=True)
	outcome=models.CharField(max_length= 300 ,blank=True)
	risk_score=models.CharField(max_length= 300 ,blank=True)
	Diagnosis_Date=models.DateField(blank=True,default=timezone.now)
	def __str__(self):
		return self.username

class Bug(models.Model):
	reported_on=models.DateField(blank=True,default=timezone.now)
	problem = models.CharField(max_length= 200)
	problem_description=models.TextField(blank=True)

	problem_image = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.problem

	@property
	def problem_imageURL(self):
		try:
			url = self.problem_image.url
		except:
			url = ''
		return url


class HealthcareExpert(models.Model):

	expert_username = models.CharField(max_length= 1000)
	expert_name = models.CharField(max_length= 1000, blank=True)
	expert_email = models.CharField(max_length= 1000,blank=True)
	expert_designation= models.CharField(max_length= 2000)
	expert_specialization= models.CharField(max_length= 4000)
	expert_address= models.CharField(max_length= 4000)
	expert_contact= models.CharField(max_length= 1000)
	expert_image = models.ImageField(null=True, blank=True)
	def __str__(self):
		return self.expert_username

	@property
	def expert_imageURL(self):
		try:
			url = self.expert_image.url
		except:
			url = ''
		return url


class Appointment(models.Model):
	booked_on=models.DateField(blank=True,default=timezone.now)
	preferred_date=models.DateField(blank=True,default=timezone.now)
	booked_by = models.CharField(max_length= 1000)
	user_email = models.CharField(max_length= 1000)
	expert_username = models.CharField(max_length= 1000)
	expert_email = models.CharField(max_length= 1000)
	problem =models.TextField(blank=False)
	accepted = models.BooleanField(default=False,null=True, blank=True)
	def __str__(self):
		return self.booked_by


class MedicalProfile(models.Model):
	username = models.CharField(max_length= 1000)
	updated_on=models.DateField(blank=True,default=timezone.now)
	age = models.CharField(max_length= 100, blank=True)
	gender = models.CharField(max_length= 100, blank=True)
	blood_group = models.CharField(max_length= 100, blank=True)
	height = models.CharField(max_length= 100, blank=True)
	weight = models.CharField(max_length= 100, blank=True)
	emergency_contact = models.CharField(max_length= 100, blank=True)
	diabetic = models.BooleanField(default=False,null=True, blank=True)
	def __str__(self):
		return self.username
