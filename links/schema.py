import graphene
from graphene_django import DjangoObjectType

from .models import Link


class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

class CreateLink(graphene.Mutation):
    # クライアントに返却されるデータ(フィールド変数)
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()

    #2 サーバに送信することができるデータ
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3 DBに登録
    def mutate(self, info, url, description):
        link = Link(url=url, description=description)
        link.save()

        return CreateLink(
            id=link.id,
            url=link.url,
            description=link.description,
        )


#4 mutationクラスを作成
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
