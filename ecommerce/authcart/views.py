from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages  
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token  #this file and methods are created manually
from django.utils.encoding import force_bytes, force_str
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.views.generic import View
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def signup(request): #first should declare the fuvtions and therir returns like create map for kitchen, bathroom,bedrrom next comes logic
    #after decalring the functions should create the html pages where it should land
    #then write the logic what respective function should do
    #print("authcart views is running")
    #print("Running sign up function") runs when signup button pressed
    # here method uded is post method to know the type use request.method    
    
    #logic for the user creation
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['pass1']  #takes this values from frontend signup page
        confirm_password=request.POST['pass2']
        if len(password)<6:
            messages.warning(request,'password length must be alteast 6')
            return render(request,'authentication/signup.html') # can add more features such as spl chars should contain
        if password!=confirm_password:
            messages.warning(request,'password is not matching') #messages takes two parameter colour and the message warning is a bootstrap colour and u can use info for blue if wanna use danger the rename it danger is an keyword in django
            return render(request,'authentication/signup.html')
        
        try:
            if User.objects.get(username=email): #checks from the User database
                messages.info(request,'Email already in use')
                return render(request,'authentication/signup.html')
            
        except Exception as identifier:
            pass 
        
        user=User.objects.create_user(email,email,password) #adds into the users data table in django
        user.is_active=False
        user.save()
        email_subject="Activate Your Account"
        message=render_to_string('activate.html',{
            'user':user, #below is local host
            'domain':'127.0.0.1:8000', #should change website name if universal if hosted some where else shopping.com like
            'uid':urlsafe_base64_encode(force_bytes(user.pk)), #this is primary key of every user encoding
            'token':generate_token.make_token(user)  #generating token for the with the primary key and pass it to the html
                                                    #generated token should be redirected to activate.html to display the mail
        })
        
        email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        email_message.send()
        messages.success(request,"Activate Your Account by Clicking the link in your gmail")
        return redirect('/auth/login/')
    return render(request,'authentication/signup.html')

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None 
        if user is not None and TokenGenerator().check_token(user,token):
            user.is_active=True
            user.save=()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/login') 
        return render(request,'activatefail.html')       


def handlelogin(request):
    if request.method=="POST":
        username=request.POST['email']
        userpassword=request.POST['pass1']
        myuser=authenticate(username=username,password=userpassword)
        
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            #return redirect(request,'index.html')
            return redirect('/')  #will redirect to the home page
        
        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login')
    return render(request,"authentication/login.html")


def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login')

class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            # email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            # email_message.send()

            messages.info(request,f"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD {message} " )
            return render(request,'request-reset-email.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/auth/login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)



