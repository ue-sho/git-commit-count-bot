from graphene import ObjectType, String, Schema
import requests

GITHUB_ACCESS_TOKEN = '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'
END_POINT = 'https://api.github.com/graphql'

# class Query(ObjectType):
#     # this defines a Field `hello` in our Schema with a single Argument `name`
#     hello = String(name=String(default_value="stranger"))
#     goodbye = String()

#     # our Resolver method takes the GraphQL context (root, info) as well as
#     # Argument (name) for the Field and returns data for the query Response
#     def resolve_hello(root, info, name):
#         return f'Hello {name}!'

#     def resolve_goodbye(root, info):
#         return 'See ya!'

# schema = Schema(query=Query)

def post(query):
    headers = {"Authorization": "bearer " + GITHUB_ACCESS_TOKEN}
    res = requests.post(END_POINT, json=query, headers=headers)
    if res.status_code != 200:
        raise Exception("fail : {}".format(res.status_code))
    return res

# query
query={ 'query' : """
  query {
    search(query: "language:python stars:>=1000 sort:stars", type: REPOSITORY, first: 10) {
      edges {
        node {
          ... on Repository {
            nameWithOwner
            url
            createdAt
            description
            stargazers{
              totalCount
            }
          }
        }
      }
    }
  }
  """
}

res = post(query)
print('{}'.format(res.json()))
