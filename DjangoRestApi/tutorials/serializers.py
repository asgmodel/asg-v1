from rest_framework import serializers
from tutorials.models import Tutorial,Scenario
import sys
sys.path.insert(0, "/home/wasmasg/asg-model-api-v1.0/DjangoRestApi/tutorials/ASG")


from TypeModels import TypeModel
from BasePath import BASEPATH
from ModelTEC import *
from ASGModels import ASG


MST=TEC(typemodel="svmL",model_setting=TypeModel['technique'])
MST.loadmodel()
ASGAI=ASG()
class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')

class ScenarioSerializer(serializers.ModelSerializer):

    class Meta:
        model = Scenario
        fields = ('id',
                  'seqtactic',
                  'iduser',
                  'seqtec','score')



