from django.contrib.auth.decorators import login_required
from spices.coach360.models import Survey,Question,Response
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User

  
@login_required
def index(request):
    lSurveys = request.user.surveys.all()
    return render(request, 'coach360/index.html', {'lSurveys':lSurveys})

@login_required
def survey(request, survey_id):
    try:
        # Check if user has access to this survey
        oSurvey = Survey.objects.get(pk = survey_id)
        if not request.user in oSurvey.users.all():
            raise Http404
        lUsers = oSurvey.users.exclude(pk = request.user.pk)
    except Exception,e:
        raise Http404
    return render(request, 'coach360/survey.html', {'lUsers':lUsers, 'oSurvey':oSurvey})

@login_required
def usersurvey(request, survey_id, user_id):
    try:
        # Check if user has access to this survey
        oSurvey = Survey.objects.get(pk = survey_id)
        oToUser = User.objects.get(pk=user_id)
        
        if not request.user in oSurvey.users.all():
                raise Http404
            
        if request.method == "POST":
            lQuestions = [k for k in request.POST.keys() if k.startswith('question_')]
            for sQuestion in lQuestions:
                oQuestion = Question.objects.get(pk=sQuestion.replace('question_',''))
                lResponses = Response.objects.filter(question = oQuestion,
                                     from_user = request.user,
                                     to_user = oToUser
                                     )
                if lResponses:
                    oResponse = lResponses[0]
                    oResponse.response = request.POST[sQuestion]
                    oResponse.save()
                else:
                    Response.objects.create(response = request.POST[sQuestion],
                                        question = oQuestion,
                                        from_user = request.user,
                                        to_user = oToUser
                                        )
            return render(request, 'coach360/thankyou.html')
        else:
            dQuestions = {}
            lQuestions = Question.objects.filter(survey__pk = survey_id)
            for oQuestion in lQuestions:
                lResponses = Response.objects.filter(question=oQuestion,
                                                     from_user=request.user,
                                                     to_user=oToUser
                                                     )
                if lResponses:
                    dQuestions[oQuestion] = lResponses[0]
                else:
                    dQuestions[oQuestion] = None
            return render(request, 'coach360/usersurvey.html', {'dQuestions':dQuestions, 'survey_id':survey_id, "oUser":oToUser})
    except Exception,e:
        raise Http404
    
@login_required
def indexresults(request):
    if not request.user.username=='centroglobal2':
        raise Http404
    lSurveys = Survey.objects.all()
    return render(request, 'coach360/indexresults.html', {'lSurveys':lSurveys})
    
        

@login_required
def surveyresults(request, survey_id):
    if not request.user.username=='centroglobal2':
        raise Http404
    try:
        oSurvey = Survey.objects.get(pk = survey_id)
        lUsers = User.objects.filter(surveys = survey_id)
    except Exception,e:
        raise Http404
    return render(request, 'coach360/surveyresults.html', {'lUsers':lUsers, 'oSurvey':oSurvey})

@login_required
def usersurveyresults(request, survey_id, user_id):
    if not request.user.username=='centroglobal2':
        raise Http404
    try:
        dInfo = {}
        oSurvey = Survey.objects.get(pk=survey_id)
        oEvaluatedUser = User.objects.get(pk=user_id)
        lUsers = User.objects.filter(surveys = survey_id).exclude(pk=user_id).order_by('username')
        lQuestions = Question.objects.filter(survey__pk = survey_id)
        lMeans = []
        for oQuestion in lQuestions:
            suma = 0
            num = 0
            if not oQuestion in dInfo:
                dInfo[oQuestion] = []
            for oUser in lUsers:
                lResponses = Response.objects.filter(question=oQuestion,to_user = oEvaluatedUser,from_user = oUser)
                if lResponses:
                    dInfo[oQuestion].append(lResponses[0])
                    suma += lResponses[0].response
                    num +=1;
                else:
                    dInfo[oQuestion].append(None)
            # Calculate  mean
            if (num!=0): 
                result = float(suma)/float(num)
            else: 
                result = 0
            lMeans.append(result)
    except Exception,e:
        raise Http404
    return render(request, 'coach360/usersurveyresults.html', {'lUsers':lUsers, 'dInfo': dInfo, 'oEvaluatedUser':oEvaluatedUser, 'oSurvey': oSurvey, 'lMeans':lMeans})
