from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from tutorials.models import Tutorial,Scenario
from tutorials.serializers import TutorialSerializer,MST,ASGAI,ScenarioSerializer
from rest_framework.decorators import api_view
import requests
import uuid
from tutorials.chats import  ask_ai
def toclean(txt):
    try:
        url="https://ansaltwyl256.pythonanywhere.com/api/nlp/"+txt
        response = requests.get(url)

        return response.json()['description']
    except:
        return txt


@api_view(['GET', 'POST', 'DELETE'])
def input(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'

        langs=''#ASGAI.Soft.detector.detect(pk)
        text_output,dis=MST.predictAPI(MST.to_tran(pk))

        dis=dis#MST.to_tran(dis,dest=langs.lang)


        tutorials = {"title":str(text_output),"description":dis,"published":True if str(langs)=='ar' else False}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tutorials = {"title":str(text_output),"description":text_output,"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def input_soft(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'

        langs=''#ASGAI.Soft.detector.detect(pk)
        text_output,dis=ASGAI.Soft.predictAPI(ASGAI.Soft.to_tran(pk))

        dis=dis#ASGAI.Soft.to_tran(dis,dest=langs.lang)


        tutorials = {"title":str(text_output),"description":dis +str(request.data),"published":True if str(langs)=='ar' else False}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
       pass

@api_view(['GET', 'POST', 'DELETE'])
def input_group(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'

        langs=''#ASGAI.Group.detector.detect(pk)
        text_output,dis=ASGAI.Group.predictAPI(ASGAI.Group.to_tran(pk))

        dis=dis#ASGAI.Group.to_tran(dis,dest=langs.lang)


        tutorials = {"title":str(text_output),"description":dis,"published":True if str(langs)=='ar' else False}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
       pass

@api_view(['GET', 'POST', 'DELETE'])
def search(request,pk):

    print(pk)
    if request.method == 'GET':
        doc='A:'
        Scenario.objects.all().delete()
        c=0
        userid=str(uuid.uuid4())
        def addsenario(inputs):


            data,pd=inputs
            seqtactic=''
            seqtec=''
            for ob in data[0]:
                seqtactic+=ob[0]+"$@"
                seqtec+=ob[1]+"$@"

            out,_=ASGAI.Soft.predictAPI(seqtec)
            score=out+"  is state &socre : "+data[1][1]+"   "+str(round(data[2],2))

            tutorial = {"seqtactic":seqtactic,'iduser':userid,"seqtec":seqtec,"score":score}

            serrr = ScenarioSerializer(data=tutorial)
            if serrr.is_valid():
                serrr.save()



        ASGAI.cks.onsequens=addsenario

        text_output=ASGAI.search([pk],istrans=True,numstop=20)
        allob=Scenario.objects.all()



        tutorial_serializer = ScenarioSerializer(data=allob,many=True)
        tutorial_serializer.is_valid()



        return JsonResponse(tutorial_serializer.data, safe=False)
    else:
        tutorials = {"seqtactic":'tttttttt','iduser':'user1',"seqtec":'yhtyhtyhty',"score":'0.9'}

        tutorial_serializer = ScenarioSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def generatingai(request,pk):

    print(pk)
    if request.method == 'GET':
        doc='A:'
        Scenario.objects.all().delete()
        c=0
        userid=str(uuid.uuid4())
        def addsenario(inputs):


            data,pd=inputs
            seqtactic=''
            seqtec=''
            for ob in data[0]:
                seqtactic+=ob[0]+"$@"
                seqtec+=ob[1]+"$@"

            out,_=ASGAI.Soft.predictAPI(seqtec)
            out2,_=ASGAI.Group.predictAPI(seqtec+" "+out)
            score=out2+"@"+out+"@"+data[1][1]+"@"+str(round(data[2],2))

            tutorial = {"seqtactic":seqtactic,'iduser':userid,"seqtec":seqtec,"score":score}

            serrr = ScenarioSerializer(data=tutorial)
            if serrr.is_valid():
                serrr.save()



        ASGAI.cks.onsequens=addsenario

        text_output=ASGAI.search([pk],istrans=True,numstop=500)
        allob=Scenario.objects.filter(iduser=userid)

        tutorials = {"title":str(len(allob)),"description":userid,"published":True }

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tutorials = {"seqtactic":'tttttttt','iduser':'user1',"seqtec":'yhtyhtyhty',"score":'0.9'}

        tutorial_serializer = ScenarioSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST', 'DELETE'])
def searchall(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'
      #  Scenario.objects.all().delete()
        c=0
        def addsenario(inputs):


            data,pd=inputs
            seqtactic=''
            seqtec=''
            for ob in data[0]:
                seqtactic+=ob[0]+"$@"
                seqtec+=ob[1]+"$@"

            out,_=ASGAI.Soft.predictAPI(seqtec)
            score=out+"  is state &socre : "+data[1][1]+"   "+str(round(data[2],2))

            tutorial = {"seqtactic":seqtactic,'iduser':'user'+str(10),"seqtec":seqtec,"score":score}

            serrr = ScenarioSerializer(data=tutorial)
            if serrr.is_valid():
                serrr.save()



        ASGAI.cks.onsequens=addsenario

        text_output=ASGAI.search([pk],istrans=True)
        allob=Scenario.objects.all()



        tutorial_serializer = ScenarioSerializer(data=allob,many=True)
        tutorial_serializer.is_valid()



        return JsonResponse(tutorial_serializer.data, safe=False)
    else:
        tutorials = {"seqtactic":'tttttttt','iduser':'user1',"seqtec":'yhtyhtyhty',"score":'0.9'}

        tutorial_serializer = ScenarioSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def inputpipline(request,pk):
    if request.method == 'GET':
        doc='A:'

        langs='' #ASGAI.Soft.detector.detect(pk)
        txtp=ASGAI.Group.to_tran(pk)
        text_output,_,dis=ASGAI.Group.Predict_ALL(txtp)
        items=text_output.split('--')
        text_output= "Technique:"+items[1]+",Incident: "+items[2]+", Group:"+ dis['svmK']
        txtdes= items[1]+" " +ASGAI.Tec.DES[items[1]][0:500]+"  @@$ "+items[2]+" :" +ASGAI.Soft.DES[items[2]][0:500]+"   @@$  "+ASGAI.Group.DES[dis['svmK']][0:500]
        langs='en' #langs.lang


        payload={
             "question":txtp,
             "required":" يث تكون الاجابة  بنفس لغة  السوال   ",
             "answermodel":text_output


             }


        try:
            txtdes=ask_ai(str(payload)+ "قم اعادة صياغة الاجابة بشكل مختصر  ")

        except:pass

        tutorials = {"title":str(text_output),"description":txtdes,"published":True if str(langs)=='ar' else False}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return
        # return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)onResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tutorials = {"title":str(text_output),"description":text_output,"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def search2(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'

        allob=Scenario.objects.filter(iduser=pk)





        tutorial_serializer = ScenarioSerializer(data=allob,many=True)
        tutorial_serializer.is_valid()



        return JsonResponse(tutorial_serializer.data, safe=False)
    else:
        tutorials = {"seqtactic":'tttttttt','iduser':'user1',"seqtec":'yhtyhtyhty',"score":'0.9'}

        tutorial_serializer = ScenarioSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST', 'DELETE'])
def input_info_Group(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'

        text_output=ASGAI.Group.getLables()





        tutorials = {"title":str(text_output[0]),"description":str(text_output),"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tutorials = {"title":str(text_output),"description":text_output,"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def input_info_Soft(request,pk):
    print(pk)
    if request.method == 'GET':
        doc='A:'
        lste=[]
        langs='a' #ASGAI.Soft.detector.detect(pk)

        text_output=ASGAI.Soft.getLables()




        tutorials = {"title":str(langs),"description":str(text_output),"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        tutorials = {"title":str(text_output),"description":text_output,"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




def  getsubdes(des):
    nl=len(des)-1
    return des[0:(500  if nl>500 else nl)]
#source .virtualenvs/myprojectvenv/bin/activate
@api_view(['GET', 'POST', 'DELETE'])
def transe(request,pk):
    print(pk)
    if request.method == 'GET':
        langs='' #ASGAI.Soft.detector.detect(pk)
        txtp=ASGAI.Group.to_tran(pk)
        text_output,_,dis=ASGAI.Group.Predict_ALL(txtp)
        items=text_output.split('--')

        text_output= "Technique:"+items[1]+",Incident: "+items[2]+", Group:"+ dis['svmK']

        txtdes= items[1]+" " +ASGAI.Tec.DES[items[1]][0:500]+"  @@$ "+items[2]+" :" +ASGAI.Soft.DES[items[2]][0:500]+"   @@$  "+ASGAI.Group.DES[dis['svmK']][0:500]
        payload={
             "question":txtp,
             "required":"اريد منك  ترتيب  الاجابة وفقا لسوال المستخدم بحيث تكون الاجابة بنفس  لغة السوال  دائما     واذا كانت الاجابة   لا تعبر  عن السوال   فجاوب انت  نيابه عنه ",
             "answermodel":txtdes


             }


        try:
            txtdes=ask_ai(str(payload)+ "اجب  بشكل مختصر ")

        except:pass

        langs=''

        tutorials = {"title":text_output,"description":txtdes,"published":True if str(langs)=='ar' else False}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
       pass



@api_view(['GET', 'POST', 'DELETE'])
def nlpto(request,pk):
    print(pk)
    if request.method == 'GET':


        tutorials = {"title":"yes","description":str(request.data),"published":True}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
       pass


@api_view(['GET', 'POST', 'DELETE'])
def getteck(request,pk):
    print(pk)
    if request.method == 'GET':

        tree=ASGAI.SGT.getordertactics()


        text=''
        istec=True
        try:
            index=int(pk)
            for ob in tree[index].Techniques:
                text=text+"@@"+ob.Name
        except:
            for ob in tree:
                text +="@@"+ob.Name
                istec=False


        tutorials = {"title":str(uuid.uuid4()),"description":str(text),"published":istec}

        tutorial_serializer = TutorialSerializer(data=tutorials)

        if tutorial_serializer.is_valid():

            # tutorial_serializer.create()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
       pass
