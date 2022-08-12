from django.forms.models import model_to_dict
from django.shortcuts import render
from rest_framework.views import APIView, Response, status

# Create your views here.
from content.models import Content


class ContentView(APIView):
    def get(self, request):
        # equilavente a SELECT * FROM persons_person;
        contents = Content.objects.all()

        contents_list = [model_to_dict(content) for content in contents]
        #equilavente do list comprehension acima no for abaixo
        # empty_list = []
        # for content in contents:
        #     empty_list.append(model_to_dict(content))
        return Response(contents_list)

    def post(self, request):
        my_dict = {
            "title": "string",
            "module": "string",
            "students": 1,
            "description": "string",
            "is_active": True
        }
        reqdata = request.data

        error_list = []

        #verifica se possui todas as chaves obrigatórias e se o tipo esperado está correto
        for key, value in my_dict.items():
            if not reqdata.get(key):
                error_list.append({"Missing key": key})

            if reqdata.get(key) and type(reqdata[key]) != type(my_dict[key]):
                error_list.append({"TypeError": f"{key} are not of expected type. Expected type: {type(my_dict[key])}"})
        
        #verifica se há chaves além das obrigatórias
        for key in reqdata:
            if key not in my_dict:
                error_list.append({"Strange Key": f"{key} is not a expected key."})
        
        #retorna mensagem de erro se houver erros
        if len(error_list) > 0:
            return Response({
                "Message": "Invalid data",
                "Errors": error_list
                }, status.HTTP_409_CONFLICT)
            
        #cria novo objeto do tipo Content, distribuindo nele o que foi pego do body(request.data)
        content = Content.objects.create(**request.data)
        #converte num dicionario
        content_dict = model_to_dict(content)

        return Response(content_dict, status.HTTP_201_CREATED)

class ContentDetailView(APIView):
    def get(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"Message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        content_to_dict = model_to_dict(content)

        return Response(content_to_dict)

    def patch(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"Message": "Content not found"}, status.HTTP_404_NOT_FOUND)

        reqdata = request.data

        for key, value in reqdata.items():
            #reatribuindo chave e valor do objeto content a partir dos dados recebidos no body request
            setattr(content, key, value)

        content.save()

        content_to_dict = model_to_dict(content)

        return Response(content_to_dict, status.HTTP_200_OK)

    def delete(self, request, content_id: int):
        try:
            content = Content.objects.get(id=content_id)
        except Content.DoesNotExist:
            return Response({"Message": "Content not found"}, status.HTTP_404_NOT_FOUND)
        
        content.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentTitleView(APIView):
    def get(self, request):
        title_param = request.query_params.get("title")

        #filtrando database a partir do filtro de query param, case insensitive(ignora maiusculas e minusculas)
        contents = Content.objects.filter(title__iexact=title_param)
        #convertendo em uma lista de dicionarios
        filtered_content = [model_to_dict(content) for content in contents]

        return Response(filtered_content, status.HTTP_200_OK)
