from django.shortcuts import render, redirect,get_object_or_404,HttpResponse
from .models import *
from django.http import JsonResponse
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import *
from django.forms import inlineformset_factory
from django.forms.models import modelformset_factory
from django.db.models import Q
from . serializers import *



def Signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password1']
        confirm_password = request.POST['password2']
        
        if password != confirm_password:
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')  
    return render(request, "signup.html")

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            return redirect("/")
        else:
            return render(request, "login.html") 
    return render(request, "login.html")

def Logout(request):
    logout(request)
    return redirect('/')


def qzz(request):
    qq = Quiz.objects.all()
    print(qq)
    return render(request,'qz.html',{'topics':qq})

@login_required(login_url='/login')
# correct
def quiz_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = []
    for q in quiz.get_questions():
        options = [(a.id, a.content) for a in q.get_answers()] 
        questions.append({q: options})
    quiz_name = quiz.name
    
    print(quiz)
    return render(request, 'qq.html', {'quiz_name': quiz_name, 'questions': questions, 'quiz_id': quiz_id,'quiz':quiz})
# correct


def submit(request, quiz_id):
    if request.method == 'POST':
        quiz = get_object_or_404(Quiz, id=quiz_id)
        user = request.user
        total_questions = quiz.number_of_questions
        correct_answers = 0
        user_responses = []

        for question in quiz.get_questions():
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                selected_answer = Answer.objects.get(id=answer_id)
                user_responses.append({
                    'question': question.content,
                    'selected_answer': selected_answer.content,
                    'is_correct': selected_answer.correct
                })
                if selected_answer.correct:
                    correct_answers += 1

        if total_questions > 0:
            score = (correct_answers / total_questions) * 100
        else:
            score = 0
        
        print(user_responses)

        Marks_Of_User.objects.create(
            quiz=quiz,
            user=user,
            score=score,
            user_responses=user_responses
        )

        return render(request, 'score.html', {'score': score})
    return HttpResponse('Invalid request.')



def result(request):
    user_id = request.session.get('user_id')
    # single user
    marks_list = Marks_Of_User.objects.filter(user_id=user_id).order_by('-id')
    paginator_marks_list = Paginator(marks_list, 5) 
    page_number_marks_list = request.GET.get('page')
    page_obj_marks_list = paginator_marks_list.get_page(page_number_marks_list)

    # all user
    marks = Marks_Of_User.objects.all().order_by('-id')
    paginator_marks = Paginator(marks, 5) 
    page_number_marks = request.GET.get('page')
    page_obj_marks = paginator_marks.get_page(page_number_marks)

    return render(request, "result2.html", {'page_obj': page_obj_marks_list, 'page_obj_marks': page_obj_marks})



def result_description(request,res_id):
    qresult = get_object_or_404(Marks_Of_User, id=res_id)
    # print(qresult.user_responses)
    return render(request,'result3.html',{'qresult':qresult})


def add_quiz(request):
    quiz = Quiz.objects.all().order_by('-id')
    if request.method == "POST":
        form = QuizForm(data=request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('add_quiz')
    else:
        form = QuizForm()
    return render(request, "add_quiz.html", {'form': form,'all_quiz':quiz})


def add_question(request):
    questions = Question.objects.all().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_question')
    else:
        form=QuestionForm()
    return render(request, "add_question.html", {'form':form,'questions':questions})


def add_option(request, que_id):
    question = Question.objects.get(id=que_id)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        print(999999999)
        if formset.is_valid():
            print('ggggggggggggg')
            formset.save()
            
            # alert = True
            # return render(request, "add_option.html", {'alert':alert})
            return redirect('add_question')
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "add_option.html", {'formset':formset, 'question':question})

def delete_result(request, res_id):
    marks = Marks_Of_User.objects.get(id=res_id)
    if request.method == "POST":
        marks.delete()
        return redirect('/result')
    return render(request, "result2.html", {'marks':marks})
    

def delete_question(request, que_id):
    questions = Question.objects.all().get(id=que_id)
    print(7877878)
    if request.method == "POST":
        questions.delete()
        print(455445)
        return redirect('/add_question')
    return render(request, "qq.html", {'questions':questions})

def delete_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    if request.method == "POST":
        quiz.delete()
        return redirect('/add_quiz')
    return render(request, "add_quiz.html", {'quiz':quiz})
    
def search_quiz(request):
    if request.method == 'POST':
        search_quiz = request.POST.get('search')
        search_result = Quiz.objects.filter(Q(name__icontains=search_quiz))
        return render(request, "qz.html", {'search_result':search_result})
    


