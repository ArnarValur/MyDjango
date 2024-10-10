import graphene
from graphene_django import DjangoObjectType
from .models import Page, Link, Post


# Define the types for the models
class PageType(DjangoObjectType):
    class Meta:
        model = Page
        fields = '__all__'


class LinkType(DjangoObjectType):
    class Meta:
        model = Link
        fields = '__all__'


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = '__all__'


# Define the query class
def resolve_all_pages(info, **kwargs):
    return Page.objects.all()


def resolve_all_links(info, **kwargs):
    return Link.objects.all()


def resolve_all_posts(info, **kwargs):
    return Post.objects.all()


class Query(graphene.ObjectType):
    all_pages = graphene.List(PageType)
    all_links = graphene.List(
        LinkType,
        location=graphene.String(),
        orderBy=graphene.String(),
    )
    all_posts = graphene.List(PostType)

    def resolve_all_pages(root, info, **kwargs):
        return Page.objects.all()

    def resolve_all_links(root, info, location=None, orderBy=None, **kwargs):
        qs = Link.objects.all()
        if location:
            qs = qs.filter(location=location)
        if orderBy:
            qs = qs.order_by(orderBy)
        return qs


    def resolve_all_posts(root, info, **kwargs):
        return Post.objects.all()


# Define the schema
schema = graphene.Schema(query=Query)
